import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import StockLevels from '../StockLevels';

global.fetch = jest.fn();

describe('StockLevels Component', () => {
  it('renders stock data correctly', async () => {
    // Arrange
    const mockData = [
      { blood_type: 'A-', status: 'Stable', last_updated: '2026-04-30T14:15:28Z' },
      { blood_type: 'O-', status: 'Critical', last_updated: '2026-04-30T14:15:28Z' },
      { blood_type: 'AB-', status: 'Alert', last_updated: '2026-04-30T14:15:28Z' }
    ];
    
    fetch.mockResolvedValueOnce({
      json: async () => mockData,
    });

    // Act
    render(<StockLevels />);

    // Assert
    await waitFor(() => {
      expect(screen.getByText('A-')).toBeInTheDocument();
      expect(screen.getByText('O-')).toBeInTheDocument();
      expect(screen.getByText('AB-')).toBeInTheDocument();
    });
    
    expect(screen.getByText('ESTÁVEL')).toBeInTheDocument();
    expect(screen.getByText('CRÍTICO')).toBeInTheDocument();
    expect(screen.getByText('BAIXO')).toBeInTheDocument();
  });
});
