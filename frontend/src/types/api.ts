export interface CorrelationResponse {
  correlation_matrix: Record<string, Record<string, number>>;
  assets: string[];
  data_points: number;
}

export interface BaseResponse<T = unknown> {
  success: boolean;
  data: T | null;
  message: string;
  status_code: number;
  timestamp: string;
}

