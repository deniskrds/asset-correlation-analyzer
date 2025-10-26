from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import yfinance as yf

from server.config import settings
from server.utils.logger import setup_logger


class YahooFinanceClient:
    """Client for fetching financial data from Yahoo Finance API"""

    def __init__(self):
        self.assets = settings.asset_symbols
        self.data_dir = Path(settings.data_directory)
        self.logger = setup_logger('yahoo_finance_client')

    def save_to_csv(self, df: pd.DataFrame, filename: str) -> bool:
        success = True
        try:
            filepath = self.data_dir / filename
            df.to_csv(filepath, index=False)
            self.logger.info(f"Data saved to {filepath}")
        except Exception as e:
            self.logger.exception(f"Failed to save data to {filename}: {e}")
            success = False
        return success

    def fetch_asset_data(self, symbol: str, asset_name: str) -> pd.DataFrame:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=settings.data_fetch_years * 365)

        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start_date, end=end_date)

        if not df.empty:
            df = df.reset_index()
            df['symbol'] = symbol
            df['asset_name'] = asset_name
            df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'symbol', 'asset_name']]
            df.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'symbol', 'asset_name']
            self.logger.info(f"Successfully fetched {len(df)} data points for {asset_name}")
        else:
            self.logger.error(f"No data found for {asset_name} ({symbol})")

        return df

    def fetch_all_assets(self):
        for asset_name, symbol in self.assets.items():
            self.logger.info(f"Fetching data for {asset_name} ({symbol})")

            df = self.fetch_asset_data(symbol, asset_name)

            if not df.empty:
                filename = f"{symbol.replace('^', '').replace('=', '_').replace('.', '_')}.csv"
                success = self.save_to_csv(df, filename)
                if success:
                    self.logger.info(f"Data for {asset_name} saved successfully.")
                else:
                    self.logger.error(f"Failed to save data for {asset_name}.")


def main():
    yahoo_finance_client = YahooFinanceClient()
    yahoo_finance_client.logger.info("Starting data fetch for all assets")
    yahoo_finance_client.fetch_all_assets()


if __name__ == "__main__":
    main()
