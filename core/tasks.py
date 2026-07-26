from celery import shared_task

from core.service.user_payouts import UserPayoutsDetails


@shared_task
def generate_payouts():
    UserPayoutsDetails().create_user_payouts()