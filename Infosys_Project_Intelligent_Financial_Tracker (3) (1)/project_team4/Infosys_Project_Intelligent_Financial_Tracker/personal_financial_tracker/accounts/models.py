from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Utilities', 'Utilities'),
        ('Entertainment', 'Entertainment'),
        ('Others', 'Others'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    date = models.DateField()
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Others')

    def _str_(self):
        return f"{self.description} - {self.amount} INR"


from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Utilities', 'Utilities'),
        ('Entertainment', 'Entertainment'),
        ('Others', 'Others'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def _str_(self):
        return f"{self.user.username} - {self.category} - ₹{self.amount}"



# from django.contrib.auth.models import User
# from django.db import models

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     total_budget = models.DecimalField(max_digits=10, decimal_places=2, default=10000.00)  # Default budget

#     def _str_(self):
#         return f"{self.user.username}'s Profile"




from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def _str_(self):
        return f"{self.user.username}'s Profile"