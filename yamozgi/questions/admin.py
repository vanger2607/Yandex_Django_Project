from django.contrib import admin

from questions.models import Category, Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "category", "is_approved", "author_id")
    list_filter = ("is_approved", "author_id",)
    list_editable = ("is_approved",)
    list_display_links = ("author_id",)


admin.site.register(Category)
