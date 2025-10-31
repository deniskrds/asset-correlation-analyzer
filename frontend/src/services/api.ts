import type { CorrelationResponse, BaseResponse } from '@/types/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export const fetchCorrelations = async (): Promise<CorrelationResponse> => {
  const response = await fetch(`${API_BASE_URL}/correlations`);
  
  if (!response.ok) {
    throw new Error('Failed to fetch correlation data');
  }
  
  const result: BaseResponse<CorrelationResponse> = await response.json();
    debugger;

  if (!result.success) {
    throw new Error(result.message || 'Failed to fetch correlation data');
  }
  
  if (!result.data) {
    throw new Error('No correlation data available');
  }
  debugger;
  
  return result.data;
};

