# BioE234 MCP Starter

A minimal MCP (Model Context Protocol) server for bioinformatics, with a Gemini-powered CLI client for testing.

## Overview

This project provides a framework for building bioinformatics tools that can be used with LLM assistants like Claude Code or Google Gemini. Students write pure Python functions for sequence analysis; the framework handles all MCP connectivity automatically.

**Key features:**
- Auto-discovery of tools and resources (no registration code needed)
- Tools accept resource names or raw sequences interchangeably
- SKILL.md files provide domain guidance to LLMs
- Compatible with both Claude Code and Gemini

## Quick Start

1. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   # or: .venv\Scripts\Activate.ps1  # Windows
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**

   Create a `.env` file with your Gemini API key:
   ```
   GEMINI_API_KEY="YOUR_KEY_HERE"
   ```
   Get a free key at https://ai.google.dev

4. **Run the client**
   ```bash
   python client_gemini.py
   ```

## Project Structure

```
.
├── server.py                 # MCP server entry point
├── client_gemini.py          # Gemini-powered CLI client
├── SPEC.md                   # Architecture specification
├── modules/
│   └── seq_basics/           # Example module
│       ├── SKILL.md          # LLM guidance for this module
│       ├── _plumbing/        # Auto-registration (don't modify)
│       ├── _utils.py         # Shared constants (codon table, etc.)
│       ├── data/
│       │   └── pBR322.gb     # Sequence resources
│       └── tools/
│           ├── translate.py
│           └── reverse_complement.py
```

## Adding a New Tool

1. Copy an existing tool file:
   ```bash
   cp modules/seq_basics/tools/translate.py modules/seq_basics/tools/gc_content.py
   ```

2. Edit the new file:
   ```python
   """Calculate GC content of a DNA sequence."""

   TOOL_META = {
       "name": "gc_content",
       "description": "Calculate the GC content (proportion of G and C bases).",
       "seq_param": "seq",
   }

   def gc_content(seq: str) -> float:
       """Calculate GC content.

       Args:
           seq: DNA sequence (resource name or raw sequence)

       Returns:
           GC content as a fraction (0.0 to 1.0)
       """
       gc = sum(1 for b in seq if b in "GC")
       return gc / len(seq) if seq else 0.0

   if __name__ == "__main__":
       print(gc_content("ATGCGCTA"))  # 0.5
   ```

3. Restart the server. The tool is auto-discovered.

## Adding a New Resource

1. Drop a sequence file in `data/`:
   ```bash
   cp my_plasmid.gb modules/seq_basics/data/
   ```

2. Optionally add metadata:
   ```bash
   echo '{"description": "My custom plasmid"}' > modules/seq_basics/data/my_plasmid.meta.json
   ```

3. Restart the server. The resource is auto-discovered.

## Available Tools

### dna_translate
Translate DNA to protein using the standard genetic code.

```
dna_translate(seq="pBR322", start=0, end=300, frame=1)
dna_translate(seq="ATGGCTAGC")
```

### dna_reverse_complement
Return the reverse complement of a DNA sequence.

```
dna_reverse_complement(seq="pBR322")
dna_reverse_complement(seq="ATGCGATCG")
```

## Client Commands

```
/help                         Show help
/tools                        List available tools
/resources                    List available resources
/resource <uri>               Read a resource
/prompts                      List prompts
/prompt <name> [json_args]    Render and run a prompt
```

Or just type natural language requests:
```
You: Translate the first 100bp of pBR322 in frame 2
```

## Claude Code Integration

This project is designed to work with Claude Code. To use as an MCP server:

1. Add to your Claude Code MCP settings
2. Tools and resources will be available in Claude Code
3. SKILL.md provides guidance automatically

To make skills discoverable by Claude Code, symlink them:
```bash
mkdir -p .claude/skills/seq-basics
ln -s ../../../modules/seq_basics/SKILL.md .claude/skills/seq-basics/SKILL.md
```

## Architecture

See [SPEC.md](SPEC.md) for the full architecture specification, including:
- Tool file conventions
- Sequence resolution logic
- Auto-discovery flow
- SKILL.md format

## For Students

Focus on writing pure functions in `tools/`. The framework handles:
- MCP registration
- Resource name resolution
- Sequence format parsing (GenBank, FASTA, raw)
- Input validation

Your functions receive clean sequence strings and return results. Test standalone:
```bash
python -m modules.seq_basics.tools.translate
```
