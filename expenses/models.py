from django.db import models


class Expense(models.Model):
    category = models.CharField(max_length=100)

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    description = models.CharField(
        max_length=255,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.category}: {self.amount}"