from services.config import RedisClient
from celery import shared_task
from django.db import IntegrityError, transaction

from yamozgi.settings import LOGGER
from .models import Battle, Round





@shared_task
def match_users():
    r = RedisClient().conn
    ## Попытка избежать гонок, в будущем нужно будет получае разобраться в lock или возможно lua скрипт на стороне redis
    if len(r.smembers("online_users")) < 2:
        return
    pair = r.spop("online_users", 2)

    user1_id, user2_id = [int(x) for x in pair]
    try:
        with transaction.atomic():
            obj, created = Battle.objects.get_or_create(
                    player_1_id=user1_id,
                    player_2_id=user2_id,
                    is_over=False,
                )
            battle_id = obj.pk
            if created:
                Round.objects.bulk_create(
                    [
                        Round(battle_id_id=battle_id, is_over=False),
                        Round(battle_id_id=battle_id, is_over=False),
                        Round(battle_id_id=battle_id, is_over=False),
                        Round(battle_id_id=battle_id, is_over=False),
                        Round(battle_id_id=battle_id, is_over=False),
                        Round(battle_id_id=battle_id, is_over=False),
                    ]
                )
            next_round = Round.objects.filter(
                battle_id_id=battle_id, is_over=False
            ).first()
            obj.round_now = next_round.pk
            obj.save()
    except IntegrityError:
        # Кто-то другой успел вставить запись из-за гонки — просто достаём существующую запись
        obj = Battle.objects.filter(player_1_id=user1_id, player_2_id=user2_id, is_over=False).first()
        if not obj:
            LOGGER.debug("Страсти какие-то, что-то забагалось в БД резкий дисконнект транзакции")
    r.srem('online_users', str(user1_id), str(user2_id))
    r.set(f"pending_match:{user1_id}", str(obj.pk), ex=300)
    r.set(f"pending_match:{user2_id}", str(obj.pk), ex=300)