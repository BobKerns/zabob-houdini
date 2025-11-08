#!/bin/bash
# setup-vscode.sh - Quick setup script for VS Code configuration

set -e  # Exit on any error

echo "🚀 Setting up VS Code configuration for Zabob-Houdini..."

# Check if .vscode directory exists
if [ ! -d ".vscode" ]; then
    echo "❌ Error: .vscode directory not found. Are you in the project root?"
    exit 1
fi

# Copy settings if they don't exist
if [ ! -f ".vscode/settings.json" ]; then
    if [ -f ".vscode/settings.json.example" ]; then
        cp ".vscode/settings.json.example" ".vscode/settings.json"
        echo "✅ Created .vscode/settings.json from example"
    else
        echo "❌ Error: .vscode/settings.json.example not found"
        exit 1
    fi
else
    echo "ℹ️  .vscode/settings.json already exists, skipping..."
fi

# Copy environment file if it doesn't exist
if [ ! -f ".env" ]; then
    # Detect platform and copy appropriate example
    case "$(uname -s)" in
        Darwin)
            if [ -f ".env.example.macos" ]; then
                cp ".env.example.macos" ".env"
                echo "✅ Created .env for macOS"
            fi
            ;;
        Linux)
            if [ -f ".env.example.linux" ]; then
                cp ".env.example.linux" ".env"
                echo "✅ Created .env for Linux"
            fi
            ;;
        CYGWIN*|MINGW*|MSYS*)
            if [ -f ".env.example.windows" ]; then
                cp ".env.example.windows" ".env"
                echo "✅ Created .env for Windows"
            fi
            ;;
        *)
            echo "⚠️  Unknown platform, please manually copy the appropriate .env.example.* file"
            ;;
    esac
else
    echo "ℹ️  .env already exists, skipping..."
fi

echo ""
echo "🎉 VS Code setup complete!"
echo ""
echo "Next steps:"
echo "1. Open VS Code in this directory: code ."
echo "2. Install recommended extensions if prompted"
echo "3. Edit .env if your Houdini installation path is different"
echo "4. Edit .vscode/settings.json to add your personal preferences"
echo ""
echo "Recommended VS Code extensions:"
echo "  - Python (ms-python.python)"
echo "  - Code Spell Checker (streetsidesoftware.code-spell-checker)"
echo "  - Pylance (ms-python.vscode-pylance)"
