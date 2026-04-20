import re

# input a plasmid name i.e. pBR322
def get_sequence(seq_name):
    valid_nucleotides = {'A', 'T', 'C', 'G'}
    if all(nucleotide in valid_nucleotides for nucleotide in seq_name):
        return seq_name

    with open(f"modules/seq_basics/data/{seq_name}.gb", "r") as f:
        content = f.read()
        # Find the ORIGIN section (the actual DNA sequence)
        sequence_match = re.search(r"ORIGIN\s+(.*)//", content, re.DOTALL)
        if sequence_match:
            # Clean out numbers and whitespace
            raw_seq = sequence_match.group(1)
            clean_seq = "".join(re.findall(r'[atgc]+', raw_seq.lower()))
            return clean_seq.upper()
        
if __name__ == "__main__":
    seq = get_sequence("pBR322")
    print(f"Sequence length: {len(seq)}")

    seq = get_sequence("ACTGACTGCGTAACTGACTGACGTACGTACTGACGTACTG")
    print(f"Sequence length: {seq}")