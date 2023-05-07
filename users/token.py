from django.contrib.auth.tokens import PasswordResetTokenGenerator
from users.models import UserBase


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user: UserBase, timestamp: int) -> str:
        return super()._make_hash_value(user, timestamp)


account_activation_token = AccountActivationTokenGenerator()
