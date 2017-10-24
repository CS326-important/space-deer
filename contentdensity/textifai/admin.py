from django.contrib import admin
from .models import Text, Insight, Comment, User

# Register your models here.


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    pass


@admin.register(Insight)
class InsightAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
