"""
Tests for enhanced ZChain.copy() functionality.

This module tests the positional reordering capabilities of ZChain.copy() method.
"""


class TestChainCopyPositional:
    """Test ZChain.copy() with positional reordering parameters."""

    def test_positional_reordering(self, hython_test):
        """Test that ZChain.copy() can reorder nodes positionally."""
        data = hython_test('h_test_positional_reordering')

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
        """Test that ZChain.copy() signature supports *args."""
        data = hython_test('h_test_copy_signature_includes_args')

        # ZChain.copy() should use *args for positional parameters
        assert data['chain_uses_args']

        # Base parameters should still be present
        assert '_inputs' in data['chain_all_parameters']
