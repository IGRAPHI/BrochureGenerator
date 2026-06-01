import { RefreshCw, PenTool } from 'lucide-react';
import Card from '../components/Card.jsx';
import Button from '../components/Button.jsx';
import { KEYWORD_CLUSTERS } from '../data/mockData.js';

const priorityStyles = {
  High:   'bg-red-50 text-red-700',
  Medium: 'bg-amber-50 text-amber-700',
  Low:    'bg-slate-100 text-slate-700',
};

export default function KeywordStrategyView() {
  return (
    <div className="animate-in fade-in space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Keyword &amp; Topic Strategy</h2>
          <p className="text-sm text-slate-500">Targeted clusters organised by research engine</p>
        </div>
        <Button icon={RefreshCw}>Refresh Strategy</Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        {KEYWORD_CLUSTERS.map((cluster, i) => (
          <Card key={i} className="flex flex-col">
            <div className="p-5 border-b border-slate-100 flex-1">
              <div className="flex justify-between items-start mb-3 gap-2">
                <span className={`text-xs px-2 py-1 rounded font-medium shrink-0 ${priorityStyles[cluster.priority]}`}>
                  {cluster.priority} Priority
                </span>
                <span className="text-xs text-slate-500 font-medium bg-slate-50 px-2 py-1 rounded text-right">
                  {cluster.type}
                </span>
              </div>
              <h3 className="font-bold text-slate-900 text-base leading-tight mb-1">{cluster.topic}</h3>
              <p className="text-xs text-slate-500 mb-4">Intent: {cluster.intent}</p>

              <h4 className="text-xs font-semibold text-slate-700 mb-2 uppercase tracking-wider">
                Supporting Keywords
              </h4>
              <div className="flex flex-wrap gap-2">
                {cluster.keywords.map((kw, j) => (
                  <span
                    key={j}
                    className="text-xs bg-blue-50 text-blue-700 border border-blue-100 px-2 py-1 rounded-full"
                  >
                    {kw}
                  </span>
                ))}
              </div>
            </div>
            <div className="p-4 bg-slate-50 border-t border-slate-100">
              <Button variant="secondary" className="w-full text-xs" icon={PenTool}>
                Draft Content for Cluster
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
