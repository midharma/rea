import asyncio
import random
import requests

from pyrogram.enums import MessagesFilter


class API:
    async def wall(client):
        anime_channel = random.choice(["@animehikarixa", "@Anime_WallpapersHD"])
        animenya = [
            anime
            async for anime in client.search_messages(
                anime_channel, filter=MessagesFilter.PHOTO
            )
        ]
        return random.choice(animenya)

    def waifu():
        url = "https://www.waifu.im/search"
        response = requests.get(url)
        content = response.text
        start_index = content.find("var files = [") + len("var files = ")
        end_index = content.find("]", start_index)
        files_str = content[start_index:end_index]
        files = [file.strip('" ') for file in files_str.split(",")]
        return random.choice(files)


# class OpenAi:
    # @staticmethod
    # async def ChatGPT(question):
        # response = await asyncio.to_thread(
            # openai.ChatCompletion.create,
            # model="gpt-3.5-turbo",
            # messages=[{"role": "user", "content": question}],
        # )
        # return response.choices[0].message["content"].strip()

    # @staticmethod
    # async def ImageDalle(question):
        # response = await asyncio.to_thread(
            # openai.Image.create,
            # prompt=question,
            # n=1,
        # )
        # return response["data"][0]["url"]

    # @staticmethod
    # async def SpeechToText(file):
        # audio_file = open(file, "rb")
        # response = await asyncio.to_thread(
            # openai.Audio.transcribe, "whisper-1", audio_file
        # )
        # return response["text"]
