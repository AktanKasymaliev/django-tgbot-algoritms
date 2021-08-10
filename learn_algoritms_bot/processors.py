from datetime import datetime
from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from django_tgbot.types.replykeyboardmarkup import ReplyKeyboardMarkup, keyboardbutton

from .bot import state_manager
from .models import TelegramState
from .bot import TelegramBot
from memo.models import Review, TaskToMemorize


GREETING = 'Hello 👋! Send me url link of task'
GOT_IT = "Well, I got your link. ✅\nRate it! 🌟"
RATE_CHOICE = ("1", "2", "3", "4", "5")

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

def create_instance_TaskToMemorize(url, quality):
    return TaskToMemorize.objects.create (
        title=str(datetime.now().microsecond),
        url=url, 
        quality=quality
    )

@processor(state_manager, from_states=state_types.All, message_types=message_types.Text)
def welcome(bot: TelegramBot, update: Update, state: TelegramState):

    if update.get_message().get_text() == "/start":
        bot.sendMessage(
            update.get_chat().get_id(), GREETING
            )


@processor(state_manager, from_states=state_types.All, message_types=message_types.Text)
def create_views(bot: TelegramBot, update: Update, state: TelegramState):
    url: str = ''

    if update.get_message().get_text().startswith("http"):
        url += update.get_message().get_text()
        bot.sendMessage(
            update.get_chat().get_id(), GOT_IT,
                reply_markup=ReplyKeyboard
            )

    if update.get_message().get_text() in RATE_CHOICE:
        quality = update.get_message().get_text()
        instance = create_instance_TaskToMemorize(url, quality)

        review = Review.objects.get(item=instance)
        bot.sendMessage(update.get_chat().get_id(), f"You should review 👀 this taks at {review.next_review_date} 📅")

