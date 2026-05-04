import { useState, useEffect } from 'react';
import { RefreshCw } from 'lucide-react';

export default function StockSyncControl() {
  const [lastSync, setLastSync] = useState(null);
  const [isSyncing, setIsSyncing] = useState(false);

  useEffect(() => {
    const fetchInitialSyncDate = async () => {
      try {
        const response = await fetch('http://localhost:8000/stock/');
        const data = await response.json();
        if (data && data.length > 0 && data[0].last_updated) {
          setLastSync(data[0].last_updated);
        }
      } catch (error) {
        console.error('Error fetching initial stock date:', error);
      }
    };
    fetchInitialSyncDate();
  }, []);

  const handleSync = async () => {
    setIsSyncing(true);
    try {
      const response = await fetch('http://localhost:8000/stock/sync', {
        method: 'POST',
      });
      const data = await response.json();
      if (data && data.length > 0 && data[0].last_updated) {
        setLastSync(data[0].last_updated);
        // Dispatch an event so StockLevels can listen and refresh if needed
        window.dispatchEvent(new Event('stock-synced'));
      }
    } catch (error) {
      console.error('Error syncing stock:', error);
    } finally {
      setIsSyncing(false);
    }
  };

  const formattedDate = lastSync 
    ? new Date(lastSync).toLocaleString('pt-BR') 
    : 'Não sincronizado recentemente';

  return (
    <section className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm mt-8">
      <h3 className="text-xl font-bold text-slate-900 mb-2">
        Controle de Sincronização Manual
      </h3>
      <p className="text-slate-600 mb-6">
        Para uma sincronização imediata dos níveis de estoque com o banco de sangue centralizado (p.ex., Hemocentro), use o controle abaixo.
      </p>
      
      <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4">
        <button 
          onClick={handleSync}
          disabled={isSyncing}
          className="flex items-center justify-center bg-red-600 hover:bg-red-700 text-white px-5 py-2.5 rounded-lg font-medium transition-colors disabled:opacity-70 disabled:cursor-not-allowed"
        >
          <RefreshCw className={`mr-2 h-5 w-5 ${isSyncing ? 'animate-spin' : ''}`} />
          {isSyncing ? 'Sincronizando...' : 'Sincronizar Agora com o Hemocentro'}
        </button>
        <div className="text-sm text-slate-500 font-medium mt-2 sm:mt-0">
          Última sincronização: <span className="text-slate-700">{formattedDate}</span>
        </div>
      </div>
    </section>
  );
}
