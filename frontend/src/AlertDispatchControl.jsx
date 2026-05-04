import { useState } from 'react';
import { Bell } from 'lucide-react';

export default function AlertDispatchControl({ onAlertSent, lastAlertDate }) {
  const [isSending, setIsSending] = useState(false);

  const handleDispatch = async () => {
    setIsSending(true);
    try {
      await fetch('http://localhost:8000/notifications/send-alerts', {
        method: 'POST',
      });
      if (onAlertSent) {
        onAlertSent();
      }
    } catch (error) {
      console.error('Error sending alerts:', error);
    } finally {
      setIsSending(false);
    }
  };

  const displayDate = lastAlertDate ? new Date(lastAlertDate) : null;
  const formattedDate = displayDate 
    ? displayDate.toLocaleString('pt-BR') 
    : 'Nenhum alerta disparado';

  return (
    <section className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm mb-8">
      <h3 className="text-xl font-bold text-slate-900 mb-2">
        Controle de Disparo de Alertas
      </h3>
      <p className="text-slate-600 mb-6">
        Para avaliar os níveis críticos de estoque e notificar imediatamente os doadores compatíveis, use o controle abaixo.
      </p>
      
      <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4">
        <button 
          onClick={handleDispatch}
          disabled={isSending}
          className="flex items-center justify-center bg-red-600 hover:bg-red-700 text-white px-5 py-2.5 rounded-lg font-medium transition-colors disabled:opacity-70 disabled:cursor-not-allowed"
        >
          <Bell className={`mr-2 h-5 w-5 ${isSending ? 'animate-bounce' : ''}`} />
          {isSending ? 'Disparando...' : 'Disparar Alertas'}
        </button>
        <div className="text-sm text-slate-500 font-medium mt-2 sm:mt-0">
          Último disparo: <span className="text-slate-700">{formattedDate}</span>
        </div>
      </div>
    </section>
  );
}
