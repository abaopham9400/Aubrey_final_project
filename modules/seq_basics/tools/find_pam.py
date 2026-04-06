from typing import Optional, List, Tuple
from modules.seq_basics.tools.validate_DNA import validate_DNA
from modules.seq_basics.tools.reverse_complement import reverse_complement

def find_pam(target: str) -> List[Tuple[int, str]]:
    """
    Description:
        Finds the position of all occurrences of the 'NGG' PAM sequence (targeting both 
        the sense and anti-sense strands) in a DNA target sequence.

    Input:
        target (str): The DNA sequence to be searched. The input string must consist of valid DNA
                      nucleotides ('A', 'T', 'C', 'G').

    Output:
        list of tuples: A list containing tuples of (index, strand) for all occurrences 
                        of a valid PAM after the 23rd position.
                        Example: [(32, '+'), (36, '-')]

    Tests:
        - Case:
            Input: seq="CCCTAGATGCCTGGCTCAGAAACCTGCCAGTTTGCTGGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGTCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
            Expected Output: [(36, '+')]
            Description: Basic sequence.
        - Case:
            Input: seq="CCCTAGATGCCTGGCTCAGAAACCTGCCAGTTTGCTGGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGGCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
            Expected Output: [(36, '+'), (73, '+')]
            Description: multiple pam sites
        - Case:
            Input: seq="CCCTAGATGCCTGGCGGAGAAACCTGCCAGTTTGCTGTCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGTCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
            Expected Output: []
            Description: Early GG; lack valid GG after 20th bp (Returns empty list)
    """
    if not validate_DNA(target):
        raise ValueError("Invalid target sequence")
    if len(target) < 23:
        raise ValueError(f"Target sequence must be at least 23bp (20bp guide + 3bp PAM). Provided length: {len(target)}")

    # Helper function to get raw indices of 'GG' for a given sequence string
    def get_indices(seq: str) -> List[int]:
        found_indices = []
        # Start searching from index 21 (meaning the 22nd base, leaving room for a 20bp guide + N)
        current_pos = seq.find('GG', 21)

        while current_pos != -1:
            found_indices.append(current_pos)
            # To find the NEXT instance, start searching from current_pos + 1
            # This allows for overlapping 'GGG' to return both indices
            current_pos = seq.find('GG', current_pos + 1)

        return found_indices

    # 1. Find targets on the (+) sense strand
    top_indices = get_indices(target)
    pam_locations = [(idx, '+') for idx in top_indices]

    # 2. Find targets on the (-) anti-sense strand
    reverse_target = reverse_complement(target)
    rev_indices = get_indices(reverse_target)
    seq_length = len(target)

    # Map the reverse indices back to the 5'->3' top strand coordinates
    # and create the list of tuples using a list comprehension
    bottom_strand_pams = [(seq_length - rev_idx - 2, '-') for rev_idx in rev_indices]
    
    # Use extend() to add the bottom strand tuples to our main list
    pam_locations.extend(bottom_strand_pams)

    # 3. Sort the list so indices appear in numerical order regardless of strand
    # lambda x: x[0] tells the sort function to look at the first item in the tuple (the index number)
    pam_locations.sort(key=lambda x: x[0])

    return pam_locations
 
 
# ---------------------------------------------------------------------------
# Module-level alias — keeps existing tests and direct imports working.
#
#   from modules.seq_basics.tools.find_pam import find_pam
#
# The alias creates ONE shared instance and exposes run() as a plain callable.
# ---------------------------------------------------------------------------
# _instance = find_pam()
# _instance.initiate()
# find_pam = _instance.run   # callable: find_pam(target) -> list
 
 
# Standalone test
if __name__ == "__main__":
    # Note: Because we now check both strands, your test outputs might find more PAMs 
    # than just the top-strand ones you originally noted!
    
    test = "CCCTAGATGCCTGGCTCAGAAACCTGCCAGTTGGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGTCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
    print(f"Test #1: {find_pam(test)}") # finds PAM on sense strand: [32] and on anti-sense strand: [0,1,9,22,26]

    test = "CCCTAGATGCCTGGCTCAGAGTACGATCAACCTGCCAGTTGGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGTCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
    print(f"Test #2: {find_pam(test)}") # finds PAM on sense strand: [40] and on anti-sense strand: [0,1,9,26,30,34]

    test = "CCCTAGATGCCTGGCTCAGAGTACGATCAACCGGCCAGTTGGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGTCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
    print(f"Test #3: {find_pam(test)}") # finds PAM on sense strand: [32,40] and on anti-sense strand: [0,1,9,30,34]

    test = "CCCTAGATGCCTGGCTCAGAAACCTGCCAGTTTGCTGGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGGCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
    print(f"Test #4: {find_pam(test)}") # finds PAM on sense strand: [36,73] and on anti-sense strand: [0,1,9,22,26]

    test = "CCCTAGATGCCTGGCTCAGAGTACGATCAACCTGCCAGTTCGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGTCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
    print(f"Test #5: {find_pam(test)}") # should not find any valid GG on sense strand and finds PAM on anti-sense strand: [0,1,9,30,34]