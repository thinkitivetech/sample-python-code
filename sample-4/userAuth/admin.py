from django.contrib import admin

from userAuth.models import CustomUser
from django.contrib.auth.models import User 


admin.site.register(CustomUser)

