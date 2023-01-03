from django import template

from yamozgi.settings import MEDIA_URL

register = template.Library()


@register.simple_tag
def index(indexable, i, num=0):
    try:
        return indexable[i + num]["login"]
    except IndexError:
        return False


@register.simple_tag
def get_user_pk(indexable, i, num=0):
    try:
        return indexable[i + num]["id"]
    except IndexError:
        return False


@register.simple_tag
def index_url(indexable, i, num=0):
    try:
        return MEDIA_URL + indexable[i + num]["avatar"]
    except IndexError:
        return False


@register.filter(name="times")
def times(number):
    return range(0, 3 * number + 1, 3)
