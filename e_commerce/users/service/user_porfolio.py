from collections import defaultdict

from django.db.models import F, Sum
from dateutil import parser as parser
from datetime import  datetime, timedelta
from core.models import UserSubscriberMapping, UserPortfolio
from e_commerce.models import AdminCompanyPortfolio

from utility.common_utils import custom_response_obj


class UserPortfolioService:


    def portfolio_details(self, user_id):
        user = UserSubscriberMapping.objects.filter(
            user__id=user_id,
            is_active=True
        ).values('last_payout_done','subscription_plan__price','amount').annotate(

            name=F('subscription_plan__name'),
            price=F('subscription_plan__price'),
            description=F('subscription_plan__description'),
            sub_icon=F('subscription_plan__sub_icon'),
            subscription_plan=F('subscription_plan__plan_id'),

        ).order_by('-last_payout_done')



        plans = {x['subscription_plan']: x['last_payout_done'] for x in user}
        portfolio_details = UserPortfolio.objects.filter(
            user__id=user_id,
            subscription_plan__in=list(plans.keys())
        )

        total_invested = sum([x['amount'] for x in user])

        trades_performed = 0
        earnings = 0

        # Get current year's start and end dates
        current_year = datetime.now().year
        start_date = datetime(current_year, 1, 1)
        end_date = datetime(current_year, 12, 31, 23, 59, 59)

        # Get portfolio data for current year
        portfolio_data = UserPortfolio.objects.filter(
            user__id=user_id,
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

        trade_details=defaultdict(list)
        for i in portfolio_details:
            if plans[i.subscription_plan.plan_id] is None or (
                    parser.parse(str(plans[i.subscription_plan.plan_id])).date() >=
                    parser.parse(str(i.amount_added_on)).date()
            ):
                earnings += i.amount
                trade_details[str(i.amount_added_on)].append(i.amount)

            trades_performed += 1
        company_portfolio=list(AdminCompanyPortfolio.objects.all().values())
        if len(company_portfolio)>=1:
            company_portfolio=company_portfolio[0]

        holdings=list(UserSubscriberMapping.objects.filter(
            user__id=user_id,
            is_active=True
        ).values('subscription_plan__price', 'amount').annotate(
            name=F('subscription_plan__name'),
            price=F('subscription_plan__price'),
            description=F('subscription_plan__description'),
            sub_icon=F('subscription_plan__sub_icon'),
            subscription_plan=F('subscription_plan__plan_id'),

        ))
        results = {
            'portfolio': round(float(total_invested) + float(earnings),2),
            'earnings': earnings,
            'invested':total_invested,
            'earnings_in_percentage':earnings / total_invested * 100 if earnings>0 and total_invested>0 else 0,
            'trades_performed': trades_performed,
            'trades_details':trade_details,
            'graph': graph_data,
            'company_portfolio':company_portfolio,
            'current_holdings':holdings
        }
        return custom_response_obj(data=results, code=200)


