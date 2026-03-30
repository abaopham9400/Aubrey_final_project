from typing import Optional
from find_pam import find_PAM

def find_protospacer(target):
    """
    Description:
        Identifies the protospacer sequence within a DNA target sequence based on the location of the PAM sequence. 
        The protospacer is a 20 base pair sequence that immediately precedes the PAM sequence ('NGG'). This function 
        locates the PAM sequence using the `find_PAM` function and then extracts the 20 bp protospacer sequence located 
        just before it.

    Inputs:
        target (str): The DNA sequence to be searched. The input string must consist of valid DNA
                      nucleotides ('A', 'T', 'C', 'G').

    Outputs:
        str: The 20 base pair protospacer sequence found immediately before the PAM sequence.

    Tests:
        - Case:
            Input: target="CCCTAGATGCCTGGCTCAGAAACCTGCCAGTTTGCTGGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGTCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
            Expected Output: "TCAGAAACCTGCCAGTTTGC"
            Description: Finds the protospacer from a valid sequence.
        - Case:
            Input: target="ATGAACTGGTACGGATCCGATCAT"
            Expected Exception: ValueError
            Description: The Sequence is too short for a valid protospacer
    """
    # Find the index of the PAM sequence using the find_PAM function
    pam_index = find_PAM(target)

    protospacer = target[pam_index-21:pam_index-1]

    return protospacer


# Standalone test
if __name__ == "__main__":
    test = "CCCTAGATGCCTGGCTCAGAAACCTGCCAGTTGGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGTCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
    valid = find_protospacer(test) == "TGGCTCAGAAACCTGCCAGT"
    print(f"Test #1: {valid}") # varifies that it returns the correct protospacer

    test = "CCCTAGATGCCTGGCTCAGAGTACGATCAACCTGCCAGTTGGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGTCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
    valid = find_protospacer(test) == "AGTACGATCAACCTGCCAGT"
    print(f"Test #2: {valid}") # should find 20bp behind NGG

    test = "CCCTAGATGCCTGGCTCAGAGTACGATCAACCTGCCAGTTCGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGTCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
    print(f"Test #3: {find_PAM(test)}") # should not find any valid GG