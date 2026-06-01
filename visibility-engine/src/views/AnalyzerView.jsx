import { useState } from 'react';
import { Globe, Search, CheckCircle2, RefreshCw, Loader2 } from 'lucide-react';
import Card from '../components/Card.jsx';
import Button from '../components/Button.jsx';
import ErrorBanner from '../components/ErrorBanner.jsx';
import { aiService } from '../services/aiService.js';

const STEPS = [
  'Reading homepage content...',
  'Extracting brand voice...',
  'Identifying core services...',
  'Finding SEO gaps...',
  'Generating strategic recommendations...',
];

export default function AnalyzerView() {
  const [url, setUrl] = useState('https://igraphi.com');
  const [analyzing, setAnalyzing] = useState(false);
  const [step, setStep] = useState(-1);
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    if (!url.trim()) { setError('Please enter a URL.'); return; }
    setError('');
    setResults(null);
    setAnalyzing(true);
    setStep(0);

    const interval = setInterval(() => {
      setStep((s) => {
        if (s >= STEPS.length - 1) { clearInterval(interval); return s; }
        return s + 1;
      });
    }, 800);

    try {
      const data = await aiService.analyzeWithGemini(url);
      clearInterval(interval);
      setStep(STEPS.length - 1);
      setResults(data);
    } catch (err) {
      clearInterval(interval);
      setError(err.message);
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="max-w-4xl animate-in fade-in space-y-6">
      <Card className="p-6">
        <h2 className="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
          <Globe className="w-5 h-5 text-blue-600" /> Analyse Website
        </h2>
        <div className="flex flex-col sm:flex-row gap-3">
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="flex-1 bg-slate-50 border border-slate-200 text-slate-900 text-sm rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 block p-2.5"
            placeholder="https://example.com"
          />
          <Button onClick={handleAnalyze} disabled={analyzing} icon={analyzing ? Loader2 : Search}>
            {analyzing ? 'Analysing…' : 'Run Analysis'}
          </Button>
        </div>

        <ErrorBanner message={error} onDismiss={() => setError('')} />

        {analyzing && (
          <div className="mt-6 bg-slate-50 p-6 rounded-lg border border-slate-100">
            <h4 className="text-sm font-semibold text-slate-700 mb-4">Research Engine in Progress</h4>
            <div className="space-y-3">
              {STEPS.map((text, i) => (
                <div
                  key={i}
                  className={`flex items-center text-sm gap-2 ${
                    i < step
                      ? 'text-emerald-600'
                      : i === step
                      ? 'text-blue-600 font-medium'
                      : 'text-slate-300'
                  }`}
                >
                  {i < step ? (
                    <CheckCircle2 className="w-4 h-4 shrink-0" />
                  ) : i === step ? (
                    <RefreshCw className="w-4 h-4 shrink-0 animate-spin" />
                  ) : (
                    <div className="w-4 h-4 shrink-0 rounded-full border-2 border-slate-200" />
                  )}
                  {text}
                </div>
              ))}
            </div>
          </div>
        )}
      </Card>

      {results && !analyzing && (
        <Card className="p-6 bg-gradient-to-br from-white to-blue-50/50 animate-in fade-in">
          <h3 className="font-bold text-slate-900 mb-4">
            Analysis Results: <span className="text-blue-600">{url}</span>
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <h4 className="text-xs uppercase tracking-wider text-slate-500 font-semibold mb-2">
                Detected Brand Voice
              </h4>
              <p className="text-sm text-slate-800 bg-white p-3 rounded border border-slate-100">
                {results.brandVoice}
              </p>
            </div>
            <div>
              <h4 className="text-xs uppercase tracking-wider text-slate-500 font-semibold mb-2">
                Primary Audience
              </h4>
              <p className="text-sm text-slate-800 bg-white p-3 rounded border border-slate-100">
                {results.primaryAudience}
              </p>
            </div>
          </div>

          <h4 className="text-xs uppercase tracking-wider text-slate-500 font-semibold mb-2">
            SEO Gaps &amp; Opportunities ({results.opportunities})
          </h4>
          <div className="space-y-2">
            {results.seoGaps.map((gap, i) => (
              <div
                key={i}
                className="bg-white p-3 rounded border border-red-100 border-l-4 border-l-red-500 text-sm flex justify-between items-center gap-4"
              >
                <span>{gap}</span>
                <Button variant="ghost" className="text-xs py-0 h-auto text-blue-600 shrink-0">
                  Create Brief
                </Button>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
}
