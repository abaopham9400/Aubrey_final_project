"""Module registry for the MCP server.

This file registers all available modules. The server imports this
and calls register_all(mcp) to set up tools, resources, and prompts.

To add a new module:
  1. Create a new directory in modules/ (copy seq_basics as a template)
  2. Import and register it below
"""

from __future__ import annotations

from .seq_basics import register_tools as register_seq_basics_tools
from .seq_basics import register_resources as register_seq_basics_resources
from .seq_basics import register_prompts as register_seq_basics_prompts


def register_all(mcp) -> None:
    """Register all modules with the MCP server."""
    # seq_basics: Basic sequence analysis tools (example module)
    register_seq_basics_tools(mcp)
    register_seq_basics_resources(mcp)
    register_seq_basics_prompts(mcp)

    # Add more modules here as needed:
    # register_cloning_tools(mcp)
    # register_cloning_resources(mcp)
