from django.contrib import admin

from main.models import *


class CodeImageInline(admin.TabularInline):
    model = CodeImage
    max_num = 1

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    inlines = [CodeImageInline, ]


admin.site.register(Comment)
