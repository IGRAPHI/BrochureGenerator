import { useState } from 'react';
import { Briefcase, Cpu, UploadCloud, Loader2, FileEdit } from 'lucide-react';
import Card from '../components/Card.jsx';
import Button from '../components/Button.jsx';
import ContentPreview from '../components/ContentPreview.jsx';
import ErrorBanner from '../components/ErrorBanner.jsx';
import { aiService } from '../services/aiService.js';
import { useSettings } from '../hooks/useSettings.js';

export default function CaseStudyBuilderView() {
  const { settings } = useSettings();
  const [fields, setFields] = useState({ client: '', services: '', challenge: '', solution: '', outcome: '' });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState('');
  const [error, setError] = useState('');

  const set = (key) => (e) => setFields((f) => ({ ...f, [key]: e.target.value }));

  const handleGenerate = async () => {
    setError('');
    setResult('');
    setLoading(true);
    try {
      const text = await aiService.generateCaseStudy(fields, settings.brandVoice, settings.coreServices);
      setResult(text);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const isReady = fields.client.trim() && fields.challenge.trim();

  return (
    <div className="max-w-5xl animate-in fade-in space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
            <Briefcase className="w-6 h-6 text-indigo-600" /> Case Study Builder
          </h2>
          <p className="text-sm text-slate-500">Transform client projects into polished portfolio pieces.</p>
        </div>
        <Button icon={loading ? Loader2 : Cpu} onClick={handleGenerate} disabled={loading || !isReady}>
          {loading ? 'Generating…' : 'Generate Polished Copy'}
        </Button>
      </div>

      <ErrorBanner message={error} onDismiss={() => setError('')} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2 p-6">
          <h3 className="font-semibold text-slate-800 mb-4 border-b border-slate-100 pb-2">Project Details</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1 uppercase tracking-wider">
                Client / Organisation <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                className="w-full bg-slate-50 border border-slate-200 text-sm rounded p-2 focus:ring-2 focus:ring-blue-500"
                placeholder="e.g., World Health Organization"
                value={fields.client}
                onChange={set('client')}
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1 uppercase tracking-wider">Services Used</label>
              <input
                type="text"
                className="w-full bg-slate-50 border border-slate-200 text-sm rounded p-2 focus:ring-2 focus:ring-blue-500"
                placeholder="Brand Identity, Annual Report"
                value={fields.services}
                onChange={set('services')}
              />
            </div>
          </div>
          <div className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1 uppercase tracking-wider">
                The Challenge <span className="text-red-500">*</span>
              </label>
              <textarea
                rows={3}
                className="w-full bg-slate-50 border border-slate-200 text-sm rounded p-2 focus:ring-2 focus:ring-blue-500"
                placeholder="Describe the problem or context…"
                value={fields.challenge}
                onChange={set('challenge')}
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1 uppercase tracking-wider">Our Approach / Solution</label>
              <textarea
                rows={3}
                className="w-full bg-slate-50 border border-slate-200 text-sm rounded p-2 focus:ring-2 focus:ring-blue-500"
                placeholder="How did iGraphi solve it?"
                value={fields.solution}
                onChange={set('solution')}
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1 uppercase tracking-wider">The Outcome / Impact</label>
              <textarea
                rows={2}
                className="w-full bg-slate-50 border border-slate-200 text-sm rounded p-2 focus:ring-2 focus:ring-blue-500"
                placeholder="Results, metrics, client feedback…"
                value={fields.outcome}
                onChange={set('outcome')}
              />
            </div>
          </div>
        </Card>

        <div className="space-y-6">
          <Card className="p-6 bg-slate-50 border-dashed border-2 border-slate-200">
            <div className="text-center">
              <UploadCloud className="w-8 h-8 text-slate-400 mx-auto mb-2" />
              <h4 className="text-sm font-semibold text-slate-700">Visual Assets</h4>
              <p className="text-xs text-slate-500 mb-4 mt-1">Upload mockups, before/afters, deliverables.</p>
              <Button variant="secondary" className="w-full text-xs">Browse Files</Button>
            </div>
          </Card>

          <Card className="p-5">
            <h4 className="text-sm font-semibold text-slate-800 mb-3">AI Context</h4>
            <ul className="text-xs text-slate-600 space-y-2 list-disc pl-4">
              <li>Maintains the iGraphi authoritative-but-warm tone.</li>
              <li>Focuses on business impact, not just design aesthetics.</li>
              <li>Includes pull-quote placeholders for the client voice.</li>
            </ul>
          </Card>
        </div>
      </div>

      {loading && (
        <div className="flex flex-col items-center justify-center py-16 text-slate-400 gap-3">
          <Loader2 className="w-8 h-8 animate-spin" />
          <p className="text-sm">Claude is writing your case study…</p>
        </div>
      )}

      {!loading && result && <ContentPreview content={result} filename={`${fields.client.slice(0, 30)}-case-study`} />}

      {!loading && !result && (
        <div className="flex items-center justify-center py-12 border-2 border-dashed border-slate-200 rounded-xl text-slate-300 gap-3">
          <FileEdit className="w-8 h-8" />
          <p className="text-sm text-slate-400">Generated case study will appear here</p>
        </div>
      )}
    </div>
  );
}
