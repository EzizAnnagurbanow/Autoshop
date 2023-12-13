# Autoshop
Autoshop Telegram bot for selling electron products

# Autoshop Telegram Bot

Welcome to Autoshop Telegram Bot! This bot provides a convenient interface for managing an automated store through Telegram.

## Installation

Install the required dependencies:

   ```bash
   pip install telebot
  ```
1. Create an SQLite database if not already present:
   `touch your_database.db`
2. Fill in the config.ini file with the necessary configuration information. Example:
 ```
[Telegram]
[tgbot]
token= id_of_your_bot
admin_id= your_id
  ```
# Usage
Start a conversation with the bot using the command /start.
Use inline commands and buttons to interact with the store.
Configure products, prices, and other parameters in the SQLite database.
Features
Telegram Interface: Manage the store from any device connected to Telegram.
SQLite Database: Store information about products, customers, and orders in an easily accessible and scalable SQLite database.
Inline Commands and Buttons: Enhance the user experience with inline commands and buttons.
Examples
Example

# Requirements
Python 3.6+
telebot library
SQLite database
License
This project is licensed under the MIT License - see the LICENSE.md file for details.

# Contribution
We welcome contributions and suggestions for improving the bot. If you have ideas or found bugs, create an issue or submit a pull request.
