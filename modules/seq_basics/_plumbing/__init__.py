"""Plumbing for MCP tool registration and sequence resolution.

Students should not need to modify anything in this package.
"""

from .resolve import resolve_to_seq, register_resource, get_resource_path
from .register import register_tools, register_resources

__all__ = [
    "resolve_to_seq",
    "register_resource",
    "get_resource_path",
    "register_tools",
    "register_resources",
]
