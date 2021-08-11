from datetime import datetime
from learn_algoritms_bot.models import TelegramUser

from learn_algoritms_bot.bot import TelegramBot
from django_tgbot.types.update import Update

from memo.models import TaskToMemorize
from config.settings import MESSAGES_TO_SEND

def create_instance_TaskToMemorize(update: Update, **kwargs) -> TaskToMemorize:
    return TaskToMemorize.objects.create(
        telegram_username=update.get_user().get_username(),
        title=str(datetime.now().microsecond),
        **kwargs
    )

def isexist_task(bot: TelegramBot, update: Update, url: str) -> bool:
    user = update.get_user().get_username()
    if TaskToMemorize.objects.filter(telegram_username=user, url=url).exists():
        bot.sendMessage(
            update.get_chat().get_id(),
            MESSAGES_TO_SEND.get("TASK_EXIST", None)
            )
        return False
    return True