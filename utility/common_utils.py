import calendar
import datetime


def custom_response_obj(data=None,code=200,message=None , **kwargs):
    resp_status='success' if code==200 or code==201 or code==204 else 'error'
    resp={'status': resp_status, 'message':message,'data': data, 'status_code': code}
    if len(kwargs)>0:
        resp.update(**kwargs)
    return resp

def serializer_instance(serializer_instance,read_only=False,**kwargs):

    if read_only:
        data=kwargs.get('data')
        many=kwargs.get('many', False)
        serializer = serializer_instance(data, many=many)
        return custom_response_obj(data=serializer.data, code=200, message='data retrieved')
    else:
        serializer = serializer_instance(**kwargs)
        if serializer.is_valid():
            serializer.save()
            return custom_response_obj(data=serializer.data, code=200, message='success')
        is_many=kwargs.get('many',False)
        if not is_many:
            error= normalize_serializer_error(serializer.errors.items())
        else:
            error=serializer.errors
            print(error)
        return custom_response_obj(data=error, code=400, message='bad request')

def normalize_serializer_error(data):
    return {k: ','.join([str(j) for j in v]) for k, v in data}

def divide_into_batches(lst, batch_size):
    num_batches = len(lst) // batch_size
    batches = {}

    for i in range(num_batches):
        start = i * batch_size
        end = start + batch_size
        batch = lst[start:end]
        batches[i + 1] = batch

    if len(lst) % batch_size != 0:
        remaining = lst[num_batches * batch_size:]
        batches[num_batches + 1] = remaining

    return batches

def total_days_in_a_month():
    # Get the current month and year
    current_month = calendar.month_name[datetime.datetime.now().month]
    current_year = datetime.datetime.now().year

    # Get the total number of days in the current month
    total_days = calendar.monthrange(current_year, datetime.datetime.now().month)[1]
    return total_days

def get_next_generation_date(due_date):
    # Calculate the interest per day using ExpressionWrapper
    one_month_later = due_date.replace(month=due_date.month + 1)
    # Subtract one day
    result_date = one_month_later - datetime.timedelta(days=1)
    return result_date

def get_days_difference(due_date):
    todays=datetime.datetime.today().date()
    delta = todays - due_date
    # Extract the number of days from the difference
    days_difference = delta.days
    return days_difference

def calculate_apr(loan_amount, interest_rate, loan_term, fees):
    # Calculate the monthly interest rate
    monthly_interest_rate = interest_rate / 12 / 100

    # Calculate the total number of payments
    total_payments = loan_term * 12

    # Calculate the monthly payment
    monthly_payment = loan_amount * (monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** -total_payments))

    # Calculate the total cost of the loan
    total_cost = monthly_payment * total_payments + fees

    # Calculate the APR
    apr = (total_cost / loan_amount) * 100

    return apr



def make_query_options(filter_asked, query_options):
    query_options={i:filter_asked.get(i) for i in query_options if filter_asked.get(i) is not None }
    return query_options

