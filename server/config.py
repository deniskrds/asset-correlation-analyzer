from typing import Dict

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )

    data_fetch_years: int = 2
    data_directory: str

    asset_symbols: Dict[str, str] = {
        'S&P 500': '^GSPC',
        'NASDAQ': '^IXIC',
        'FTSE 100': '^FTSE',
        'US 10-Year Treasury': '^TNX',
        'Corporate Bonds': 'FP74.MU',
        'Gold': 'GC=F',
        'Crude Oil': 'CL=F',
        'US Dollar Index': 'DX-Y.NYB',
        'Bitcoin': 'BTC-USD'
    }
    
    asset_filenames: Dict[str, str] = {
        'S&P 500': 'GSPC.csv',
        'NASDAQ': 'IXIC.csv',
        'FTSE 100': 'FTSE.csv',
        'US 10-Year Treasury': 'TNX.csv',
        'Corporate Bonds': 'FP74_MU.csv',
        'Gold': 'GC_F.csv',
        'Crude Oil': 'CL_F.csv',
        'US Dollar Index': 'DX-Y_NYB.csv',
        'Bitcoin': 'BTC-USD.csv'
    }


settings = Settings()
