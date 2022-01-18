from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile


class UserAdmin(BaseUserAdmin):
    list_display = ('email',
                    'is_students', 'is_admin', 'is_staff')
    list_filter = ('is_students', 'is_admin',)
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

class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "preferred_name", "bio", "current_level")


admin.site.register(UserProfile, ItemAdmin)


admin.site.register(User, UserAdmin)
