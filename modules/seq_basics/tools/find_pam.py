from typing import Optional
from modules.seq_basics.tools.validate_DNA import validate_DNA

def find_pam(target):
    """
    Description:
        Finds the position of all occurrence of the 'GG' PAM sequence in a DNA target sequence.

    Input:
        target (str): The DNA sequence to be searched. The input string must consist of valid DNA
                      nucleotides ('A', 'T', 'C', 'G').

    Output:
        list: The index of all occurrence of 'GG' in the sequence after the 23rd position.

    Tests:
        - Case:
            Input: seq="CCCTAGATGCCTGGCTCAGAAACCTGCCAGTTTGCTGGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGTCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
            Expected Output: [36]
            Description: Basic sequence.
        - Case:
            Input: seq="CCCTAGATGCCTGGCTCAGAAACCTGCCAGTTTGCTGGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGGCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
            Expected Output: [36,73]
            Description: multiple pam sites
        - Case:
            Input: seq="CCCTAGATGCCTGGCGGAGAAACCTGCCAGTTTGCTGTCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGTCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
            Expected Exception: ValueError
            Description: Early GG; lack valid GG after 20th bp
    """
    if not validate_DNA(target):
        raise ValueError("Invalid target sequence")
    if len(target) < 23:
        raise ValueError(f"Target sequence must be at least 23bp (20bp guide + 3bp PAM). Provided length: {len(target)}")

    pam_indices = []
    # Start searching from index 21
    current_pos = target.find('GG', 21)

    # If no GG is found at all after index 21, raise the error immediately
    if current_pos == -1:
        return []

    while current_pos != -1:
        pam_indices.append(current_pos)
        # To find the NEXT instance, start searching from current_pos + 1
        # This allows for overlapping 'GGG' to return both indices
        current_pos = target.find('GG', current_pos + 1)

    return pam_indices
 
 
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
    print(f"Test #1: {find_pam(test)}") # should find GG at index [32]

    test = "CCCTAGATGCCTGGCTCAGAGTACGATCAACCTGCCAGTTGGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGTCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
    print(f"Test #2: {find_pam(test)}") # should find GG at index [40]

    test = "CCCTAGATGCCTGGCTCAGAGTACGATCAACCGGCCAGTTGGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGTCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
    print(f"Test #3: {find_pam(test)}") # should find GG at index [32,40]

    test = "CCCTAGATGCCTGGCTCAGAAACCTGCCAGTTTGCTGGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGGCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
    print(f"Test #4: {find_pam(test)}") # should find GG at index [36,73]

    test = "CCCTAGATGCCTGGCTCAGAGTACGATCAACCTGCCAGTTCGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGTCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
    print(f"Test #3: {find_pam(test)}") # should not find any valid GG and return []