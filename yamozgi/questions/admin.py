from django.contrib import admin

from questions.models import Category, Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display=("question_text", "category")


admin.site.register(Category)
