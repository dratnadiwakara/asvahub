from django.contrib.auth.forms import UserCreationForm
from users.models.auth import User


class InvestorForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'nic_number', 'phone_number', 'address', 'password1', 'password2'
        )
