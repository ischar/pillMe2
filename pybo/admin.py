from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import User
# Register your models here.

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('userId', 'userName',  'userPhoneNumber')
    list_filter = ('is_admin', )

    fieldsets = (
        (None, {'fields': ('userId', 'userName', 'password', 'userPhoneNumber')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('userId', 'userName', 'userPhoneNumber', 'password1', 'password2')}),
    )
    search_fields = ('userId', 'userName')
    ordering = ('userName', )
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
