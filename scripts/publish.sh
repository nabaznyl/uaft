#!/bin/bash
set -e

# Get the absolute path of the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Project root is one level up
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Ensure we are in the project root
cd "$PROJECT_ROOT"

echo "📦 Building UAFT in $PROJECT_ROOT..."
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build
python3 -m build

echo "✅ Build complete."
echo "Artifacts are in: $PROJECT_ROOT/dist/"

# Check if twine is installed
if ! command -v twine &> /dev/null; then
    echo "⚠️  Twine is not installed. Install it with: pip install twine"
    echo "Then run: twine upload \"$PROJECT_ROOT/dist/*\""
    exit 0
fi

# Interactive upload
echo ""
read -p "Do you want to upload to PyPI now? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Uploading to PyPI..."
    twine upload dist/*
else
    echo "To publish later, run:"
    echo "twine upload \"$PROJECT_ROOT/dist/*\""
fi
