from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Field, Layout, Submit
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User


class UserCreateForm(UserCreationForm):
    FORM_ID = 'registerForm'

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = self.FORM_ID
        self.helper.form_method = 'post'
        self.helper.form_action = 'register'
        self.helper.layout = Layout(
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
            FormActions(
                Submit('submit', 'Submit'),
                css_class="form-row justify-content-center"
            ),
        )
        self.helper.label_class = 'text-capitalize'


class LoginForm(forms.Form):
    FORM_ID = 'loginForm'

    email = forms.EmailField()
    password = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
    error_messages = {
        'invalid_login': _(
            'Please enter a correct %(username)s and password. Note that both '
            'fields may be case-sensitive.'
        ),
        'inactive': _('This account is inactive.'),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        self.username_field = User._meta.get_field(User.USERNAME_FIELD)
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = self.FORM_ID
        self.helper.layout = Layout(
            Field('email'),
            Field('password'),
            FormActions(
                Submit('submit', 'Login'),
                css_class="form-row justify-content-center"
            )
        )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': self.username_field.verbose_name},
        )


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'email',
            FormActions(
                Submit('submit', 'Reset my password'),
                css_class="form-row justify-content-center"
            )
        )


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('new_password1'),
            'new_password2',
            FormActions(
                Submit('submit', 'Reset my password'),
                css_class="form-row justify-content-center"
            )
        )
        self.helper.label_class = 'text-capitalize'


class CustomChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'old_password',
            'new_password1',
            'new_password2',
            FormActions(
                Submit('submit', 'Change my password'),
                css_class="form-row justify-content-center"
            )
        )
        self.helper.label_class = 'text-capitalize'


class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'email',
            'first_name',
            'last_name',
            HTML('''<label for="id_change_password">Password</label><br>
                <a id="changePasswordBtn" class="btn btn-primary" href="{% url 'password_change_view' %}">Change Password</a>
                <hr>
            '''),
            FormActions(
                Submit('submit', 'Update'),
                css_class="form-row justify-content-end"
            )
        )

        self.helper.label_class = 'text-capitalize'
