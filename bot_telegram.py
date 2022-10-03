import time,emoji
import asyncio, json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from config import TOKEN
from prog import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.types import ReplyKeyboardRemove

storage = MemoryStorage()

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

async def on_startup(self):
    print('Бот запущен')


class FSMDiscount(StatesGroup):
    discount =State()

@dp.message_handler(commands='start')
async def start(message: types.Message):
    activity_bot('stop', float(20),str(message.chat.id))
    start_buttons = ['/Search', '/Change_discount']
    keybord = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keybord.add(*start_buttons)

    await message.answer('Выберите с чего вы хотите начать', reply_markup=keybord)


@dp.message_handler(commands='Search')
async def start_op(message: types.Message):
    if (get_activity(str(message.chat.id))['condition'] == 'stop'):
        set_condition('start',str(message.chat.id))
        set_price(get_price(),str(message.chat.id))
        search_buttons = ['/Stop', '/Change_discount','/Min_price']
        keybord = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keybord.add(*search_buttons)
        await message.answer('Бот запущен', reply_markup=keybord)
        while (get_activity(str(message.chat.id))['condition']=='start'):
            price = get_price()
            new_price = get_price()*(1+(get_activity(str(message.chat.id))['discount'])/100)
            old_price = get_activity(str(message.chat.id))['price']
            if(new_price<old_price):
                set_price(get_price(), str(message.chat.id))
                disc = (old_price/price)*100-100
                await bot.send_message(message.chat.id,f"Появился новый единорог, не упусти прибыль {disc}%")
            await asyncio.sleep(1)
    else:
        await message.answer('Бот уже запущен')


@dp.message_handler(commands='Change_discount',state=None)
async def change_disc(message: types.Message):
    set_condition('stop',str(message.chat.id))
    await FSMDiscount.discount.set()
    disc_buttons = ['10','15', '20']
    keybord = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keybord.add(*disc_buttons)
    await message.answer('Выберите скидку: ', reply_markup=keybord)

@dp.message_handler(state=FSMDiscount.discount)
async def get_disc(message: types.Message,state:FSMContext):
    try:
        set_discount(float(message.text),str(message.chat.id))
        if not (float(message.text)>=0):
            print(message.text)
            raise ValueError()
        start_buttons = ['/Search', '/Change_discount']
        keybord = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keybord.add(*start_buttons)
        await state.finish()
        await message.reply('Скидка выбрана '+emoji.emojize(":check_mark_button:"), reply_markup=keybord)
    except:
        disc_buttons = ['10', '15', '20']
        keybord = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keybord.add(*disc_buttons)
        await message.reply('Это не число,попробуйте заново ', reply_markup=keybord)


@dp.message_handler(commands='Stop')
async def stop(message: types.Message):
        set_condition('stop',str(message.chat.id))
        start_buttons = ['/Search', '/Change_discount']
        keybord = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keybord.add(*start_buttons)
        await message.answer('Бот остановлен',reply_markup=keybord)

@dp.message_handler(commands='Min_price')
async def min_price(message: types.Message):
    price = get_price()
    await bot.send_message(message.chat.id, f"В настоящий момент минимальная цена {price} эфира")

def main():
    executor.start_polling(dp,skip_updates=True, on_startup=on_startup)


if __name__ == '__main__':
    main()
