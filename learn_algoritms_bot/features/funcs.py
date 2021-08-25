from datetime import datetime

from supermemo2.sm_two import SMTwo

from learn_algoritms_bot.bot import TelegramBot
from django_tgbot.types.update import Update

from memo.models import Review, TaskToMemorize
from config.settings import MESSAGES_TO_SEND

def create_instance_TaskToMemorize(update: Update, **kwargs) -> TaskToMemorize:
    return TaskToMemorize.objects.create(
        chat_id=update.get_chat().get_id(),
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

def set_review(review_instance: Review, callback_data: int) -> Review:
    smtwo = SMTwo(float(review_instance.easiness), review_instance.interval, review_instance.repetitions).review(callback_data)
    review_instance.easiness = smtwo.easiness
    review_instance.interval = smtwo.interval
    review_instance.repetitions = smtwo.repetitions
    review_instance.quality = callback_data
    review_instance.next_review_date = smtwo.review_date
    review_instance.save()
    return review_instance