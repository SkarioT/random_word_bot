from aiogram import types
from aiogram.types import KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext

from bot_app.states import GameStates
from .app import dp,bot


from get_word_cli import get_and_genirate_words

welcome_msg = "Ceść!\nБот позволяет изучать польские слова и фразы. Список доступных команд:\n/help - возвращет данное сообщение\n/start - возвращет данное сообщение\n/10words - запускает тест на изучение 10 случайных слов"


test_btn = KeyboardButton ("/start")
test_btn2 = KeyboardButton ("/10words")
rkmu = ReplyKeyboardMarkup(resize_keyboard=True).add(test_btn,test_btn2)

@dp.message_handler(commands=['start','help'],state="*")
async def send_welcome(message: types.Message,state: FSMContext):
    ress = await state.get_state()
    if 'random' not in str(ress):
        await bot.send_message(message.from_user.id,welcome_msg,reply_markup=rkmu)
        await GameStates.start.set()
    else:
        await message.reply(f"Невозможно повторно запустить новое/повторное задание.\nЗавершите выполнение текущего задания")
        

@dp.message_handler(commands=['10words'],state='*')
async def send_welcome(message: types.Message,state: FSMContext):
    ress = await state.get_state()
    if 'random' in str(ress):
        await message.reply(f"Невозможно повторно запустить новое/повторное задание.\nЗавершите выполнение текущего задания")
        return
    elif 'None' in str(ress):
        await message.reply(f"Сперва выполните команду /start ")
        return
    await GameStates.random_word.set()
    #получая слово, его перевод и варинты 
    words = get_and_genirate_words()
    #наполняю актуальные кнопки информацией
    inline_button_1 = InlineKeyboardButton(f' {words[2][0]}',callback_data=words[2][0])
    inline_button_2 = InlineKeyboardButton(f' {words[2][1]}',callback_data=words[2][1])
    inline_button_3 = InlineKeyboardButton(f' {words[2][2]}',callback_data=words[2][2])
    inline_kb = InlineKeyboardMarkup()
    inline_kb.add(inline_button_1)
    inline_kb.add(inline_button_2)
    inline_kb.add(inline_button_3)
    
    async with state.proxy() as data:
        data['step'] = 1
        data['counter']=0
        data['answer'] = words[1]
        data['true_word'] = words[0]
        data['words'] = [words[2][2],words[2][1],words[2][0]]
    await message.reply(f" Что означает \'{data['true_word']}\' ?",reply_markup= inline_kb)
                          

@dp.callback_query_handler(state=GameStates.random_word)
async def batton_click_cb(callback_query: types.CallbackQuery,state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    answer = callback_query.data
    async with state.proxy() as data:
        curr_word = data.get("true_word")
        curr_ans = data.get('answer')
        words = get_and_genirate_words()
        inline_button_1 = InlineKeyboardButton(f' {words[2][0]}',callback_data=words[2][0])
        inline_button_2 = InlineKeyboardButton(f' {words[2][1]}',callback_data=words[2][1])
        inline_button_3 = InlineKeyboardButton(f' {words[2][2]}',callback_data=words[2][2])
        inline_kb = InlineKeyboardMarkup()
        inline_kb.add(inline_button_1)
        inline_kb.add(inline_button_2)
        inline_kb.add(inline_button_3)
        

        data['answer'] = words[1]
        data['true_word'] = words[0]
        if answer == curr_ans:
            data['counter'] += 1
            await bot.send_message(callback_query.from_user.id,f" Очень хорошо!  \'{curr_word}\' это \'{answer}\'")
        else:
            await bot.send_message(callback_query.from_user.id,f"Ваш варинт ответа \'{answer}\' не верен.\n Верное значение \'{curr_ans}\'")
        
        if data['step'] >= 10:
            await bot.send_message(callback_query.from_user.id,f"Игра окончина.\nКол-во верных ответов {data['counter']} из {data['step']} попыток")
            await GameStates.start.set()
            return 
        else:
            await bot.send_message(callback_query.from_user.id,f"Кол-во верных ответов {data['counter']} из {data['step']} попыток")
            await bot.send_message(callback_query.from_user.id,f" Что означает \'{data['true_word']}\' ?",reply_markup = inline_kb)
            data['step'] += 1