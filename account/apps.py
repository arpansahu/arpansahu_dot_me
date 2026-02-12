from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = 'account'
    label = 'user_account'  # Different label to avoid conflict with allauth.account
    verbose_name = 'User Account'
