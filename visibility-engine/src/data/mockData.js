export const KEYWORD_CLUSTERS = [
  {
    topic: 'Graphic design for international organizations',
    keywords: ['NGO graphic design', 'development sector branding', 'global health design'],
    intent: 'Transactional / Informational',
    type: 'Pillar Page',
    priority: 'High',
  },
  {
    topic: 'PowerPoint presentation design',
    keywords: ['executive slide decks', 'investor pitch deck design', 'conference presentation design'],
    intent: 'Transactional',
    type: 'Service Page',
    priority: 'High',
  },
  {
    topic: 'Annual report design',
    keywords: ['nonprofit annual reports', 'impact report design', 'interactive digital reports'],
    intent: 'Commercial',
    type: 'Case Study / Portfolio',
    priority: 'Medium',
  },
  {
    topic: 'Visual storytelling',
    keywords: ['data visualization for NGOs', 'infographic design', 'storytelling through design'],
    intent: 'Informational',
    type: 'Blog Article',
    priority: 'High',
  },
  {
    topic: 'AI-assisted communication design',
    keywords: ['AI in graphic design', 'efficient design workflows', 'AI for corporate communications'],
    intent: 'Informational',
    type: 'Blog Article',
    priority: 'Low',
  },
];

export const CONTENT_CALENDAR = [
  {
    title: 'Transforming Data into Impact: Visual Storytelling for NGOs',
    audience: 'Comms Directors',
    goal: 'Thought Leadership',
    keyword: 'Visual storytelling',
    status: 'draft',
    type: 'Blog',
  },
  {
    title: '5 Things Your Annual Report Must Have in 2026',
    audience: 'Executive Directors',
    goal: 'Lead Gen',
    keyword: 'Annual report design',
    status: 'ready',
    type: 'LinkedIn',
  },
  {
    title: 'Global Health Initiative: Rebrand Case Study',
    audience: 'Program Managers',
    goal: 'Proof of Competence',
    keyword: 'NGO graphic design',
    status: 'published',
    type: 'Case Study',
  },
  {
    title: 'Q3 Insights: The Future of AI in Design',
    audience: 'Current Clients',
    goal: 'Retention',
    keyword: 'AI-assisted communication design',
    status: 'idea',
    type: 'Newsletter',
  },
];

export const PUBLISHING_QUEUE = [
  {
    title: 'Why Your Pitch Deck is Failing (And How to Fix It)',
    type: 'LinkedIn Post',
    status: 'Ready to Publish',
    updated: '2 hours ago',
  },
  {
    title: 'The Anatomy of a Perfect Annual Report',
    type: 'Blog Article',
    status: 'Needs Review',
    updated: '5 hours ago',
  },
  {
    title: 'UN Environment Program Redesign',
    type: 'Case Study',
    status: 'Draft',
    updated: '1 day ago',
  },
];

export const DEFAULT_SETTINGS = {
  targetUrl: 'https://igraphi.com',
  brandVoice:
    'Strategic, clear, warm, professional, and focused on helping organizations turn complex ideas into impactful design. Avoid agency buzzwords. Be authoritative but accessible.',
  coreServices:
    'Graphic design for international organizations, PowerPoint presentation design, Annual report design, Nonprofit web design, Visual storytelling',
  defaultCta:
    'Need help turning your complex data into a clear visual story? Contact the team at iGraphi today.',
  writingModel: 'claude-opus-4-8',
  researchModel: 'gemini-1.5-pro',
  reviewModel: 'gpt-4o',
};
