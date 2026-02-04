"""seq_basics: Basic DNA sequence analysis tools.

This is an example module demonstrating the MCP tool architecture.
Students can copy this module structure to create new skill areas.

To add a new tool:
  1. Create a new .py file in tools/ (e.g., gc_content.py)
  2. Add TOOL_META dict and a function matching the filename
  3. Restart the server - it will be auto-discovered

To add a new resource:
  1. Drop a sequence file in data/ (.gb, .fasta, etc.)
  2. Restart the server - it will be auto-discovered
"""

from __future__ import annotations

from .tools import register_tools
from .resources import register_resources


def register_prompts(mcp) -> None:
    """Register prompts for this module.

    Prompts are optional. Add them here if needed.
    """
    pass
