#!/bin/bash
echo "         NEKOPAGES          "
echo "============================"
echo "A webpage downloader bot for"
echo "      vk.com / vk.ru        "
echo "                            "
echo "                 by gravitos"
echo ""
echo ">> Setting up python venv"
python3 -m venv .
echo ">> Entering venv"
source bin/activate
echo ">> Installing dependencies"
python3 -m pip install -r requirements.txt
echo ">> Checking for chromium"
which chromium || {
	echo "+---------/ WARNING /--+"
	echo "|Chromium was not found|"
	echo "| in your PATH. Ensure |"
	echo "|  you have a working  |"
	echo "|Chromium-based browser|"
	echo "|as it is vital for the|"
	echo "|  single-file-cli to  |"
	echo "|       function.      |"
	echo "+----------------------+"
}
echo ">> Downloading the latest release of single-file-cli"
wget "https://github.com/gildas-lormeau/single-file-cli/releases/latest/download/single-file-$(uname -m)-linux" -O ./single-file
echo ">> Fixing up permissions"
chmod a+x ./single-file
echo ">> Should be done now. Set up your credentials in bot.ini, enter the venv with 'source bin/activate' and run the bot like 'python3 ./bot.py'"
