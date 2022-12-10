import logging
from aiogram import Bot, Dispatcher, executor, types

from oxfordLookup import getDesinitions
from googletrans import Translator

translate = Translator()

API_TOKEN = '5683933279:AAEurbhaesDWs7l1uxmg71OLKv4SFW1BCQs'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def Salom(message: types.Message):
    """
    start kamandasi yangi kelgan odamga salom beradi
    """
    await message.answer("Assalomu aleykum\nBotimizga xush kelibsiz")
async def Yordam(message: types.Message):
    """
    Yordam commandasi bot xaqida malumot beradi
    """
    await message.answer("/start Tugmasini bosing va uzun matn yuborsanggiz\nsizga perevodini qaytaradi, yoki bitta matn yuborsangiz \nsizga uning manosini qaytaradi.")


@dp.message_handler()
async def Tarjimon(message: types.Message):
    lang = translate.detect(message.text).lang
    if len(message.text.split())>2:
        dest = 'uz' if lang == 'en' else 'en'
        await message.reply(translate.translate(message.text, dest).text)
    else:
        if lang=='en':
            word_id = message.text
        else:
            word_id = translate.translate(message.text, dest='en').text

        lookup = getDesinitions(word_id)
        if lookup:
            await message.reply(f"Word: {word_id} \nDefinitions:\n{lookup['definitions']}")
            if lookup.get('audio'):
                await message.answer_voice(lookup['audio'])
        else:
            await message.reply(f"Bunday so'z topilmadi")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)