from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, Application, MessageHandler, filters 
import re
import logging
import asyncio
import nest_asyncio

# Enable logging for easier troubleshooting
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Apply nest_asyncio to enable asyncio in environments that do not support it natively
nest_asyncio.apply()

# Telegram Bot Token
TOKEN = 'Your_token_here'

# Start command handler function
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Пришлите ссылку на историю VK.')

# Message processing handler function
async def process_message(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text
    # Regex pattern to find VK story links
    link_pattern = r'https?://vk\.com/([a-zA-Z0-9_.-]+)\?act=stories&w=story-([0-9]+)_([0-9]+)'
    found_links = re.findall(link_pattern, message_text)

    if found_links:
        # Create and format the links into a single message
        reformatted_links = [f'https://vk.com/story-{group[1]}_{group[2]}' for group in found_links]
        links_message = '\n'.join(reformatted_links)
        await update.message.reply_text(links_message)
    else:
        await update.message.reply_text('Пришлите ссылку на историю.')

# Main function to set up and run the bot
async def main():
    application = Application.builder().token(TOKEN).build()

    # Add handlers to the application
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_message))

    # Start polling
    await application.run_polling()

# Standard Python entry point check
if __name__ == '__main__':
    asyncio.run(main())
