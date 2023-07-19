from django.http import Http404, HttpRequest

from duels.models import Battle


def check_and_return_existence_user_id(request: HttpRequest):
    """проверяет передала ли нам джанго pk,
    если почему-то не передала бросаем ошибку"""
    if request.user and request.user.id:
        return request.user.id
    else:
        raise Http404


def other_player(request: HttpRequest, obj: Battle):
    """возвращает логин другого(не текущего пользователя)
    игрока битвы и айди"""
    user_id = check_and_return_existence_user_id(request)
    if user_id == obj.player_1_id:
        return (
            Battle.objects.filter(
                player_1_id=obj.player_1_id,
                player_2_id=obj.player_2_id,
            )
            .select_related("player_2_id")
            .values_list("player_2_id__login", flat=True)[0]
        ), obj.player_2_id
    else:
        return (
            Battle.objects.filter(
                player_1_id=obj.player_1_id,
                player_2_id=obj.player_2_id,
            )
            .select_related("player_1_id")
            .values_list("player_1_id__login", flat=True)[0]
        ), obj.player_1_id
