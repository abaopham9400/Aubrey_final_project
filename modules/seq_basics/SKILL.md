# seq_basics — Skill Guidance for Gemini

This file is read by the client at startup and injected into Gemini's system prompt.
Its purpose is to give Gemini the domain knowledge it needs to use the tools in this
module correctly and interpret their results meaningfully.

---

## What this module does

The `seq_basics` module provides fundamental DNA sequence analysis tools for working
with sequences stored as resources or provided as raw strings.

---

## Available resources

| Resource name | Description |
|---------------|-------------|
| `pBR322`      | E. coli cloning vector pBR322, 4361 bp, circular, double-stranded. A classic lab plasmid commonly used as a reference sequence. Contains genes for ampicillin resistance (bla) and tetracycline resistance (tet). |

When a user refers to "pBR322" or "the plasmid", use the resource name `"pBR322"` directly
as the sequence argument — do not ask the user to paste the sequence.

---

## Tools and when to use them

### `dna_reverse_complement`
Returns the reverse complement of a DNA or RNA sequence.

Use when the user asks for:
- "reverse complement of X"
- "complement of the bottom strand"
- "what does the antisense strand look like"
- "flip the sequence"

The result is the same length as the input. Uppercase output.

### `find_PAM`
Finds the index positions and strand orientation of all 'NGG' Protospacer Adjacent Motif (PAM) sequences.

Use when the user asks:
- "Find the PAM sites in this sequence."
- "Where can Cas9 bind?"
- "Does this DNA contain a valid PAM?"
- "List the NGG locations."

Technical details:
- Searches both the sense (+) and anti-sense (-) strands.
- Only identifies PAMs located after the 23rd position to allow for a preceding 20bp guide.
- Returns a list of tuples: (index, strand).

### 'find_protospacer'
Identifies the 20bp DNA sequences (protospacers) immediately preceding a valid PAM site.

Use when the user asks:
- "What are the protospacers in this sequence?"
- "Find the 20bp sequences upstream of the PAM."
- "Extract the target sequences for CRISPR."

Strand behavior:
- For the sense (+) strand, it extracts the 20bp immediately before the PAM.
- For the anti-sense (-) strand, it extracts the 20bp region and returns its reverse complement to provide the 5'->3' sequence.

### 'calculate_score'
Evaluates the efficacy and safety of a list of guide RNAs (sgRNAs) against a target genome sequence.

Use when the user asks:
- "Which of these gRNAs is the best?"
- "Check these guides for off-target effects."
- "Score these CRISPR sequences."
- "Rank these guides by efficiency."

Technical details:
- Efficiency Score: Calculates a base score based on GC content, with an ideal target of 50%.
- Sequence Penalties: Heavily penalizes sequences containing "TTTT" (Poly-T), which can terminate RNA polymerase III transcription.
- Off-target Analysis: Scans the provided genome for occurrences of the 20bp protospacer followed by an 'NGG' PAM.
- Scoring Logic: Each additional match in the genome (beyond the intended target) incurs a 30-point penalty.
- Output: Returns a list of dictionaries containing the full gRNA sequence and its final numerical score, sorted from highest to lowest.

### 'design_cas9_RNA'
Designs complete single guide RNA (sgRNA) sequences by combining a protospacer with a standard gRNA scaffold.

Use when the user asks to:
- "Design a gRNA for this sequence."
- "What is the best gRNA to use for this genome?"
- "Provide a list of possible guide RNAs and their scores."
- "Create a CRISPR tool for this target."

Output format:
- Returns a list of dictionaries containing the gRNA string (in RNA format, using 'U' instead of 'T') and a numerical score ranking its efficacy.
- The resulting sequence includes the 20bp protospacer followed by the scaffold: GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAucaacuugaaaaaguGGCACCGAGUCGGUGC.

---

## Interpreting results

- High Scores: A score of 90.0 or higher indicates a highly favorable guide. If multiple guides are returned, prioritize the one with the highest score for your experiment.
- Empty Results: If the tool returns an empty list, it means no valid NGG PAM sites were found far enough into the sequence (at least 23bp from the start) to allow for a full 20bp guide.
- RNA vs DNA: The output is an RNA sequence. When ordering synthetic oligos or designing primers for cloning, remember to convert these back to DNA (U → T) as required by your specific protocol.
- Scaffold Length: The total length of the output will be 96 nucleotides (20bp protospacer + 76bp scaffold). If your result is significantly different, verify that the input sequence was long enough to identify a full protospacer.

---

## Sequence input rules (handled automatically)

You never need to paste the full sequence. The framework resolves these automatically:
- The input requires a DNA sequence (ATCG)
- Input must be a string that is at least 23 characters long.
