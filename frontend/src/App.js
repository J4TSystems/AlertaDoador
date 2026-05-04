import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './Sidebar';
import StockLevels from './StockLevels';
import StockSyncControl from './StockSyncControl';
import AlertHistory from './AlertHistory';
import DonorsPage from './pages/DonorsPage';
import { Droplet } from 'lucide-react';

export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-slate-50 text-slate-900 font-sans flex flex-col">
        <header className="bg-white px-6 py-4 flex items-center border-b border-slate-200">
          <Droplet className="text-red-700 fill-current mr-2" size={24} />
          <h1 className="text-2xl font-bold">
            Painel <span className="text-red-600 font-normal">AlertaDoador</span>
          </h1>
        </header>
        <div className="flex flex-1">
          <Sidebar />
          <main className="flex-1 p-8">
            <Routes>
              <Route path="/" element={
                <>
                  <h2 className="text-3xl font-bold mb-6">Visão Geral</h2>
                  <StockLevels />
                </>
              } />
              <Route path="/doadores" element={
                <>
                  <h2 className="text-3xl font-bold mb-6">Doadores</h2>
                  <DonorsPage />
                </>
              } />
              <Route path="/historico" element={
                <>
                  <h2 className="text-3xl font-bold mb-6">Histórico de Alertas</h2>
                  <AlertHistory />
                </>
              } />
              <Route path="/estoque" element={
                <>
                  <h2 className="text-3xl font-bold mb-6">Gestão de Estoque</h2>
                  <StockLevels />
                  <StockSyncControl />
                </>
              } />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}
