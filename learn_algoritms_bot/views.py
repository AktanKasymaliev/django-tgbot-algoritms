import logging

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_tgbot.types.update import Update

from .bot import bot


@csrf_exempt
def handle_bot_request(request):
    update = Update(request.body.decode("utf-8"))

    try:
        bot.handle_update(update)
    except Exception as e:
        if settings.DEBUG:
            raise e
        else:
            logging.exception(e)
    return HttpResponse("OK")


def poll_updates(request):
    """
    Polls all waiting updates from the server. Note that webhook should not be set if polling is used.
    You can delete the webhook by passing an empty URL as the address.
    """
    count = bot.poll_updates_and_handle()
    return HttpResponse(f"Processed {count} update{'' if count == 1 else 's'}.")
