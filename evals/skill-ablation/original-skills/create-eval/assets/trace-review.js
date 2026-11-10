'use strict';
const $ = id => document.getElementById(id);
const token = location.hash.slice(1) || sessionStorage.getItem('trace-review-token');
if (token) sessionStorage.setItem('trace-review-token', token);
history.replaceState(null, '', '/');
let rows = [], reviews = [], index = 0, currentReview = null, dirty = false, busy = false;
const fields = ['reviewer', 'scope', 'verdict', 'notes', 'correction', 'rubric'];

async function api(path, body) {
  const response = await fetch(path, {method: body ? 'POST' : 'GET', headers: {
    Authorization: `Bearer ${token || ''}`, 'Content-Type': 'application/json'
  }, ...(body ? {body: JSON.stringify(body)} : {})});
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || 'Request failed');
  return result;
}
function element(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = String(text);
  if (className) node.className = className;
  return node;
}
function renderValue(value, depth = 0) {
  if (value === null || typeof value !== 'object') return element('div', value === null ? 'null' : value, 'text');
  if (depth > 8) return element('pre', JSON.stringify(value, null, 2));
  const container = element('div');
  for (const [key, child] of Object.entries(value)) {
    if (child !== null && typeof child === 'object') {
      const details = element('details');
      details.append(element('summary', `${key} · ${Array.isArray(child) ? `${child.length} items` : 'details'}`));
      const nested = renderValue(child, depth + 1); nested.classList.add('value');
      details.append(nested); container.append(details);
    } else {
      container.append(element('div', key, 'key'), renderValue(child, depth + 1));
    }
  }
  return container;
}
function section(title, value, collapsed = false) {
  if (value === undefined) return;
  const root = element(collapsed ? 'details' : 'section');
  root.append(element(collapsed ? 'summary' : 'h3', title), renderValue(value));
  $('trace-content').append(root);
}
function traceReviews() {
  const row = rows[index];
  return reviews.filter(review => review.trace_id === row.trace.id && review.trace_sha256 === row.sha256);
}
function loadReview(review) {
  currentReview = review || null;
  $('scope').value = review?.scope || '';
  $('verdict').value = review?.verdict || 'UNREVIEWED';
  $('notes').value = review?.notes || '';
  $('correction').value = review?.correction || '';
  $('rubric').value = (review?.rubric_questions || []).join('\n');
  if (review) $('reviewer').value = review.reviewer;
  $('review-select').value = review?.review_id || '';
  dirty = false;
  $('save-status').textContent = review ? 'Saved locally. Editing creates a new revision.' : 'New observation; not saved.';
}
function updateReviews(selected) {
  $('review-select').replaceChildren(new Option('New observation', ''));
  for (const review of traceReviews()) $('review-select').add(new Option(`${review.verdict}: ${review.scope}`, review.review_id));
  loadReview(selected || null);
}
function show(nextIndex) {
  index = nextIndex;
  const trace = rows[index].trace;
  $('trace-title').textContent = trace.id;
  $('trace-content').replaceChildren();
  section('Input', trace.input);
  section('Output', trace.output);
  section('Execution error', trace.error);
  section('Context', trace.context, true);
  section('Reference', trace.reference, true);
  if (Array.isArray(trace.messages)) {
    const details = element('details'); details.append(element('summary', `Messages (${trace.messages.length})`));
    for (const message of trace.messages) {
      const block = element('section', undefined, 'message');
      block.append(element('h3', message?.role || 'Message'), renderValue(message)); details.append(block);
    }
    $('trace-content').append(details);
  }
  const shown = new Set(['id', 'input', 'output', 'error', 'context', 'reference', 'messages']);
  const remaining = Object.fromEntries(Object.entries(trace).filter(([key]) => !shown.has(key)));
  if (Object.keys(remaining).length) section('Run evidence and provenance', remaining, true);
  $('trace-select').value = String(index);
  $('previous').disabled = index === 0;
  $('next').disabled = index === rows.length - 1;
  const observed = rows.filter(row => reviews.some(review => review.trace_id === row.trace.id && review.trace_sha256 === row.sha256)).length;
  $('progress').textContent = `Trace ${index + 1} of ${rows.length} · ${observed} with saved observations`;
  updateReviews(traceReviews().at(-1));
}
async function save(advance = false) {
  if (busy || !$('review-form').reportValidity()) return;
  busy = true;
  const controls = [...$('review-form').elements, $('review-select'), $('new-review')];
  controls.forEach(control => { control.disabled = true; });
  $('save-status').textContent = 'Saving…';
  try {
    const row = rows[index];
    const body = {trace_id: row.trace.id, trace_sha256: row.sha256,
      review_id: currentReview?.review_id || crypto.randomUUID(), amends: currentReview?.record_id || null,
      reviewer: $('reviewer').value, scope: $('scope').value, verdict: $('verdict').value,
      notes: $('notes').value, correction: $('correction').value,
      rubric_questions: $('rubric').value.split('\n').map(q => q.trim()).filter(Boolean)};
    const saved = await api('/api/reviews', body);
    reviews = reviews.filter(review => review.review_id !== saved.review_id).concat(saved);
    show(advance ? Math.min(index + 1, rows.length - 1) : index);
    if (!advance) updateReviews(saved);
  } catch (error) { $('save-status').textContent = `Not saved: ${error.message}`; }
  finally { busy = false; controls.forEach(control => { control.disabled = false; }); }
}
function canLeave() { return !busy && (!dirty || confirm('Leave this observation without saving?')); }
function move(delta) { if (canLeave()) show(Math.max(0, Math.min(index + delta, rows.length - 1))); }
$('previous').onclick = () => move(-1);
$('next').onclick = () => move(1);
$('trace-select').onchange = () => { const next = Number($('trace-select').value); if (canLeave()) show(next); else $('trace-select').value = String(index); };
$('review-select').onchange = () => {
  const id = $('review-select').value;
  if (canLeave()) loadReview(reviews.find(review => review.review_id === id));
  else $('review-select').value = currentReview?.review_id || '';
};
$('new-review').onclick = () => { if (canLeave()) loadReview(null); };
$('review-form').onsubmit = event => { event.preventDefault(); save(); };
$('save-next').onclick = () => save(true);
for (const id of fields) $(id).addEventListener('input', () => { dirty = true; $('save-status').textContent = 'Unsaved changes.'; });
document.addEventListener('keydown', event => {
  if ((event.metaKey || event.ctrlKey) && event.key === 'Enter') { event.preventDefault(); save(true); }
  if (event.altKey && ['ArrowLeft', 'ArrowRight'].includes(event.key)) { event.preventDefault(); move(event.key === 'ArrowLeft' ? -1 : 1); }
});
window.addEventListener('beforeunload', event => { if (dirty || busy) { event.preventDefault(); event.returnValue = ''; } });
api('/api/data').then(data => {
  rows = data.rows; reviews = data.reviews; $('reviewer').value = data.reviewer;
  rows.forEach((row, i) => $('trace-select').add(new Option(row.trace.id, String(i))));
  show(0);
}).catch(error => { $('save-status').textContent = error.message; });
