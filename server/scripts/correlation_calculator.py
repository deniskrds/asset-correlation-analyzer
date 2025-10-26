from functools import reduce
from pathlib import Path

import pandas as pd

from server.config import settings
from server.utils.logger import setup_logger


class CorrelationCalculator:
    """Calculate correlation matrix for financial assets"""

    def __init__(self):
        self.data_dir = Path(settings.data_directory)
        self.logger = setup_logger('correlation_calculator')

    def load_data(self) -> pd.DataFrame:
        all_data = []
        merged_df = pd.DataFrame()

        for asset_name in settings.asset_symbols.keys():
            filename = settings.asset_filenames[asset_name]
            filepath = self.data_dir / filename

            if filepath.exists():
                df = pd.read_csv(filepath)
                df['date'] = pd.to_datetime(df['date'], utc=True).dt.strftime('%Y-%m-%d')
                df = df[['date', 'close']].rename(columns={'close': asset_name})

                if len(df) >= 10:
                    self.logger.info(
                        f"Loaded {asset_name}: {len(df)} rows, dates: {df['date'].min()} to {df['date'].max()}")
                    all_data.append(df)
                else:
                    self.logger.warning(f"Skipping {asset_name}: only {len(df)} data points")
            else:
                self.logger.warning(f"File not found: {filepath}")

        if all_data:
            merged_df = reduce(lambda x, y: pd.merge(x, y, on='date', how='inner'), all_data)
            merged_df = merged_df.sort_values('date')
            self.logger.info(f"Loaded data for {len(merged_df.columns) - 1} assets with {len(merged_df)} data points")
        else:
            self.logger.error("No data files found")
        
        return merged_df

    def calculate_correlation(self, df: pd.DataFrame) -> pd.DataFrame:
        correlation_matrix = pd.DataFrame()

        if not df.empty:
            close_prices = df.drop('date', axis=1)
            correlation_matrix = close_prices.corr()
            self.logger.info("Correlation matrix calculated successfully")

        return correlation_matrix

    def run(self):
        self.logger.info("Starting correlation analysis")

        df = self.load_data()
        correlation_matrix = self.calculate_correlation(df)

        if not correlation_matrix.empty:
            output_path = self.data_dir / 'correlation_matrix.csv'
            correlation_matrix.to_csv(output_path)
            self.logger.info(f"Correlation matrix saved to {output_path}")

        self.logger.info("Correlation analysis complete")


def main():
    calculator = CorrelationCalculator()
    calculator.run()


if __name__ == "__main__":
    main()
