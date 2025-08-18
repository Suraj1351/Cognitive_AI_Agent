import cohere
from rich import print
from dotenv import dote, dotenv_values
env_vars = dotenv_values(".env")
CohereAPIKey = env_vars.get("COHERE_API_KEY")
co = cohere.Client(api_key=CohereAPIKey)
funcs = [
    "exit",
    "general",
    "realtime",
    "open",
    "close",
    "play",
    "generate",
    "image",
    "system",
    "content",
    "google search",
    "youtube search",
    "reminder"
]
messages=[]
preamble=""
ChatHistory = []