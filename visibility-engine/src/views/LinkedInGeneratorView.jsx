import { useState } from 'react';
import { Linkedin, Cpu, FileEdit, Loader2 } from 'lucide-react';
import Card from '../components/Card.jsx';
import Button from '../components/Button.jsx';
import ContentPreview from '../components/ContentPreview.jsx';
import ErrorBanner from '../components/ErrorBanner.jsx';
import { aiService } from '../services/aiService.js';
import { useSettings } from '../hooks/useSettings.js';

const TONES = [
  'Professional Insight / Thought Leadership',
  'Behind the Scenes / Agency Life',
  'Direct Call to Action (Service Promo)',
  'Educational / How-To',
];

export default function LinkedInGeneratorView() {
  const { settings } = useSettings();
  const [source, setSource] = useState('');
  const [tone, setTone] = useState(TONES[0]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState('');
  const [error, setError] = useState('');

  const handleGenerate = async () => {
    setError('');
    setResult('');
    setLoading(true);
    try {
      const text = await aiService.generateLinkedInPosts(source, tone, settings.brandVoice, settings.coreServices);
      setResult(text);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl animate-in fade-in space-y-6">
      <div>
        <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
          <Linkedin className="w-6 h-6 text-blue-600" /> LinkedIn Post Generator
        </h2>
        <p className="text-sm text-slate-500">
          Create 3 post variations from scratch or from an existing article.
        </p>
      </div>

      <ErrorBanner message={error} onDismiss={() => setError('')} />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-6">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Source Material or Topic
              </label>
              <textarea
                rows={5}
                className="w-full bg-slate-50 border border-slate-200 text-slate-900 text-sm rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 block p-3"
                placeholder="Paste an article link, a paragraph, or describe what you want to post about…"
                value={source}
                onChange={(e) => setSource(e.target.value)}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Tone &amp; Goal</label>
              <select
                className="w-full bg-slate-50 border border-slate-200 text-slate-900 text-sm rounded-lg p-2.5 focus:ring-2 focus:ring-blue-500"
                value={tone}
                onChange={(e) => setTone(e.target.value)}
              >
                {TONES.map((t) => (
                  <option key={t}>{t}</option>
                ))}
              </select>
            </div>
            <Button
              className="w-full"
              icon={loading ? Loader2 : Cpu}
              onClick={handleGenerate}
              disabled={loading || !source.trim()}
            >
              {loading ? 'Generating…' : 'Generate 3 Variations'}
            </Button>
          </div>
        </Card>

        <div className="flex flex-col">
          {loading && (
            <div className="flex flex-col items-center justify-center flex-1 text-slate-400 gap-3 py-16">
              <Loader2 className="w-8 h-8 animate-spin" />
              <p className="text-sm">Claude is writing your posts…</p>
            </div>
          )}
          {!loading && result && (
            <ContentPreview content={result} filename="linkedin-posts" />
          )}
          {!loading && !result && (
            <div className="flex flex-col items-center justify-center flex-1 text-slate-300 gap-3 py-16 border-2 border-dashed border-slate-200 rounded-xl">
              <FileEdit className="w-10 h-10" />
              <p className="text-sm text-slate-400">Your posts will appear here</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
