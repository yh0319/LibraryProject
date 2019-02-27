import json
from django.db.models import Avg
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views import generic
from .models import loan, recommendations, members

class LoanListView(LoginRequiredMixin, ListView):
    model = loan
    template_name = 'mypage/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(LoanListView, self).get_context_data(*args, **kwargs)
        # 평점순위 Top5
        context['top_rates'] = loan.objects.filter(id_id = self.request.user.username).order_by('-rate')[:5]
        # 나의 도서 이력
        context['read_books'] = loan.objects.filter(id_id = self.request.user.username)
        # 내가 읽은 도서 총 권수
        context['num_of_read_books'] = loan.objects.filter(id_id = self.request.user.username).count()
        # 나의 평점 분포
        raw_rates = loan.objects.filter(id_id = self.request.user.username).values_list('bName', 'rate')
        rNames = []
        rRates = []
        for key, value in raw_rates:
            rNames.append(key)
            rRates.append(float(value))
        context['bName_list'] = rNames
        # context['bName_list'] = [rNames]
        context['rate_list'] = rRates
        # context['rate_list'] = [rRates]
        # context['rates'] = [[rNames],[rRates]]
        # 나의 평균 평점
        context['avg_rate'] = loan.objects.filter(id_id = self.request.user.username).aggregate(Avg('rate'))
        # 추천 도서 목록
        context['rec_list'] = recommendations.objects.filter(id_id = self.request.user.username)
        context['word_cloud'] = members.objects.filter(id = self.request.user.username)

        return context