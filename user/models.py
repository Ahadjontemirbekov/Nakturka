from django.db import models

class Nakrutka(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


from django.db import models


class UCOrder(models.Model):
    game_id = models.CharField(max_length=50)
    server = models.CharField(max_length=20)
    uc_amount = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=255)
    terms = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  self.email
