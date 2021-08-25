import json
from typing import Text
import requests
from celery import shared_task

from datetime import datetime

from memo.models import Review, TaskToMemorize
from config.settings import MESSAGES_TO_SEND
from learn_algoritms_bot.credentials import API_URL
from .bot import bot
from .processors import inline_kb

@shared_task
def remind():
    data = {}
    for task in TaskToMemorize.objects.all():
        review = Review.objects.get(item=task)
        if datetime.now().date() == review.next_review_date:
            text = MESSAGES_TO_SEND.get("REMIND", None).format(review.item.url)
            data.update({
                "chat_id": task.chat_id, 
                "text": text,
                "reply_markup": json.dumps(inline_kb.to_dict())
            })
            requests.post(url=API_URL,
                            data=data)


