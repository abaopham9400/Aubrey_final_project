from typing import Optional
from modules.seq_basics.tools.find_protospacer import find_protospacer
from modules.seq_basics.tools.calculate_score import calculate_score

class Design_Cas9_RNA:
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
    def initiate(self) -> None:
        """One-time setup: Define the gRNA scaffold sequence."""
        self.trcrRNA = 'GTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGC'

    def run(self, target):
        protospacer = find_protospacer(target)

        cas9_DNA = []
        for proto in protospacer:
            guide = proto + self.trcrRNA
            cas9_DNA.append(guide)

        # converts to RNA
        cas9_RNA = [dna.replace('T', 'U') for dna in cas9_DNA]

        # ranks each gRNA
        cas9_RNA_ranked = calculate_score(cas9_RNA, target)

        # Return the full Cas9 guide sequence
        return cas9_RNA_ranked
 
 
# ---------------------------------------------------------------------------
#Module-level alias — keeps existing tests and direct imports working.
#
#   from modules.seq_basics.tools.design_cas9_RNA import design_cas9_RNA
#
# The alias creates ONE shared instance and exposes run() as a plain callable.
# ---------------------------------------------------------------------------
_instance = Design_Cas9_RNA()
_instance.initiate()
design_cas9_RNA = _instance.run   # callable: find_pam(target) -> int
 
 
# Standalone test
if __name__ == "__main__":
    test1 = "CTCTAGATGTCTGGCTCAGAAACATGCGAGTTGGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGTCATACTTGACAACGCTTCTTTAACGAAATATAATTGTTC"
    valid = design_cas9_RNA(test1) #== ['UGGCUCAGAAACAUGCGAGUGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGC']
    print(f"Test #1: {valid}") # should find protospacer with PAM at index 32 and add the trcrRNA

    test2 = "CTCTAGATGTCTGGCTCAGAAACATGCGAGTTGGCACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGCCATACTTGACAACGCTTCTTTAACGAAATATAATTGTTC"
    valid = design_cas9_RNA(test2) #== ['UGGCUCAGAAACAUGCGAGUGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGC', 'UAAAGAAGCGUUGUCAAGUAGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGC']
    print(f"Test #2: {valid}") # there are two valid protospacers

    test3 = "CTCTAGATGTCTGGCTCAGAAACATGCGAGTTGACACGTTTTTTTCTTTTGTCTTTAGTTCTCACGTTTGTCATACTTGACAACGCTTCTTTAACGAAATATAATTGTTC"
    #valid = design_cas9_RNA(test3) == []
    #print(f"Test #3: {valid}") # should throw an error since no valid PAM