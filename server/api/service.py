from pathlib import Path

import pandas as pd

from server.api.models import CorrelationResponse, BaseResponse
from server.config import settings
from server.utils.logger import setup_logger

logger = setup_logger('correlation_service')


def get_correlation_matrix() -> BaseResponse[CorrelationResponse]:
    try:
        data_dir = Path(settings.data_directory)
        correlation_file = data_dir / 'correlation_matrix.csv'

        if not correlation_file.exists():
            logger.error("Correlation matrix file not found")
            return BaseResponse(
                success=False,
                message="Correlation matrix not found. Please run the correlation calculator first.",
                status_code=404
            )

        df = pd.read_csv(correlation_file, index_col=0)

        response_data = CorrelationResponse(
            correlation_matrix=df.to_dict(),
            assets=list(df.columns),
            data_points=len(df)
        )

        return BaseResponse(
            success=True,
            data=response_data,
            message="Correlation matrix retrieved successfully",
            status_code=200
        )

    except Exception as e:
        logger.exception("Error reading correlation matrix")
        return BaseResponse(
            success=False,
            message="Failed to retrieve correlation matrix",
            status_code=500
        )
