import { useEffect, useState } from 'react';
import type { CorrelationResponse } from '@/types/api';
import { fetchCorrelations } from '@/services/api';

const CorrelationHeatmap = () => {
  const [data, setData] = useState<CorrelationResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadData = async () => {
      console.log('Loading correlation data...');
      try {
        const response = await fetchCorrelations();
        console.log('Data received:', response);
        setData(response);
      } catch (err) {
        console.error('Error loading data:', err);
        setError(err instanceof Error ? err.message : 'Failed to load data');
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-32">
        <div className="text-center">
          <div className="inline-block w-12 h-12 border-2 border-gray-900 border-t-transparent rounded-full animate-spin mb-4"></div>
          <p className="text-gray-400 text-sm tracking-wide">Loading</p>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="border border-gray-200 p-8 text-center">
        <p className="text-gray-900 font-medium mb-2">Unable to load data</p>
        <p className="text-gray-500 text-sm">{error}</p>
      </div>
    );
  }
  
  if (!data) {
    return null;
  }

  const matrix = data.assets.map(asset => 
    data.assets.map(asset2 => data.correlation_matrix[asset][asset2])
  );

  const getColor = (value: number) => {
    if (value >= 0.7) return 'rgb(34, 197, 94)'; // green-500
    if (value >= 0.4) return 'rgb(59, 130, 246)'; // blue-500
    if (value >= 0) return 'rgb(229, 231, 235)'; // gray-200
    if (value >= -0.4) return 'rgb(251, 146, 60)'; // orange-400
    return 'rgb(239, 68, 68)'; // red-500
  };

  return (
    <div className="space-y-12">
      <div className="flex justify-center">
        <div className="text-center">
          <p className="text-5xl font-light text-gray-900 mb-2">{data.data_points}</p>
          <p className="text-xs text-gray-400 uppercase tracking-widest">Data Points</p>
        </div>
      </div>

      <div className="border border-gray-200">
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr>
                <th className="border-b border-r border-gray-200 bg-white p-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider sticky left-0 z-10">
                  Asset
                </th>
                {data.assets.map(asset => (
                  <th 
                    key={asset} 
                    className="border-b border-gray-200 p-4 text-xs font-medium text-gray-500 uppercase tracking-wider min-w-[100px]"
                  >
                    <div className="flex items-center justify-center h-20">
                      <span className="transform -rotate-45 whitespace-nowrap">
                        {asset}
                      </span>
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.assets.map((asset, i) => (
                <tr key={asset}>
                  <td className="border-b border-r border-gray-200 bg-white p-4 text-xs font-medium text-gray-900 uppercase tracking-wider sticky left-0 z-10">
                    {asset}
                  </td>
                  {data.assets.map((asset2, j) => {
                    const value = matrix[i][j];
                    const bgColor = getColor(value);
                    const textColor = Math.abs(value) > 0.5 ? 'white' : 'black';
                    
                    return (
                      <td 
                        key={asset2} 
                        className="border-b border-gray-200 p-4 text-center transition-all duration-200 hover:scale-110 cursor-pointer"
                        style={{ 
                          backgroundColor: bgColor,
                          color: textColor
                        }}
                        title={`${asset} × ${asset2}: ${value.toFixed(3)}`}
                      >
                        <span className="text-xs font-mono">{value.toFixed(2)}</span>
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="flex justify-center gap-6 text-sm text-gray-600">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 bg-green-500 rounded"></div>
          <span>Strong Positive (≥0.7)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 bg-blue-500 rounded"></div>
          <span>Moderate (0.4-0.7)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 bg-gray-200 rounded border border-gray-300"></div>
          <span>Weak (0-0.4)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 bg-orange-400 rounded"></div>
          <span>Negative (-0.4-0)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 bg-red-500 rounded"></div>
          <span>Strong Negative (&lt;-0.4)</span>
        </div>
      </div>
    </div>
  );
};

export default CorrelationHeatmap;
