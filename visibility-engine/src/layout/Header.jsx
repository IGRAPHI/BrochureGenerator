import { AlertCircle, Menu } from 'lucide-react';
import { NAV_ITEMS } from './Sidebar.jsx';

export default function Header({ activeTab, setMobileOpen }) {
  const currentItem = NAV_ITEMS.find((i) => i.id === activeTab);

  return (
    <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-4 sm:px-8 z-10 sticky top-0 shadow-sm shrink-0">
      <div className="flex items-center gap-3">
        {/* Mobile hamburger */}
        <button
          className="lg:hidden p-2 rounded-lg text-slate-500 hover:bg-slate-100"
          onClick={() => setMobileOpen(true)}
        >
          <Menu className="w-5 h-5" />
        </button>
        <h1 className="text-base sm:text-lg font-bold text-slate-800">
          {currentItem?.label ?? 'Dashboard'}
        </h1>
      </div>

      <div className="flex items-center space-x-3">
        <span className="hidden sm:block text-xs font-medium text-slate-500 bg-slate-100 px-3 py-1.5 rounded-full">
          Turn your expertise into discoverable content.
        </span>
        <div className="h-5 w-px bg-slate-200 hidden sm:block" />
        <button className="p-2 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors">
          <AlertCircle className="w-5 h-5" />
        </button>
      </div>
    </header>
  );
}
