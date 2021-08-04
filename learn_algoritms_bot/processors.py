from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from .bot import state_manager
from .models import TelegramState
from .bot import TelegramBot
from memo.models import TaskToMemorize

from datetime import datetime

GREETING = 'Hello! Send me url link of task'

@processor(state_manager, from_states=state_types.All, message_types=message_types.Text)
def welcome(bot: TelegramBot, update: Update, state: TelegramState):
    if update.get_message().get_text() == "/start":
        bot.sendMessage(update.get_chat().get_id(), GREETING)
    if update.get_message().get_text().startswith("http"):
        url = bot.sendMessage(update.get_chat().get_id(), "Well, I got your link. Good luck in work)")
        TaskToMemorize().objects.create(
            title=str(datetime.now().microsecond),
            url=url
        )
        return url