import { useState, useEffect } from 'react';

const statusConfig = {
  Critical: { label: 'CRÍTICO', classes: 'bg-red-200 text-red-800 border-red-300' },
  Alert: { label: 'BAIXO', classes: 'bg-yellow-100 text-yellow-800 border-yellow-300' },
  Stable: { label: 'ESTÁVEL', classes: 'bg-green-200 text-green-800 border-green-300' }
};

export default function StockLevels() {
  const [stock, setStock] = useState([]);

  useEffect(() => {
    const fetchStock = async () => {
      try {
        const response = await fetch('http://localhost:8000/stock/');
        const data = await response.json();
        setStock(data);
      } catch (error) {
        console.error(error);
      }
    };
    
    fetchStock();

    window.addEventListener('stock-synced', fetchStock);
    return () => window.removeEventListener('stock-synced', fetchStock);
  }, []);

  return (
    <section className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
      <h3 className="text-xl font-bold mb-4 text-slate-900">
        Níveis de Estoque em Tempo Real
      </h3>
      <div className="flex flex-wrap gap-3">
        {stock.map(({ blood_type, status }) => {
          const config = statusConfig[status] || statusConfig.Stable;
          
          return (
            <div
              key={blood_type}
              className={`flex flex-col items-center justify-center w-[120px] h-[90px] rounded-lg border shadow-sm ${config.classes}`}
            >
              <span className="text-3xl font-extrabold tracking-tight">
                {blood_type}
              </span>
              <span className="text-sm font-semibold mt-1">
                {config.label}
              </span>
            </div>
          );
        })}
      </div>
    </section>
  );
}
