# Telegram Bot - Python Version

This is a Python conversion of a Node.js Telegram bot that handles image fetching for GR (student) and ER (faculty) numbers.

## Features

- **User Bot**: Handles `/grno` and `/erno` commands for regular users
- **Admin Bot**: Provides administrative functions for managing users and IDs
- **Firebase Integration**: User management, logging, and access control
- **Image Fetching**: Downloads images from Marwadi Education API
- **Web Server**: Flask server for health checks and monitoring

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Configuration**:
   - Copy `.env.example` to `.env`
   - Add your Telegram bot tokens:
     ```
     IMAGE_BOT_API=your_user_bot_token
     ADMIN_BOT_API=your_admin_bot_token
     ```

3. **Firebase Setup** (Optional):
   - Add your Firebase service account credentials
   - Update the Firebase initialization in the modules

4. **Run the Bot**:
   ```bash
   python main.py
   ```

## Bot Commands

### User Commands
- `/grno` - Request a GR (student) image
- `/erno` - Request an ER (faculty) image

### Admin Commands (Admin ID: 6644752841)
- `/blockmuid` - Block a MUID
- `/allowmuid` - Allow a MUID
- `/allowuser` - Allow a Telegram user
- `/blockuser` - Block a Telegram user

## Project Structure

```
├── main.py                 # Main bot application
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── Bot/
│   ├── Firebase/
│   │   ├── User/          # User-related Firebase functions
│   │   └── Admin/         # Admin-related Firebase functions
│   └── User/
│       └── FetchImage.py  # Image fetching functionality
└── images/                # Downloaded images directory
```

## Key Differences from Node.js Version

1. **Async/Await**: Uses Python's asyncio for asynchronous operations
2. **HTTP Requests**: Uses `aiohttp` instead of Node.js `https` module
3. **Telegram Library**: Uses `python-telegram-bot` instead of `node-telegram-bot-api`
4. **Web Server**: Uses Flask instead of Express
5. **Environment Variables**: Uses `python-dotenv` instead of Node.js `dotenv`

## Notes

- The bot maintains the same functionality as the original Node.js version
- Firebase functions are modularized for better organization
- Error handling and logging are preserved
- Admin privileges are maintained with the same ADMIN_ID
