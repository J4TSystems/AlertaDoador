import { useState, useEffect } from 'react';

export default function DonorForm({ initialData, onSubmit, onCancel }) {
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    blood_type: 'A+',
  });

  useEffect(() => {
    if (initialData) {
      setFormData(initialData);
    } else {
      setFormData({ full_name: '', email: '', blood_type: 'A+' });
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
    if (!initialData) {
      setFormData({ full_name: '', email: '', blood_type: 'A+' });
    }
  };

  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm mb-8">
      <h3 className="text-xl font-bold text-slate-900 mb-2 flex items-center gap-2">
        💛 {initialData ? 'Edição de Doador' : 'Adição Rápida de Doador'}
      </h3>
      <p className="text-slate-600 mb-6 text-sm">
        Receba alertas de emergência quando o seu tipo sanguíneo estiver em baixas.
      </p>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-semibold text-slate-700 mb-1">
            Nome Completo:
          </label>
          <input
            type="text"
            name="full_name"
            value={formData.full_name}
            onChange={handleChange}
            required
            className="w-full border border-slate-300 rounded-lg p-2 focus:ring-2 focus:ring-red-500 focus:outline-none"
          />
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
           <div>
              <label className="block text-sm font-semibold text-slate-700 mb-1">
                E-mail:
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                className="w-full border border-slate-300 rounded-lg p-2 focus:ring-2 focus:ring-red-500 focus:outline-none"
              />
           </div>
           <div>
              <label className="block text-sm font-semibold text-slate-700 mb-1">
                Tipo Sanguíneo:
              </label>
              <select
                name="blood_type"
                value={formData.blood_type}
                onChange={handleChange}
                className="w-full border border-slate-300 rounded-lg p-2 focus:ring-2 focus:ring-red-500 focus:outline-none bg-white"
              >
                {['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'].map((type) => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
           </div>
        </div>

        <div className="flex gap-2 pt-2">
          <button
            type="submit"
            className="flex-1 bg-red-600 hover:bg-red-700 text-white py-2.5 rounded-lg font-bold transition-colors"
          >
            {initialData ? 'Atualizar Doador' : 'Cadastrar no AlertaDoar'}
          </button>
          {initialData && (
            <button
              type="button"
              onClick={onCancel}
              className="flex-1 bg-slate-200 hover:bg-slate-300 text-slate-800 py-2.5 rounded-lg font-bold transition-colors"
            >
              Cancelar
            </button>
          )}
        </div>
      </form>
    </div>
  );
}
