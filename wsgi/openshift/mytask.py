__author__ = 'Joanna667'
import os, sys
from microblog.models import UserActivation
from django.contrib.auth.models import User

def run():
    activation = UserActivation.objects.all()
    for u in activation:
        to_user = User.objects.all().filter(id=u.user.id)[0]
        to_user.is_active = True
        to_user.save()
        u.delete()
run()