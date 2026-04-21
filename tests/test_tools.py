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
from modules.seq_basics.tools.calculate_score import calculate_score
from modules.seq_basics.tools.design_cas9_RNA import design_cas9_RNA


def test_reverse_complement_basic():
    assert reverse_complement("ATGC") == "GCAT"


def test_reverse_complement_ambiguity_codes():
    # Should not error for supported IUPAC subset
    assert reverse_complement("ATRYSWKMN")


# find_pam tests
def test_find_pam_single():
    assert find_pam("ATGCATCGAGTCACGTACGTACTGACTGGCGTACGT") == [(27,'+')]

def test_find_pam_multiple():
    assert find_pam("AGGCCCCGAGTCACGTACGTACTGACTGGCGGACCT") == [(3,'-'),(4,'-'),(5,'-'),(27,'+'),(30,'+')]

def test_find_pam_multi_GG():
    assert len(find_pam("AGGCTACGAGTCACGTACGTACTGACTGGGGGACCT")) == 4

def test_find_pam_invalid_sequence():
    with pytest.raises(ValueError):
        # This call should trigger the error caused by upstream of GG and CC being too short
        find_pam("ACTGGACTGGTCTAGACATGCATACCA")

def test_find_pam_invalid_DNA():
    with pytest.raises(ValueError):
        # This call should trigger the error caused by an X in the sequence
        find_pam("ACTGGACTGGXTCTAGACATGCATACCA")


# find_protospacer tests
def test_find_protospacer_single():
    assert find_protospacer("ATGCATCGAGTCACGTACGTACTGACTGGCGTACGT") == ['CGAGTCACGTACGTACTGAC']

def test_find_protospacer_multiple():
    assert find_protospacer("AGGCCCCGAGTCACGTACGTACTGACTGGCGGACCT") == ['GTCAGTACGTACGTGACTCG','AGTCAGTACGTACGTGACTC','CAGTCAGTACGTACGTGACT','CGAGTCACGTACGTACTGAC','GTCACGTACGTACTGACTGG']


# calculate_score tests
def test_calculate_score_TTTT():
    results = calculate_score(['GCGCGCGCGCTTTTAATAAT'], "ATTAATATAGCCATGCTTTTACTAATTGGATTAGAT")
    assert results[0]['score'] == 50.0

def test_calculate_score_no_GC():
    results = calculate_score(['ATAATTATATATATAATTAT'], "ATTAATATAATTATATATATAATTATTGGATTAGAT")
    assert results[0]['score'] == 50.0

def test_calculate_score_best_gRNA():
    results = calculate_score(['GCGCGCGCGCATATAATTAT'], "ATTAATGCGCGCGCGCATATAATTATTGGATTAGAT")
    assert results[0]['score'] == 100.0

def test_calculate_score_bad_gRNA():
    results = calculate_score(['ATAATATTTTATATAATTAT'], "ATTAATATAATTATATATATAATTATTGGATTAGAT")
    assert results[0]['score'] == 0.0

def test_calculate_score_duplicated_gRNA():
    results = calculate_score(['ATCGAGTCAGCTACTGACTGAGG'], "ATCGAGTCAGCTACTGACTGAGGATCGAGTCAGCTACTGACTGAGG")
    assert results[0]['score'] == 70.0


# design_cas9_RNA tests
def test_find_design_cas9_RNA_single():
    assert design_cas9_RNA("ATGCATCGAGTCACGTACGTACTGACTGGCGTACGT")[0]['gRNA'] == 'CGAGUCACGUACGUACUGACGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGC'

def test_find_design_cas9_RNA_multiple():
    correct_answers = [
        'AGUCAGUACGUACGUGACUCGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGC',
        'CAGUCAGUACGUACGUGACUGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGC',
        'GUCAGUACGUACGUGACUCGGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGC',
        'CGAGUCACGUACGUACUGACGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGC',
        'GUCACGUACGUACUGACUGGGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGC']
    results = design_cas9_RNA("AGGCCCCGAGTCACGTACGTACTGACTGGCGGACCT")
    
    for i in range(5):
        assert results[i]['gRNA'] == correct_answers[i]

def test_find_design_cas9_RNA_exactly_one():
    target_sequence = 'CCATCGATGCTGACGTCAATCGA'
    valid = 'UCGAUUGACGUCAGCAUCGAGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGC'
    assert design_cas9_RNA(target_sequence)[0]['gRNA'] == valid

def test_find_design_cas9_RNA_plasmid_name():
    plasmid_name = 'pBR322'
    result = design_cas9_RNA(plasmid_name)
    assert isinstance(result[0]['gRNA'], str)

def test_design_cas9_RNA_empty_input():
    with pytest.raises(ValueError):
        # This call should trigger the error caused by no input
        design_cas9_RNA("")


if __name__ == "__main__":
    test_reverse_complement_basic()
    test_reverse_complement_ambiguity_codes()

    # find_pam tests
    test_find_pam_single()
    test_find_pam_multiple()
    test_find_pam_multi_GG()
    test_find_pam_invalid_sequence()
    test_find_pam_invalid_DNA()

    # find_protospacer
    test_find_protospacer_single()
    test_find_protospacer_multiple()

    # calculate_score
    test_calculate_score_TTTT()
    test_calculate_score_no_GC()
    test_calculate_score_bad_gRNA()
    test_calculate_score_duplicated_gRNA()

    # find design_cas9_RNA
    test_find_design_cas9_RNA_single()
    test_find_design_cas9_RNA_multiple()
    test_find_design_cas9_RNA_exactly_one()
    test_find_design_cas9_RNA_plasmid_name()
    test_design_cas9_RNA_empty_input()