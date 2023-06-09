from django.urls import path

from trades_info.views import MainView, COINMView
from authorization.views import SendOutputRequest

app_name = 'trade_info'
urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('coinm', COINMView.as_view(), name='coinm'),
    path('outputrequest', SendOutputRequest.as_view(), name='send_output_request'),
]
