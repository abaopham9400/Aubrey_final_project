import requests
import re

def get_sequence(symbol, species="human"):
    # determines if input is a raw sequence
    valid_nucleotides = {'A', 'T', 'C', 'G'}
    if all(nucleotide in valid_nucleotides for nucleotide in symbol):
        return symbol

    server = "https://rest.ensembl.org"
    
    # 1. Get the Ensembl ID
    ext = f"/lookup/symbol/{species}/{symbol}?"
    r = requests.get(server + ext, headers={"Content-Type": "application/json"})
    gene_id = r.json().get("id")
    
    # 2. Get the sequence
    ext = f"/sequence/id/{gene_id}?"
    r = requests.get(server + ext, headers={"Content-Type": "text/x-fasta"})
    clean_test = r.text.replace("\n", "").replace("\r", "").replace(" ", "").upper()
    just_dna = clean_test.split(":")[-1][2:]
    return just_dna

def get_just_the_dna(data):
    parts = data.strip().split('\n', 1) 

    # 2. Get the sequence (the second part of the split)
    # We then use re to remove any internal newlines or spaces
    if len(parts) > 1:
        sequence = re.sub(r'\s+', '', parts[1])
    else:
        sequence = "No DNA found after header"
    
    return sequence

#print(get_sequence("BRCA2"))
#print(get_sequence("TP53"))
print(get_sequence("PTEN"))
