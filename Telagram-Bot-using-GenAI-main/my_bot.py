from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import logging
from cohere import Client
import uuid
import asyncio
import aiohttp


load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
TOKEN_TELEGRAM = os.getenv("TOKEN_TELEGRAM")

# Connect with Cohere
co = Client(COHERE_API_KEY)

print("Ok")

MODEL_NAME = "command-light"

# Initialize bot
bot = Bot(token=TOKEN_TELEGRAM)
dp = Dispatcher(bot)

# Define a reference class to store the response
class Reference:
    def __init__(self):
        self.history = []

reference = Reference()

# Function to clear past conversation
def clear_past():
    reference.history = []

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    """
    A handler to start the conversation.
    """
    clear_past()
    await message.reply("Welcome to Nehazzbot!\nHow can I assist you?")

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi there, I'm a bot created by Neha! Please follow these commands -
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)

@dp.message_handler(commands=['clear'])
async def clear_command(message: types.Message):
    """
    A handler to clear the past conversation and context.
    """
    clear_past()
    await message.reply("I've cleared the past conversation and context.")

@dp.message_handler()
async def main_bot(message: types.Message):
    """
    A handler to process the user's input and generate a response using the openai API.
    """

    print(f">>> USER: \n\t{message.text}")
    # Increase the timeout duration for the HTTP request
    try:
        # Make the request to Cohere API with a longer timeout
        response = co.chat(message=message.text)
        
        logging.info(response)  # Log the response object
        
        await bot.send_message(chat_id=message.chat.id, text="An unexpected error occurred. Please try again later.")
    
    except asyncio.TimeoutError:
        await message.reply("Sorry, the request timed out. Please try again later.")
    
    except Exception as e:
        logging.exception("An unexpected error occurred:")
        await message.reply(f"An unexpected error occurred 123. Please try again later: {e}")

# Start the bot

if __name__ == "__main__":
    # Create and close the client session properly
    async def on_startup(dp):
        global session
        session = aiohttp.ClientSession()
    
    async def on_shutdown(dp):
        await dp.storage.close()
        await dp.storage.wait_closed()
        await session.close()

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
