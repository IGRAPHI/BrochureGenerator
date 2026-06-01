import { AlertCircle, X } from 'lucide-react';

export default function ErrorBanner({ message, onDismiss }) {
  if (!message) return null;
  return (
    <div className="flex items-start gap-3 p-4 bg-red-50 border border-red-200 rounded-lg text-red-800 text-sm">
      <AlertCircle className="w-5 h-5 shrink-0 mt-0.5 text-red-500" />
      <span className="flex-1">{message}</span>
      {onDismiss && (
        <button onClick={onDismiss} className="text-red-400 hover:text-red-600 ml-2">
          <X className="w-4 h-4" />
        </button>
      )}
    </div>
  );
}
