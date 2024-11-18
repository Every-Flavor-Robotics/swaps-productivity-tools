#!/bin/bash

# Install script for all tools

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/tools/code_sync.py"

# Check if code_sync.py exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Error: code_sync.py not found in the script directory."
    exit 1
fi

# Add alias to .bashrc
if [ -f "$HOME/.bashrc" ]; then
    if ! grep -Fxq "alias code_sync='python3 \"$SCRIPT_PATH\"'" "$HOME/.bashrc"; then
        echo "alias code_sync='python3 \"$SCRIPT_PATH\"'" >> "$HOME/.bashrc"
        echo "Alias added to ~/.bashrc"
    else
        echo "Alias already exists in ~/.bashrc"
    fi
else
    echo "No ~/.bashrc file found. Skipping Bash alias setup."
fi

# Add alias to .zshrc
if [ -f "$HOME/.zshrc" ]; then
    if ! grep -Fxq "alias code_sync='python3 \"$SCRIPT_PATH\"'" "$HOME/.zshrc"; then
        echo "alias code_sync='python3 \"$SCRIPT_PATH\"'" >> "$HOME/.zshrc"
        echo "Alias added to ~/.zshrc"
    else
        echo "Alias already exists in ~/.zshrc"
    fi
else
    echo "No ~/.zshrc file found. Skipping Zsh alias setup."
fi

echo "Installation complete. Please restart your terminal or run 'source ~/.bashrc' or 'source ~/.zshrc' to start using 'code_sync' as a command."