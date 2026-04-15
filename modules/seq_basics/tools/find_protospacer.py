from typing import Optional
from modules.seq_basics.tools.find_pam import find_pam
from modules.seq_basics.tools.reverse_complement import reverse_complement

def find_protospacer(target):
    """
    Description:
        Identifies the protospacer sequence within a DNA target sequence based on the location of the PAM sequence. 
        The protospacer is a 20 base pair sequence that immediately precedes the PAM sequence ('NGG'). This function 
        locates the PAM sequence using the `find_pam` function and then extracts the 20 bp protospacer sequence located 
        just before it.

    Inputs:
        target (str): The DNA sequence to be searched. The input string must consist of valid DNA
                      nucleotides ('A', 'T', 'C', 'G').

    Outputs:
        list of str: A list of the 20 base pair protospacer sequences found. Sequences from 
                     the anti-sense strand are returned as their 5'->3' reverse complement.

    Tests:
        - Case:
            Input: target="CCCTAGATGCCTGGCTCAGAAACCTGCCAGTTTGCTGGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGTCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
            Expected Output: [
                'GTTTCTGAGCCAGGCATCTA', 
                'GGTTTCTGAGCCAGGCATCT', 
                'AACTGGCAGGTTTCTGAGCC', 
                'AAACGTGCCAGCAAACTGGC', 
                'AAAAAAACGTGCCAGCAAAC', 
                'TCAGAAACCTGCCAGTTTGC'
            ]
            Description: Finds all valid protospacers from both the sense and anti-sense strands of a sequence.
        - Case:
            Input: target="ATGAACTGGTACGGATCCGATCAT"
            Expected Exception: ValueError
            Description: The Sequence is too short for a valid protospacer
    """
    # Find the index of the PAM sequence using the find_pam function
    pam_index = find_pam(target)
    protospacer = []

    for pam in pam_index:
        index, strand = pam
        if strand == '+':
            top_strand_slice = target[index-21:index-1]
            protospacer.append(top_strand_slice)
        else:
            top_strand_slice = target[index+3:index+23]
            protospacer.append(reverse_complement(top_strand_slice)) # protospacer is no the anti-sense strand

    if len(protospacer) == 0:
        raise ValueError("Protospacer can not be located")

    return protospacer


# Standalone test
if __name__ == "__main__":
    test = "CCCTAGATGCCTGGCTCAGAAACCTGCCAGTTGGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGTCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
    valid = find_protospacer(test) == ['GTTTCTGAGCCAGGCATCTA','GGTTTCTGAGCCAGGCATCT','AACTGGCAGGTTTCTGAGCC',
                                       'AAAAAAACGTGCCAACTGGC','AAAGAAAAAAACGTGCCAAC','TGGCTCAGAAACCTGCCAGT']
    print(f"Test #1: {valid}") # varifies that it returns the correct protospacer

    test = "CCCTAGATGCCTGGCTCAGAGTACGATCAACCTGCCAGTTGGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGTCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
    valid = find_protospacer(test) == ['TACTCTGAGCCAGGCATCTA','GTACTCTGAGCCAGGCATCT','GGTTGATCGTACTCTGAGCC',
                                       'AAAAAAACGTGCCAACTGGC','AAAGAAAAAAACGTGCCAAC','AGTACGATCAACCTGCCAGT']
    print(f"Test #2: {valid}") # should find 20bp behind NGG

    test = "CCCTAGATGCCTGGCTCAGAAACCTGCCAGTTTGCTGGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGGCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
    valid = find_protospacer(test) == ['GTTTCTGAGCCAGGCATCTA','GGTTTCTGAGCCAGGCATCT','AACTGGCAGGTTTCTGAGCC',
                                       'AAACGTGCCAGCAAACTGGC','AAAAAAACGTGCCAGCAAAC','TCAGAAACCTGCCAGTTTGC',
                                       'TTGTCTTTAGTTCTCACGTT']
    print(f"Test #3: {valid}") # test for multiple protospacers

    test = "ACTTAGATGCTTGGCTCAGAGTACGATCAACGTGACAGTTCGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGTCATACTTGACAACGCTTCTTTAACCAAATATAATTGTTC"
    #print(f"Test #4: {find_protospacer(test)}") # should not find any valid GG on sense and no valid CC on anti-sense