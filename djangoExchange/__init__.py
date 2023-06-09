from __future__ import absolute_import, unicode_literals
from djangoExchange.celery_app import app as celery_app
import pymysql


pymysql.install_as_MySQLdb()
__all__ = ('celery_app',)
