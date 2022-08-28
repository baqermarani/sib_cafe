from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User
# Register your models here.


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('personal_id', 'full_name', 'is_admin')
    list_filter = ('is_admin',)
    sortable_by = ['last_login']
    fieldsets = (
        ('Personal Information', {'fields': ('personal_id', 'email', 'phone_number', 'full_name', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'is_superuser',
                                    'last_login', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'full_name', 'password1', 'password2')}),
    )
    search_fields = ('personal_id', 'full_name')
    ordering = ('full_name', 'last_login')
    filter_horizontal = ('groups', 'user_permissions')
    readonly_fields = ('last_login',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['is_superuser'].widget.attrs['disabled'] = True
        return form


admin.site.register(User, UserAdmin)  # Register the UserAdmin class
