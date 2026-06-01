import { Calendar, Download } from 'lucide-react';
import Card from '../components/Card.jsx';
import Button from '../components/Button.jsx';
import { CONTENT_CALENDAR } from '../data/mockData.js';

const typeStyles = {
  Blog:       'bg-indigo-50 text-indigo-700 border-indigo-100',
  LinkedIn:   'bg-blue-50 text-blue-700 border-blue-100',
  Newsletter: 'bg-purple-50 text-purple-700 border-purple-100',
  'Case Study':'bg-emerald-50 text-emerald-700 border-emerald-100',
};

const statusStyles = {
  published: 'bg-slate-100 text-slate-600',
  ready:     'bg-emerald-100 text-emerald-700',
  draft:     'bg-amber-100 text-amber-700',
  idea:      'bg-slate-100 text-slate-500',
};

export default function CalendarView() {
  return (
    <div className="animate-in fade-in space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Monthly Content Calendar</h2>
          <p className="text-sm text-slate-500">Automated schedule for Blog, Social, and Newsletters</p>
        </div>
        <div className="flex gap-2">
          <Button variant="secondary" icon={Download}>Export Plan</Button>
          <Button icon={Calendar}>Generate Next Month</Button>
        </div>
      </div>

      <Card className="overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left text-slate-500 min-w-[700px]">
            <thead className="text-xs text-slate-700 uppercase bg-slate-50 border-b border-slate-200">
              <tr>
                <th className="px-6 py-4 font-semibold">Content Title / Topic</th>
                <th className="px-6 py-4 font-semibold">Type</th>
                <th className="px-6 py-4 font-semibold">Target Audience</th>
                <th className="px-6 py-4 font-semibold">SEO Keyword</th>
                <th className="px-6 py-4 font-semibold">Status</th>
                <th className="px-6 py-4 font-semibold text-right">Action</th>
              </tr>
            </thead>
            <tbody>
              {CONTENT_CALENDAR.map((item, i) => (
                <tr key={i} className="bg-white border-b border-slate-100 hover:bg-slate-50">
                  <td className="px-6 py-4 font-medium text-slate-900">{item.title}</td>
                  <td className="px-6 py-4">
                    <span className={`px-2 py-1 rounded text-xs font-medium border ${typeStyles[item.type] ?? ''}`}>
                      {item.type}
                    </span>
                  </td>
                  <td className="px-6 py-4">{item.audience}</td>
                  <td className="px-6 py-4 text-xs">{item.keyword}</td>
                  <td className="px-6 py-4">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium capitalize ${statusStyles[item.status] ?? ''}`}>
                      {item.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <Button variant="ghost" className="text-blue-600 px-2 text-xs">Edit</Button>
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
