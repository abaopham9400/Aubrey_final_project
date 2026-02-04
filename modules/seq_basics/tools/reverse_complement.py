"""Compute reverse complement of DNA sequence."""

TOOL_META = {
    "name": "dna_reverse_complement",
    "description": "Return the reverse complement of a DNA sequence. The seq parameter accepts either a resource name (e.g., 'pBR322', 'mg1655') or a raw DNA sequence string.",
    "seq_param": "seq",
}

# Complement mapping (includes IUPAC ambiguity codes)
_COMPLEMENT = {
    "A": "T", "T": "A", "C": "G", "G": "C",
    "U": "A",  # RNA
    "R": "Y", "Y": "R",  # Purine/Pyrimidine
    "S": "S", "W": "W",  # Strong/Weak (self-complementary)
    "K": "M", "M": "K",  # Keto/Amino
    "N": "N",  # Any
}


def reverse_complement(seq: str) -> str:
    """Compute the reverse complement of a DNA sequence.

    Args:
        seq: DNA sequence (resource name or raw sequence)

    Returns:
        Reverse complement of the input sequence.
    """
    try:
        return "".join(_COMPLEMENT[b] for b in reversed(seq))
    except KeyError as e:
        raise ValueError(f"Invalid base for complement: {e.args[0]}") from None


# For standalone testing
if __name__ == "__main__":
    test_seq = "ATGCGATCG"
    print(f"Input:    {test_seq}")
    print(f"RevComp:  {reverse_complement(test_seq)}")

    # Test with ambiguity codes
    test_ambig = "ATRYSWKM"
    print(f"\nInput:    {test_ambig}")
    print(f"RevComp:  {reverse_complement(test_ambig)}")
