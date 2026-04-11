const pptxgen = require('pptxgenjs');
const fs = require('fs');

const data = JSON.parse(fs.readFileSync('/tmp/bw_analysis_summary.json', 'utf8'));
const pptx = new pptxgen();

// Theme
const BG = '03242D';
const GREEN = '45cd98';
const GOLD = 'ffc572';
const RED = 'f54943';
const WHITE = 'e8f0f2';
const MUTED = '7a9aa8';
const DARK2 = '0a3d4a';

pptx.layout = 'LAYOUT_16x9';
pptx.author = 'BetonWin AI';
pptx.subject = 'QA Analysis Report';

// ==================== SLIDE 1: COVER ====================
let slide = pptx.addSlide();
slide.background = { color: BG };
slide.addText('BetonWin AI Support', { x: 0.8, y: 1.5, w: 8.4, h: 1, fontSize: 36, fontFace: 'Helvetica', color: WHITE, bold: true });
slide.addText('Agent Performance Report', { x: 0.8, y: 2.4, w: 8.4, h: 0.6, fontSize: 22, fontFace: 'Helvetica', color: GREEN });
slide.addText('March 28 — April 1, 2026  |  4-Day Analysis', { x: 0.8, y: 3.2, w: 8.4, h: 0.4, fontSize: 14, fontFace: 'Helvetica', color: MUTED });
slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 0.8, y: 4.2, w: 2.5, h: 0.05, fill: { color: GREEN } });
slide.addText('10 Specialized AI Agents  •  n8n Backend  •  Zendesk Integration', { x: 0.8, y: 4.6, w: 8, h: 0.4, fontSize: 11, fontFace: 'Helvetica', color: MUTED });

// ==================== SLIDE 2: EXECUTIVE SUMMARY ====================
slide = pptx.addSlide();
slide.background = { color: BG };
slide.addText('Executive Summary', { x: 0.8, y: 0.4, w: 8, h: 0.6, fontSize: 24, fontFace: 'Helvetica', color: WHITE, bold: true });
slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 0.8, y: 0.95, w: 1.5, h: 0.04, fill: { color: GREEN } });

// 4 stat boxes
const stats = [
  { val: '137', label: 'Total Messages', color: GREEN },
  { val: '32', label: 'Unique Sessions', color: GREEN },
  { val: '0%', label: 'Error Rate', color: GREEN },
  { val: '0', label: 'Escalations', color: RED },
];
stats.forEach((s, i) => {
  const x = 0.8 + i * 2.25;
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x, y: 1.4, w: 2, h: 1.4, fill: { color: DARK2 }, rectRadius: 0.1 });
  slide.addText(s.val, { x, y: 1.5, w: 2, h: 0.7, fontSize: 32, fontFace: 'Helvetica', color: s.color, bold: true, align: 'center' });
  slide.addText(s.label, { x, y: 2.15, w: 2, h: 0.4, fontSize: 11, fontFace: 'Helvetica', color: MUTED, align: 'center' });
});

// Key findings
slide.addText('Key Findings', { x: 0.8, y: 3.2, w: 8, h: 0.4, fontSize: 14, fontFace: 'Helvetica', color: WHITE, bold: true });
const findings = [
  { icon: '✅', text: 'System 100% stable — zero execution errors in 137 requests', color: GREEN },
  { icon: '⚠️', text: 'Escalation to human agent NOT working — 5 attempts, 0 successful', color: GOLD },
  { icon: '⚠️', text: 'Knowledge Base used in only 18% of queries — AI relies on training data', color: GOLD },
  { icon: '🔴', text: 'Zero live agent escalations in 4 days — critical feature gap', color: RED },
];
findings.forEach((f, i) => {
  slide.addText(`${f.icon}  ${f.text}`, { x: 0.8, y: 3.7 + i * 0.4, w: 8.4, h: 0.35, fontSize: 11, fontFace: 'Helvetica', color: f.color });
});

// ==================== SLIDE 3: VOLUME & ACTIVITY ====================
slide = pptx.addSlide();
slide.background = { color: BG };
slide.addText('Volume & Activity Pattern', { x: 0.8, y: 0.4, w: 8, h: 0.6, fontSize: 24, fontFace: 'Helvetica', color: WHITE, bold: true });
slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 0.8, y: 0.95, w: 1.5, h: 0.04, fill: { color: GREEN } });

// Daily breakdown
slide.addText('Daily Message Volume', { x: 0.8, y: 1.3, w: 4, h: 0.4, fontSize: 13, fontFace: 'Helvetica', color: WHITE, bold: true });
const daily = Object.entries(data.daily);
daily.forEach(([day, count], i) => {
  const x = 0.8;
  const y = 1.8 + i * 0.55;
  const barW = (count / 80) * 4;
  slide.addText(day, { x, y, w: 1.8, h: 0.4, fontSize: 10, fontFace: 'Helvetica', color: MUTED });
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: x + 1.8, y: y + 0.08, w: barW, h: 0.25, fill: { color: GREEN }, rectRadius: 0.03 });
  slide.addText(`${count}`, { x: x + 1.8 + barW + 0.1, y, w: 0.5, h: 0.4, fontSize: 10, fontFace: 'Helvetica', color: WHITE, bold: true });
});

// Hourly heatmap
slide.addText('Hourly Distribution (UTC)', { x: 5.5, y: 1.3, w: 4, h: 0.4, fontSize: 13, fontFace: 'Helvetica', color: WHITE, bold: true });
const hourly = data.hourly;
const maxH = Math.max(...Object.values(hourly));
let hy = 1.8;
for (let h = 7; h <= 23; h++) {
  const count = hourly[h] || 0;
  if (count === 0) continue;
  const barW = (count / maxH) * 3;
  slide.addText(`${h}:00`, { x: 5.5, y: hy, w: 0.8, h: 0.3, fontSize: 9, fontFace: 'Helvetica', color: MUTED });
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 6.3, y: hy + 0.05, w: barW, h: 0.2, fill: { color: count > 15 ? GREEN : DARK2 }, rectRadius: 0.02 });
  slide.addText(`${count}`, { x: 6.3 + barW + 0.1, y: hy, w: 0.4, h: 0.3, fontSize: 9, fontFace: 'Helvetica', color: WHITE });
  hy += 0.3;
}

// Session stats
slide.addText('Session Depth', { x: 0.8, y: 3.8, w: 4, h: 0.4, fontSize: 13, fontFace: 'Helvetica', color: WHITE, bold: true });
slide.addText(`Average: ${data.avg_per_session} messages/session`, { x: 0.8, y: 4.2, w: 4, h: 0.3, fontSize: 11, fontFace: 'Helvetica', color: MUTED });
slide.addText(`Longest session: ${data.session_lengths[0]} messages`, { x: 0.8, y: 4.5, w: 4, h: 0.3, fontSize: 11, fontFace: 'Helvetica', color: MUTED });
slide.addText(`Deep conversations (6+ turns): 31%`, { x: 0.8, y: 4.8, w: 4, h: 0.3, fontSize: 11, fontFace: 'Helvetica', color: GREEN });

// ==================== SLIDE 4: LANGUAGE & TOPICS ====================
slide = pptx.addSlide();
slide.background = { color: BG };
slide.addText('Language & Topic Distribution', { x: 0.8, y: 0.4, w: 8, h: 0.6, fontSize: 24, fontFace: 'Helvetica', color: WHITE, bold: true });
slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 0.8, y: 0.95, w: 1.5, h: 0.04, fill: { color: GREEN } });

// Languages
slide.addText('Languages', { x: 0.8, y: 1.3, w: 3.5, h: 0.4, fontSize: 13, fontFace: 'Helvetica', color: WHITE, bold: true });
const langs = [
  { name: 'Spanish', pct: 82, count: 113 },
  { name: 'Italian', pct: 15, count: 20 },
  { name: 'English', pct: 2, count: 3 },
  { name: 'Portuguese', pct: 1, count: 1 },
];
langs.forEach((l, i) => {
  const y = 1.8 + i * 0.5;
  slide.addText(l.name, { x: 0.8, y, w: 1.5, h: 0.35, fontSize: 10, fontFace: 'Helvetica', color: WHITE });
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 2.3, y: y + 0.05, w: (l.pct / 100) * 2, h: 0.25, fill: { color: GREEN }, rectRadius: 0.03 });
  slide.addText(`${l.pct}%`, { x: 2.3 + (l.pct / 100) * 2 + 0.1, y, w: 0.6, h: 0.35, fontSize: 10, fontFace: 'Helvetica', color: MUTED });
});

// Topics
slide.addText('Topic Breakdown', { x: 5.2, y: 1.3, w: 4, h: 0.4, fontSize: 13, fontFace: 'Helvetica', color: WHITE, bold: true });
const topics = [
  { name: 'General/Follow-up', pct: 39, color: MUTED },
  { name: 'Greetings/Tests', pct: 22, color: MUTED },
  { name: 'Deposits', pct: 14, color: GREEN },
  { name: 'Account/Closure', pct: 9, color: GOLD },
  { name: 'Withdrawals', pct: 9, color: GOLD },
  { name: 'Sports Betting', pct: 3, color: MUTED },
  { name: 'Casino/Slots', pct: 3, color: MUTED },
  { name: 'KYC/Verification', pct: 1, color: MUTED },
];
topics.forEach((t, i) => {
  const y = 1.8 + i * 0.4;
  slide.addText(t.name, { x: 5.2, y, w: 2, h: 0.3, fontSize: 9.5, fontFace: 'Helvetica', color: WHITE });
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 7.2, y: y + 0.04, w: (t.pct / 40) * 2, h: 0.22, fill: { color: t.color }, rectRadius: 0.02 });
  slide.addText(`${t.pct}%`, { x: 7.2 + (t.pct / 40) * 2 + 0.08, y, w: 0.5, h: 0.3, fontSize: 9, fontFace: 'Helvetica', color: MUTED });
});

// ==================== SLIDE 5: CRITICAL ISSUES ====================
slide = pptx.addSlide();
slide.background = { color: BG };
slide.addText('Critical Issues Found', { x: 0.8, y: 0.4, w: 8, h: 0.6, fontSize: 24, fontFace: 'Helvetica', color: RED, bold: true });
slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 0.8, y: 0.95, w: 1.5, h: 0.04, fill: { color: RED } });

// Issue 1
slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 0.8, y: 1.3, w: 8.4, h: 1.5, fill: { color: DARK2 }, rectRadius: 0.1 });
slide.addText('🔴  ISSUE #1: Escalation to Human Agent Not Working', { x: 1.1, y: 1.4, w: 7.8, h: 0.35, fontSize: 13, fontFace: 'Helvetica', color: RED, bold: true });
slide.addText([
  'A user wrote "human" 4 times and "quiero hablar con un agente no con un bot"',
  'but the bot NEVER escalated. It kept saying "let me try to help you first."',
  '',
  'Root cause: The n8n AI agents do not produce the WANTS_HUMAN signal.',
  'The widget\'s humanRequestCount never reaches threshold (3).',
  'Result: Users who need a human are stuck talking to the bot forever.'
].join('\n'), { x: 1.1, y: 1.8, w: 7.8, h: 0.9, fontSize: 10, fontFace: 'Helvetica', color: MUTED, lineSpacing: 14 });

// Issue 2
slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 0.8, y: 3.0, w: 8.4, h: 1.2, fill: { color: DARK2 }, rectRadius: 0.1 });
slide.addText('🔴  ISSUE #2: Knowledge Base Hit Rate Only 18%', { x: 1.1, y: 3.1, w: 7.8, h: 0.35, fontSize: 13, fontFace: 'Helvetica', color: GOLD, bold: true });
slide.addText([
  '82% of user queries had NO knowledge base context — the AI answered from',
  'training data alone. This means FAQ content is not being utilized.',
  '',
  'Likely causes: KB search timeout (3.5s), poor query matching, or missing FAQ entries.'
].join('\n'), { x: 1.1, y: 3.5, w: 7.8, h: 0.7, fontSize: 10, fontFace: 'Helvetica', color: MUTED, lineSpacing: 14 });

// Issue 3
slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 0.8, y: 4.4, w: 8.4, h: 0.8, fill: { color: DARK2 }, rectRadius: 0.1 });
slide.addText('⚠️  ISSUE #3: Sensitive Requests Not Escalated', { x: 1.1, y: 4.5, w: 7.8, h: 0.35, fontSize: 13, fontFace: 'Helvetica', color: GOLD, bold: true });
slide.addText('Account closure for gambling problems and fraud accusations ("es una estafa") handled by bot only — no human escalation triggered.', { x: 1.1, y: 4.85, w: 7.8, h: 0.3, fontSize: 10, fontFace: 'Helvetica', color: MUTED });

// ==================== SLIDE 6: CONVERSATION EXAMPLES ====================
slide = pptx.addSlide();
slide.background = { color: BG };
slide.addText('Real Conversation Examples', { x: 0.8, y: 0.4, w: 8, h: 0.6, fontSize: 24, fontFace: 'Helvetica', color: WHITE, bold: true });
slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 0.8, y: 0.95, w: 1.5, h: 0.04, fill: { color: GREEN } });

// Good example
slide.addText('✅  Good Response — Deposit Process', { x: 0.8, y: 1.3, w: 8, h: 0.35, fontSize: 12, fontFace: 'Helvetica', color: GREEN, bold: true });
slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 0.8, y: 1.7, w: 8.4, h: 1.0, fill: { color: DARK2 }, rectRadius: 0.08 });
slide.addText('User: "¿Me pueden explicar paso a paso cómo hacer un depósito?"', { x: 1.1, y: 1.75, w: 7.8, h: 0.3, fontSize: 10, fontFace: 'Helvetica', color: GREEN, italic: true });
slide.addText('Bot: Provided detailed step-by-step instructions with payment methods, minimum amounts, and processing times. Response: 450+ chars, well-structured.', { x: 1.1, y: 2.1, w: 7.8, h: 0.4, fontSize: 10, fontFace: 'Helvetica', color: MUTED });

// Bad example
slide.addText('🔴  Failed Response — Human Request', { x: 0.8, y: 2.9, w: 8, h: 0.35, fontSize: 12, fontFace: 'Helvetica', color: RED, bold: true });
slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 0.8, y: 3.3, w: 8.4, h: 1.2, fill: { color: DARK2 }, rectRadius: 0.08 });
slide.addText('User: "quiero hablar con un agente no con un bot"', { x: 1.1, y: 3.35, w: 7.8, h: 0.3, fontSize: 10, fontFace: 'Helvetica', color: RED, italic: true });
slide.addText('Bot: "Comprendo tu preferencia. Aunque soy un bot, puedo responder muchas preguntas sobre BetonWin..."', { x: 1.1, y: 3.7, w: 7.8, h: 0.3, fontSize: 10, fontFace: 'Helvetica', color: MUTED, italic: true });
slide.addText('⛔ User explicitly requested human 5 times across the session. Bot never escalated.', { x: 1.1, y: 4.1, w: 7.8, h: 0.3, fontSize: 10, fontFace: 'Helvetica', color: RED });

// Sensitive example
slide.addText('⚠️  Sensitive — Gambling Problem', { x: 0.8, y: 4.7, w: 8, h: 0.35, fontSize: 12, fontFace: 'Helvetica', color: GOLD, bold: true });
slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 0.8, y: 5.05, w: 4, h: 0.4, fill: { color: DARK2 }, rectRadius: 0.08 });
slide.addText('User: "Quiero cerrar mi cuenta porque tengo problemas con el juego"', { x: 1.1, y: 5.1, w: 3.7, h: 0.3, fontSize: 9, fontFace: 'Helvetica', color: GOLD, italic: true });
slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 5.2, y: 5.05, w: 4, h: 0.4, fill: { color: DARK2 }, rectRadius: 0.08 });
slide.addText('Bot provided Gamblers Anonymous link + self-exclusion info. Good content but should escalate to human.', { x: 5.4, y: 5.1, w: 3.7, h: 0.3, fontSize: 9, fontFace: 'Helvetica', color: MUTED });

// ==================== SLIDE 7: KB ANALYSIS ====================
slide = pptx.addSlide();
slide.background = { color: BG };
slide.addText('Knowledge Base Gap Analysis', { x: 0.8, y: 0.4, w: 8, h: 0.6, fontSize: 24, fontFace: 'Helvetica', color: WHITE, bold: true });
slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 0.8, y: 0.95, w: 1.5, h: 0.04, fill: { color: GREEN } });

// Stats
slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 0.8, y: 1.3, w: 3.5, h: 1.2, fill: { color: DARK2 }, rectRadius: 0.1 });
slide.addText('18%', { x: 0.8, y: 1.35, w: 3.5, h: 0.6, fontSize: 42, fontFace: 'Helvetica', color: RED, bold: true, align: 'center' });
slide.addText('of queries had KB context', { x: 0.8, y: 1.95, w: 3.5, h: 0.3, fontSize: 11, fontFace: 'Helvetica', color: MUTED, align: 'center' });

slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 4.6, y: 1.3, w: 3.5, h: 1.2, fill: { color: DARK2 }, rectRadius: 0.1 });
slide.addText('82%', { x: 4.6, y: 1.35, w: 3.5, h: 0.6, fontSize: 42, fontFace: 'Helvetica', color: GOLD, bold: true, align: 'center' });
slide.addText('AI answered without FAQ', { x: 4.6, y: 1.95, w: 3.5, h: 0.3, fontSize: 11, fontFace: 'Helvetica', color: MUTED, align: 'center' });

// Missing FAQ topics
slide.addText('Missing FAQ Entries (based on user queries)', { x: 0.8, y: 2.8, w: 8, h: 0.4, fontSize: 13, fontFace: 'Helvetica', color: WHITE, bold: true });
const missing = [
  'Step-by-step deposit instructions for each payment method',
  'Available payment methods with limits and processing times',
  'How slots/casino games work (RTP, volatility explained)',
  'How to change interface language',
  'Phone number verification process',
  'Account closure process and implications',
  'Self-exclusion and responsible gambling tools',
  'Sports betting: combined bets, live betting rules',
  'Why withdrawals get cancelled/delayed',
  'How to reopen a closed account',
];
missing.forEach((m, i) => {
  const x = i < 5 ? 0.8 : 5.2;
  const y = 3.3 + (i % 5) * 0.35;
  slide.addText(`•  ${m}`, { x, y, w: 4.2, h: 0.3, fontSize: 9.5, fontFace: 'Helvetica', color: MUTED });
});

// ==================== SLIDE 8: RECOMMENDATIONS ====================
slide = pptx.addSlide();
slide.background = { color: BG };
slide.addText('Recommendations & Next Steps', { x: 0.8, y: 0.4, w: 8, h: 0.6, fontSize: 24, fontFace: 'Helvetica', color: WHITE, bold: true });
slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 0.8, y: 0.95, w: 1.5, h: 0.04, fill: { color: GREEN } });

const recs = [
  { priority: 'P0', title: 'Fix escalation detection', desc: 'Update n8n AI agents to produce WANTS_HUMAN action tag. Add widget-side keyword detection for "human", "agente", "operatore" as direct triggers.', color: RED },
  { priority: 'P0', title: 'Add gambling sensitivity escalation', desc: 'Auto-escalate to human when user mentions gambling addiction, self-exclusion, or account closure due to gambling problems. Required for regulatory compliance.', color: RED },
  { priority: 'P1', title: 'Expand Knowledge Base', desc: 'Add 10+ missing FAQ entries identified from real user queries. Focus on deposits, payments, slot mechanics, and account management.', color: GOLD },
  { priority: 'P1', title: 'Improve KB search performance', desc: 'Current 18% hit rate is too low. Consider: caching warm queries, increasing timeout to 5s, adding synonym matching.', color: GOLD },
  { priority: 'P2', title: 'Add fraud/complaint detection', desc: 'Keywords like "estafa", "manipulado", "scam" should trigger immediate human escalation with high priority.', color: GREEN },
  { priority: 'P2', title: 'Connect deposit verification flow', desc: 'Enable the VERIFY endpoint so bot can check deposit status directly instead of saying "I don\'t have access."', color: GREEN },
  { priority: 'P3', title: 'Monitor conversation depth', desc: 'Sessions with 10+ messages may indicate user frustration. Consider auto-offering escalation after 8 turns.', color: MUTED },
  { priority: 'P3', title: 'Add analytics tracking', desc: 'Implement event tracking (currently stubbed) to measure: response time, satisfaction, escalation rate, topic distribution.', color: MUTED },
];

recs.forEach((r, i) => {
  const y = 1.3 + i * 0.52;
  // Priority badge
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 0.8, y: y + 0.02, w: 0.45, h: 0.3, fill: { color: r.color }, rectRadius: 0.05 });
  slide.addText(r.priority, { x: 0.8, y: y, w: 0.45, h: 0.35, fontSize: 9, fontFace: 'Helvetica', color: r.priority === 'P3' ? '333333' : 'ffffff', bold: true, align: 'center' });
  slide.addText(r.title, { x: 1.4, y: y, w: 2.5, h: 0.35, fontSize: 11, fontFace: 'Helvetica', color: WHITE, bold: true });
  slide.addText(r.desc, { x: 4, y: y, w: 5.8, h: 0.4, fontSize: 9, fontFace: 'Helvetica', color: MUTED, lineSpacing: 12 });
});

// ==================== SLIDE 9: OVERALL VERDICT ====================
slide = pptx.addSlide();
slide.background = { color: BG };
slide.addText('Overall Assessment', { x: 0.8, y: 0.4, w: 8, h: 0.6, fontSize: 24, fontFace: 'Helvetica', color: WHITE, bold: true });
slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 0.8, y: 0.95, w: 1.5, h: 0.04, fill: { color: GREEN } });

// Score
slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 3, y: 1.5, w: 4, h: 2, fill: { color: DARK2 }, rectRadius: 0.15 });
slide.addText('7/10', { x: 3, y: 1.6, w: 4, h: 1, fontSize: 54, fontFace: 'Helvetica', color: GOLD, bold: true, align: 'center' });
slide.addText('Agent Performance Score', { x: 3, y: 2.5, w: 4, h: 0.4, fontSize: 13, fontFace: 'Helvetica', color: MUTED, align: 'center' });
slide.addText('Stable & responsive, but escalation is broken', { x: 3, y: 2.9, w: 4, h: 0.3, fontSize: 10, fontFace: 'Helvetica', color: MUTED, align: 'center' });

// Verdict items
const verdicts = [
  { cat: 'Stability', score: '10/10', desc: 'Zero errors in 137 executions', color: GREEN },
  { cat: 'Response Quality', score: '8/10', desc: 'Detailed, helpful answers in most cases', color: GREEN },
  { cat: 'Language Handling', score: '7/10', desc: 'Works for ES/IT, limited EN/PT testing', color: GOLD },
  { cat: 'Knowledge Base', score: '4/10', desc: '18% hit rate — most queries unanswered by KB', color: RED },
  { cat: 'Escalation', score: '1/10', desc: 'Completely broken — zero successful escalations', color: RED },
  { cat: 'Compliance', score: '5/10', desc: 'Gambling problem requests not auto-escalated', color: GOLD },
];
verdicts.forEach((v, i) => {
  const y = 3.7 + i * 0.35;
  slide.addText(v.cat, { x: 0.8, y, w: 2, h: 0.3, fontSize: 10, fontFace: 'Helvetica', color: WHITE });
  slide.addText(v.score, { x: 2.8, y, w: 0.8, h: 0.3, fontSize: 10, fontFace: 'Helvetica', color: v.color, bold: true });
  slide.addText(v.desc, { x: 3.8, y, w: 5.8, h: 0.3, fontSize: 9.5, fontFace: 'Helvetica', color: MUTED });
});

// Save
const outPath = '/Users/serhiykorenyev/Desktop/vs code/widget cs/BetonWin_AI_Agent_Report.pptx';
pptx.writeFile({ fileName: outPath }).then(() => {
  console.log('PPTX saved:', outPath);
}).catch(err => console.error(err));
