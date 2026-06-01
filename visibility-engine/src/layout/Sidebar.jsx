import {
  LayoutDashboard, Search, ListTree, Calendar, PenTool,
  Linkedin, Briefcase, UploadCloud, Settings, X,
} from 'lucide-react';

export const NAV_ITEMS = [
  { id: 'dashboard',  label: 'Dashboard',        icon: LayoutDashboard },
  { id: 'analyzer',   label: 'Website Analyzer',  icon: Search },
  { id: 'strategy',   label: 'Keyword Strategy',  icon: ListTree },
  { id: 'calendar',   label: 'Content Calendar',  icon: Calendar },
  { id: 'blog',       label: 'Blog Generator',    icon: PenTool },
  { id: 'linkedin',   label: 'LinkedIn Posts',    icon: Linkedin },
  { id: 'casestudy',  label: 'Case Studies',      icon: Briefcase },
  { id: 'queue',      label: 'Publishing Queue',  icon: UploadCloud },
  { id: 'settings',   label: 'Settings',          icon: Settings },
];

export default function Sidebar({ activeTab, setActiveTab, mobileOpen, setMobileOpen }) {
  const content = (
    <div className="flex flex-col h-full bg-slate-900 text-slate-300">
      <div className="h-16 flex items-center px-6 bg-slate-950/50 border-b border-slate-800 shrink-0">
        <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold mr-3 shadow-lg shadow-blue-900/50 shrink-0">
          iG
        </div>
        <span className="font-bold text-white tracking-wide text-lg leading-tight">
          Visibility Engine
        </span>
      </div>

      <div className="flex-1 overflow-y-auto py-6 px-3">
        <p className="text-xs font-semibold text-slate-500 uppercase tracking-widest px-3 mb-4">
          Main Menu
        </p>
        <nav className="space-y-1">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => { setActiveTab(item.id); setMobileOpen(false); }}
                className={`w-full flex items-center px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 group ${
                  isActive
                    ? 'bg-blue-600 text-white shadow-md'
                    : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                }`}
              >
                <Icon
                  className={`w-5 h-5 mr-3 shrink-0 ${
                    isActive ? 'text-blue-200' : 'text-slate-500 group-hover:text-slate-300'
                  }`}
                />
                {item.label}
              </button>
            );
          })}
        </nav>
      </div>

      <div className="p-4 bg-slate-950/50 border-t border-slate-800 shrink-0">
        <div className="flex items-center space-x-3">
          <div className="w-9 h-9 rounded-full bg-gradient-to-tr from-slate-700 to-slate-600 flex items-center justify-center text-white font-semibold border-2 border-slate-700 shrink-0">
            V
          </div>
          <div className="overflow-hidden">
            <p className="text-sm font-medium text-white truncate">Vlad</p>
            <p className="text-xs text-slate-500 truncate">Admin / Strategist</p>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <>
      {/* Desktop sidebar */}
      <aside className="hidden lg:flex w-64 shrink-0 flex-col shadow-xl z-20 h-screen sticky top-0">
        {content}
      </aside>

      {/* Mobile overlay */}
      {mobileOpen && (
        <div className="fixed inset-0 z-40 lg:hidden">
          <div
            className="absolute inset-0 bg-slate-900/50 backdrop-blur-sm"
            onClick={() => setMobileOpen(false)}
          />
          <aside className="absolute left-0 top-0 h-full w-64 z-50 shadow-2xl flex flex-col">
            <button
              onClick={() => setMobileOpen(false)}
              className="absolute top-4 right-4 text-slate-400 hover:text-white z-50"
            >
              <X className="w-5 h-5" />
            </button>
            {content}
          </aside>
        </div>
      )}
    </>
  );
}
