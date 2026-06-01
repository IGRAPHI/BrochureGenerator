import { useState } from 'react';
import { Copy, Download, Check } from 'lucide-react';
import Button from './Button.jsx';

// Renders AI-generated Markdown as styled HTML
function renderMarkdown(text) {
  return text
    .replace(/^#{3} (.+)$/gm, '<h3>$1</h3>')
    .replace(/^#{2} (.+)$/gm, '<h2>$1</h2>')
    .replace(/^#{1} (.+)$/gm, '<h1>$1</h1>')
    .replace(/^\*\*(.+?)\*\*/gm, '<strong>$1</strong>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>')
    .replace(/^---$/gm, '<hr>')
    .replace(/^\* (.+)$/gm, '<li>$1</li>')
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/^(\d+)\. (.+)$/gm, '<li>$2</li>')
    .replace(/(<li>.*<\/li>\n?)+/g, (m) => `<ul>${m}</ul>`)
    .replace(/\n\n/g, '</p><p>')
    .replace(/^(?!<[h|u|b|l|h])/gm, '')
    .split('\n')
    .map((line) => {
      if (line.match(/^<(h[1-3]|blockquote|ul|hr)/)) return line;
      if (line.trim() === '') return '';
      return `<p>${line}</p>`;
    })
    .join('\n');
}

export default function ContentPreview({ content, filename = 'content' }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleExportHtml = () => {
    const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${filename}</title>
<style>
  body { font-family: Georgia, serif; max-width: 760px; margin: 2rem auto; padding: 0 1.5rem; line-height: 1.7; color: #1e293b; }
  h1 { font-size: 2rem; margin-bottom: 0.5rem; }
  h2 { font-size: 1.5rem; margin-top: 2rem; }
  h3 { font-size: 1.2rem; margin-top: 1.5rem; }
  blockquote { border-left: 4px solid #3b82f6; padding-left: 1rem; font-style: italic; color: #475569; }
  ul { padding-left: 1.5rem; }
</style>
</head>
<body>
${renderMarkdown(content)}
</body>
</html>`;
    const blob = new Blob([html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${filename}.html`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
          Generated Content
        </span>
        <div className="flex gap-2">
          <Button variant="secondary" className="text-xs py-1 px-3 h-auto" onClick={handleCopy} icon={copied ? Check : Copy}>
            {copied ? 'Copied!' : 'Copy'}
          </Button>
          <Button variant="secondary" className="text-xs py-1 px-3 h-auto" onClick={handleExportHtml} icon={Download}>
            Export HTML
          </Button>
        </div>
      </div>
      <div
        className="prose-content bg-white border border-slate-200 rounded-lg p-6 max-h-[520px] overflow-y-auto text-sm"
        dangerouslySetInnerHTML={{ __html: renderMarkdown(content) }}
      />
    </div>
  );
}
