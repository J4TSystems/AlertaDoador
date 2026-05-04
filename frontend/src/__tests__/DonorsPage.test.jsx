import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import DonorsPage from '../pages/DonorsPage';

global.fetch = jest.fn();

describe('DonorsPage Component', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  it('loads donors and populates form when edit is clicked', async () => {
    // Arrange
    const mockDonors = [
      { id: 2, full_name: 'Teste2', email: 'teste2@gmail.com', blood_type: 'A+' }
    ];
    
    fetch.mockResolvedValueOnce({
      json: async () => mockDonors,
    });

    render(<DonorsPage />);

    // Act
    await waitFor(() => {
      expect(screen.getByText('Teste2')).toBeInTheDocument();
    });

    const editButton = screen.getByLabelText('Edit');
    fireEvent.click(editButton);

    // Assert
    const nameInput = screen.getByDisplayValue('Teste2');
    const emailInput = screen.getByDisplayValue('teste2@gmail.com');
    const updateButton = screen.getByText('Atualizar Doador');
    
    expect(nameInput).toBeInTheDocument();
    expect(emailInput).toBeInTheDocument();
    expect(updateButton).toBeInTheDocument();
  });

  it('submits a new donor successfully', async () => {
    // Arrange
    fetch
      .mockResolvedValueOnce({ json: async () => [] })
      .mockResolvedValueOnce({ ok: true }) 
      .mockResolvedValueOnce({ json: async () => [] }); 

    render(<DonorsPage />);
    
    await waitFor(() => {
      expect(screen.getByText('Nenhum doador cadastrado.')).toBeInTheDocument();
    });

    const nameInput = screen.getByLabelText(/Nome Completo/i);
    const emailInput = screen.getByLabelText(/E-mail/i);
    const submitButton = screen.getByText('Cadastrar no AlertaDoar');

    // Act
    fireEvent.change(nameInput, { target: { value: 'New Donor' } });
    fireEvent.change(emailInput, { target: { value: 'new@donor.com' } });
    fireEvent.click(submitButton);

    // Assert
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/donors/', expect.objectContaining({
        method: 'POST',
        body: expect.stringContaining('New Donor'),
      }));
    });
  });
});
