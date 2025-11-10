#!/usr/bin/env bash

# Test runner script for zabob-houdini
# Provides different test execution modes

set -e

echo "Zabob-Houdini Test Runner"
echo "=========================="

case "${1:-help}" in
    "unit"|"u")
        echo "Running unit tests (no Houdini required)..."
        uv run pytest -m "unit and not integration" -v
        ;;

    "integration"|"i")
        echo "Running integration tests (requires Houdini)..."
        echo "Make sure you have:"
        echo "  1. Houdini installed"
        echo "  2. HOUDINI_PATH set in your .env file"
        echo ""
        uv run pytest -m "integration" -v
        ;;

    "all"|"a")
        echo "Running all tests..."
        echo "This will fail if Houdini is not installed."
        echo ""
        uv run pytest -v
        ;;

    "ci")
        echo "Running CI test suite (unit tests only)..."
        uv run pytest -m "unit and not integration" -v --tb=short --junit-xml=test-results.xml
        ;;

    "list"|"l")
        echo "Available tests:"
        echo ""
        echo "Unit tests (can run without Houdini):"
        uv run pytest -m "unit and not integration" --collect-only -q
        echo ""
        echo "Integration tests (require Houdini):"
        uv run pytest -m "integration" --collect-only -q
        ;;

    "help"|"h"|*)
        echo ""
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  unit, u          Run unit tests (no Houdini required)"
        echo "  integration, i   Run integration tests (requires Houdini)"
        echo "  all, a           Run all tests"
        echo "  ci               Run CI test suite with JUnit output"
        echo "  list, l          List available tests"
        echo "  help, h          Show this help"
        echo ""
        echo "Examples:"
        echo "  $0 unit                    # Run unit tests"
        echo "  $0 integration             # Run integration tests"
        echo "  $0 list                    # List all tests"
        echo ""
        echo "Environment setup:"
        echo "  1. Copy .env.example.macos (or your platform) to .env"
        echo "  2. Set HOUDINI_PATH to your Houdini installation"
        echo "  3. For download functionality, set SIDEFX_USERNAME and SIDEFX_PASSWORD"
        ;;
esac
