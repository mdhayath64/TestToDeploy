# core/service/stock_service.py
import yfinance as yf
from utility.common_utils import custom_response_obj


class StockService:
    def __init__(self):
        self.trending_symbols = [
            # Cryptocurrencies (Top 25)
            'BTC-USD', 'ETH-USD', 'USDT-USD', 'BNB-USD', 'XRP-USD',
            'USDC-USD', 'SOL-USD', 'ADA-USD', 'DOGE-USD', 'TRX-USD',
            'DOT-USD', 'MATIC-USD', 'DAI-USD', 'LTC-USD', 'BCH-USD',
            'SHIB-USD', 'LINK-USD', 'ATOM-USD', 'UNI-USD', 'XLM-USD',
            'AVAX-USD', 'XMR-USD', 'ALGO-USD', 'ICP-USD', 'OP-USD'
        ]

    def get_trending_items(self):
        try:
            results = []
            for symbol in self.trending_symbols:
                try:
                    stock = yf.Ticker(symbol)
                    info = stock.info
                    history = stock.history(period='1d', interval='1m')

                    if not history.empty:
                        current_price = history['Close'].iloc[-1]
                        open_price = history['Open'].iloc[0]
                        price_change = ((current_price - open_price) / open_price) * 100
                    else:
                        current_price = None
                        price_change = None

                    results.append({
                        'symbol': symbol,
                        'name': info.get('longName', info.get('shortName', symbol)),
                        'type': 'crypto' if '-USD' in symbol else 'stock',
                        'price': current_price,
                        'change': price_change,
                        'market_cap': info.get('marketCap'),
                        'volume': info.get('volume')
                    })
                except Exception as e:
                    print(f"Error fetching data for {symbol}: {str(e)}")
                    continue

            return custom_response_obj(
                data={'finance': {'result': [{'quotes': results}]}},
                message="Successfully fetched trending items",
                code=200
            )
        except Exception as e:
            return custom_response_obj(
                message=f"Failed to fetch trending items: {str(e)}",
                code=400
            )

    def search_stocks(self, query):
        try:
            if not query or len(query) < 2:
                return custom_response_obj(
                    data={'quotes': []},
                    message="Query too short",
                    code=200
                )

            tickers = yf.Tickers(query)
            results = []

            for symbol in query.split():
                try:
                    ticker = getattr(tickers, symbol)
                    info = ticker.info
                    results.append({
                        'symbol': symbol,
                        'shortname': info.get('longName', info.get('shortName', symbol)),
                        'quoteType': 'crypto' if '-USD' in symbol else 'stock',
                        'exchange': info.get('exchange', '')
                    })
                except:
                    continue

            return custom_response_obj(
                data={'quotes': results},
                message="Successfully searched stocks",
                code=200
            )
        except Exception as e:
            return custom_response_obj(
                message=f"Failed to search stocks: {str(e)}",
                code=400
            )

    def get_stock_price(self, symbol):
        try:
            stock = yf.Ticker(symbol)
            history = stock.history(period='1d', interval='1m')

            if not history.empty:
                current_price = history['Close'].iloc[-1]
                open_price = history['Open'].iloc[0]
                price_change = ((current_price - open_price) / open_price) * 100

                data = {
                    'chart': {
                        'result': [{
                            'indicators': {
                                'quote': [{
                                    'close': [float(current_price)],
                                    'open': [float(open_price)]
                                }]
                            }
                        }]
                    }
                }

                return custom_response_obj(
                    data=data,
                    message="Successfully fetched stock price",
                    code=200
                )
            else:
                return custom_response_obj(
                    message="No price data available",
                    code=404
                )
        except Exception as e:
            return custom_response_obj(
                message=f"Failed to fetch stock price: {str(e)}",
                code=400
            )

    def get_quick_prices(self):
        try:
            results = {}
            self.default_symbols = {
                'AAPL': 'Apple Inc.',
                'BTC-USD': 'Bitcoin',
                'ETH-USD': 'Ethereum'
            }
            for symbol, name in self.default_symbols.items():
                try:
                    stock = yf.Ticker(symbol)
                    history = stock.history(period='1d', interval='1m')

                    if not history.empty:
                        current_price = history['Close'].iloc[-1]
                        open_price = history['Open'].iloc[0]
                        price_change = ((current_price - open_price) / open_price) * 100

                        # Store with clean symbol (without -USD)
                        clean_symbol = symbol.replace('-USD', '')
                        results[clean_symbol] = {
                            'price': float(current_price),
                            'change': float(price_change)
                        }
                except Exception as e:
                    print(f"Error fetching data for {symbol}: {str(e)}")
                    # Initialize with zeros if fetch fails
                    clean_symbol = symbol.replace('-USD', '')
                    results[clean_symbol] = {
                        'price': 0,
                        'change': 0
                    }

            return custom_response_obj(
                data={'chart': {
                    'result': [{
                        'prices': results
                    }]
                }},
                message="Successfully fetched quick prices",
                code=200
            )
        except Exception as e:
            return custom_response_obj(
                message=f"Failed to fetch quick prices: {str(e)}",
                code=400
            )