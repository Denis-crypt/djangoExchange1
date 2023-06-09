from djangoExchange.celery_app import app

from trades_info.services import request_to_update_trades_for_users


@app.task
def update_trades():
    request_to_update_trades_for_users()
