import type { CorrelationResponse } from '@/types/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export const fetchCorrelations = async (): Promise<CorrelationResponse> => {
  const response = await fetch(`${API_BASE_URL}/correlations`);
  
  if (!response.ok) {
    throw new Error('Failed to fetch correlation data');
  }
  
  return response.json();
};

