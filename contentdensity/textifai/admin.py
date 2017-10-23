from django.contrib import admin
from .models import Text, Insight

# Register your models here.

@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    pass


@admin.register(Insight)
class InsightAdmin(admin.ModelAdmin):
    pass