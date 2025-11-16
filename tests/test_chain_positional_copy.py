"""
Tests for enhanced Chain.copy() functionality.

This module tests the positional reordering capabilities of Chain.copy() method.
"""

import pytest

class TestChainCopyPositional:
    """Test Chain.copy() with positional reordering parameters."""

    @pytest.fixture
    def sample_chain(self, hython_test):
        """Create a sample chain for testing."""
        data = hython_test('test_chain_positional_reordering')
        return data

    def test_positional_reordering(self, sample_chain):
        """Test that Chain.copy() can reorder nodes positionally."""
        data = sample_chain['result']

        # Verify original order
        assert data['original_names'] == ['first', 'second', 'third']

        # Test reverse reordering
        assert data['reversed_names'] == ['third', 'second', 'first']

        # Test partial copy
        assert data['partial_names'] == ['first', 'third']

        # Test duplication
        assert data['duplicate_names'] == ['second', 'second', 'first']

        # Test default copy preserves order
        assert data['default_names'] == ['first', 'second', 'third']

        # Test name-based access
        assert data['by_name_names'] == ['third', 'first']

        # Test mixed index/name access
        assert data['mixed_names'] == ['first', 'third']

        # Test node insertion
        assert data['inserted_names'] == ['first', 'inserted', 'third']

    def test_copy_signature_includes_args(self, hython_test):
        """Test that Chain.copy() signature supports *args."""
        result = hython_test('test_copy_signature_validation')
        data = result['result']

        # Chain.copy() should use *args for positional parameters
        assert data['chain_uses_args']

        # Base parameters should still be present
        assert '_inputs' in data['chain_all_parameters']
