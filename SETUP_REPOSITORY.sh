#!/bin/bash

# DetectMe Repository Setup Script
# This script prepares the repository for GitHub

echo "DetectMe Repository Setup"
echo "========================="
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "Initializing new git repository..."
    git init
    git branch -M main
    echo "Repository initialized"
    echo ""
fi

# Add all files (respecting .gitignore)
echo "Adding files to repository..."
git add README.md
git add LICENSE
git add requirements.txt
git add install.sh
git add AppleOSINT.py
git add .gitignore
git add .gitattributes
git add Core/
git add GUI/
git add Configuration/
git add Launchers/
git add .github/
git add *.md
echo "Files added"
echo ""

# Show status
echo "Repository status:"
git status --short
echo ""

echo "Next steps:"
echo "1. Review the changes: git status"
echo "2. Commit the changes:"
echo "   git commit -m 'Initial commit: DetectMe OSINT tool'"
echo ""
echo "3. Create a new repository on GitHub/GitLab"
echo "4. Add remote:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/DetectMe.git"
echo "5. Push to repository:"
echo "   git push -u origin main"
echo ""

