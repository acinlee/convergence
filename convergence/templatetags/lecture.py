from convergence.models import Lecture, Lecture_Status, User
from django import template
import os
register = template.Library()


@register.simple_tag
def is_finished_lecture(user_id, lecture):
    print(user_id, lecture)
    if user_id and lecture:
        try:
            ls = Lecture_Status.objects.get(
                ls_learner__Convergence_ID = user_id,
                ls_lecture = lecture
            )

            status = '수강 완료' if ls.ls_isFinished else '미수강'
            return status
        except:
            pass

    return ""