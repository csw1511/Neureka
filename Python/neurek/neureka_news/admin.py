from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
# loglogs/admin.py
from django.contrib import admin
# from .models import RequestLog

# Register your models here.


class MultiDBModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


class RequestLogAdmin(MultiDBModelAdmin):
    using = 'mongodb'

    list_display = ('status_code', 'request_method', 'remote_address', 'request_path', 'request_user', 'created_at')
    list_filter = ('status_code', 'request_method',)
    ordering = ('-created_at',)


# admin.site.register(RequestLog, RequestLogAdmin)