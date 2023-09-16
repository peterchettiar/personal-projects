from stocksymbol import StockSymbol
import yfinance as yf


class StockScreener:
    def __init__(self, api_key="4f61a805-aceb-485c-8af0-bfeab22c9069"):
        self.api_key = api_key

    def stock_symbols(self, index=None, market=None):
        stock_symbol = StockSymbol(self.api_key)

        if index is not None:
            symbol_list = stock_symbol.get_symbol_list(index=index, symbols_only=True)
        elif market is not None:
            symbol_list = stock_symbol.get_symbol_list(market=market, symbols_only=True)
        else:
            raise MissingArgumentException

        return symbol_list


class MissingArgumentException(Exception):
    def __init__(
        self,
        message="At least one positional argument is required - please provide either index or market",
    ):
        super().__init__(message)
