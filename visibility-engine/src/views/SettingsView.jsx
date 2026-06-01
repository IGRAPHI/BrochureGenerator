import { Settings, CheckCircle2, AlertTriangle } from 'lucide-react';
import Card from '../components/Card.jsx';
import Button from '../components/Button.jsx';
import { useSettings } from '../hooks/useSettings.js';

const hasApiKey = () => {
  const key = import.meta.env.VITE_CLAUDE_API_KEY;
  return key && key !== 'sk-ant-your-key-here';
};

export default function SettingsView() {
  const { settings, update, save, saved } = useSettings();

  return (
    <div className="max-w-4xl animate-in fade-in space-y-6">
      <div>
        <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
          <Settings className="w-6 h-6 text-slate-600" /> Platform Settings
        </h2>
        <p className="text-sm text-slate-500">
          Configure global context, brand voice, and AI models for iGraphi.com.
        </p>
      </div>

      {/* API Key Status */}
      <div
        className={`flex items-start gap-3 p-4 rounded-lg border text-sm ${
          hasApiKey()
            ? 'bg-emerald-50 border-emerald-200 text-emerald-800'
            : 'bg-amber-50 border-amber-200 text-amber-800'
        }`}
      >
        {hasApiKey() ? (
          <CheckCircle2 className="w-5 h-5 shrink-0 mt-0.5 text-emerald-500" />
        ) : (
          <AlertTriangle className="w-5 h-5 shrink-0 mt-0.5 text-amber-500" />
        )}
        <div>
          {hasApiKey() ? (
            <span><strong>Claude API key detected.</strong> AI generation is enabled.</span>
          ) : (
            <span>
              <strong>Claude API key not found.</strong> Add{' '}
              <code className="bg-amber-100 px-1 rounded font-mono text-xs">VITE_CLAUDE_API_KEY</code>{' '}
              to your <code className="bg-amber-100 px-1 rounded font-mono text-xs">.env</code> file and restart the dev server.
              AI generation will not work until this is set.
            </span>
          )}
        </div>
      </div>

      <Card className="p-6">
        <h3 className="font-semibold text-slate-800 mb-1 border-b border-slate-100 pb-2">AI Model Preferences</h3>
        <p className="text-xs text-slate-500 mb-4">API keys are managed via environment variables — never stored here.</p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1 uppercase tracking-wider">Primary Writing Engine</label>
            <select
              className="w-full bg-slate-50 border border-slate-200 text-sm rounded-lg p-2.5 focus:ring-2 focus:ring-blue-500"
              value={settings.writingModel}
              onChange={(e) => update('writingModel', e.target.value)}
            >
              <option value="claude-opus-4-8">Claude Opus 4 (Recommended)</option>
              <option value="claude-sonnet-4-6">Claude Sonnet 4</option>
              <option value="claude-haiku-4-5">Claude Haiku 4</option>
            </select>
          </div>
          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1 uppercase tracking-wider">Research &amp; SEO Analysis</label>
            <select
              className="w-full bg-slate-50 border border-slate-200 text-sm rounded-lg p-2.5 focus:ring-2 focus:ring-blue-500"
              value={settings.researchModel}
              onChange={(e) => update('researchModel', e.target.value)}
            >
              <option value="gemini-1.5-pro">Gemini 1.5 Pro (Placeholder)</option>
              <option value="gpt-4o">GPT-4o</option>
            </select>
          </div>
          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1 uppercase tracking-wider">Review &amp; Strategy</label>
            <select
              className="w-full bg-slate-50 border border-slate-200 text-sm rounded-lg p-2.5 focus:ring-2 focus:ring-blue-500"
              value={settings.reviewModel}
              onChange={(e) => update('reviewModel', e.target.value)}
            >
              <option value="gpt-4o">GPT-4o</option>
              <option value="claude-sonnet-4-6">Claude Sonnet 4</option>
            </select>
          </div>
        </div>
      </Card>

      <Card className="p-6">
        <h3 className="font-semibold text-slate-800 mb-4 border-b border-slate-100 pb-2">Brand Context</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Target Website URL</label>
            <input
              type="url"
              className="w-full bg-slate-50 border border-slate-200 text-sm rounded-lg p-2.5 focus:ring-2 focus:ring-blue-500"
              value={settings.targetUrl}
              onChange={(e) => update('targetUrl', e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Brand Voice Directives</label>
            <textarea
              rows={3}
              className="w-full bg-slate-50 border border-slate-200 text-sm rounded-lg p-2.5 focus:ring-2 focus:ring-blue-500"
              value={settings.brandVoice}
              onChange={(e) => update('brandVoice', e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Core Services (comma-separated)</label>
            <input
              type="text"
              className="w-full bg-slate-50 border border-slate-200 text-sm rounded-lg p-2.5 focus:ring-2 focus:ring-blue-500"
              value={settings.coreServices}
              onChange={(e) => update('coreServices', e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Default Call to Action (CTA)</label>
            <input
              type="text"
              className="w-full bg-slate-50 border border-slate-200 text-sm rounded-lg p-2.5 focus:ring-2 focus:ring-blue-500"
              value={settings.defaultCta}
              onChange={(e) => update('defaultCta', e.target.value)}
            />
          </div>
        </div>
        <div className="mt-6 flex items-center justify-end gap-3">
          {saved && (
            <span className="text-sm text-emerald-600 flex items-center gap-1">
              <CheckCircle2 className="w-4 h-4" /> Saved
            </span>
          )}
          <Button icon={CheckCircle2} onClick={save}>Save Settings</Button>
        </div>
      </Card>
    </div>
  );
}
