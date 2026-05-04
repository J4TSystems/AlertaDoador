import { NavLink } from 'react-router-dom';
import { Home, Users, Megaphone, BarChart2 } from 'lucide-react';

export default function Sidebar() {
  return (
    <aside className="w-64 bg-slate-800 text-slate-300 flex flex-col min-h-full">
      <nav className="flex flex-col gap-1 p-2 mt-2">
        <NavItem to="/" icon={<Home size={20} />} label="Visão Geral" />
        <NavItem to="/doadores" icon={<Users size={20} />} label="Doadores" />
        <NavItem to="/historico" icon={<Megaphone size={20} />} label="Histórico de Alertas" />
        <NavItem to="/estoque" icon={<BarChart2 size={20} />} label="Gestão de Estoque" />
      </nav>
    </aside>
  );
}

function NavItem({ to, icon, label }) {
  return (
    <NavLink
      to={to}
      className={({ isActive }) =>
        `flex items-center gap-3 px-4 py-3 rounded-md transition-colors ${
          isActive
            ? 'bg-slate-700 text-white'
            : 'hover:bg-slate-700 hover:text-white'
        }`
      }
    >
      {icon}
      <span className="font-medium text-sm">{label}</span>
    </NavLink>
  );
}
