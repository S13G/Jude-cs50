from django.urls import path
from .views import portfolio, buy, sell, history, quotes

app_name = 'dashboard'
urlpatterns = [
    path('', portfolio,name='index'),
    path('buy', buy,name='buy'),
    path('sell', sell,name='sell'),
    path('history', history,name='history'),
    path('quotes', quotes,name='quotes'),
]