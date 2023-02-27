import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InputFile
from aiogram.dispatcher.filters import ChatTypeFilter, filters
import re
from io import BytesIO
import aiohttp
#Python 3.11.2: aiogram 2.25.1, aiohttp 3.8.4, aiosignal  1.3.1, openai 0.26.5
token = "enter here your tokens"
openai.api_key = "enter here your api-key from openai"
bot = Bot(token)
dp = Dispatcher(bot)

@dp.message_handler(chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def send(message: types.Message):
    if "bot" in message.text.lower() or "бот" in message.text.lower():
        responce = openai.Completion.create(
            model="text-davinci-003",
            prompt=message.text,
            temperature=0.5,
            max_tokens=3000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["Стоп"],
        )
        await message.answer(responce['choices'][0]['text'])
    if "сгенерируй" in message.text.lower() or "генерируй" in message.text.lower() or "ganerate" in message.text.lower():
        size = '256x256' if "smallSize" in message.text else "512x512" if "mediumSize" in message.text else "1024x1024"
        responce = openai.Image.create(
            prompt=message.text,
            size=size,
        )
        image_url = responce['data'][0]['url']
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                content = await resp.content.read()
        await message.answer_photo(InputFile(BytesIO(content), filename="generated_image.png"), caption="Запрос: " + message.text + ", " + size)

@dp.message_handler(ChatTypeFilter(types.ChatType.PRIVATE))
async def private(message: types.Message):
    if "сгенерируй" in message.text.lower() or "генерируй" in message.text.lower() or "ganerate" in message.text.lower():
        try:
            size = '256x256' if "smallSize" in message.text else "512x512" if "mediumSize" in message.text else "1024x1024"

            responce = openai.Image.create(
                prompt=message.text,
                size=size,
            )
            image_url = responce['data'][0]['url']
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as resp:
                    content = await resp.content.read()
            await message.answer_photo(InputFile(BytesIO(content), filename="generated_image.png"), caption="Запрос: " + message.text + ", " + size)
            return
        except openai.error.OpenAIError as error:
            print(f"OpenAI API error: {error}")
            responce = f"OpenAI API error: {error}"
            await message.answer(responce)
        
    try:
        responce = openai.Completion.create(
            model="text-davinci-003",
            prompt=message.text,
            temperature=0.5,
            max_tokens=4000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["Стоп"],
        )   
        await message.answer(responce['choices'][0]['text'])
    except openai.error.OpenAIError as error:
        print(f"OpenAI API error: {error}")
        responce = f"OpenAI API error: {error}"
        await message.answer(responce)
executor.start_polling(dp, skip_updates=True)
