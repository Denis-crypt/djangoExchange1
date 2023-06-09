from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import ListView
from django.views.generic.edit import FormView

from trades_info.models import TradeBinanceCOINM, TradeBinanceUSDT
from trades_info.forms import DateRangeForm


class MainView(LoginRequiredMixin, FormView, ListView):
    template_name = 'trades_info/trades_binance_list.html'
    form_class = DateRangeForm

    def get_initial(self):
        return {
            'start_date': str(self.request.GET.get('start_date', (
                    timezone.localdate().today() - timezone.timedelta(days=30)
            ))),
            'end_date': str(self.request.GET.get('end_date', timezone.localdate().today()))
        }

    def get_queryset(self):
        form = DateRangeForm(self.request.GET)

        if form.is_valid():
            start_date, end_date = form.cleaned_data['start_date'], form.cleaned_data['end_date']
            start_datetime = timezone.datetime.combine(start_date, timezone.datetime.min.time())
            end_datetime = timezone.datetime.combine(end_date, timezone.datetime.max.time())
        else:
            start_datetime = timezone.datetime.today() - timezone.timedelta(days=30)
            end_datetime = timezone.datetime.today()

        return TradeBinanceUSDT.objects.filter(
            user=self.request.user,
            open_datetime__gte=start_datetime,
            open_datetime__lte=end_datetime
        ).select_related('position_side', 'symbol',).only(
            'open_datetime', 'close_datetime', 'open_price', 'close_price', 'symbol__name', 'position_side__name',
            'realized_pnl', 'commission', 'net_profit',
        ).order_by('is_close', '-open_datetime')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trades_binance'] = context.pop('object_list')
        return context


class COINMView(LoginRequiredMixin, FormView, ListView):
    template_name = 'trades_info/trades_binance_list.html'
    form_class = DateRangeForm

    def get_initial(self):
        return {
            'start_date': str(self.request.GET.get('start_date', (
                    timezone.localdate().today() - timezone.timedelta(days=30)
            ))),
            'end_date': str(self.request.GET.get('end_date', timezone.localdate().today()))
        }

    def get_queryset(self):
        form = DateRangeForm(self.request.GET)

        if form.is_valid():
            start_date, end_date = form.cleaned_data['start_date'], form.cleaned_data['end_date']
            start_datetime = timezone.datetime.combine(start_date, timezone.datetime.min.time())
            end_datetime = timezone.datetime.combine(end_date, timezone.datetime.max.time())
        else:
            start_datetime = timezone.datetime.today() - timezone.timedelta(days=30)
            end_datetime = timezone.datetime.today()

        return TradeBinanceCOINM.objects.filter(
            user=self.request.user,
            open_datetime__gte=start_datetime,
            open_datetime__lte=end_datetime
        ).select_related('position_side', 'symbol',).only(
            'open_datetime', 'close_datetime', 'open_price', 'close_price', 'symbol__name', 'position_side__name',
            'realized_pnl', 'commission', 'net_profit',
        ).order_by('-open_datetime')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trades_binance'] = context.pop('object_list')
        return context
