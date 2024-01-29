import requests
from datetime import datetime
from telegram import Bot
import asyncio
from environs import Env

# Read environment variables from .env file
env = Env()
env.read_env()

# Constants
# replace telegram token and chat id with environment variables
TELEGRAM_TOKEN = env("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = env("TELEGRAM_CHAT_ID")

# Initialize the bot
bot = Bot(TELEGRAM_TOKEN)


def check_post():
    print("Checking post...")

    # Send a GET request to the API.
    # Replace the author.id with your own author id, which you can find on your profile page
    response = requests.get(
        "https://strapi-lifelog.herokuapp.com/posts?author.id=91&_sort=id:DESC&_limit=1"
    )

    # Parse the JSON response
    post = response.json()[0]  # Get the first (and only) post

    # Get the 'published_at' date
    published_at = datetime.strptime(post["published_at"], "%Y-%m-%dT%H:%M:%S.%fZ")

    # Compare the 'published_at' date with the current date
    if published_at.date() == datetime.now().date():
        # The post was published today
        asyncio.run(
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="You have posted today!")
        )
    else:
        # The post was not published today
        asyncio.run(
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="You haven't posted today!")
        )


check_post()
