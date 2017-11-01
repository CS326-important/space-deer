from django.contrib import admin
from .models import Text, Insight, Comment, User, GeneralInsight, GrammaticalInsight

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


@admin.register(GeneralInsight)
class GeneralInsightAdmin(admin.ModelAdmin):
    pass


@admin.register(GrammaticalInsight)
class GrammaticalInsightAdmin(admin.ModelAdmin):
    pass

