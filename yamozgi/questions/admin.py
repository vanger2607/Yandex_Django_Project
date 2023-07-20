from django.contrib import admin

from questions.models import Category, Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "question_text",
        "category",
        "is_approved",
        "author",
    )
    list_filter = (
        "is_approved",
        "author",
        "category",
    )
    list_editable = ("is_approved",)
    list_display_links = ("author", "question_text",)

    def author_name(self, instance):
        return instance.author.login


admin.site.register(Category)
