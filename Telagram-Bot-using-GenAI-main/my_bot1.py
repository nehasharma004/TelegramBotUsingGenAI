from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import logging
import atexit
import cohere

load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
TOKEN_TELEGRAM = os.getenv("TOKEN_TELEGRAM")

# Connect with Cohere
cohere.api_key = COHERE_API_KEY

# Initialize bot
bot = Bot(token=TOKEN_TELEGRAM)
dp = Dispatcher(bot)

# Create a client session for Cohere
cohere_session = cohere.Client()

# Define a reference class to store the response
class Reference:
    def __init__(self) -> None:
        self.response = ""

# Initialize the reference object
reference = Reference()

# Function to clear past conversation
def clear_past():
    reference.response = ""

# Handler to clear past conversation
@dp.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    A handler to clear the previous conversation and context.
    """
    clear_past()
    await message.reply("I've cleared the past conversation and context.")

# Handler to welcome the user
@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """This handler receives messages with `/start` command

    Args:
        message (types.Message): _description_
    """
    await message.reply("Hi\nI am a Chat Bot! Created by Bappy. How can I assist you?")

# Handler to provide help menu
@dp.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm a bot created by Bappy! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)

# Register a cleanup function to close the Cohere client session
def cleanup():
    try:
        cohere_session.close()
    except Exception as e:
        logging.error(f"Error occurred during cleanup: {e}")

# Register cleanup function
atexit.register(cleanup)

# Start the bot
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
