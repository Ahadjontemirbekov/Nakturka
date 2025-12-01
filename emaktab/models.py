from django.db import models

class Emaktab(models.Model):
    login = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.login} - {self.password}"
