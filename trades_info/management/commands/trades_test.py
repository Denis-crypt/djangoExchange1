from django.core.management import BaseCommand

from trades_info.services import request_to_update_trades_for_users


class Command(BaseCommand):
    def handle(self, *args, **options):
        request_to_update_trades_for_users()
