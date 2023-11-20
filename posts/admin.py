from django.contrib import admin
from .models import Post, Comment, Reply
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class PostAdmin(ImportExportModelAdmin):
    pass

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Reply)