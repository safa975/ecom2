from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

# Get the custom user model
CustomUser = get_user_model()

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password",
        required=True
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password",
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'phone_number', 'address', 'date_of_birth']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])  # Hash the password before saving
        if commit:
            user.save()
        return user
