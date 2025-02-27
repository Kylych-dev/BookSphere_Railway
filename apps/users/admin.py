from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class UserAdmin(UserAdmin):
    model = User
    list_display = (
        'email',
        'username',
        'is_staff',
        'is_active'
    )
    list_filter = ('is_staff', 'is_active')

    fieldsets = (
        # (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('email', 'username')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
