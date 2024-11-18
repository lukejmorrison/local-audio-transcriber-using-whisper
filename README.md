# local-audio-transcriber-using-whisper

**Audio Transcriber** is a Python script that uses the Whisper model to automatically transcribe audio files into text and SRT subtitles. 

## Table of Contents

- [Installation Guide](#installation-guide)
  - [Windows Users (Windows 10/11)](#windows-users-windows-1011)
  - [Ubuntu Linux Users](#ubuntu-linux-users)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Script Metadata](#script-metadata)

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

#### Step 3: Install CUDA Drivers (for NVIDIA GPU users)

E.g If you have an NVIDIA GPU like the GTX 1070 TI:

1. **Install NVIDIA Graphics Drivers:**
   
   - Navigate to NVIDIA's website to download the latest drivers for your GPU model.
   - Follow their instructions to install the drivers on your Windows system.

3. **Install CUDA Toolkit:**
   
   - Download the CUDA Toolkit from NVIDIA's CUDA download page, ensuring you select the version compatible with your GPU and WSL setup.
   - Follow the installation instructions provided by NVIDIA for WSL.
   
 4. **Install and download CUDA-enabled PyTorch:**

     ```bash
      - pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu126
      ```
   - Replace cu126 with the CUDA version you have installed if different.
   
3. **Verify CUDA Installation:**
   
   - After installation, verify CUDA is recognized by running:
     ```bash
     nvidia-smi
     ```
   - This should display information about your GPU and CUDA version if installed correctly.

5. Install NVIDIA GPU Drivers (for NVIDIA GPU users)

**Install NVIDIA Drivers:**

```bash
sudo ubuntu-drivers autoinstall
