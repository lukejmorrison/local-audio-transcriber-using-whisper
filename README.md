# local-audio-transcriber-using-whisper
*Audio Transcriber** is a Python script that uses the Whisper model to automatically transcribe audio files into text and SRT subtitles. 

**Audio Transcriber** is a Python script that uses the Whisper model to automatically transcribe audio files into text and SRT subtitles. 

## Installation Guide

### Windows Users (Windows 10/11)

#### Step 1: Install WSL (Windows Subsystem for Linux)

1. **Enable WSL:**
   - Open **PowerShell** as Administrator.
   - Run:
     ```powershell
     wsl --install
     ```
   - Restart your computer.

2. **Install Ubuntu from Microsoft Store:**
   - Open the Microsoft Store app.
   - Search for `Ubuntu` and install the latest version (e.g., Ubuntu 20.04 LTS).

3. **Set up Ubuntu:**
   - Open Ubuntu from the Start Menu.
   - Follow the prompts to complete the installation and set up a username and password.

#### Step 2: Install Python and Required Packages

1. **Update Ubuntu packages:**
   - Open your WSL terminal (Ubuntu) and run:
     ```bash
     sudo apt update
     sudo apt upgrade -y
     ```

2. **Install Python3:**
   - If not already installed, run:
     ```bash
     sudo apt install python3 python3-pip -y
     ```

3. **Install Dependencies:**
   - Use `pip` to install Python packages:
     ```bash
     pip3 install torch==1.10.0 torchaudio==0.10.0 pydub whisper
     ```
   - Note: Ensure you're using `pip3` to install packages for Python 3.

### Ubuntu Linux Users

#### Step 1: Install Python

1. **Update and Upgrade System:**
   ```bash
   sudo apt update && sudo apt upgrade -y
