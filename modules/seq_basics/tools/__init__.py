"""Tool registration for seq_basics.

Tools are auto-discovered from this directory. Each .py file (except __init__.py
and files starting with _) should contain:
  - TOOL_META: dict with 'name', 'description', and optionally 'seq_param'
  - A function matching the filename (e.g., translate.py has translate())

Students don't need to modify this file.
"""

from __future__ import annotations

from pathlib import Path

from .._plumbing import register_tools as _register_tools


def register_tools(mcp) -> None:
    """Auto-discover and register all tools in this directory."""
    tools_dir = Path(__file__).parent
    _register_tools(mcp, tools_dir)
