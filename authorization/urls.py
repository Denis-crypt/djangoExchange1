from django.urls import path

from authorization.views import SendOutputRequest

app_name = 'authorization'
urlpatterns = [
    path('outputrequest', SendOutputRequest.as_view(), name='send_output_request')
]
