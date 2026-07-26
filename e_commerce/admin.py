from django.contrib import admin


from django.contrib.auth.admin import UserAdmin
from e_commerce.models import User, AdminCompanyPortfolio


@admin.register(User)
class UserAdmin(UserAdmin):

    list_display = ('username','phone',)
    search_fields = ['username','phone',]

    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': ('phone','user_consent','subscription_done','referral_code', 'referred_by','wallet_id','subscription_payment_update')
        }),

    )




@admin.register(AdminCompanyPortfolio)
class AdminCompanyPortfolioAdmin(admin.ModelAdmin):
    list_display = ('invested','change','trade_performed')