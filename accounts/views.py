from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from accounts.models import Account
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, CreateView
from accounts import forms


class AccountList(ListView):
    model = Account
    context_object_name = 'accounts'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AccountList, self).dispatch(*args, **kwargs)


class AccountCreate(CreateView):
    model = Account
    form_class = forms.NewAccountForm

    def get_context_data(self, **kwargs):
        context = super(AccountCreate, self).get_context_data(**kwargs)
        context['title'] = "Create Account"
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AccountCreate, self).dispatch(*args, **kwargs)


class AccountDetail(DetailView):
    model = Account
    slug_field = 'username'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AccountDetail, self).dispatch(*args, **kwargs)


class AccountUpdate(UpdateView):
    model = Account
    slug_field = 'username'
    form_class = forms.EditAccountForm

    def get_context_data(self, **kwargs):
        context = super(AccountUpdate, self).get_context_data(**kwargs)
        context['title'] = "Update Account"
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AccountUpdate, self).dispatch(*args, **kwargs)


class AccountDelete(DeleteView):
    model = Account
    slug_field = 'username'
    success_url = reverse_lazy('account_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AccountDelete, self).dispatch(*args, **kwargs)