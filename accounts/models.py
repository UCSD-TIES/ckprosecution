from django.contrib.auth.models import User

class Account(User):
    class Meta:
        proxy = True

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('account_detail', args=[str(self.username)])




