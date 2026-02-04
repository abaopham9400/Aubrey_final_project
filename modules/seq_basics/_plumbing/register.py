"""Auto-discovery and MCP registration for tools and resources.

This module scans the tools/ and data/ directories and automatically
registers everything it finds with the MCP server.
"""

from __future__ import annotations

import importlib
import inspect
import json
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Optional, get_type_hints

from Bio import SeqIO

from .resolve import resolve_to_seq, register_resource


def register_tools(mcp, tools_dir: Path) -> None:
    """Auto-discover and register all tools in the tools directory.

    Scans for .py files (excluding __init__.py and _*.py), imports them,
    and registers any that have TOOL_META defined.
    """
    for py_file in sorted(tools_dir.glob("*.py")):
        if py_file.name.startswith("_") or py_file.name == "__init__.py":
            continue

        module_name = py_file.stem

        # Build the import path relative to the package
        # tools_dir is something like .../modules/seq_basics/tools
        # We need to import as modules.seq_basics.tools.<module_name>
        package_parts = []
        current = tools_dir
        while current.name != "modules" and current.parent != current:
            package_parts.insert(0, current.name)
            current = current.parent
        package_parts.insert(0, "modules")

        import_path = ".".join(package_parts) + f".{module_name}"

        try:
            module = importlib.import_module(import_path)
        except Exception as e:
            print(f"Warning: Could not import {import_path}: {e}")
            continue

        if not hasattr(module, "TOOL_META"):
            print(f"Warning: {py_file.name} has no TOOL_META, skipping")
            continue

        meta = module.TOOL_META
        func_name = module_name  # Convention: function name matches filename

        if not hasattr(module, func_name):
            print(f"Warning: {py_file.name} has no function '{func_name}', skipping")
            continue

        func = getattr(module, func_name)
        _register_tool(mcp, func, meta)


def _register_tool(mcp, func: Callable, meta: dict) -> None:
    """Register a single tool function with MCP, wrapping with resolve_to_seq."""
    seq_param = meta.get("seq_param", "seq")
    seq_params = meta.get("seq_params", [])  # For multiple sequence params

    # Combine single and multiple seq params
    all_seq_params = set(seq_params)
    if seq_param:
        all_seq_params.add(seq_param)

    @wraps(func)
    def wrapped(**kwargs):
        # Resolve sequence parameters
        for param in all_seq_params:
            if param in kwargs and kwargs[param] is not None:
                kwargs[param] = resolve_to_seq(kwargs[param])
        return func(**kwargs)

    # Set the name and docstring for MCP
    wrapped.__name__ = meta["name"]
    wrapped.__doc__ = meta.get("description", func.__doc__ or "")

    # Copy type hints for schema generation
    if hasattr(func, "__annotations__"):
        wrapped.__annotations__ = func.__annotations__

    # Register with MCP
    mcp.tool(wrapped)


def register_resources(mcp, data_dir: Path, module_name: str) -> None:
    """Auto-discover and register all resources in the data directory.

    Scans for sequence files (.gb, .gbk, .genbank, .fa, .fasta, .fna),
    registers them in the resource registry, and creates MCP resource endpoints.
    """
    sequence_extensions = {".gb", ".gbk", ".genbank", ".fa", ".fasta", ".fna"}

    for data_file in sorted(data_dir.iterdir()):
        if data_file.is_dir():
            continue
        if data_file.suffix.lower() not in sequence_extensions:
            continue
        if data_file.name.startswith("_"):
            continue

        resource_name = data_file.stem
        register_resource(resource_name, data_file)

        # Load optional metadata
        meta = _load_resource_metadata(data_file)

        # Create MCP resource endpoint
        _register_resource(mcp, data_file, resource_name, module_name, meta)


def _load_resource_metadata(data_file: Path) -> dict:
    """Load metadata from a .meta.json file if it exists."""
    meta_file = data_file.with_suffix(data_file.suffix + ".meta.json")
    if not meta_file.exists():
        meta_file = data_file.parent / f"{data_file.stem}.meta.json"

    if meta_file.exists():
        try:
            return json.loads(meta_file.read_text())
        except Exception:
            pass

    # Auto-generate description from file
    return {"description": _extract_description(data_file)}


def _extract_description(data_file: Path) -> str:
    """Extract a description from a sequence file."""
    suffix = data_file.suffix.lower()

    try:
        if suffix in (".gb", ".gbk", ".genbank"):
            record = SeqIO.read(data_file, "genbank")
            definition = record.description or record.name or data_file.stem
            length = len(record.seq)
            return f"{definition} ({length}bp, GenBank)"

        elif suffix in (".fa", ".fasta", ".fna"):
            record = SeqIO.read(data_file, "fasta")
            # FASTA description is often in the header
            desc = record.description or data_file.stem
            length = len(record.seq)
            return f"{desc} ({length}bp, FASTA)"

    except Exception:
        pass

    return f"Sequence file: {data_file.name}"


def _register_resource(
    mcp,
    data_file: Path,
    resource_name: str,
    module_name: str,
    meta: dict
) -> None:
    """Register a single resource with MCP."""
    uri = f"resource://{module_name}/{resource_name}"
    description = meta.get("description", f"Sequence resource: {resource_name}")

    @mcp.resource(uri)
    def resource_reader() -> str:
        return data_file.read_text()

    # Override the docstring for the resource
    resource_reader.__doc__ = description
    resource_reader.__name__ = resource_name
