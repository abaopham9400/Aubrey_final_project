"""Translate DNA to protein."""

from .._utils import CODON_TABLE

TOOL_META = {
    "name": "dna_translate",
    "description": "Translate DNA to protein using the standard genetic code. The seq parameter accepts either a resource name (e.g., 'pBR322', 'mg1655') or a raw DNA sequence string. Use start/end to specify coordinates.",
    "seq_param": "seq",
}


def translate(seq: str, start: int = None, end: int = None, frame: int = 1) -> str:
    """Translate DNA sequence to protein.

    Args:
        seq: DNA sequence (resource name or raw sequence)
        start: Start position, 0-indexed (optional)
        end: End position (optional)
        frame: Reading frame 1, 2, or 3 (default: 1)

    Returns:
        Protein sequence as single-letter amino acids. Stop codons shown as '*'.
    """
    if frame not in (1, 2, 3):
        raise ValueError(f"Frame must be 1, 2, or 3, got {frame}")

    # Apply coordinates
    if start is not None or end is not None:
        seq = seq[start:end]

    # Apply frame offset (frame 1 = no offset, frame 2 = skip 1, frame 3 = skip 2)
    if frame in (2, 3):
        seq = seq[frame - 1:]

    # Translate
    protein = []
    for i in range(0, len(seq) - 2, 3):
        codon = seq[i:i+3]
        protein.append(CODON_TABLE.get(codon, "X"))

    return "".join(protein)


# For standalone testing
if __name__ == "__main__":
    # Test with a simple sequence
    test_seq = "ATGGCTAGCTAG"
    print(f"Input: {test_seq}")
    print(f"Frame 1: {translate(test_seq, frame=1)}")
    print(f"Frame 2: {translate(test_seq, frame=2)}")
    print(f"Frame 3: {translate(test_seq, frame=3)}")
