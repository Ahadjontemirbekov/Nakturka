from django.db import models

class Nakrutka(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
