from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['Convergence_Name']

admin.site.register(User, UserAdmin)
admin.site.register(Convergence_Board)
admin.site.register(Convergence_Comment)
admin.site.register(Convergence_Comment_reply)

