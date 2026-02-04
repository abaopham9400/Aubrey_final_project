"""Resource registration for seq_basics.

Resources are auto-discovered from the data/ directory. Sequence files
(.gb, .gbk, .genbank, .fa, .fasta, .fna) are automatically registered.

Students don't need to modify this file. Just add sequence files to data/.
"""

from __future__ import annotations

from pathlib import Path

from .._plumbing import register_resources as _register_resources


def register_resources(mcp) -> None:
    """Auto-discover and register all resources from the data directory."""
    data_dir = Path(__file__).parent.parent / "data"
    _register_resources(mcp, data_dir, module_name="seq_basics")
