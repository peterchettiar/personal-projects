from stocksymbol import StockSymbol
import yfinance as yf
from datetime import datetime, timedelta


class StockScreener:
    def __init__(self, api_key="4f61a805-aceb-485c-8af0-bfeab22c9069"):
        self.api_key = api_key
        self.symbol_list = []
        self.heavy_volume_stocks = []

    def get_stock_symbols(self, index=None, market=None) -> list[str]:
        stock_symbols = StockSymbol(self.api_key)

        if index is not None:
            self.symbol_list = stock_symbols.get_symbol_list(
                index=index, symbols_only=True
            )
        elif market is not None:
            self.symbol_list = stock_symbols.get_symbol_list(
                market=market, symbols_only=True
            )
        else:
            raise MissingArgumentException

        return self.symbol_list

    def get_heavy_volume_stocks(
        self,
        start_date=datetime.now() - timedelta(days=30),
        end_date=datetime.now(),
        frequency="1d",
    ) -> list[str]:
        tickers = yf.Tickers(self.symbol_list)

        tickers_volume = tickers.history(
            start=start_date, end=end_date, interval=frequency
        )["Volume"]

        for ticker in tickers_volume.columns:
            if tickers_volume[ticker].iloc[-1] > (1.5 * tickers_volume[ticker].mean()):
                self.heavy_volume_stocks.append(ticker)

        return list(set(self.heavy_volume_stocks))


class MissingArgumentException(Exception):
    def __init__(
        self,
        message="At least one positional argument is required - please provide either index or market code",
    ):
        super().__init__(message)
