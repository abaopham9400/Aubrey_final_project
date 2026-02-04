# MCP Tool Architecture Specification

This document specifies the architecture for the BioE234 MCP starter project. The goal is to separate business logic from plumbing so students can focus on writing bioinformatics functions without worrying about MCP connectivity.

## Design Principles

1. **Students write pure functions** - Business logic operates on clean inputs, testable standalone
2. **Convention over configuration** - Auto-discovery based on file structure and naming
3. **No plumbing in tool files** - Students never import MCP, decorators, or registration code
4. **Copy-paste friendly** - New tools created by copying an example and modifying it

## Directory Structure

```
modules/
└── seq_basics/                     # A "skill" or topic area
    ├── __init__.py                 # Registers tools, resources, prompts
    ├── SKILL.md                    # LLM instructions for using this module
    ├── _plumbing/
    │   ├── __init__.py
    │   ├── resolve.py              # resolve_to_seq() and resource registry
    │   └── register.py             # Auto-discovery and MCP registration
    ├── _utils.py                   # Shared constants (CODON_TABLE, etc.)
    ├── data/
    │   ├── pBR322.gb               # Sequence files (GenBank, FASTA, etc.)
    │   └── ...
    ├── tools/
    │   ├── __init__.py             # Auto-discovers and registers all tools
    │   ├── translate.py            # Student-written tool
    │   ├── reverse_complement.py
    │   └── ...
    └── resources/
        ├── __init__.py             # Auto-discovers and registers all resources
        └── ...
```

## Tool File Convention

Each tool is a single Python file in the `tools/` directory. The file must contain:

1. **`TOOL_META` dict** - Metadata for MCP registration
2. **A function matching the filename** - The business logic

### Example Tool File

```python
# modules/seq_basics/tools/translate.py

"""Translate DNA to protein."""

from .._utils import CODON_TABLE

TOOL_META = {
    "name": "dna_translate",
    "description": "Translate DNA to protein using the standard genetic code.",
    "seq_param": "seq",  # Optional: which param gets resolve_to_seq treatment
}

def translate(seq: str, start: int = None, end: int = None, frame: int = 1) -> str:
    """Translate DNA sequence to protein.

    Args:
        seq: Clean DNA string [ACGT]+
        start: Start position (0-indexed)
        end: End position
        frame: Reading frame 1, 2, or 3

    Returns:
        Protein sequence, stop codons as '*'
    """
    if start is not None or end is not None:
        seq = seq[start:end]

    if frame in (2, 3):
        seq = seq[frame - 1:]

    protein = []
    for i in range(0, len(seq) - 2, 3):
        codon = seq[i:i+3]
        protein.append(CODON_TABLE.get(codon, "X"))

    return "".join(protein)


# For standalone testing
if __name__ == "__main__":
    print(translate("ATGGCTAGCTAG"))  # MAS*
```

### TOOL_META Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | MCP tool name (e.g., `"dna_translate"`) |
| `description` | Yes | Human-readable description for LLM |
| `seq_param` | No | Parameter name to pass through `resolve_to_seq`. Default: `"seq"`. Set to `None` for tools that don't operate on sequences. |

### Function Naming Convention

The function name must match the filename:
- `translate.py` contains `translate()`
- `reverse_complement.py` contains `reverse_complement()`
- `gc_content.py` contains `gc_content()`

This eliminates ambiguity and makes auto-discovery simple.

### Function Signature Requirements

- All parameters must have type hints
- Parameters with defaults become optional in the MCP schema
- The `seq` parameter (or whatever `seq_param` specifies) accepts heterogeneous input (see below)
- Return type should be `str`, `float`, `int`, `dict`, or `list`

## Sequence Resolution

The `resolve_to_seq()` function handles heterogeneous sequence inputs. Students don't call this directly; the plumbing invokes it automatically for the parameter specified by `seq_param`.

### Accepted Input Types

| Input | Example | Behavior |
|-------|---------|----------|
| Resource name | `"pBR322"` | Looks up in resource registry, parses file |
| GenBank content | `"LOCUS pBR322..."` | Parses with BioPython |
| FASTA content | `">seq1\nATGC..."` | Parses with BioPython |
| Raw sequence | `"ATGCGATCGATCG"` | Cleans whitespace, validates |
| Dirty sequence | `"ATG CGA\nTCG"` | Strips whitespace/numbers, validates |

### Valid Sequence Characters

After resolution, sequences contain only: `A T U C G R S Y K W M N` (DNA/RNA plus IUPAC ambiguity codes)

### Resolution Logic

```
resolve_to_seq(input):
    1. Strip whitespace from input
    2. If input is a registered resource name -> parse the file
    3. If input starts with "LOCUS" -> parse as GenBank string
    4. If input starts with ">" -> parse as FASTA string
    5. Otherwise -> clean as raw sequence (remove whitespace/numbers, validate)
```

## Resource Registry

Resources are sequence files in the `data/` directory. They are registered automatically based on file presence.

### Auto-Registration

All files in `data/` with recognized extensions are registered:
- `.gb`, `.gbk`, `.genbank` - GenBank format
- `.fa`, `.fasta`, `.fna` - FASTA format

The resource name is the filename without extension:
- `data/pBR322.gb` -> resource name `"pBR322"`
- `data/ecoli_k12.fasta` -> resource name `"ecoli_k12"`

### Resource Metadata

For `resources/list`, each resource returns metadata (not content):

```json
{
  "uri": "resource://seq_basics/pBR322",
  "name": "pBR322",
  "description": "...",
  "mimeType": "application/genbank",
  "size": 4361
}
```

The description is auto-generated from the file:
- GenBank: extracted from DEFINITION line
- FASTA: extracted from header line

### Custom Resource Metadata (Optional)

To override auto-generated metadata, create a `.meta.json` file:

```json
// data/pBR322.meta.json
{
  "description": "Classic cloning vector, 4361bp, contains ampR and tetR",
  "tags": ["plasmid", "cloning vector", "ampicillin", "tetracycline"]
}
```

## Auto-Discovery Flow

At server startup:

```
1. For each module in modules/:
   a. Scan tools/*.py (excluding _*.py)
      - Import module
      - Extract TOOL_META and function
      - Wrap function with resolve_to_seq for seq_param
      - Register with MCP

   b. Scan data/* for sequence files
      - Register each as a resource
      - Extract or load metadata

   c. Scan resources/*.py for custom resources (optional)
      - Import and register
```

## MCP Registration Details

### Tool Registration

Each tool function is wrapped before registration:

```python
def wrap_tool(func, meta):
    seq_param = meta.get("seq_param", "seq")

    def wrapped(**kwargs):
        if seq_param and seq_param in kwargs:
            kwargs[seq_param] = resolve_to_seq(kwargs[seq_param])
        return func(**kwargs)

    return wrapped
```

The MCP tool schema is auto-generated from the function signature:

```python
def translate(seq: str, start: int = None, end: int = None, frame: int = 1) -> str:
```

Becomes:

```json
{
  "name": "dna_translate",
  "description": "Translate DNA to protein using the standard genetic code.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "seq": {"type": "string", "description": "DNA sequence or resource name"},
      "start": {"type": "integer", "description": "Start position (0-indexed)"},
      "end": {"type": "integer", "description": "End position"},
      "frame": {"type": "integer", "description": "Reading frame 1, 2, or 3", "default": 1}
    },
    "required": ["seq"]
  }
}
```

### Parameter Descriptions

Parameter descriptions are extracted from the function's docstring (Google-style or NumPy-style) if present. Otherwise, a generic description is used.

## Testing Tools Standalone

Students can test their functions without MCP:

```bash
# Direct execution
python -m modules.seq_basics.tools.translate

# Or with pytest
pytest modules/seq_basics/tools/test_translate.py
```

The `if __name__ == "__main__":` block in each tool file allows quick manual testing.

## Adding a New Tool (Student Workflow)

1. Copy an existing tool file:
   ```bash
   cp modules/seq_basics/tools/translate.py modules/seq_basics/tools/gc_content.py
   ```

2. Edit the new file:
   - Update `TOOL_META` with new name and description
   - Rename the function to match filename
   - Implement the business logic

3. Test standalone:
   ```bash
   python -m modules.seq_basics.tools.gc_content
   ```

4. Restart the server - tool is auto-discovered

## Adding a New Resource (Student Workflow)

1. Drop a sequence file in `data/`:
   ```bash
   cp my_plasmid.gb modules/seq_basics/data/
   ```

2. Optionally add metadata:
   ```bash
   echo '{"description": "My custom plasmid for project X"}' > modules/seq_basics/data/my_plasmid.meta.json
   ```

3. Restart the server - resource is auto-discovered

## Error Handling

### Tool Errors

Tool functions should raise `ValueError` for invalid inputs:

```python
def translate(seq: str, frame: int = 1) -> str:
    if frame not in (1, 2, 3):
        raise ValueError(f"Frame must be 1, 2, or 3, got {frame}")
    ...
```

The plumbing catches exceptions and returns them as MCP error responses.

### Resolution Errors

`resolve_to_seq()` raises `ValueError` for:
- Unknown resource names
- Unparseable file content
- Invalid sequence characters

## Client-Side Considerations

The MCP client (Gemini or Claude Code) sees:

1. **resources/list** - Metadata only, including descriptions
2. **tools/list** - All registered tools with schemas
3. **tools/call** - Executes tool; `seq` param can be resource name or raw sequence

The LLM typically:
1. Reviews available resources from metadata
2. Calls tools with resource names (e.g., `dna_translate(seq="pBR322", frame=1)`)
3. Or passes raw sequences for small inputs

## Future Extensions

### Chunked Reading

For very large sequences (genomes), add optional `offset` and `length` params:

```python
TOOL_META = {
    "name": "read_sequence",
    "description": "Read a portion of a sequence resource.",
    "seq_param": None,  # This tool manages its own resolution
}

def read_sequence(resource: str, offset: int = 0, length: int = 10000) -> str:
    """Read a chunk of sequence from a resource."""
    ...
```

### Multiple Sequence Parameters

For tools comparing two sequences:

```python
TOOL_META = {
    "name": "align_sequences",
    "description": "Align two DNA sequences.",
    "seq_params": ["seq1", "seq2"],  # Note: plural
}

def align_sequences(seq1: str, seq2: str) -> dict:
    ...
```

### Non-Sequence Tools

For tools that don't operate on sequences:

```python
TOOL_META = {
    "name": "list_features",
    "description": "List annotated features in a GenBank resource.",
    "seq_param": None,  # No sequence resolution
}

def list_features(resource: str) -> list:
    """Parse GenBank and return feature list."""
    ...
```

This tool would access the resource file directly, not through `resolve_to_seq`.

## SKILL.md (LLM Instructions)

Each module includes a `SKILL.md` file that provides guidance to the LLM on how to use the tools effectively. This is domain expertise that helps the LLM make better decisions.

### Claude Code Integration

Claude Code automatically discovers `SKILL.md` files in `.claude/skills/` directories. For this project, we symlink or copy module skills there:

```
.claude/
└── skills/
    └── seq_basics/
        └── SKILL.md -> ../../../modules/seq_basics/SKILL.md
```

Alternatively, students can place skills directly in `.claude/skills/` if they prefer.

### Gemini Client Integration

The Gemini client manually loads `SKILL.md` and injects it into the system prompt:

```python
def load_skill_context(module_path: Path) -> str:
    """Load SKILL.md if present."""
    skill_file = module_path / "SKILL.md"
    if skill_file.exists():
        return skill_file.read_text()
    return ""
```

This ensures the same skill instructions work for both Claude Code and the Gemini-based tester.

### SKILL.md Format

```markdown
---
name: seq-basics
description: DNA sequence analysis tools for bioinformatics
---

# Sequence Analysis Tools

## Overview

This module provides tools for basic DNA sequence manipulation:
translation, reverse complement, GC content, etc.

## Working with Resources

Available sequence resources can be listed with `resources/list`.
Each resource has a name (e.g., "pBR322") that can be passed directly
to tools instead of raw sequence data.

**Prefer resource names over raw sequences** when the data is available
as a resource. This avoids token limits and keeps context clean.

## Tool Usage Guidelines

### dna_translate

Translates DNA to protein. Consider:
- Check all 3 reading frames when searching for ORFs
- Frame 1 starts at position 0, frame 2 at position 1, frame 3 at position 2
- Stop codons appear as '*' in output

### dna_reverse_complement

Returns the reverse complement. Useful for:
- Getting the sequence of the opposite strand
- Preparing sequences for primer design

## Common Workflows

### Finding ORFs in a plasmid
1. Get resource metadata to understand what's available
2. Translate in all 3 frames on forward strand
3. Translate in all 3 frames on reverse complement
4. Look for long stretches without stop codons

### Analyzing a gene
1. Use resource name to reference the sequence
2. Specify start/end coordinates if analyzing a specific region
3. Translate to verify the expected protein
```

### SKILL.md Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Skill identifier (used for slash command in Claude Code) |
| `description` | Yes | Brief description for LLM to understand when to apply this skill |

### What to Include in SKILL.md

1. **Overview** - What this module does at a high level
2. **Resource guidance** - How to work with available data files
3. **Tool-specific tips** - Nuances for each tool (edge cases, best practices)
4. **Common workflows** - Step-by-step patterns for typical tasks
5. **Domain knowledge** - Bioinformatics context the LLM might not know

### What NOT to Include

- Tool schemas (auto-generated from code)
- Implementation details (the LLM calls tools, doesn't need to know internals)
- Overly verbose explanations (keep it concise, LLMs have limited context)

## Adding a New Module (Student Workflow)

To create a new skill area (e.g., `cloning_tools`):

1. Copy the module structure:
   ```bash
   cp -r modules/seq_basics modules/cloning_tools
   ```

2. Update `modules/cloning_tools/SKILL.md` with domain-specific guidance

3. Replace tools in `modules/cloning_tools/tools/` with new implementations

4. Add any data files to `modules/cloning_tools/data/`

5. Register the module in `modules/__init__.py`

6. Optionally symlink for Claude Code:
   ```bash
   mkdir -p .claude/skills/cloning_tools
   ln -s ../../../modules/cloning_tools/SKILL.md .claude/skills/cloning_tools/SKILL.md
   ```
