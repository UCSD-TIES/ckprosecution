from django.core.urlresolvers import reverse_lazy
from accounts.models import Account
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, CreateView
from accounts import forms

class AccountList(ListView):
    model = Account
    context_object_name = 'accounts'

class AccountCreate(CreateView):
    model = Account
    form_class = forms.NewAccountForm

class AccountDetail(DetailView):
    model = Account
    slug_field = 'username'

class AccountUpdate(UpdateView):
    model = Account
    slug_field = 'username'
    form_class = forms.EditAccountForm

class AccountDelete(DeleteView):
    model = Account
    slug_field = 'username'
    success_url = reverse_lazy('account_list')