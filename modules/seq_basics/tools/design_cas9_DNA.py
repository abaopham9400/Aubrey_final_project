from typing import Optional
from modules.seq_basics.tools.find_protospacer import find_protospacer

def design_cas9_DNA(target):
    """
    Description:
        Designs a DNA sequence for use in CRISPR-Cas9 gene editing by combining a protospacer sequence
        with a standard gRNA scaffold.

    Input:
        target (str): The DNA sequence to be searched. The input string must consist of valid DNA
                      nucleotides ('A', 'T', 'C', 'G').

    Output:
        str: A DNA sequence that includes the protospacer followed by the gRNA scaffold sequence.

    Tests:
        - Case:
            Input: target="CCCTAGATGCCTGGCTCAGAAACCTGCCAGTTGGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGTCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
            Expected Output: ['TGGCTCAGAAACCTGCCAGTGTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGC']
            Description: Basic sequence with a single GG.
        - Case:
            Input: target="CCCTAGATGCCTGGCTCAGAAACCTGCCAGTTTGCTGGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGGCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
            Expected Output: ['TCAGAAACCTGCCAGTTTGCGTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGC','TTGTCTTTAGTTCTCACGTTGTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGC']
            Description: multiple pam sites, means mutliple cas9_DNA
    """
    # Find the protospacer sequence within the target DNA
    protospacer = find_protospacer(target)

    # Define the gRNA scaffold sequence
    trcrRNA = 'gttttagagctagaaatagcaagttaaaataaggctagtccgttatcaacttgaaaaagtggcaccgagtcggtgc'.upper()

    cas9_DNA = []
    for proto in protospacer:
        guide = proto + trcrRNA
        cas9_DNA.append(guide)

    # Return the full Cas9 guide sequence
    return cas9_DNA
 
 
# ---------------------------------------------------------------------------
#Module-level alias — keeps existing tests and direct imports working.
#
#   from modules.seq_basics.tools.find_pam import find_pam
#
# The alias creates ONE shared instance and exposes run() as a plain callable.
# ---------------------------------------------------------------------------
#_instance = find_pam()
#_instance.initiate()
#find_pam = _instance.run   # callable: find_pam(target) -> int
 
 
# Standalone test
if __name__ == "__main__":
    test = "CCCTAGATGCCTGGCTCAGAAACCTGCCAGTTGGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGTCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
    valid = design_cas9_DNA(test) == ['TGGCTCAGAAACCTGCCAGTGTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGC']
    print(f"Test #1: {valid}") # should find GG at index [32]