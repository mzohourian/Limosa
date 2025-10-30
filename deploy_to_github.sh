#!/bin/bash

echo "🚀 Deploying Limosa to GitHub + Streamlit Cloud"
echo "=============================================="

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📁 Initializing Git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Add all files
echo "📄 Adding files to Git..."
git add .

# Create commit
echo "💾 Creating commit..."
git commit -m "🦆 Limosa: Professional Veterinary AI Assistant MVP

- Claude-style UI with veterinary green theme
- AI-powered image analysis with Claude 3.5 Haiku
- Species-specific diagnostic capabilities
- Professional medical reporting
- Ready for veterinary clinic demos
- Streamlit Cloud deployment configured"

echo "✅ Commit created successfully"

# Instructions for GitHub setup
echo ""
echo "📋 NEXT STEPS - GitHub Setup:"
echo "=============================================="
echo "1. Create a new repository on GitHub:"
echo "   - Go to https://github.com/new"
echo "   - Repository name: limosa-vet-ai"
echo "   - Description: 🦆 Limosa - AI-Powered Veterinary Diagnostics"
echo "   - Make it Public (for free Streamlit Cloud)"
echo "   - Don't initialize with README (we have files already)"
echo ""
echo "2. Connect this repository to GitHub:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/limosa-vet-ai.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Deploy to Streamlit Cloud:"
echo "   - Go to https://share.streamlit.io"
echo "   - Click 'New app'"
echo "   - Connect your GitHub account"
echo "   - Select repository: limosa-vet-ai"
echo "   - Main file path: veterinary_assistant.py"
echo "   - Click 'Advanced settings' and add secrets:"
echo "     ANTHROPIC_API_KEY = your_api_key_here"
echo "   - Click 'Deploy!'"
echo ""
echo "🎉 Your app will be live at: https://limosa-vet-ai.streamlit.app"
echo ""
echo "💡 Need the API key? Check your .env file or original project"