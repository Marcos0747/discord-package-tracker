# 📦 Discord Package Tracker Bot 🤖

This is a Discord bot designed to track packages using the AfterShip API. The bot can operate in two modes: as a regular bot or as a self-bot (though using self-bot mode is not recommended, as it violates Discord's Terms of Service).

## ✨ Features

- **📦 Package Tracking**: Get the status of a package using its tracking number.
- **🖱️ Interactive UI**: Buttons and modals for ease of use.
- **📜 Simple Commands**: Easy to use with commands like `-!help` and `-!track`.

## 🛠️ Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/Marcos0747/discord-package-tracker.git
   cd discord-package-tracker

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt

3. Configure the `config.py` file with your bot token, admin ID, server ID, and AfterShip API key.

4. Run the bot:
    
    python main.py

## 📋 Commands

- `-!help`: Displays the list of available commands.
- `-!track <tracking_number>`: Tracks a package using its tracking number.

## ⚠️ Warning

Using self-bots is against Discord's Terms of Service. It is highly recommended not to enable self-bot mode.

## 🤝 Contributions

Contributions are welcome! Please open an issue or a pull request if you wish to contribute.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

### File `requirements.txt`

discord.py
requests
pystyle

### File `setup.bat`

@echo off
echo 📦 Installing dependencies...
pip install -r requirements.txt
echo ✅ Dependencies installed.
echo 🤖 Running the bot...
python main.py
pause