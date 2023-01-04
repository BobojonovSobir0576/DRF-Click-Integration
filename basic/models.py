from django.db import models

class ClickOrder(models.Model):
    is_paid = models.BooleanField(default=False)
    amount = models.DecimalField(decimal_places=2, max_digits=12)