import { useState } from 'react';
import { CheckCircle2, ChevronRight, Cpu, FileEdit, Loader2, RefreshCw } from 'lucide-react';
import Card from '../components/Card.jsx';
import Button from '../components/Button.jsx';
import ContentPreview from '../components/ContentPreview.jsx';
import ErrorBanner from '../components/ErrorBanner.jsx';
import { aiService } from '../services/aiService.js';
import { useSettings } from '../hooks/useSettings.js';

const STEP_LABELS = ['Topic', 'SEO Brief', 'Outline', 'Article Draft', 'Meta & Social', 'Review & Export'];

export default function BlogGeneratorView() {
  const { settings } = useSettings();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [topic, setTopic] = useState('');
  const [seoBrief, setSeoBrief] = useState('');
  const [outline, setOutline] = useState('');
  const [draft, setDraft] = useState('');
  const [metaSocial, setMetaSocial] = useState('');

  const clearError = () => setError('');

  const withLoading = async (fn) => {
    setLoading(true);
    setError('');
    try {
      await fn();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateBrief = () =>
    withLoading(async () => {
      const result = await aiService.generateSeoBrief(topic, settings.brandVoice, settings.coreServices);
      setSeoBrief(result);
      setStep(2);
    });

  const handleGenerateOutline = () =>
    withLoading(async () => {
      const result = await aiService.generateOutline(topic, seoBrief, settings.brandVoice, settings.coreServices);
      setOutline(result);
      setStep(3);
    });

  const handleGenerateDraft = () =>
    withLoading(async () => {
      const result = await aiService.generateArticleDraft(topic, outline, settings.brandVoice, settings.coreServices);
      setDraft(result);
      setStep(4);
    });

  const handleGenerateMeta = () =>
    withLoading(async () => {
      const result = await aiService.generateMetaAndSocial(draft, settings.brandVoice, settings.coreServices);
      setMetaSocial(result);
      setStep(5);
    });

  const handleReset = () => {
    setStep(1); setTopic(''); setSeoBrief(''); setOutline(''); setDraft(''); setMetaSocial(''); setError('');
  };

  return (
    <div className="max-w-5xl animate-in fade-in space-y-6">
      <div>
        <h2 className="text-xl font-bold text-slate-900">AI Blog Article Generator</h2>
        <p className="text-sm text-slate-500">Powered by Claude — configure model in Settings</p>
      </div>

      {/* Progress steps */}
      <div className="flex">
        {STEP_LABELS.map((label, i) => (
          <div key={i} className="flex-1 text-center relative">
            <div
              className={`w-8 h-8 mx-auto rounded-full flex items-center justify-center text-sm font-bold border-2 relative z-10 ${
                step > i + 1
                  ? 'bg-blue-600 border-blue-600 text-white'
                  : step === i + 1
                  ? 'bg-white border-blue-600 text-blue-600 ring-4 ring-blue-100'
                  : 'bg-slate-50 border-slate-200 text-slate-400'
              }`}
            >
              {step > i + 1 ? <CheckCircle2 className="w-4 h-4" /> : i + 1}
            </div>
            <div className={`text-xs font-medium mt-1 hidden sm:block ${step === i + 1 ? 'text-blue-600' : 'text-slate-400'}`}>
              {label}
            </div>
            {i < STEP_LABELS.length - 1 && (
              <div className={`absolute top-4 left-1/2 w-full h-0.5 -z-0 ${step > i + 1 ? 'bg-blue-600' : 'bg-slate-200'}`} />
            )}
          </div>
        ))}
      </div>

      <ErrorBanner message={error} onDismiss={clearError} />

      <Card className="p-6 sm:p-8 shadow-sm">
        {step === 1 && (
          <div className="space-y-4 animate-in fade-in">
            <h3 className="text-lg font-semibold text-slate-900">What do you want to write about?</h3>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Topic or title idea</label>
              <input
                type="text"
                className="w-full bg-slate-50 border border-slate-200 text-slate-900 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 block p-3"
                placeholder="e.g., How visual storytelling impacts NGO fundraising…"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && topic.trim() && handleGenerateBrief()}
              />
            </div>
            <div className="flex justify-end">
              <Button onClick={handleGenerateBrief} disabled={!topic.trim() || loading} icon={loading ? Loader2 : Cpu}>
                {loading ? 'Generating Brief…' : 'Generate SEO Brief'}
              </Button>
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="space-y-4 animate-in fade-in">
            <h3 className="text-lg font-semibold text-slate-900">SEO Brief</h3>
            <p className="text-sm text-slate-500">Review and edit the brief before generating the outline.</p>
            <textarea
              rows={14}
              className="w-full bg-slate-50 border border-slate-200 text-slate-800 text-sm font-mono rounded-lg p-4 focus:ring-2 focus:ring-blue-500"
              value={seoBrief}
              onChange={(e) => setSeoBrief(e.target.value)}
            />
            <div className="flex justify-between gap-3">
              <Button variant="secondary" onClick={() => setStep(1)}>Back</Button>
              <Button onClick={handleGenerateOutline} disabled={loading} icon={loading ? Loader2 : ChevronRight}>
                {loading ? 'Generating Outline…' : 'Generate Outline'}
              </Button>
            </div>
          </div>
        )}

        {step === 3 && (
          <div className="space-y-4 animate-in fade-in">
            <h3 className="text-lg font-semibold text-slate-900">Article Outline</h3>
            <p className="text-sm text-slate-500">Adjust the structure before generating the full draft.</p>
            <textarea
              rows={14}
              className="w-full bg-slate-50 border border-slate-200 text-slate-800 text-sm font-mono rounded-lg p-4 focus:ring-2 focus:ring-blue-500"
              value={outline}
              onChange={(e) => setOutline(e.target.value)}
            />
            <div className="flex justify-between gap-3">
              <Button variant="secondary" onClick={() => setStep(2)}>Back</Button>
              <Button onClick={handleGenerateDraft} disabled={loading} icon={loading ? Loader2 : Cpu}>
                {loading ? 'Writing Draft…' : 'Generate Article Draft'}
              </Button>
            </div>
          </div>
        )}

        {step === 4 && (
          <div className="space-y-4 animate-in fade-in">
            <h3 className="text-lg font-semibold text-slate-900">Article Draft</h3>
            {loading ? (
              <div className="flex flex-col items-center justify-center py-16 text-slate-400 gap-3">
                <RefreshCw className="w-8 h-8 animate-spin" />
                <p className="text-sm">Claude is writing the draft in your brand voice…</p>
              </div>
            ) : (
              <>
                <ContentPreview content={draft} filename={topic.slice(0, 40).replace(/\s+/g, '-')} />
                <div className="flex justify-between gap-3 pt-2">
                  <Button variant="secondary" onClick={() => setStep(3)}>Back to Outline</Button>
                  <Button onClick={handleGenerateMeta} disabled={loading} icon={loading ? Loader2 : Cpu}>
                    {loading ? 'Generating…' : 'Generate Meta & Social Posts'}
                  </Button>
                </div>
              </>
            )}
          </div>
        )}

        {step === 5 && (
          <div className="space-y-4 animate-in fade-in">
            <h3 className="text-lg font-semibold text-slate-900">Meta Data &amp; LinkedIn Posts</h3>
            {loading ? (
              <div className="flex flex-col items-center justify-center py-16 text-slate-400 gap-3">
                <RefreshCw className="w-8 h-8 animate-spin" />
                <p className="text-sm">Generating meta tags and social posts…</p>
              </div>
            ) : (
              <>
                <ContentPreview content={metaSocial} filename="meta-and-social" />
                <div className="flex justify-between gap-3 pt-2">
                  <Button variant="secondary" onClick={() => setStep(4)}>Back to Draft</Button>
                  <Button onClick={() => setStep(6)} icon={CheckCircle2}>Approve &amp; Finish</Button>
                </div>
              </>
            )}
          </div>
        )}

        {step === 6 && (
          <div className="text-center py-10 animate-in zoom-in-95 fade-in">
            <div className="w-20 h-20 bg-emerald-100 rounded-full flex items-center justify-center text-emerald-600 mx-auto mb-6">
              <CheckCircle2 size={40} />
            </div>
            <h3 className="text-2xl font-bold text-slate-900 mb-2">Content Ready!</h3>
            <p className="text-slate-500 mb-8">
              Article, meta data, and LinkedIn posts have been generated and saved locally.
            </p>
            <div className="flex flex-wrap justify-center gap-3">
              <Button variant="secondary" onClick={() => setStep(4)} icon={FileEdit}>Review Draft</Button>
              <Button variant="secondary" onClick={() => setStep(5)} icon={FileEdit}>Review Social</Button>
              <Button variant="outline" onClick={handleReset}>Start New Article</Button>
            </div>
          </div>
        )}
      </Card>
    </div>
  );
}
