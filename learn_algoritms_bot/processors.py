from typing import Dict

from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from django_tgbot.types.replykeyboardmarkup import ReplyKeyboardMarkup, keyboardbutton

from .bot import state_manager
from .models import TelegramState
from .bot import TelegramBot
from memo.models import Review
from learn_algoritms_bot.features.funcs import (
                                                isexist_task,
                                                create_instance_TaskToMemorize)
from config.settings import MESSAGES_TO_SEND

KEYBOARDS_RATE = [
    keyboardbutton.KeyboardButton.a('1'), 
    keyboardbutton.KeyboardButton.a('2'),
    keyboardbutton.KeyboardButton.a('3'),
    keyboardbutton.KeyboardButton.a('4'),
    keyboardbutton.KeyboardButton.a('5')
    ]

ReplyKeyboard = ReplyKeyboardMarkup.a(
                    [KEYBOARDS_RATE], one_time_keyboard=True, resize_keyboard=True,
                        )

DATA: Dict = {} # dict -> {url: str, "quality": int}

@processor(state_manager, from_states=state_types.All, message_types=message_types.Text)
def welcome(bot: TelegramBot, update: Update, state: TelegramState):

    if update.get_message().get_text() == "/start":
        bot.sendMessage(
            update.get_chat().get_id(), MESSAGES_TO_SEND.get("GREETING", None)
            )


@processor(state_manager, from_states=state_types.All, message_types=message_types.Text)
def create_views(bot: TelegramBot, update: Update, state: TelegramState):
    if update.get_message().get_text().startswith("http"):
        url = update.get_message().get_text()
        if isexist_task(update=update, bot=bot, url=url):
            DATA["url"] = url

            bot.sendMessage(
                update.get_chat().get_id(), MESSAGES_TO_SEND.get("GOT_IT", None),
                reply_markup=ReplyKeyboard
                )

    if update.get_message().get_text() in MESSAGES_TO_SEND.get("RATE_CHOICE", None):
        quality = update.get_message().get_text()
        DATA["quality"] = quality

        instance = create_instance_TaskToMemorize(update, **DATA)
        review = Review.objects.get(item=instance)

        bot.sendMessage(
                update.get_chat().get_id(),
                MESSAGES_TO_SEND.get("DATE_OF_REVIEW", None).format(review.next_review_date
                )
            )
