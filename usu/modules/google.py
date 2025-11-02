import requests
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pyrogram.types import Message
from usu import *

import glob
import io
import os
import re
import urllib
import urllib.request

import bs4
import requests
from PIL import Image
from search_engine_parser import GoogleSearch

import urllib.parse

import aiohttp

async def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            results = []
            for result in soup.find_all("a"):
                link = result.get("href")
                if link and link.startswith("/url?q="):
                    title = result.text
                    link = link.replace("/url?q=", "")
                    results.append({
                        "title": title,
                        "link": link
                    })
            return results

@USU.UBOT("google")
async def gsearch(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    usu = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    match = get_arg(message)
    if not match:
        await usu.edit(f"<i><b>{ggl}Berikan sesuatu!</b></i>")
        return
    try:
        hasil = await search_google(match)
        text = f"{broad}Search Query: {match}\n\n"
        for result in hasil[:5]: # tampilkan 5 hasil pertama
            text += f"{result['title']}: {result['link']}\n\n"
        await usu.edit(text)
    except Exception as a:
        return await usu.edit(a)