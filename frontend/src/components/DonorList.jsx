import { Edit2, Trash2 } from 'lucide-react';

const maskEmail = (email) => {
  if (!email || !email.includes('@')) return email;
  const [name, domain] = email.split('@');
  if (name.length <= 2) return `${name[0]}****@${domain}`;
  const mid = Math.floor(name.length / 2);
  return `${name.substring(0, mid - 1)}****${name.substring(mid + 1)}@${domain}`;
};

const maskName = (name) => {
  if (!name) return name;
  const parts = name.split(' ');
  return parts.map((part, index) => {
    if (index === 0) return part; // Keep first name mostly intact or you can mask it too. Let's mask all words longer than 2.
    if (part.length <= 2) return `${part[0]}*`;
    const mid = Math.floor(part.length / 2);
    return `${part.substring(0, mid - 1)}****${part.substring(mid + 1)}`;
  }).join(' ');
};


export default function DonorList({ donors, onEdit, onDelete }) {
  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
      <h3 className="text-xl font-bold text-slate-900 mb-4">Doadores Cadastrados</h3>
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-slate-200 text-slate-600">
              <th className="p-3 font-semibold">Nome</th>
              <th className="p-3 font-semibold">E-mail</th>
              <th className="p-3 font-semibold">Tipo Sanguíneo</th>
              <th className="p-3 font-semibold text-right">Ações</th>
            </tr>
          </thead>
          <tbody>
            {donors.map((donor) => (
              <tr key={donor.id} className="border-b border-slate-100 hover:bg-slate-50 text-slate-800">
                <td className="p-3">{maskName(donor.full_name)}</td>
                <td className="p-3">{maskEmail(donor.email)}</td>
                <td className="p-3 font-bold">{donor.blood_type}</td>
                <td className="p-3 text-right">
                  <button
                    onClick={() => onEdit(donor)}
                    aria-label="Edit"
                    disabled
                    title="Em breve"
                    className="text-slate-400 cursor-not-allowed p-1 mx-1"
                  >
                    <Edit2 size={18} />
                  </button>
                  <button
                    onClick={() => onDelete(donor.id)}
                    aria-label="Delete"
                    className="text-red-600 hover:text-red-800 p-1 mx-1"
                  >
                    <Trash2 size={18} />
                  </button>
                </td>
              </tr>
            ))}
            {donors.length === 0 && (
              <tr>
                <td colSpan="4" className="p-4 text-center text-slate-500">
                  Nenhum doador cadastrado.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
