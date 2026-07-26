from django.urls import path

from e_commerce.users.views.admin_home import AdminHomeView
from e_commerce.users.views.login import LoginUserView
from e_commerce.users.views.registration import UserView
from e_commerce.users.views.reset_password import ResetPasswordView
from e_commerce.users.views.update_company_portfolio import UpdateCompanyPortfolioView
from e_commerce.users.views.user_details import UserDetailsView
from e_commerce.users.views.user_home import UserHomeView
from e_commerce.users.views.users_plans import UsersPlansView
from e_commerce.users.views.verify_user_registration import VerifyUserView

urlpatterns = [
    path('', UserView.as_view()),
    path('login', LoginUserView.as_view()),
    path('plans', UsersPlansView.as_view()),
    path('details', UserDetailsView.as_view()),
    path('home',UserHomeView.as_view()),
    path('admin-home', AdminHomeView.as_view()),
    path('reset/password',ResetPasswordView.as_view()),
    path('verify', VerifyUserView.as_view()),
    path('company/portfolio',UpdateCompanyPortfolioView.as_view())
]