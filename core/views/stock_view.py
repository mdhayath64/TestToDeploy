# core/views/stock_views.py
from rest_framework.views import APIView
from core.service.stock_service import StockService
from utility.api_framework import ApiFramework

class TrendingStocksView(APIView, ApiFramework):
    serializer = None

    def process(self):
        service = StockService()
        return service.get_trending_items()

    def get(self, request):
        self.method = 'GET'
        return self.main()

class StockSearchView(APIView, ApiFramework):
    serializer = None

    def process(self):
        service = StockService()
        query = self.request.GET.get('q', '')
        return service.search_stocks(query)

    def get(self, request):
        self.method = 'GET'
        self.request = request
        return self.main()

class StockPriceView(APIView, ApiFramework):
    serializer = None

    def process(self):
        service = StockService()
        symbol = self.kwargs.get('symbol')
        return service.get_stock_price(symbol)

    def get(self, request, symbol):
        self.method = 'GET'
        self.kwargs = {'symbol': symbol}
        return self.main()


class QuickPricesView(APIView, ApiFramework):
    serializer = None

    def process(self):
        service = StockService()
        return service.get_quick_prices()

    def get(self, request):
        self.method = 'GET'
        return self.main()