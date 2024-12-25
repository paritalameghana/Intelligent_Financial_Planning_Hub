from django import forms
from django.contrib.auth.models import User
from .models import Expense

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
        label="Confirm Password"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter email address'}),
        label="Email Address"
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}),
        label="Username"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # Add 'email' to fields
        help_texts = {
            'username': None,  # Remove the default help text for the username field
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")
        return cleaned_data


class ExpenseForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    category = forms.ChoiceField(choices=Expense.CATEGORY_CHOICES, widget=forms.Select())

    class Meta:
        model = Expense
        fields = ['date', 'description', 'amount', 'category']







from django import forms
from .models import UserProfile

class BudgetForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['total_budget']