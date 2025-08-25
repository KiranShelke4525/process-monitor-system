from django.contrib import admin

# Register your models here.
# backend/backend_app/admin.py
from django.contrib import admin
from .models import ApiKey, SystemInfo, ProcessInfo

@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ("name","key","created_at")

class ProcessInline(admin.TabularInline):
    model = ProcessInfo
    extra = 0
    readonly_fields = ("name","pid","ppid","cpu_percent","memory_mb")

@admin.register(SystemInfo)
class SystemInfoAdmin(admin.ModelAdmin):
    list_display = ("hostname","timestamp","ram_used_gb")
    inlines = [ProcessInline]
