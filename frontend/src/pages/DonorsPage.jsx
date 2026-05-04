import { useState, useEffect } from 'react';
import DonorForm from '../components/DonorForm';
import DonorList from '../components/DonorList';

export default function DonorsPage() {
  const [donors, setDonors] = useState([]);
  const [editingDonor, setEditingDonor] = useState(null);

  const fetchDonors = async () => {
    try {
      const response = await fetch('http://localhost:8000/donors/');
      const data = await response.json();
      setDonors(data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchDonors();
  }, []);

  const handleSave = async (donorData) => {
    try {
      const isEditing = !!donorData.id;
      const url = isEditing 
        ? `http://localhost:8000/donors/${donorData.id}` 
        : 'http://localhost:8000/donors/';
      const method = isEditing ? 'PUT' : 'POST';

      await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          full_name: donorData.full_name,
          email: donorData.email,
          blood_type: donorData.blood_type,
        }),
      });

      setEditingDonor(null);
      fetchDonors();
    } catch (error) {
      console.error(error);
    }
  };

  const handleDelete = async (id) => {
    try {
      await fetch(`http://localhost:8000/donors/${id}`, {
        method: 'DELETE',
      });
      fetchDonors();
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <DonorForm 
        initialData={editingDonor} 
        onSubmit={handleSave} 
        onCancel={() => setEditingDonor(null)} 
      />
      <DonorList 
        donors={donors} 
        onEdit={setEditingDonor} 
        onDelete={handleDelete} 
      />
    </div>
  );
}
