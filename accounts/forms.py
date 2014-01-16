from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import Account
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Hidden


class NewAccountForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ("username", "first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        super(NewAccountForm, self).__init__(*args, **kwargs)


class EditAccountForm(UserChangeForm):
    class Meta:
        model = Account
        fields = ("username", "first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'

        super(EditAccountForm, self).__init__(*args, **kwargs)
