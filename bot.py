import requests
import re
import asyncio
from bs4 import BeautifulSoup
from telegram import Bot
from datetime import datetime, timedelta

# Import environs to read environment variables from .env file
from environs import Env

# Read environment variables from .env file
env = Env()
env.read_env()

# Constants
# replace telegram token and chat id with environment variables
# Replace golifelog username with your own username
TELEGRAM_TOKEN = env("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = env("TELEGRAM_CHAT_ID")
GOLIFELOG_USERNAME = "drodol"
CHECK_TIME = "18:00"

# Initialize the bot
bot = Bot(TELEGRAM_TOKEN)


def check_post():
    # Implement the logic to check if you've posted on golifelog.com
    # This could be an API request or scraping the website
    # Example (you'll need to modify this based on how golifelog.com works):
    print("Checking post...")
    response = requests.get(f"https://golifelog.com/{GOLIFELOG_USERNAME}")
    if response.status_code == 200:
        print("Username accesible...")
        soup = BeautifulSoup(response.content, "html.parser")
        # Find all <div> elements with class 'ml-2' and attribute 'data-v-7efafa62'
        date_divs = soup.find_all("div", {"class": "ml-2", "data-v-7efafa62": ""})

        for div in date_divs:
            div_text = div.get_text(strip=True)
            # Use regex to find the date pattern in the text
            match = re.search(r"\d{1,2} \w{3} \d{4}", div_text)
            if match:
                post_date_str = match.group()
                # Parse the date string into a datetime object
                post_date = datetime.strptime(post_date_str, "%d %b %Y").date()
                # Compare the post date to today's date
                if post_date == datetime.now().date():
                    asyncio.run(
                        bot.send_message(
                            chat_id=TELEGRAM_CHAT_ID, text="You have posted today!"
                        )
                    )
                    return True  # Post found for today, no need to send reminder

        # No post found for today
        asyncio.run(
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="You haven't posted today!")
        )
        return False

    return False  # Error accessing golifelog.com


def send_reminder():
    current_time = datetime.now().strftime("%H:%M")
    if current_time >= CHECK_TIME and not check_post():
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID, text="You haven't posted on golifelog.com today!"
        )


# Schedule this to run every day at a specific time
send_reminder()
check_post()
