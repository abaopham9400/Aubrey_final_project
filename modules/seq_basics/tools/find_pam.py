from typing import Optional
from validate_DNA import validate_DNA

def find_PAM(target):
    """
    Description:
        Finds the position of the first occurrence of the 'GG' PAM sequence in a DNA target sequence.

    Input:
        target (str): The DNA sequence to be searched. The input string must consist of valid DNA
                      nucleotides ('A', 'T', 'C', 'G').

    Output:
        int: The index of the first occurrence of 'GG' in the target sequence after the 23rd position.

    Tests:
        - Case:
            Input: seq="CCCTAGATGCCTGGCTCAGAAACCTGCCAGTTTGCTGGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGTCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
            Expected Output: 36
            Description: Basic sequence.
        - Case:
            Input: seq="CCCTAGATGCCTGGCGGAGAAACCTGCCAGTTTGCTGTCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGTCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
            Expected Exception: ValueError
            Description: Early GG; lack valid GG after 20th bp
    """
    if not validate_DNA(target):
        raise ValueError("Invalid target sequence")
    if len(target) < 23:
        raise ValueError(f"Target sequence must be at least 23bp (20bp guide + 3bp PAM). Provided length: {len(target)}")

    if target[21:].find('GG') == -1:
      raise ValueError("Does not contain valid PAM")

    pam_index = target.find("GG", 21)

    return pam_index
 
 
# ---------------------------------------------------------------------------
#Module-level alias — keeps existing tests and direct imports working.
#
#   from modules.seq_basics.tools.find_pam import find_PAM
#
# The alias creates ONE shared instance and exposes run() as a plain callable.
# ---------------------------------------------------------------------------
#_instance = find_PAM()
#_instance.initiate()
#find_PAM = _instance.run   # callable: find_pam(target) -> int
 
 
# Standalone test
if __name__ == "__main__":
    test = "CCCTAGATGCCTGGCTCAGAAACCTGCCAGTTGGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGTCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
    print(f"Test #1: {find_PAM(test)}") # should find GG at index 32

    test = "CCCTAGATGCCTGGCTCAGAGTACGATCAACCTGCCAGTTGGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGTCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
    print(f"Test #2: {find_PAM(test)}") # should find GG at index 40

    test = "CCCTAGATGCCTGGCTCAGAGTACGATCAACCTGCCAGTTCGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGTCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
    print(f"Test #3: {find_PAM(test)}") # should not find any valid GG