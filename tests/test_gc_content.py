"""
Tests for GcContent tool.

Covers:
  - Class interface (canonical pattern)
  - Module-level alias (convenience import)
  - Typical cases and edge cases
"""

import pytest
from modules.my_tools.tools.gc_content import GcContent, gc_content


# ─────────────────────────────────────────────────────────────────
# Class interface tests — test the Function Object Pattern directly
# ─────────────────────────────────────────────────────────────────

class TestGcContentClass:

    def setup_method(self):
        """Instantiate and initialise before each test."""
        self.tool = GcContent()
        self.tool.initiate()

    def test_balanced_sequence(self):
        assert self.tool.run("ATGCATGC") == 0.5

    def test_all_gc(self):
        assert self.tool.run("GCGCGC") == 1.0

    def test_all_at(self):
        assert self.tool.run("AAAA") == 0.0

    def test_single_g(self):
        assert self.tool.run("G") == 1.0

    def test_single_a(self):
        assert self.tool.run("A") == 0.0

    def test_empty_returns_zero(self):
        # Empty input should not raise — return 0.0 gracefully
        assert self.tool.run("") == 0.0

    def test_lowercase_handled(self):
        # run() should uppercase before counting
        assert self.tool.run("atgcatgc") == 0.5

    def test_mixed_case_handled(self):
        assert self.tool.run("AtGcAtGc") == 0.5

    def test_result_is_float(self):
        result = self.tool.run("ATGC")
        assert isinstance(result, float)

    def test_known_value_three_quarters_gc(self):
        # GGGAT: 3 GC out of 5 = 0.6
        assert self.tool.run("GGGAT") == pytest.approx(0.6)


# ─────────────────────────────────────────────────────────────────
# Alias tests — confirm the module-level shorthand works
# ─────────────────────────────────────────────────────────────────

def test_alias_balanced():
    assert gc_content("ATGCATGC") == 0.5

def test_alias_all_gc():
    assert gc_content("GCGC") == 1.0

def test_alias_empty():
    assert gc_content("") == 0.0
