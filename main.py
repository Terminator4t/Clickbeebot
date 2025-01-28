from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.errors import SessionPasswordNeededError
import os
import sys
from time import sleep
import threading

# Check and import required modules
try:
    import colorama
    from colorama import Fore, Style
    colorama.init(autoreset=True)
    hijau = Style.RESET_ALL + Style.BRIGHT + Fore.GREEN
    res = Style.RESET_ALL
    abu2 = Style.DIM + Fore.WHITE
    yellow = Style.RESET_ALL + Style.BRIGHT + Fore.YELLOW
    red = Style.RESET_ALL + Style.BRIGHT + Fore.RED
except ImportError:
    print("Error: 'colorama' module not installed.\n")
    sys.exit()

# Banner
BANNER = (
    Style.NORMAL + Fore.MAGENTA +
    """
  _   _   _   _   _   _   _ 
 / \ / \ / \ / \ / \ / \ / \ 
| H | U | Z | Z | I | O | N | 
 \_/ \_/ \_/ \_/ \_/ \_/ \_/ 

         /___/                   """
    + Style.DIM + Fore.WHITE +
    "@Bot\n" +
    Style.NORMAL + Fore.GREEN +
    "=========================================================\n" +
    Style.BRIGHT + Fore.GREEN +
    "Author By    : " + Style.RESET_ALL + "Huzzion2op\n" +
    "Channel YT   : " + Style.RESET_ALL + "Huzzion"
)

# Create session directory if not exists
if not os.path.exists("session"):
    os.makedirs("session")

# Login Function
async def login(phone_number):
    global client
    api_id = 28731121
    api_hash = '4ba3e5b5acbe0b20200a07a528a65def'

    client = TelegramClient(f"session/{phone_number}", api_id, api_hash)
    await client.connect()

    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone_number)
            code = input(f"{hijau}Enter Your Code {res}: ")
            await client.sign_in(phone_number, code)
        except SessionPasswordNeededError:
            password = input(f"{hijau}Your 2FA Password {res}: ")
            await client.start(phone_number, password)

    user = await client.get_me()
    os.system("clear")
    print(BANNER)
    print(f"{hijau}Telegram Number{res}: {phone_number}")
    print(f"{hijau}Welcome To TeleBot{res}: {user.first_name}")
    print(f"{hijau}This bot is used for automating Telegram tasks.\n\n")

# Countdown Timer
def countdown_timer(seconds):
    while seconds > 0:
        for char in ["|", "/", "-", "\\"]:
            sys.stdout.write(f"\r{abu2}[{yellow}{char}{abu2}]{res} {seconds} seconds remaining")
            sys.stdout.flush()
            sleep(0.25)
        seconds -= 1
    sys.stdout.write("\r" + " " * 50 + "\r")  # Clear line

# Function to open the URL in a headless browser and wait 30 seconds
def open_link_in_browser(url):
    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Set up the WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open the URL in the browser
        driver.get(url)
        print(f"{abu2}[{yellow}!{abu2}]{yellow} Opened site: {url}")
        
        # Wait for 30 seconds
        sleep(30)
        print(f"{abu2}[{yellow}!{abu2}]{yellow} Waited for 30 seconds. Closing browser.")
    except Exception as e:
        print(f"{abu2}[{red}!{abu2}]{red} Error: {e}")
    finally:
        # Close the browser
        driver.quit()

# Main Process
async def main():
    if len(sys.argv) < 2:
        print(BANNER)
        print(f"{yellow}\nUsage: python {sys.argv[0]} +62xxxxxxxxxx")
        sys.exit(1)

    phone_number = sys.argv[1]
    await login(phone_number)

    channel_entity = await client.get_entity("@ClickBeeDOGEBot")

    while True:
        print(f"{abu2}[{yellow}!{abu2}]{yellow} Attempting to retrieve 'Visit Sites' task...")
        await client.send_message(entity=channel_entity, message="\ud83d\udcbb Visit Sites")
        sleep(3)

        history = await client(GetHistoryRequest(
            peer=channel_entity,
            limit=1,
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0
        ))

        message = history.messages[0]
        if "\u26d4\ufe0f Oh no! There are NO TASKS available at the moment. Please check back later! \u23f0" in message.message:
            print(f"{abu2}[{red}x{abu2}] {red}No more 'Visit Sites' tasks available. Starting countdown.")
            countdown_timer(400)
            continue

        try:
            if message.reply_markup and message.reply_markup.rows:
                buttons = message.reply_markup.rows[0].buttons

                for button in buttons:
                    if button.url:
                        url = button.url
                        print(f"{abu2}[{yellow}!{abu2}]{yellow} Visiting site: {url}")
                        threading.Thread(target=open_link_in_browser, args=(url,)).start()
                        countdown_timer(60)
                        break

        except Exception as e:
            print(f"{abu2}[{red}!{abu2}]{red} Error: {e}")

        print(f"{abu2}[{yellow}!{abu2}]{yellow} Restarting loop after countdown.")
        countdown_timer(400)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
