import datetime
from collections import defaultdict

from django.db.models import Sum, F

from core.models import UserSubscriberMapping, UserPayouts, UserPortfolio
from utility.common_utils import custom_response_obj

from datetime import  datetime, timedelta, date

class AdminHome:


    def get_admin_home(self):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        users_details=UserSubscriberMapping.objects.all()
        active_users=len(users_details.filter(is_active=True))
        users_joined_last_30_days=len(users_details.filter(paid_on__gte=start_date, paid_on__lte=end_date,is_active=True))

        payouts_done_last_30_days=UserPayouts.objects.filter(created_at__gte=start_date, created_at__lte=end_date).aggregate(payouts_done=Sum(F('payout_amount')))

        end_date = date(datetime.now().year, 12, 31)  # December 31st of current year
        start_date = date(datetime.now().year, 1, 1)  # January 1st of current year

        # Get portfolio data for current year
        portfolio_data = UserPortfolio.objects.filter(
            amount_added_on__gte=start_date,
            amount_added_on__lte=end_date
        ).values('amount_added_on', 'amount')

        # Initialize monthly data dictionary with all months
        monthly_data = defaultdict(float)
        for month in range(1, 13):
            monthly_data[month] = 0

        # Aggregate amounts by month
        for entry in portfolio_data:
            month = entry['amount_added_on'].month
            monthly_data[month] += entry['amount']

        # Format data for graph
        graph_data = [
            {
                'month': datetime(2024, month, 1).strftime('%b'),  # Full month name
                'amount': amount
            }
            for month, amount in monthly_data.items()
        ]
        results={'active_users':active_users,
                 'user_joined_30_days':users_joined_last_30_days,
                 'graph_data':graph_data,
                 'payouts_done_last_30_days':payouts_done_last_30_days}

        return custom_response_obj(data=results)