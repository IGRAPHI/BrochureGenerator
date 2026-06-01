import { Download } from 'lucide-react';
import Card from '../components/Card.jsx';
import Button from '../components/Button.jsx';
import { PUBLISHING_QUEUE } from '../data/mockData.js';

const statusStyles = {
  'Ready to Publish': 'bg-emerald-100 text-emerald-700',
  'Needs Review':     'bg-amber-100 text-amber-700',
  'Draft':            'bg-slate-100 text-slate-600',
};

export default function PublishingQueueView() {
  return (
    <div className="animate-in fade-in space-y-6">
      <div>
        <h2 className="text-xl font-bold text-slate-900">Publishing Queue</h2>
        <p className="text-sm text-slate-500">Review and export finalised content ready for distribution.</p>
      </div>

      <Card className="overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left text-slate-600 min-w-[600px]">
            <thead className="text-xs text-slate-700 uppercase bg-slate-50 border-b border-slate-200">
              <tr>
                <th className="px-6 py-4 font-semibold">Content Title</th>
                <th className="px-6 py-4 font-semibold">Type</th>
                <th className="px-6 py-4 font-semibold">Last Edited</th>
                <th className="px-6 py-4 font-semibold">Status</th>
                <th className="px-6 py-4 font-semibold text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              {PUBLISHING_QUEUE.map((item, i) => (
                <tr key={i} className="bg-white border-b border-slate-100 hover:bg-slate-50">
                  <td className="px-6 py-4 font-medium text-slate-900">{item.title}</td>
                  <td className="px-6 py-4">{item.type}</td>
                  <td className="px-6 py-4 text-xs text-slate-400">{item.updated}</td>
                  <td className="px-6 py-4">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${statusStyles[item.status] ?? ''}`}>
                      {item.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right space-x-2">
                    <Button variant="ghost" className="px-2 py-1 text-xs" icon={Download}>Export</Button>
                    <Button variant="secondary" className="px-2 py-1 text-xs">Mark Published</Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
