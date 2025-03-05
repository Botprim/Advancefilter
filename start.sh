#!/bin/bash

# Check if UPSTREAM_REPO is empty
if [ -z "$UPSTREAM_REPO" ]; then
  echo "Cloning main Repository..."
  git clone https://github.com/1238muj/THALAPATHY-FILTER-BOT.git /THALAPATHY-FILTER-BOT
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO..."
  git clone "$UPSTREAM_REPO" /THALAPATHY-FILTER-BOT
fi

# Change to the cloned directory, exit if failed
cd /THALAPATHY-FILTER-BOT || { echo "Failed to enter directory"; exit 1; }

# Install requirements
echo "Installing dependencies..."
pip3 install -U -r requirements.txt || { echo "Failed to install dependencies"; exit 1; }

# Start the bot
echo "Starting Bot..."
exec python3 bot.py
