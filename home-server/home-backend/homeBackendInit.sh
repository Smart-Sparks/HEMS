#!/bin/bash

# GitHub Info
GITHUB_URL="https://github.com/Smart-Sparks/HEMS"
GITHUB_REPO="HEMS"
GITHUB_BRANCH="main"
GITHUB_FOLDER="home-server/home-backend"

# Folder info
BASE_FOLDER="~/homeBackend"
INPUT_FOLDER="${BASE_FOLDER}/input"
VENV_FOLDER="${BASE_FOLDER}/venv"


# update system
sudo apt update

# sudo apt install git
sudo apt -y install git

# install latest stable python3.8
sudo apt -y install python3.8

# install pip3 for python3
sudo apt -y install python3-pip

# install virtualenv
sudo pip3 install virtualenv
sudo apt-get -y install python3-venv

# creates directories
eval mkdir "${BASE_FOLDER}"
eval mkdir "${INPUT_FOLDER}"

# create python virtual environment for backend
eval python3 -m venv "${VENV_FOLDER}"

# clone from github (may need work)
eval cd "${BASE_FOLDER}"
#eval git clone --depth 1 --filter=blob:none --branch central --no-checkout https://github.com/Smart-Sparks/HEMS;
#eval git checkout central -- home-server/home-backend
eval git clone --depth 1 --filter=blob:none --branch "${GITHUB_BRANCH}" --no-checkout "${GITHUB_URL}";
eval cd "${BASE_FOLDER}/${GITHUB_REPO}"
eval git checkout "${GITHUB_BRANCH}" -- "${GITHUB_FOLDER}"
#git clone https://github.com/Smart-Sparks/HEMS.git
cd ~

# source the virtualenvironment
eval source "${VENV_FOLDER}/bin/activate"

# download/install pip dependencies
eval pip3 install -r "${BASE_FOLDER}/${GITHUB_REPO}/${GITHUB_FOLDER}/requirementsHome.txt"
#pip3 install -r ~/homeBackend/central-server/v2/centralCode/requirementsHome.txt
