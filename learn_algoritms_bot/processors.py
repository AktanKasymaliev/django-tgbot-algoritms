from typing import Dict, List

from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from django_tgbot.types.replykeyboardmarkup import ReplyKeyboardMarkup, keyboardbutton
from django_tgbot.types.inlinekeyboardbutton import InlineKeyboardButton
from django_tgbot.types.inlinekeyboardmarkup import InlineKeyboardMarkup

from .bot import state_manager
from .models import TelegramState
from .bot import TelegramBot
from memo.models import Review, TaskToMemorize
from learn_algoritms_bot.features.funcs import (handle_new_task, set_review,
                                                handle_rating,
                                                create_instance_TaskToMemorize,
                                                task_exists,
                                                handle_existing_task)
from config.settings import MESSAGES_TO_SEND


KEYBOARDS_RATE: List[keyboardbutton.KeyboardButton] = [
    keyboardbutton.KeyboardButton.a('1'), 
    keyboardbutton.KeyboardButton.a('2'),
    keyboardbutton.KeyboardButton.a('3'),
    keyboardbutton.KeyboardButton.a('4'),
    keyboardbutton.KeyboardButton.a('5')
    ]

inline_kb = InlineKeyboardMarkup.a(inline_keyboard=[
    [
        InlineKeyboardButton.a(text='1', callback_data="1"),
        InlineKeyboardButton.a(text='2', callback_data="2"),
        InlineKeyboardButton.a(text='3', callback_data="3"),
    ],
    [InlineKeyboardButton.a(text='4', callback_data="4"),
     InlineKeyboardButton.a(text='5', callback_data="5")]
])

ReplyKeyboard = ReplyKeyboardMarkup.a(
                    [KEYBOARDS_RATE], one_time_keyboard=True, resize_keyboard=True,
                        )

DATA: Dict = {} # {"url": str, "quality": int}


@processor(state_manager, from_states=state_types.All, message_types=message_types.Text)
def welcome(bot: TelegramBot, update: Update, state: TelegramState):
    try:
        if update.get_message().get_text() == "/start":
            bot.sendMessage(
                update.get_chat().get_id(), MESSAGES_TO_SEND.get("GREETING", None)
                )
    except AttributeError:
        pass


@processor(state_manager, from_states=state_types.All, message_types=message_types.Text)
def create_views(bot: TelegramBot, update: Update, state: TelegramState):
    try:
        text = update.get_message().get_text()
        if text.startswith("http"):
            url = text
            
            if task_exists(update, url):
                handle_existing_task(bot, update)
            else:
                handle_new_task(bot, update, url)

        if text in MESSAGES_TO_SEND.get("RATE_CHOICE", None):
            handle_rating(bot, update, text)

    except AttributeError:
        pass

@processor(state_manager, from_states=state_types.All, message_types=message_types.Text)
def next_review(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    try:
        callback_data = int(update.get_callback_query().get_data())
        if callback_data:
            url = update.get_callback_query().get_message().get_text().split("this: ")[-1]
            
            task_instance: TaskToMemorize = TaskToMemorize.objects.get(chat_id=chat_id, url=url)
            review_instance: Review = Review.objects.get(item=task_instance)

            review_obj = set_review(review_instance, callback_data)

            bot.sendMessage(
                    chat_id,
                    MESSAGES_TO_SEND.get("REVIEW", None).format(date=review_obj.next_review_date, url=url)
                )
    except (TaskToMemorize.DoesNotExist, Review.DoesNotExist, AttributeError):
        pass