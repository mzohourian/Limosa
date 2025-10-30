#!/bin/bash

# Streamlit Cloud setup script
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
[theme]\n\
primaryColor = \"#2E7D32\"\n\
backgroundColor = \"#FAFAFA\"\n\
secondaryBackgroundColor = \"#FFFFFF\"\n\
textColor = \"#212121\"\n\
" > ~/.streamlit/config.toml