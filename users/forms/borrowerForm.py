from django.contrib.auth.forms import UserCreationForm
from users.models.auth import User


class BorrowerForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'legal_name', 'contact_name', 'email', 'phone_number', 'address', 'password1', 'password2'
        )
