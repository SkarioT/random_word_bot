from aiogram import types
from aiogram.types import KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from bot_app.states import GameStates
from .app import dp,bot

import time
from get_word_cli import get_and_genirate_words,all_verbs,all_words

welcome_msg = "Ceść!\nБот позволяет изучать польские слова и фразы. Список доступных команд:\n/help - возвращет данное сообщение\n/start - возвращет данное сообщение\n/10words - запускает тест на изучение 10 случайных слов"


btn_start = KeyboardButton ("/start")
btn_10words = KeyboardButton ("/10words")
btn_10verbs = KeyboardButton ("/10verbs")
rkmu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_start,btn_10words,btn_10verbs)


@dp.message_handler(commands=['start','help'],state="*")
async def send_welcome(message: types.Message,state: FSMContext):
    state_bot = await state.get_state()
    if 'random' not in str(state_bot):
        await bot.send_message(message.from_user.id,welcome_msg,reply_markup=rkmu)
        await GameStates.start.set()
    else:
        bad_answer = await message.reply(f"Невозможно повторно запустить новое/повторное задание.\nЗавершите выполнение текущего задания")
        time.sleep(3)
        await bad_answer.delete()
        await message.delete()
    # await message.delete()

@dp.message_handler(commands=['10words','10verbs'],state='*')
async def send_start_game(message: types.Message,state: FSMContext):
    state_bot = await state.get_state()
    if 'random' in str(state_bot):
        bad_btn = await message.reply(f"Невозможно повторно запустить новое/повторное задание.\nЗавершите выполнение текущего задания")
        time.sleep(3)
        await message.delete()
        await bad_btn.delete()
        return
    elif 'None' in str(state_bot):
        await message.reply(f"Сперва выполните команду /start ")
        await message.delete()
        return
    await GameStates.random_word.set()
    #получая слово, его перевод и варинты 
    msg_command = str(message.get_command())
    # data_file_name - переменная с именем файла для загрузки
    if 'verbs' in msg_command:
        print("грузим глаголы")
        data_file_name = 'all_verbs'
        words = get_and_genirate_words(all_verbs)
    else:
        print('Грузим все слова')
        data_file_name = 'all_words'
        words = get_and_genirate_words(all_words)
        
    fake_word_1=words.get('question_fake')[0]
    fake_word_2=words.get('question_fake')[1]
    fake_word_3=words.get('question_fake')[2]
    
    #наполняю актуальные кнопки информацией
    inline_button_1 = InlineKeyboardButton(f' {fake_word_1}',callback_data=fake_word_1)
    inline_button_2 = InlineKeyboardButton(f' {fake_word_2}',callback_data=fake_word_2)
    inline_button_3 = InlineKeyboardButton(f' {fake_word_3}',callback_data=fake_word_3)
    inline_kb = InlineKeyboardMarkup()
    inline_kb.add(inline_button_1)
    inline_kb.add(inline_button_2)
    inline_kb.add(inline_button_3)
    
    async with state.proxy() as data:
        data['step'] = 1
        data['counter']=0
        data['answer_true'] = words.get('answer_true')
        data['question_true'] = words.get('question_true')
        data['question_fake'] = words.get('question_fake')
        data['data_file_name'] = data_file_name
    msg = await bot.send_message(message.from_user.id,"Приступим к игре!",reply_markup=ReplyKeyboardRemove())
    time.sleep(2)
    await msg.delete()
    await bot.send_message(message.from_user.id,f" Что означает \'{data['question_true']}\' ?",reply_markup = inline_kb)
                          

@dp.callback_query_handler(state=GameStates.random_word)
async def batton_click_cb(callback_query: types.CallbackQuery,state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    answer_cb_data = callback_query.data
    async with state.proxy() as data:
        current_quiestion_true = data.get("question_true")
        current_answer_true = data.get('answer_true')
        file_name = data.get('data_file_name')
        #из даты,получаю имя файла который требуется "найти"
        #через глобалс, по имени получаю саму переменную
        file_load_name = globals()[file_name]
        if 'verb' in file_name:
            words = get_and_genirate_words(file_load_name)
        else:
            words = get_and_genirate_words(file_load_name)
        fake_word_1=words.get('question_fake')[0]
        fake_word_2=words.get('question_fake')[1]
        fake_word_3=words.get('question_fake')[2]
        inline_button_1 = InlineKeyboardButton(f' {fake_word_1}',callback_data=fake_word_1)
        inline_button_2 = InlineKeyboardButton(f' {fake_word_2}',callback_data=fake_word_2)
        inline_button_3 = InlineKeyboardButton(f' {fake_word_3}',callback_data=fake_word_3)
        inline_kb = InlineKeyboardMarkup()
        inline_kb.add(inline_button_1)
        inline_kb.add(inline_button_2)
        inline_kb.add(inline_button_3)
        

        data['answer_true'] = words.get('answer_true')
        data['question_true'] = words.get('question_true')
        if answer_cb_data == current_answer_true:
            data['counter'] += 1
            msg = await bot.send_message(callback_query.from_user.id,f" Очень хорошо!  \'{current_quiestion_true}\' это \'{answer_cb_data}\'")
        else:
            msg = await bot.send_message(callback_query.from_user.id,f"Ваш варинт ответа \'{answer_cb_data}\' не верен.\n Верное значение \'{current_answer_true}\'")
        
        # await callback_query.message.delete()
        # time.sleep(3)
        # await msg.delete()
        
        if data['step'] >= 10:
            await bot.send_message(callback_query.from_user.id,f"Игра окончина!\nКол-во верных ответов {data['counter']} из {data['step']} попыток",reply_markup=rkmu)
            await GameStates.start.set()
            return 
        else:
            msg = await bot.send_message(callback_query.from_user.id,f"Кол-во верных ответов {data['counter']} из {data['step']} попыток")
            # time.sleep(3)
            # await msg.delete()
            await bot.send_message(callback_query.from_user.id,f"Что означает \'{data['question_true']}\' ?",reply_markup = inline_kb)
            data['step'] += 1