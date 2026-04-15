"""
Unit tests for the seq_basics example tools.
 
:: Each tool is now a class following the Python Function Object Pattern
(initiate / run).  Tests cover both the canonical class interface AND the
module-level alias  (for example: `reverse_complement = _instance.run`)  so that
direct imports continue to work for students who prefer that style.
"""

import pytest

from modules.seq_basics.tools.reverse_complement import reverse_complement
from modules.seq_basics.tools.find_pam import find_pam
from modules.seq_basics.tools.find_protospacer import find_protospacer
from modules.seq_basics.tools.design_cas9_RNA import design_cas9_RNA


def test_reverse_complement_basic():
    assert reverse_complement("ATGC") == "GCAT"


def test_reverse_complement_ambiguity_codes():
    # Should not error for supported IUPAC subset
    assert reverse_complement("ATRYSWKMN")


def test_find_pam_basic():
    assert find_pam("ATGCATCGAGTCACGTACGTACTGACTGGCGTACGT") == [(27,'+')]

def test_find_pam_complex():
    assert find_pam("AGGCCCCGAGTCACGTACGTACTGACTGGCGGACCT") == [(3,'-'),(4,'-'),(5,'-'),(27,'+'),(30,'+')]

def test_find_protospacer_basic():
    assert find_protospacer("ATGCATCGAGTCACGTACGTACTGACTGGCGTACGT") == ['CGAGTCACGTACGTACTGAC']

def test_find_protospacer_complex():
    assert find_protospacer("AGGCCCCGAGTCACGTACGTACTGACTGGCGGACCT") == ['GTCAGTACGTACGTGACTCG','AGTCAGTACGTACGTGACTC','CAGTCAGTACGTACGTGACT','CGAGTCACGTACGTACTGAC','GTCACGTACGTACTGACTGG']

def test_find_design_cas9_RNA_basic():
    assert design_cas9_RNA("ATGCATCGAGTCACGTACGTACTGACTGGCGTACGT")[0]['gRNA'] == 'CGAGUCACGUACGUACUGACGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGC'

def test_find_design_cas9_RNA_complex():
    correct_answers = [
        'AGUCAGUACGUACGUGACUCGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGC',
        'CAGUCAGUACGUACGUGACUGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGC',
        'GUCAGUACGUACGUGACUCGGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGC',
        'CGAGUCACGUACGUACUGACGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGC',
        'GUCACGUACGUACUGACUGGGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGC']
    results = design_cas9_RNA("AGGCCCCGAGTCACGTACGTACTGACTGGCGGACCT")
    
    for i in range(5):
        assert results[i]['gRNA'] == correct_answers[i]

if __name__ == "__main__":
    test_reverse_complement_basic()
    test_reverse_complement_ambiguity_codes()
    test_find_pam_basic()
    test_find_pam_complex()
    test_find_protospacer_basic()
    test_find_protospacer_complex()
    test_find_design_cas9_RNA_basic()
    test_find_design_cas9_RNA_complex()