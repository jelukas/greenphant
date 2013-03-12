from django import template

register = template.Library()

@register.filter(name='user_had_vote_lesson')
def user_had_vote_lesson(lesson, user_id):
    return lesson.user_had_vote_lesson(user_id)

@register.filter(name='user_had_vote_course')
def user_had_vote_course(course, user_id):
    return course.user_had_vote_course(user_id)

@register.filter(name='user_had_filled_poll')
def user_had_filled_poll(user):
    return user.get_profile().had_filled_poll()