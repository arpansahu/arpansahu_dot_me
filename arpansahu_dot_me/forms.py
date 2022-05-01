from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Your name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': "form-control", 'placeholder': "Your email"}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "your subject"}))
    contact = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "+00 1234 5678 90"}))
    message = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", "rows": 5,  'placeholder': "Enter your message..." }))
