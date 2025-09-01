from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os

# Load environment variables
load_dotenv()
GroqAPIKey = os.getenv("GroqAPIKey")

# Initialize Groq client
client = Groq(api_key=GroqAPIKey)

classes = [
    "zCubwf", "hgKElc", "LTKOO sY7ric", "ZOLcW",
    "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta",
    "IZ6rdc", "05uR6d LTKOO", "vlzY6d",
    "webanswers-webanswers_table_webanswers-table",
    "dDoNo ikb4Bb gsrt", "sXLaOe", "LWkfKe", "VQF4g",
    "qv3Wpe", "kno-rdesc", "SPZz6b"
]

useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"

professional_responses = [
    "Your satisfaction is my priority; feel free to reach out if there's anything else I can assist you with.",
    "I'm at your service for additional questions or support you may need-don't hesitate to ask."
]

messages = []
SystemChatBot = [{
    "role": "user",
    "content": f"Hello, I am {os.getenv('USERNAME', 'User')}, You're a content writer. You have to write content like letter."
}]

def GoogleSearch(Topic):
    search(Topic)
    return True

def Content(Topic):
    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor, File])

    def ContentWriter(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})

        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer

    Topic = Topic.replace("Content", "")
    ContentByAI = ContentWriter(Topic)  # FIXED here

    os.makedirs("Data", exist_ok=True)
    filename = rf"Data\{Topic.lower().replace(' ', '_')}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(ContentByAI)

    OpenNotepad(filename)
    return True

def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

def PlayYouTube(query):
    playonyt(query)
    return True

def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a', {"jsname": "UWckNb"})
            return [link.get('href') for link in links]

        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {"User-Agent": useragent}
            response = sess.get(url, headers=headers)
            if response.status_code == 200:
                return response.text
            else:
                print("Failed to retrieve search results.")
            return None

        html = search_google(app)

        if html:
            link = extract_links(html)[0]
            webopen(link)

        return True

def CloseApp(app):
    if "chrome" in app:
        pass
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except:
            return False

def System(command):
    def mute():
        keyboard.press_and_release("volume mute")

    def unmute():
        keyboard.press_and_release("volume unmute")

    def volume_up():
        keyboard.press_and_release("volume up")

    def volume_down():
        keyboard.press_and_release("volume down")

    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
    return True

async def TranslateAndExecute(command: list[str]):
    funcs = []

    for command in command:
        if command.startswith("open"):
            if "open it" in command:
                pass
            if "open file" == command:
                pass
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open"))
                funcs.append(fun)

        elif command.startswith("general"):
            pass
        elif command.startswith("realtime"):
            pass
        elif command.startswith("close"):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close"))
            funcs.append(fun)

        elif command.startswith("play"):
            fun = asyncio.to_thread(PlayYouTube, command.removeprefix("play"))
            funcs.append(fun)
        elif command.startswith("content"):
            fun = asyncio.to_thread(Content, command.removeprefix("content"))
            funcs.append(fun)
        elif command.startswith("google search"):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search"))
            funcs.append(fun)
        elif command.startswith("youtube search"):
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search"))
            funcs.append(fun)
        elif command.startswith("system"):
            fun = asyncio.to_thread(System, command.removeprefix("system"))
            funcs.append(fun)
        else:
            print(f"No Function Found. For {command}")

    results = await asyncio.gather(*funcs)

    for result in results:
        yield result

async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
        pass
    return True

if __name__ == "__main__":
    asyncio.run(Automation([
        "open notepad",
        "content write a letter to my friend",
        "google search latest news",
        "youtube search funny videos",
        "play despacito",
        "system volume up",
        "close notepad"
    ]))
