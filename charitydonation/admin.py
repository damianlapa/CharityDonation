from django.contrib import admin

from charitydonation.models import Category, Institution, Donation, UserToken

admin.site.register(Category)
admin.site.register(Institution)
admin.site.register(Donation)
admin.site.register(UserToken)