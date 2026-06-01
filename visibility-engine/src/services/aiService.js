// Claude API — direct browser calls require the header below.
// API key is read from VITE_CLAUDE_API_KEY in your .env file.
// Never hardcode the key here.

const CLAUDE_API_URL = 'https://api.anthropic.com/v1/messages';
const CLAUDE_MODEL = 'claude-opus-4-8';

function getApiKey() {
  const key = import.meta.env.VITE_CLAUDE_API_KEY;
  if (!key || key === 'sk-ant-your-key-here') {
    throw new Error(
      'Claude API key is missing. Add VITE_CLAUDE_API_KEY to your .env file and restart the dev server.'
    );
  }
  return key;
}

async function callClaude(messages, systemPrompt, maxTokens = 2000) {
  const apiKey = getApiKey();

  const response = await fetch(CLAUDE_API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01',
      // Required for direct browser access; acknowledges you own this key
      'anthropic-dangerous-direct-browser-access': 'true',
    },
    body: JSON.stringify({
      model: CLAUDE_MODEL,
      max_tokens: maxTokens,
      system: systemPrompt,
      messages,
    }),
  });

  if (!response.ok) {
    const errBody = await response.json().catch(() => ({}));
    const msg = errBody?.error?.message || `Claude API error: ${response.status} ${response.statusText}`;
    throw new Error(msg);
  }

  const data = await response.json();
  return data.content[0].text;
}

function buildSystemPrompt(brandVoice, coreServices) {
  return `You are a senior content strategist and copywriter for iGraphi, a strategic design agency specialising in international organisations, NGOs, and professional services firms.

Brand Voice: ${brandVoice}
Core Services: ${coreServices}

Writing rules:
- Write in first-person plural (we, our team, at iGraphi)
- Be authoritative but warm; never condescending
- Use concrete, specific language; avoid vague design buzzwords
- Every piece should serve a clear business goal
- Format output in clean Markdown`;
}

export const aiService = {
  async generateSeoBrief(topic, brandVoice, coreServices) {
    if (!topic?.trim()) throw new Error('Topic cannot be empty.');

    const system = buildSystemPrompt(brandVoice, coreServices);
    const userMsg = `Create a detailed SEO content brief for: "${topic}"

Include:
1. **Primary Keyword** (with estimated intent)
2. **Secondary Keywords** (4–6 supporting terms)
3. **Search Intent Analysis** (what is the user trying to accomplish?)
4. **Target Audience Persona**
5. **Recommended Word Count**
6. **Proposed Article Structure** (H1 → H2s → H3s)
7. **Key Points to Cover** (what must this article say to rank and convert?)
8. **Competitor Angle** (how should we differentiate?)
9. **Internal Link Opportunities** (suggest related iGraphi pages/topics)
10. **Call to Action** (specific CTA aligned to goal)`;

    return callClaude([{ role: 'user', content: userMsg }], system, 1600);
  },

  async generateOutline(topic, seoBrief, brandVoice, coreServices) {
    if (!topic?.trim()) throw new Error('Topic cannot be empty.');

    const system = buildSystemPrompt(brandVoice, coreServices);
    const userMsg = `Using the SEO brief below, build a detailed article outline for "${topic}".

SEO Brief:
${seoBrief || '(not provided — use your best judgement)'}

Outline must include:
- Compelling H1 title (keyword-inclusive)
- Introduction concept (hook idea, problem statement)
- 4–6 main sections (H2) each with 2–3 sub-points (H3)
- Suggested pull-quote moments (mark with ⭐)
- Conclusion approach and CTA placement`;

    return callClaude([{ role: 'user', content: userMsg }], system, 1200);
  },

  async generateArticleDraft(topic, outline, brandVoice, coreServices) {
    if (!topic?.trim()) throw new Error('Topic cannot be empty.');

    const system = buildSystemPrompt(brandVoice, coreServices);
    const userMsg = `Write a full, publication-ready blog article.

Topic: ${topic}
Outline:
${outline || '(not provided — structure it appropriately)'}

Requirements:
- 900–1 300 words
- Compelling H1 title
- Engaging introduction with a concrete hook
- Well-structured body using the outline (use ## for H2, ### for H3)
- At least one pull-quote (use > blockquote syntax)
- Practical, real-world examples relevant to NGOs and international organisations
- Strong conclusion with the brand CTA
- Output in clean Markdown`;

    return callClaude([{ role: 'user', content: userMsg }], system, 3500);
  },

  async generateMetaAndSocial(articleContent, brandVoice, coreServices) {
    if (!articleContent?.trim()) throw new Error('Article content cannot be empty.');

    const system = buildSystemPrompt(brandVoice, coreServices);
    const snippet = articleContent.substring(0, 2500);
    const userMsg = `Based on this article excerpt, generate the following assets:

---
${snippet}
---

Provide:
## Meta Title
(50–60 characters, include primary keyword)

## Meta Description
(150–160 characters, compelling with implied CTA)

## LinkedIn Post — Variation 1 (Thought Leadership, 200–250 words)

## LinkedIn Post — Variation 2 (Story / Hook, 150–200 words)

## LinkedIn Post — Variation 3 (Quick Insight, 80–120 words)

## Hashtag Sets
Provide one hashtag set per post (5–7 tags each)`;

    return callClaude([{ role: 'user', content: userMsg }], system, 2200);
  },

  async generateLinkedInPosts(sourceContent, tone, brandVoice, coreServices) {
    if (!sourceContent?.trim()) throw new Error('Source material or topic cannot be empty.');

    const system = buildSystemPrompt(brandVoice, coreServices);
    const userMsg = `Create 3 distinct LinkedIn post variations.

Source material / topic:
${sourceContent}

Requested tone: ${tone}

Rules for each post:
- Do NOT open with "I'm excited to share" or similar clichés
- Start with a concrete hook (a surprising fact, a short story, a bold statement, or a question)
- Use short paragraphs and line breaks for mobile readability
- End with a genuine question or insight that invites engagement
- Include 4–6 hashtags at the end
- Separate variations with ---

Lengths: Variation 1 (200–280 words), Variation 2 (150–200 words), Variation 3 (80–120 words)`;

    return callClaude([{ role: 'user', content: userMsg }], system, 2000);
  },

  async generateCaseStudy(projectDetails, brandVoice, coreServices) {
    const { client, services, challenge, solution, outcome } = projectDetails;
    if (!client?.trim()) throw new Error('Client/organisation name is required.');
    if (!challenge?.trim()) throw new Error('The challenge description is required.');

    const system = buildSystemPrompt(brandVoice, coreServices);
    const userMsg = `Write a polished, publication-ready case study.

Client / Organisation: ${client}
Services Delivered: ${services || 'Design and communications'}
The Challenge: ${challenge}
Our Approach / Solution: ${solution || '(to be inferred from context)'}
Outcome / Impact: ${outcome || '(to be inferred from context)'}

Structure:
## Project Overview (2–3 sentence summary)
## The Challenge
## Our Approach
## The Solution
## The Impact
> (include a pull quote here)
## Key Takeaways (3 bullet points)

Tone: authoritative, specific, results-focused. 650–900 words. Output in Markdown.`;

    return callClaude([{ role: 'user', content: userMsg }], system, 2800);
  },

  // Gemini placeholder — structured for future connection
  analyzeWithGemini: async (_url) => {
    return new Promise((resolve) =>
      setTimeout(
        () =>
          resolve({
            health: 82,
            opportunities: 14,
            primaryAudience: 'International NGOs',
            brandVoice: 'Strategic, clear, warm, professional',
            seoGaps: [
              "Missing dedicated landing page for 'Presentation Design for Executives'",
              "Homepage lacks H2 tags incorporating 'Nonprofit Web Design'",
            ],
          }),
        2000
      )
    );
  },
};
