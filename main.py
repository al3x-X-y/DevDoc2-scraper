import asyncio
import logging
from TOKEN import TOKEN, BOT_USERNAME
from telegram import Update
from telegram.ext import Application, CommandHandler,filters, MessageHandler, ContextTypes
from scraper import get_title


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)




post_text = None
#! COMMAND HANDLERS
async def start_command (update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text ("Hi, I am DevUpdatesBot. I will keep you updated with the latest news from the developer world")
    global post_text
    post_text = get_title()
    if post_text is not None:
        await update.message.reply_text(post_text)

async def help_command (update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text ("You can use the following commands:\n/start - To start the bot\n/help - To get help\n/news - To get the latest news")
async def custom_command (update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text ("This is a custom command")
async def get_updates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_auto_update(update)




#! RESPONSE HANDLERS
def handle_response (text: str)-> str:
    processed: str = text.lower()
    if 'hello' in processed :
        print (f'Hello')
        return 'Hello, how can I help you?'
    if 'how are you' in processed:
        print (f'I am fine')
        return 'I am fine, thank you'
    if 'i am a developer' in processed:
        print (f'Thats great')
        return 'Thats great! I have a lot of news for you'
    if 'news' in processed:
        print (f'Getting news')
        return get_title()
    return 'I am sorry, I do not understand you.\n Please use /help to get the list of commands'

async def handle_auto_update(update: Update):
    last_processed_news : str = ""
    while True:
        post_text : str = get_title()
        if post_text is not None and post_text != last_processed_news:
            last_processed_news = post_text
            await update.message.reply_text(post_text)
        await asyncio.sleep(60)

async def handle_message (update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print (f'User({update.message.chat.id}) in {message_type} : "{text}"')

    if (message_type == 'group'):
        if BOT_USERNAME in text :
            new_text : str =  text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else :
        response: str = handle_response(text)
    print (f'Bot: {response}')
    await update.message.reply_text (response)

async def error (update: Update, context: ContextTypes.DEFAULT_TYPE):
    print (f'Update {update} caused error {context.error}')


if __name__ == "__main__":
    logger.info ('Bot is starting')
    app = Application.builder().token(TOKEN).build()
    commands = {
        'start' : start_command,
        'help' : help_command,
        'news' : get_updates,
        'custom' : custom_command
    }

    #! COMMANDS
    for command, handler in commands.items():
        app.add_handler(CommandHandler(command, handler))

    #!MESSAGES
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    #!ERROR
    app.add_error_handler(error)

    logger.info("Bot is polling")
    app.run_polling(poll_interval = 3)
