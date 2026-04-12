from Bio.SeqUtils import gc_fraction
from Bio.Seq import Seq
import re

def calculate_score(grna_list, genome_sequence):
    """
    grna_list: List of strings
    genome_sequence: A string or Bio.Seq object
    """
    # Ensure genome is a string for regex processing
    genome_str = str(genome_sequence).upper()
    results = []

    for grna in grna_list:
        grna_long = grna.upper()
        grna = grna_long[0:20]
        
        # 1. Efficiency Score (GC Content)
        gc = gc_fraction(grna) * 100
        eff_score = 100 - abs(50 - gc) 
        
        # 2. Sequence Penalties (Poly-T)
        if "TTTT" in grna:
            eff_score -= 50

        # 3. Off-target Search (PAM: NGG)
        # We use a regex lookahead to find overlapping matches
        # The pattern looks for the gRNA followed by two of any character and a G
        pattern = re.compile(f"(?=({grna}..G))") 
        
        hits = len(pattern.findall(genome_str))
        
        # Penalty calculation: 1 hit is the intended target. 
        # Any additional hits are dangerous off-targets.
        off_penalty = max(0, hits - 1) * 30
        
        final_score = eff_score - off_penalty
        
        results.append({
            'gRNA': grna_long, 
            'score': round(final_score, 2), 
            'hits': hits
        })
    
    return sorted(results, key=lambda x: x['score'], reverse=True)

# --- Example Usage ---
user_genome = "ATCGATCGATCGATCGATCGGGATCGATCGATCGATCGATCGCGG" # Direct string input
my_grnas = ["ATCGATCGATCGATCGATCG", "CCGGCCGGCCGGCCGGCCGG"]

rankings = calculate_score(my_grnas, user_genome)

for r in rankings:
    print(f"gRNA: {r['gRNA']} | Score: {r['score']} | Total Hits: {r['hits']}")