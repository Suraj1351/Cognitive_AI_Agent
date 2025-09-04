import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep
import base64
import json


def open_image(prompt):
    folder_path = r"Data"
    os.makedirs(folder_path, exist_ok=True)
    prompt = prompt.replace(" ", "_")

    Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in Files:
        Image_path = os.path.join(folder_path, jpg_file)

        try:
            img = Image.open(Image_path)
            print(f"Opened image: {Image_path}")
            img.show()
            sleep(1)

        except IOError:
            print(f"Error opening image: {Image_path}")


API_KEY = get_key(".env", "HUGGINGFACEAPIKEY")
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {API_KEY}"}


async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        print(f"API Error {response.status_code}: {response.text}")
        return None

    try:
        data = response.json()
        # HuggingFace returns `data[0]['b64_json']`
        if isinstance(data, list) and "b64_json" in data[0]:
            return base64.b64decode(data[0]["b64_json"])
    except Exception as e:
        print(f"Response parse error: {e}")
        return None


async def generate_image(prompt: str):
    tasks = []

    for _ in range(4):
        payload = {
            "inputs": prompt,
            "options": {
                "seed": randint(1, 1000000)
            }
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):
        if image_bytes:
            file_path = fr"Data\{prompt.replace(' ', '_')}{i+1}.jpg"
            with open(file_path, "wb") as f:
                f.write(image_bytes)
            print(f"Saved: {file_path}")
        else:
            print(f"Image {i+1} failed to generate.")


def GenerateImages(prompt: str):
    asyncio.run(generate_image(prompt))
    open_image(prompt)


while True:
    try:
        if not os.path.exists(r"Frontend\Files\ImageGeneration.data"):
            os.makedirs(r"Frontend\Files", exist_ok=True)
            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("sample prompt,True")

        with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
            Data: str = f.read().strip()
        Prompt, Status = Data.split(",")

        if Status == "True":
            print(f"Generating images for: {Prompt}")
            GenerateImages(prompt=Prompt)

            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("False,False")
            break
        else:
            sleep(1)

    except:
        pass
