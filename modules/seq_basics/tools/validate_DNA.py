from typing import Optional
import os
import re

def validate_DNA(seq):
    """
    Description:
        Validates whether a given string contains only valid DNA nucleotides (A, T, C, G).

    Inputs:
        seq (str): The input string to be checked. This string can contain any characters,
                   and the function will determine if it exclusively contains 'A', 'T', 'C', and 'G'.

    Outputs:
        bool: Returns True if the string contains only 'A', 'T', 'C', and 'G';
              otherwise, returns False.

    Tests:
        - Case:
            Input: seq="AxTCAGAGATCAG"
            Expected Output: False
            Description: x is not a valid character
        - Case:
            Input: seq="A TCAGAGATCAG"
            Expected Output: False
            Description: spaces are not allowed
        - Case:
            Input: seq="1 ATCAGAGATCAG"
            Expected Output: False
            Description: numbers are not allowed
        - Case:
            Input: seq="1 atcagagatcag"
            Expected Output: False
            Description: lowercase is not alloed
        - Case:
            Input: seq="CCCTAGATGCCTGGCGGAGAAACCTGCCAGTTTGCTGTCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGTCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
            Expected Output: True
            Description: Valid DNA sequence
    """
    # Return False if seq is None (meaning there is no string, it is null, which is different from saying an empty string like "")
    if seq is None:
        return False

    # Check if every character in the string is a valid nucleotide
    return get_sequence_from_input(seq) or valid_sequence(seq)

# checks if its a valid DNA sequence
def valid_sequence(seq):
    if len(seq) < 23:
        raise ValueError(f"Target sequence must be at least 23bp (20bp guide + 3bp PAM). Provided length: {len(seq)}")
    
    # Define a set of valid nucleotides for DNA
    valid_nucleotides = {'A', 'T', 'C', 'G'}

    return all(nucleotide in valid_nucleotides for nucleotide in seq)

# check if input is a plasmid name
def get_sequence_from_input(target_input):
    # 1. Sanitize the input
    target_input = target_input.strip()
    
    # 2. Define your data directory path
    # This path goes up from 'tools/' to 'seq_basics/' then into 'data/'
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    
    # 3. Check for a local file match (e.g., pBR322.gb or pBR322.fasta)
    # We check common extensions so the user doesn't have to type them
    for ext in [".gb", ".gbk", ".fasta", ".fa"]:
        file_path = os.path.join(data_dir, f"{target_input}{ext}")
        if os.path.exists(file_path):
            return True

# ---------------------------------------------------------------------------
#Module-level alias — keeps existing tests and direct imports working.
#
#   from modules.seq_basics.tools.validate_DNA import validate_DNA
#
# The alias creates ONE shared instance and exposes run() as a plain callable.
# ---------------------------------------------------------------------------
#_instance = validate_DNA()
#validate_DNA = _instance.run   # callable: validate_DNA(seq) -> boolean

# Standalone test
if __name__ == "__main__":
    test = "ATCGTACPGACGT"
    print(f"Test #1: {validate_DNA(test) == False}") # not valid, contains others besdies ATCG

    test = "ATCGTAC1GACGT"
    print(f"Test #2: {validate_DNA(test) == False}") # not valid, contains a number

    test = "ATCGTAcGACGT"
    print(f"Test #3: {validate_DNA(test) == False}") # not valid, contains a lowercase

    test = "ATCGTA GACGT"
    print(f"Test #4: {validate_DNA(test) == False}") # not valid, contains a space

    test = "CAGTGTACGTACTGCAGTCAAGTC"
    print(f"Test #5: {validate_DNA(test) == True}") # valid DNA sequence

    