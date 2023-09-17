import pandas as pd
from stocksymbol import StockSymbol
import yfinance as yf
from datetime import datetime, timedelta


class StockScreener:
    def __init__(self, api_key="4f61a805-aceb-485c-8af0-bfeab22c9069"):
        self.api_key = api_key
        self.symbol_list = []
        self.heavy_volume_stocks = []
        self.dmi_screener_stocks = []

    def get_stock_symbols(self, index=None, market=None) -> [str]:
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
    ) -> [str]:
        tickers = yf.Tickers(self.symbol_list)

        tickers_volume = tickers.history(
            start=start_date, end=end_date, interval=frequency
        )["Volume"]

        for ticker in tickers_volume.columns:
            if tickers_volume[ticker].iloc[-1] > (1.5 * tickers_volume[ticker].mean()):
                self.heavy_volume_stocks.append(ticker)

        return list(set(self.heavy_volume_stocks))

    def dmi_screener(self, period="1m") -> [str]:
        tickers_obj = yf.Tickers(self.heavy_volume_stocks)

        tickers_hist = tickers_obj.history(period=period)

        for ticker in self.heavy_volume_stocks:
            stock = tickers_hist.loc(axis=1)[
                :, tickers_hist.columns.get_level_values(1) == ticker
            ]

            stock = stock.droplevel(level=1, axis=1)

            metrics_df = pd.concat(self._atr_di_adx(stock), axis=1)
            metrics_df.rename(
                columns={0: "plus_di", 1: "minus_di", 2: "adx_smooth"}, inplace=True
            )
            stock = pd.merge(stock, metrics_df, left_index=True, right_index=True)
            stock["signal"] = stock[["plus_di", "minus_di", "adx_smooth"]].apply(
                lambda x: True if (x[0] > x[1]) and (x[2] > 25) else False, axis=1
            )

            if stock["signal"].iloc[-5:].all() == True:
                self.dmi_screener_stocks.append(ticker)
            else:
                pass

        return self.dmi_screener_stocks

    def _atr_di_adx(self, df: pd.DataFrame(), lookback_period=14) -> pd.Series():
        tmp = df.copy()

        tmp["previous_close"] = tmp["Close"].shift(1)

        true_range = tmp[["previous_close", "High", "Low"]].apply(
            lambda x: max((x[1] - x[2]), (x[1] - x[0]), (x[0] - x[2])), axis=1
        )

        tmp["average_true_range"] = true_range.rolling(window=lookback_period).mean()

        tmp["positive_dm"] = tmp["High"] - tmp["High"].shift(1)
        tmp["negative_dm"] = tmp["Low"].shift(1) - tmp["Low"]

        tmp["positive_dm"] = tmp[["positive_dm", "negative_dm"]].apply(
            lambda x: x[0] if (x[0] > x[1]) and (x[0] > 0) else 0, axis=1
        )
        tmp["negative_dm"] = tmp[["positive_dm", "negative_dm"]].apply(
            lambda x: x[1] if (x[1] > x[0]) and (x[1] > 0) else 0, axis=1
        )

        plus_di = 100 * (
            tmp["positive_dm"].ewm(alpha=1 / lookback_period).mean()
            / tmp["average_true_range"]
        )
        minus_di = abs(
            100
            * (
                tmp["negative_dm"].ewm(alpha=1 / lookback_period).mean()
                / tmp["average_true_range"]
            )
        )

        dx = (abs(plus_di - minus_di) / abs(plus_di + minus_di)) * 100
        adx = ((dx.shift(1) * (lookback_period - 1)) + dx) / lookback_period
        adx_smooth = adx.ewm(alpha=1 / lookback_period).mean()

        return plus_di, minus_di, adx_smooth


class MissingArgumentException(Exception):
    def __init__(
        self,
        message="At least one positional argument is required - please provide either index or market code",
    ):
        super().__init__(message)
