import { BarChart3, ListTree, FileEdit, Linkedin, PlayCircle, CheckCircle2 } from 'lucide-react';
import Card from '../components/Card.jsx';
import Button from '../components/Button.jsx';

const STATS = [
  { label: 'SEO Health Score',       value: '84/100', color: 'blue-600',   bg: 'blue-50',   icon: BarChart3,  border: 'border-l-blue-600'   },
  { label: 'Content Opportunities',  value: '12',     color: 'amber-600',  bg: 'amber-50',  icon: ListTree,   border: 'border-l-amber-500'  },
  { label: 'Drafts Ready',           value: '8',      color: 'emerald-600',bg: 'emerald-50',icon: FileEdit,   border: 'border-l-emerald-500'},
  { label: 'LinkedIn Posts',         value: '24',     color: 'indigo-600', bg: 'indigo-50', icon: Linkedin,   border: 'border-l-indigo-600' },
];

const ACTIONS = [
  { msg: "Publish 'Visual Storytelling' LinkedIn Series",       priority: 'high'   },
  { msg: 'Review new AI-generated draft for Annual Reports',    priority: 'medium' },
  { msg: 'Update portfolio with UN Environment Case Study',     priority: 'medium' },
];

export default function DashboardView() {
  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4">
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
        {STATS.map(({ label, value, color, bg, icon: Icon, border }) => (
          <Card key={label} className={`p-5 flex items-center space-x-4 border-l-4 ${border}`}>
            <div className={`p-3 bg-${bg} text-${color} rounded-lg`}>
              <Icon size={24} />
            </div>
            <div>
              <p className="text-sm text-slate-500 font-medium">{label}</p>
              <h3 className="text-2xl font-bold text-slate-900">{value}</h3>
            </div>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2">
          <div className="p-5 border-b border-slate-100">
            <h3 className="font-semibold text-slate-900">Next Recommended Actions</h3>
          </div>
          <div>
            {ACTIONS.map((action, i) => (
              <div
                key={i}
                className="flex items-center p-4 border-b border-slate-50 last:border-0 hover:bg-slate-50 transition-colors"
              >
                <PlayCircle
                  className={`w-5 h-5 mr-3 shrink-0 ${
                    action.priority === 'high' ? 'text-blue-600' : 'text-slate-400'
                  }`}
                />
                <span className="text-sm font-medium text-slate-700 flex-1">{action.msg}</span>
                <Button variant="ghost" className="text-xs shrink-0">
                  Execute
                </Button>
              </div>
            ))}
          </div>
        </Card>

        <Card>
          <div className="p-5 border-b border-slate-100">
            <h3 className="font-semibold text-slate-900">Target Website</h3>
          </div>
          <div className="p-6 text-center">
            <div className="w-16 h-16 bg-gradient-to-tr from-blue-600 to-indigo-600 rounded-2xl mx-auto flex items-center justify-center text-white font-bold text-xl mb-4 shadow-lg shadow-blue-200">
              iG
            </div>
            <h4 className="font-bold text-slate-900">igraphi.com</h4>
            <p className="text-sm text-slate-500 mt-1 mb-4">Strategic Design Agency</p>
            <div className="inline-flex items-center space-x-2 text-xs font-medium text-emerald-600 bg-emerald-50 py-1.5 px-3 rounded-full">
              <CheckCircle2 className="w-4 h-4" />
              <span>Site Sync Active</span>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
