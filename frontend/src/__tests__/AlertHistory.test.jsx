import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import AlertHistory from '../AlertHistory';

global.fetch = jest.fn();

describe('AlertHistory Component', () => {
  it('renders history data correctly', async () => {
    const mockData = [
      {
        id: 'fd3728f1-f533-441a-a5a2-375817554a86',
        recipient_email: 'MaricelaJSellner@armyspy.com',
        blood_type: 'O-',
        status_at_time: 'Critical',
        sent_at: '2026-05-04T18:51:21.967685Z'
      },
      {
        id: '63a25b81-9cb4-4ea2-ab2d-a012d4146946',
        recipient_email: 'JamesMEldridge@armyspy.com',
        blood_type: 'AB-',
        status_at_time: 'Alert',
        sent_at: '2026-05-04T18:51:21.984271Z'
      }
    ];
    
    fetch.mockResolvedValueOnce({
      json: async () => mockData,
    });

    render(<AlertHistory />);

    await waitFor(() => {
      expect(screen.getByText('Maricel****Sellner@armyspy.com')).toBeInTheDocument();
      expect(screen.getByText('JamesM****ldridge@armyspy.com')).toBeInTheDocument();
    });
    
    expect(screen.getByText('O-')).toBeInTheDocument();
    expect(screen.getByText('AB-')).toBeInTheDocument();
    expect(screen.getByText('Crítico')).toBeInTheDocument();
    expect(screen.getByText('Alerta')).toBeInTheDocument();
  });
});
