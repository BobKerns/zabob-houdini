#!/bin/bash
# setup-vscode.sh - Quick setup script for VS Code configuration

set -e  # Exit on any error

echo "🚀 Setting up VS Code configuration for Zabob-Houdini..."

# Find the workspace root by searching upward for pyproject.toml
find_root() {
    local dir="$PWD"
    while [ "$dir" != "/" ]; do
        if [ -f "$dir/pyproject.toml" ]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    return 1
}

if workspace_root=$(find_root); then
    cd "$workspace_root" || exit 1
    echo "📁 Working in: $workspace_root"
else
    echo "❌ Error: Could not find workspace root (pyproject.toml not found)"
    exit 1
fi

# Add VS Code personal files to git exclude
echo "📝 Configuring git to exclude personal VS Code files..."
if [ ! -f ".git/info/exclude" ]; then
    touch ".git/info/exclude"
fi

# Add VS Code personal files to exclude if not already there
for file in ".vscode/settings.json" ".vscode/tasks.json" ".vscode/launch.json"; do
    if ! grep -q "^${file}$" ".git/info/exclude" 2>/dev/null; then
        echo "${file}" >> ".git/info/exclude"
        echo "✅ Added ${file} to git exclude"
    else
        echo "ℹ️  ${file} already in git exclude"
    fi
done

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
echo "4. Customize .vscode/settings.json, tasks.json, and launch.json as needed"
echo "   (These files are excluded from git so your changes stay personal)"
echo ""
echo "Recommended VS Code extensions:"
echo "  - Python (ms-python.python)"
echo "  - Code Spell Checker (streetsidesoftware.code-spell-checker)"
echo "  - Pylance (ms-python.vscode-pylance)"
echo "  - Command Variable (rioj7.command-variable) - for dynamic launch configs"
