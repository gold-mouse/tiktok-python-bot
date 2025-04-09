# Python Project Setup Guide

## Prerequisites
Ensure you have the hearting installed on your system:
1. Python
2. Google Chrome latest version
3. Ensure Google Chrome Path - C:\Program Files\Google\Chrome\Application\chrome.exe

### Install Python
Download and install Python from the [official Python website](https://www.python.org/downloads/).
- During installation, check the option **Add Python to PATH**.
- Verify the installation with:
  ```sh
  python --version
  ```

### Install pip (if not installed)
pip comes bundled with Python, but you can ensure it's updated with:
```sh
python -m ensurepip --default-pip
python -m pip install --upgrade pip
```

## Getting Started

### 1. Clone the Repository
If the project is hosted on a Git repository, clone it using:
```sh
git clone https://github.com/gold-mouse/tiktok-python-bot.git
cd tiktok-python-bot
```

### 2. Install Dependencies
```sh
pip install -r requirements.txt
```

### 3. Run the Application
```sh
python main.py
```

## Environment Variables
If your project requires environment variables, create a `.env` file in the root directory and define them like this:
```sh
MIN_DELAY=3
MAX_DELAY=40
RETRYABLE_COUNT=3
PORT=5000
```

## Note
If you faced bellow error:
```sh
ModuleNotFoundError: No module named 'pkg_resources'
```
You have to upgrade setuptools to latest version

```sh
pip install --upgrade setuptools
```

