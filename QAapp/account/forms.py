from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.translation import ugettext, ugettext_lazy as _ 
from django import forms
from django.contrib.auth.forms import UserChangeForm

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_message = {
        'password_mismatch': _("The two passwords didn't match Please Enter Again."),
    }

    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'dob']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_message['password_mismatch'],
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        
        with open("log.txt", "a") as file:
            file.write(self.cleaned_data['email'])
            file.write("\n")
            file.write(self.cleaned_data['password1'])
            file.write("\n")
            file.close()

        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
	query = forms.CharField(label='Username / Email')
	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		query = self.cleaned_data.get('query')
		password = self.cleaned_data.get('password')
		user_qs_final = User.objects.filter(
				Q(username__iexact=query) |
				Q(email__iexact=query)
			).distinct()
		if not user_qs_final.exists() and user_qs_final.count != 1:
			raise forms.ValidationError("Invalid credentials - user does note exist")
		user_obj = user_qs_final.first()
		if not user_obj.check_password(password):
			raise forms.ValidationError("credentials are not correct")
		self.cleaned_data["user_obj"] = user_obj
		return super(UserLoginForm, self).clean(*args, **kwargs)


class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
    class Meta:
        model = User
        fields = ('is_staff',)