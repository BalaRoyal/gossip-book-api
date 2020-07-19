from django.contrib import admin

from .models import (Question,
                     QuestionComment,
                     QuestionVote,
                     QuestionCommentVote)

# Register your models here.
admin.site.register(Question)
admin.site.register(QuestionComment)
admin.site.register(QuestionVote)
admin.site.register(QuestionCommentVote)
