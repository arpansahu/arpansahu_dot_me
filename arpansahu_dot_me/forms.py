from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Your name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': "form-control", 'placeholder': "Your email"}))
    otp = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Enter OTP"}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Your subject"}))
    contact = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "+00 1234 5678 90"}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control", 'rows': 4, 'placeholder': "Enter your message..."}))
