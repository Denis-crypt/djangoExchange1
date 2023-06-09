from django.shortcuts import redirect
from django.views import View

from authorization.services import try_make_output_request_profit


class SendOutputRequest(View):
    def post(self, request):
        try_make_output_request_profit(request.user)
        return redirect("/")
