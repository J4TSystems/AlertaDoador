import { useState, useEffect } from 'react';

const maskEmail = (email) => {
  if (!email || !email.includes('@')) return email;
  const [name, domain] = email.split('@');
  if (name.length <= 2) return `${name[0]}****@${domain}`;
  const mid = Math.floor(name.length / 2);
  return `${name.substring(0, mid - 1)}****${name.substring(mid + 1)}@${domain}`;
};

export default function AlertHistory() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await fetch('http://localhost:8000/notifications/history');
        const data = await response.json();
        setHistory(data);
      } catch (error) {
        console.error(error);
      }
    };
    
    fetchHistory();
  }, []);

  return (
    <section className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-slate-200 text-slate-600">
              <th className="p-3 font-semibold">Destinatário</th>
              <th className="p-3 font-semibold">Tipo Sanguíneo</th>
              <th className="p-3 font-semibold">Status</th>
              <th className="p-3 font-semibold">Enviado Em</th>
            </tr>
          </thead>
          <tbody>
            {history.map(({ id, recipient_email, blood_type, status_at_time, sent_at }) => (
              <tr key={id} className="border-b border-slate-100 hover:bg-slate-50 text-slate-800">
                <td className="p-3">{maskEmail(recipient_email)}</td>
                <td className="p-3 font-bold">{blood_type}</td>
                <td className="p-3">
                  <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                    status_at_time === 'Critical' ? 'bg-red-100 text-red-800' :
                    status_at_time === 'Alert' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-slate-100 text-slate-800'
                  }`}>
                    {status_at_time === 'Critical' ? 'Crítico' : status_at_time === 'Alert' ? 'Alerta' : status_at_time}
                  </span>
                </td>
                <td className="p-3 text-sm text-slate-600">
                  {new Date(sent_at).toLocaleString('pt-BR')}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
