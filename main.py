import os
import asyncio
import aiohttp
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
import threading

from Bot.Firebase.User.MessageLogger import message_logger
from Bot.User.FetchImage import fetch_and_save_image
from Bot.Firebase.User.CheckUser import check_user
from Bot.Firebase.User.CheckID import check_id
from Bot.Firebase.User.WriteLog import write_user_log
from Bot.Firebase.Admin.BlockID import block_id
from Bot.Firebase.Admin.AllowID import allow_id
from Bot.Firebase.Admin.AllowUser import allow_user
from Bot.Firebase.Admin.BlockUser import block_user
from Bot.Firebase.User.NewUser import new_user
from Bot.Firebase.User.GetBotData import get_bot_data
from Bot.Firebase.User.BotStatus import get_bot_status
from Bot.Firebase.User.Counter import counter

load_dotenv()

ADMIN_ID = 6644752841

USER_token = os.getenv("IMAGE_BOT_API")
if not USER_token:
    print("ERROR: Token not found For User")
    exit(1)

ADMIN_token = os.getenv("ADMIN_BOT_API")
if not ADMIN_token:
    print("ERROR: Token not found For Admin")
    exit(1)

Path("./images").mkdir(exist_ok=True)
user_state = {}

async def fetch_erno_image(erno):
    api_url = f"https://marwadieducation.edu.in/MEFOnline/handler/getImage.ashx?Id={erno}"
    output_path = f"./images/image_{erno}.png"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    with open(output_path, 'wb') as f:
                        async for chunk in response.content.iter_chunked(8192):
                            f.write(chunk)
                else:
                    raise Exception(f"HTTP error! status: {response.status}")
    except Exception as error:
        print(f"Error fetching ERNO image: {error}")
        raise error

async def grno_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.effective_user.id == ADMIN_ID:
            user_state[update.effective_chat.id] = "awaitingGrno"
            await message_logger(update.effective_user.id, "/grno - Admin awaiting input")
            await update.message.reply_text("Please enter GR Number:")
            return
        
        is_active = await get_bot_status()
        
        if not is_active:
            await update.message.reply_text("Bot is currently In Development Mode.")
            return
        
        is_allowed = await check_user(update.effective_user.id)
        if not is_allowed:
            await new_user(
                update.effective_chat.id,
                update.effective_user.username,
                update.effective_user.first_name,
                update.effective_user.last_name
            )
            await message_logger(update.effective_user.id, "/grno - User not allowed")
            await update.message.reply_text(
                f"Dear {update.effective_user.first_name}\nYou Have No Rights To Get Image.\nThank You"
            )
            return
        
        user_state[update.effective_chat.id] = "awaitingGrno"
        await message_logger(update.effective_user.id, "/grno - Awaiting input")
        await update.message.reply_text("Please enter GR Number:")
        
    except Exception as error:
        await message_logger(update.effective_user.id, f"/grno - Error: {error}")
        await update.message.reply_text("An error occurred while processing your request.")

async def erno_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.effective_user.id == ADMIN_ID:
            user_state[update.effective_chat.id] = "awaitingErno"
            await message_logger(update.effective_user.id, "/erno - Admin awaiting input")
            await update.message.reply_text("Please enter ER Number:")
            return
        
        is_active = await get_bot_status()
        
        if not is_active:
            await update.message.reply_text("Bot is currently In Development Mode.")
            return
        
        is_allowed = await check_user(update.effective_user.id)
        if not is_allowed:
            await new_user(
                update.effective_chat.id,
                update.effective_user.username,
                update.effective_user.first_name,
                update.effective_user.last_name
            )
            await message_logger(update.effective_user.id, "/erno - User not allowed")
            await update.message.reply_text(
                f"Dear {update.effective_user.first_name}\nYou Have No Rights To Get Image.\nThank You"
            )
            return
        
        user_state[update.effective_chat.id] = "awaitingErno"
        await message_logger(update.effective_user.id, "/erno - Awaiting input")
        await update.message.reply_text("Please enter ER Number:")
        
    except Exception as error:
        await message_logger(update.effective_user.id, f"/erno - Error: {error}")
        await update.message.reply_text("An error occurred while processing your request.")

async def handle_image_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    id_value = update.message.text.strip()
    output_path = f"./images/image_{id_value}.png"
    is_id_allowed = False
    
    if user_state.get(chat_id) == "awaitingGrno":
        is_id_allowed = await check_id(id_value, "student")
    elif user_state.get(chat_id) == "awaitingErno":
        is_id_allowed = await check_id(id_value, "faculty")
    else:
        await update.message.reply_text("Invalid state. Please use /grno or /erno command.")
        return
    
    if update.effective_user.id == ADMIN_ID:
        try:
            if user_state[chat_id] == "awaitingGrno":
                await fetch_and_save_image(id_value)
                await message_logger(update.effective_user.id, f"Admin fetched GR image: {id_value} - success")
                await counter(id_value, "student")
            elif user_state[chat_id] == "awaitingErno":
                await fetch_erno_image(id_value)
                await message_logger(update.effective_user.id, f"Admin fetched ER image: {id_value} - success")
                await counter(id_value, "faculty")
            
            if os.path.exists(output_path):
                with open(output_path, 'rb') as photo:
                    await update.message.reply_photo(photo)
        except Exception as error:
            await message_logger(update.effective_user.id, f"Admin error fetching image: {error} - failed")
            await update.message.reply_text("Error fetching image. Please try again.")
        
        del user_state[chat_id]
        return
    
    if not is_id_allowed:
        del user_state[chat_id]
        await update.message.reply_text("This ID is Blocked")
        return
    
    try:
        if user_state[chat_id] == "awaitingGrno":
            await fetch_and_save_image(id_value)
            await message_logger(update.effective_user.id, f"Fetched GR image: {id_value} - success")
            await counter(id_value, "student")
        elif user_state[chat_id] == "awaitingErno":
            await fetch_erno_image(id_value)
            await message_logger(update.effective_user.id, f"Fetched ER image: {id_value} - success")
            await counter(id_value, "faculty")
        
        if os.path.exists(output_path):
            with open(output_path, 'rb') as photo:
                await update.message.reply_photo(photo)
    except Exception as error:
        await message_logger(update.effective_user.id, f"Error fetching image: {error} - failed")
        await update.message.reply_text("Error fetching image. Please try again.")
    
    del user_state[chat_id]

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if (user_state.get(chat_id) not in ["awaitingGrno", "awaitingErno"] or 
        update.message.text.startswith("/")):
        return
    await handle_image_request(update, context)

async def block_muid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("You are not authorized.")
        return
    user_state[update.effective_chat.id] = "awaitingBlockMUID"
    await update.message.reply_text("Enter MUID to block:")

async def allow_muid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("You are not authorized.")
        return
    user_state[update.effective_chat.id] = "awaitingAllowMUID"
    await update.message.reply_text("Enter MUID to allow:")

async def allow_user_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("You are not authorized.")
        return
    user_state[update.effective_chat.id] = "awaitingAllowUser"
    await update.message.reply_text("Enter Telegram ID To Allow:")

async def block_user_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("You are not authorized.")
        return
    user_state[update.effective_chat.id] = "awaitingBlockUser"
    await update.message.reply_text("Enter Telegram ID to block:")

async def admin_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    username = update.effective_user.username
    first_name = update.effective_user.first_name
    muid = update.message.text.strip()
    
    if user_state.get(chat_id) == "awaitingBlockMUID":
        await block_id(muid)
        del user_state[chat_id]
        await update.message.reply_text(f"MUID {muid} is now blocked.")
    
    elif user_state.get(chat_id) == "awaitingAllowMUID":
        await allow_id(muid)
        del user_state[chat_id]
        await update.message.reply_text(f"MUID {muid} is now Allowed.")
    
    elif user_state.get(chat_id) == "awaitingAllowUser":
        await allow_user(muid, username, first_name)
        del user_state[chat_id]
        await update.message.reply_text(f"Telegram {muid} is now Allowed.")
    
    elif user_state.get(chat_id) == "awaitingBlockUser":
        await block_user(muid, username, first_name)
        del user_state[chat_id]
        await update.message.reply_text(f"MUID {muid} is now Blocked.")

def create_flask_app():
    app = Flask(__name__)
    
    @app.route("/")
    def health_check():
        return "Telegram bot is active!"
    
    return app

def run_flask_app():
    app = create_flask_app()
    port = int(os.getenv("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=False)

async def main():
    try:
        user_app = Application.builder().token(USER_token).build()
        admin_app = Application.builder().token(ADMIN_token).build()
        
        user_app.add_handler(CommandHandler("grno", grno_command))
        user_app.add_handler(CommandHandler("erno", erno_command))
        user_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
        
        admin_app.add_handler(CommandHandler("grno", grno_command))
        admin_app.add_handler(CommandHandler("erno", erno_command))
        admin_app.add_handler(CommandHandler("blockmuid", block_muid_command))
        admin_app.add_handler(CommandHandler("allowmuid", allow_muid_command))
        admin_app.add_handler(CommandHandler("allowuser", allow_user_command))
        admin_app.add_handler(CommandHandler("blockuser", block_user_command))
        admin_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, admin_message_handler))
        
        flask_thread = threading.Thread(target=run_flask_app, daemon=True)
        flask_thread.start()
        
        print("Starting both bots...")
        print("Server listening on port", os.getenv("PORT", 3000))
        
        await user_app.initialize()
        await admin_app.initialize()
        
        await user_app.start()
        await admin_app.start()
        
        await user_app.updater.start_polling()
        await admin_app.updater.start_polling()
        
        print("Both bots are running successfully!")
        
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            print("Shutting down bots...")
        finally:
            await user_app.updater.stop()
            await admin_app.updater.stop()
            await user_app.stop()
            await admin_app.stop()
            await user_app.shutdown()
            await admin_app.shutdown()
            
    except Exception as e:
        print(f"Error starting bots: {e}")
        print("This might be a compatibility issue with Python 3.13 and python-telegram-bot")
        print("Consider using Python 3.11 or 3.12 for better compatibility")

if __name__ == "__main__":
    asyncio.run(main())
