import pandas as pd
from stocksymbol import StockSymbol
import yfinance as yf
from datetime import datetime, timedelta


class StockScreener:
    def __init__(self, api_key):
        self.api_key = api_key
        self.stock_symbols = StockSymbol(self.api_key)

    def get_stock_symbols(self, index=None, market=None, symbols_only=True) -> [str]:
        symbol_list = self.stock_symbols.get_symbol_list(
            index=index, market=market, symbols_only=symbols_only
        )
        return symbol_list

    def get_heavy_volume_stocks(
        self,
        symbol_list,
        multiplier=1.5,
        start_date=datetime.now() - timedelta(days=30),
        end_date=datetime.now(),
        frequency="1d",
        batch_size=1000,
    ) -> [str]:
        batches = list(self.batch(symbol_list, batch_size))
        print(f"Number of symbols: {len(symbol_list)}")
        print(f"Number of batches: {len(batches)}")

        res = []
        for batch_num, symbol_batch in enumerate(batches):
            print(f"Start batch: {batch_num}")

            batch_res = self._get_heavy_volume_stocks(
                symbol_list=symbol_batch,
                multiplier=multiplier,
                start_date=start_date,
                end_date=end_date,
                frequency=frequency,
            )

            res.extend(batch_res)

            print(f"Finish batch: {batch_num}")

        return res

    def _get_heavy_volume_stocks(
        self,
        symbol_list,
        multiplier,
        start_date,
        end_date,
        frequency,
    ) -> [str]:
        tickers = yf.Tickers(symbol_list)

        tickers_volume = tickers.history(
            start=start_date,
            end=end_date,
            interval=frequency,
        )["Volume"]

        threshold = multiplier * tickers_volume.mean()

        res = [
            ticker
            for ticker in tickers_volume.columns
            if tickers_volume[ticker].iloc[-1] > threshold.loc[ticker]
        ]

        return res

    def dmi_screener(
        self,
        symbol_list,
        period="1mo",
        lookback_period=14,
        threshold=25,
        batch_size=1000,
        return_dataframe=False,
    ) -> [str]:
        batches = list(self.batch(symbol_list, batch_size))
        print(f"Number of symbols: {len(symbol_list)}")
        print(f"Number of batches: {len(batches)}")

        res = []
        for batch_num, symbol_batch in enumerate(batches):
            print(f"Start batch: {batch_num}")

            batch_res = self._dmi_screener(
                symbol_list=symbol_batch,
                period=period,
                lookback_period=lookback_period,
                threshold=threshold,
                return_dataframe=return_dataframe,
            )

            print(f"Finish batch: {batch_num}")

        if return_dataframe:
            res.append(batch_res)

            return pd.concat(res, axis=0)

        else:
            res.extend(batch_res)

            return res

    def _dmi_screener(
        self,
        symbol_list,
        period,
        lookback_period,
        threshold,
        return_dataframe,
    ) -> [str]:
        tickers_obj = yf.Tickers(symbol_list)
        tickers_hist = tickers_obj.history(period=period)
        res = []
        shortlisted_symbols = []

        for ticker in symbol_list:
            stock = tickers_hist.xs(ticker, level=1, axis=1)
            atr_di_adx_df = StockScreener._atr_di_adx(
                stock,
                lookback_period=lookback_period,
            )

            atr_di_adx_df["signal"] = atr_di_adx_df[
                ["plus_di", "minus_di", "adx_smooth"]
            ].apply(
                lambda x: True if (x[0] > x[1]) and (x[2] > threshold) else False,
                axis=1,
            )

            atr_di_adx_df["ticker"] = ticker
            res.append(atr_di_adx_df)

            if atr_di_adx_df.dropna()["signal"].all() == True:
                shortlisted_symbols.append(ticker)

        if return_dataframe:
            all_tickers = pd.concat(res, axis=0)
            return all_tickers

        return shortlisted_symbols

    @staticmethod
    def _atr_di_adx(df: pd.DataFrame(), lookback_period) -> pd.DataFrame():
        tmp = df.copy()

        tmp["previous_close"] = tmp["Close"].shift(1)

        true_range = tmp[["previous_close", "High", "Low"]].apply(
            lambda x: max((x[1] - x[2]), (x[1] - x[0]), (x[0] - x[2])),
            axis=1,
        )

        tmp["average_true_range"] = true_range.rolling(window=lookback_period).mean()

        tmp["positive_dm"] = tmp["High"] - tmp["High"].shift(1)
        tmp["negative_dm"] = tmp["Low"].shift(1) - tmp["Low"]

        tmp["positive_dm"] = tmp[["positive_dm", "negative_dm"]].apply(
            lambda x: x[0] if (x[0] > x[1]) and (x[0] > 0) else 0,
            axis=1,
        )

        tmp["negative_dm"] = tmp[["positive_dm", "negative_dm"]].apply(
            lambda x: x[1] if (x[1] > x[0]) and (x[1] > 0) else 0,
            axis=1,
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

        plus_di_df = pd.DataFrame(plus_di, columns=["plus_di"]).reset_index()
        minus_di_df = pd.DataFrame(minus_di, columns=["minus_di"]).reset_index()
        adx_smooth_df = pd.DataFrame(adx_smooth, columns=["adx_smooth"]).reset_index()

        res = pd.concat(
            [
                plus_di_df,
                minus_di_df.drop(columns=["Date"]),
                adx_smooth_df.drop(columns=["Date"]),
            ],
            axis=1,
        )

        return res

    def batch(self, iterable, n):
        l = len(iterable)
        for ndx in range(0, l, n):
            yield iterable[ndx : min(ndx + n, l)]
