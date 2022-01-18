from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email',
                    'is_students', 'is_admin', 'is_staff')
    list_filter = ('is_students',)
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        # ('Personal info', {'fields': ('email', 'is_students')}),
        ('Permissions', {'fields': ('is_students', 'is_admin', 'is_staff')})
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2',  'is_students')}
         ),
    )
    search_fields = ('email',)
    ordering = ('id',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)