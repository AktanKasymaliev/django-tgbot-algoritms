from datetime import datetime
from typing import List

from django_tgbot.types.replykeyboardmarkup import ReplyKeyboardMarkup, keyboardbutton
from supermemo2.sm_two import SMTwo

from learn_algoritms_bot.bot import TelegramBot
from django_tgbot.types.update import Update

from memo.models import Review, TaskToMemorize
from config.settings import MESSAGES_TO_SEND

def list_of_kb(task_id: int) -> List[keyboardbutton.KeyboardButton]:
    tsk_id  = str(task_id)
    return [
        keyboardbutton.KeyboardButton.a(tsk_id + '. 1'),
        keyboardbutton.KeyboardButton.a(tsk_id + '. 2'),
        keyboardbutton.KeyboardButton.a(tsk_id + '. 3'),
        keyboardbutton.KeyboardButton.a(tsk_id + '. 4'),
        keyboardbutton.KeyboardButton.a(tsk_id + '. 5')
        ]


def create_instance_TaskToMemorize(update: Update, **kwargs) -> TaskToMemorize:
    url = kwargs.get("url", "")

    if not url:
        #TODO log exception
        pass

    return TaskToMemorize.objects.create(
        chat_id=update.get_chat().get_id(),
        telegram_username=update.get_user().get_username(),
        title=str(datetime.now().microsecond),
        url=url,
        quality=kwargs.get("quality", 3)
    )

def task_exists(update: Update, url: str) -> bool:
    user = update.get_user().get_username()
    return TaskToMemorize.objects.filter(telegram_username=user, url=url).exists()

def build_rating_keyboard(task_id: int):
    return ReplyKeyboardMarkup.a(
                    [list_of_kb(task_id)], one_time_keyboard=True, resize_keyboard=True,
                        )

def handle_existing_task(bot: TelegramBot, update: Update) -> None:
    bot.sendMessage(
        update.get_chat().get_id(),
        MESSAGES_TO_SEND.get("TASK_EXIST", None)
    )

def handle_new_task(bot: TelegramBot, update: Update, url: str) -> None:
    instance = create_instance_TaskToMemorize(update, **{"url": url})
    rating_keyboard = build_rating_keyboard(instance.id)
    bot.sendMessage(
        update.get_chat().get_id(), MESSAGES_TO_SEND.get("GOT_IT", None),
        reply_markup=rating_keyboard
            )

def handle_rating(bot: TelegramBot, update: Update, text: str) -> None:
    task_id, quality = text.split(". ")
    instance: TaskToMemorize = TaskToMemorize.objects.get(id=int(task_id))
    instance.quality = int(quality)
    review: Review = Review.objects.get(item=instance)
    review.quality = int(quality)
    instance.save(), review.save()
    bot.sendMessage(
            update.get_chat().get_id(),
            MESSAGES_TO_SEND.get("DATE_OF_REVIEW", None).format(review.next_review_date)
        )

def set_review(review_instance: Review, callback_data: int) -> Review:
    smtwo = SMTwo(float(review_instance.easiness), review_instance.interval, review_instance.repetitions).review(callback_data)
    review_instance.easiness = smtwo.easiness
    review_instance.interval = smtwo.interval
    review_instance.repetitions = smtwo.repetitions
    review_instance.quality = callback_data
    review_instance.next_review_date = smtwo.review_date
    review_instance.save()
    return review_instance