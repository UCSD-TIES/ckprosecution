from django.contrib.auth.models import User
from ckprosecution.accounts.models import UserProfile

user, created = User.objects.get_or_create(username="admin")
if created:
	user.set_password("admin")
	user.is_superuser = True
	user.is_staff = True
	user.save()

	x = UserProfile.objects.create(user=user)
	x.save()
