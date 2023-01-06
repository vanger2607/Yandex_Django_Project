from django import template

from yamozgi.settings import MEDIA_URL

register = template.Library()


@register.simple_tag
def index(indexable, i, num=0):
    """получение никнейма"""
    try:
        return indexable[i + num]["login"]
    except IndexError:
        return False


@register.simple_tag
def get_user_pk(indexable, i, num=0):
    """получение айди"""
    try:
        return indexable[i + num]["id"]
    except IndexError:
        return False


@register.simple_tag
def get_user_sent_pk(indexable, i, num=0):
    """получение айди юзера отправившего вызов"""
    try:
        return indexable[i + num]["sent_id"]
    except IndexError:
        return False


@register.simple_tag
def get_user_recieved_pk(indexable, i, num=0):
    """получение айди юзера получившего вызов"""
    try:
        return indexable[i + num]["recieved_id"]
    except IndexError:
        return False


@register.simple_tag
def index_url(indexable, i, num=0):
    """получение урла для картинки"""
    try:
        return MEDIA_URL + indexable[i + num]["avatar"]
    except IndexError:
        return False


@register.simple_tag
def battle_url(indexable, i, num=0):
    """получение урла для ссылки на битву"""
    try:
        return "/battles/" + str(indexable[i + num]["id"])
    except IndexError:
        return False


@register.filter(name="times")
def times(number):
    """возвращает функцию range для цикла for в шаблонах,
    где карточки с информацией идут строчками по три карточки в каждой"""
    if number % 3 == 0:
        return range(0, 3 * (number // 3), 3)
    return range(0, 3 * (number // 3) + 1, 3)
