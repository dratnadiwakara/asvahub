from django.contrib.auth.forms import UserCreationForm
from users.models.auth import User


class AdminForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'email', 'password1', 'password2',
        )
