#!/bin/bash

# Runs home server data transfer backend

# GitHub Info
GITHUB_URL="https://github.com/Smart-Sparks/HEMS.git"
GITHUB_REPO="HEMS"
GITHUB_BRANCH="main"
GITHUB_FOLDER="home-server/home-backend"

# Folder info
BASE_FOLDER="~/homeBackend"
INPUT_FOLDER="${BASE_FOLDER}/input"
VENV_FOLDER="${BASE_FOLDER}/venv"

# Source virtualenv
eval source "${VENV_FOLDER}/bin/activate"
#source ~/homeBackend/venv/bin/activate

# Run home_server.py backend program
eval cd "${BASE_FOLDER}/${GITHUB_REPO}/${GITHUB_FOLDER}"
eval python3 "home_server.py"
#python3 ~/homeBackend/central-server/v2/centralCode/home_server.py
