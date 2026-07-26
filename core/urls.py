from django.urls import path

from core.views.referral_payouts import ReferralPayoutsView
from core.views.stock_view import TrendingStocksView, StockSearchView, StockPriceView, QuickPricesView
from core.views.upload_sub_file import UploadSubFileView
from core.views.user_payouts import UserPayoutsView
from core.views.user_portfolio_view import UserPortfolioServiceView
from core.views.subscription_service import SubscriptionServiceView
from core.views.user_subscripe_plan import UserSubscriptionView
from core.views.user_withdrawals import UserWithdrawalView

urlpatterns = [
    path('subscription', SubscriptionServiceView.as_view()),
    path('subscription-mapping',  UserSubscriptionView.as_view()),
    path('user-portfolio',  UserPortfolioServiceView.as_view()),
    path('user-withdrawal',UserWithdrawalView.as_view()),
    path('user-payouts',UserPayoutsView.as_view()),
    path('referral-payouts', ReferralPayoutsView.as_view()),
    path('upload-sub-background', UploadSubFileView.as_view()),
    path('trending/', TrendingStocksView.as_view(), name='trending-stocks'),
    path('search/', StockSearchView.as_view(), name='search-stocks'),
    path('price/<str:symbol>/', StockPriceView.as_view(), name='stock-price'),
    path('quick-prices/', QuickPricesView.as_view(), name='quick-prices'),
]