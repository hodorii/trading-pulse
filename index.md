---
layout: default
title: Trading Pulse Archive
---

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/fuse.js@7.0.0/dist/fuse.min.js"></script>
<script src="{{ '/js/search.js' | relative_url }}"></script>

<style>
  :root {
    --bg-primary: #0d1117;
    --bg-secondary: #161b22;
    --bg-tertiary: #21262d;
    --border: #30363d;
    --text-primary: #e6edf3;
    --text-secondary: #8b949e;
    --text-muted: #6e7681;
    --accent: #58a6ff;
    --accent-glow: rgba(88, 166, 255, 0.15);
    --success: #3fb950;
    --stock-tag: #ffa657;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    background: var(--bg-primary);
    color: var(--text-primary);
    line-height: 1.6;
    min-height: 100vh;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1.5rem;
  }

  .header {
    text-align: center;
    margin-bottom: 2.5rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid var(--border);
  }

  .header h1 {
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    margin-bottom: 0.5rem;
    background: linear-gradient(135deg, var(--text-primary) 0%, var(--accent) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .header .subtitle {
    color: var(--text-secondary);
    font-size: 1rem;
  }

  .release-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    padding: 0.5rem 1rem;
    border-radius: 8px;
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-top: 1rem;
  }

  .release-badge .dot {
    width: 8px;
    height: 8px;
    background: var(--success);
    border-radius: 50%;
    animation: pulse 2s infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
  }

  .search-section {
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 2rem;
  }

  .search-row {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
  }

  .search-input-wrapper {
    flex: 1;
    min-width: 280px;
    position: relative;
  }

  .search-input-wrapper::before {
    content: "⌕";
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-muted);
    font-size: 1.2rem;
  }

  .search-input {
    width: 100%;
    padding: 0.875rem 1rem 0.875rem 2.75rem;
    background: var(--bg-tertiary);
    border: 1px solid var(--border);
    border-radius: 10px;
    color: var(--text-primary);
    font-size: 1rem;
    font-family: inherit;
    transition: all 0.2s ease;
  }

  .search-input:focus {
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-glow);
  }

  .search-input::placeholder {
    color: var(--text-muted);
  }

  .filter-select {
    padding: 0.875rem 2.5rem 0.875rem 1rem;
    background: var(--bg-tertiary);
    border: 1px solid var(--border);
    border-radius: 10px;
    color: var(--text-primary);
    font-size: 0.9rem;
    font-family: inherit;
    cursor: pointer;
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%238b949e' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 1rem center;
    transition: all 0.2s ease;
  }

  .filter-select:hover {
    border-color: var(--text-muted);
  }

  .filter-select:focus {
    outline: none;
    border-color: var(--accent);
  }

  .date-input {
    padding: 0.875rem 1rem;
    background: var(--bg-tertiary);
    border: 1px solid var(--border);
    border-radius: 10px;
    color: var(--text-primary);
    font-size: 0.9rem;
    font-family: 'JetBrains Mono', monospace;
  }

  .date-input:focus {
    outline: none;
    border-color: var(--accent);
  }

  .search-btn {
    padding: 0.875rem 1.5rem;
    background: var(--accent);
    color: var(--bg-primary);
    border: none;
    border-radius: 10px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .search-btn:hover {
    background: #79b8ff;
    transform: translateY(-1px);
  }

  .result-count {
    margin-top: 1rem;
    font-size: 0.85rem;
    color: var(--text-muted);
    font-family: 'JetBrains Mono', monospace;
  }

  .results-container {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .no-results {
    text-align: center;
    padding: 4rem 2rem;
    color: var(--text-muted);
    font-size: 1.1rem;
  }

  .footer {
    text-align: center;
    margin-top: 3rem;
    padding-top: 2rem;
    border-top: 1px solid var(--border);
    color: var(--text-muted);
    font-size: 0.85rem;
  }

  @media (max-width: 768px) {
    .header h1 { font-size: 1.75rem; }
    .search-row { flex-direction: column; }
    .search-input-wrapper { min-width: 100%; }
    .filter-select, .date-input, .search-btn { width: 100%; }
    .report-title { flex-direction: column; align-items: flex-start; gap: 0.5rem; }
    .report-time { margin-left: 0; margin-top: 0.25rem; }
  }

  .session-group {
    animation: fadeIn 0.3s ease forwards;
    opacity: 0;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .session-group:nth-child(1) { animation-delay: 0s; }
  .session-group:nth-child(2) { animation-delay: 0.05s; }
  .session-group:nth-child(3) { animation-delay: 0.1s; }
  .session-group:nth-child(4) { animation-delay: 0.15s; }
  .session-group:nth-child(5) { animation-delay: 0.2s; }
</style>

<div class="container">
  <header class="header">
    <h1>Trading Pulse</h1>
    <p class="subtitle">AI 기반 정밀 실측 트레이딩 리포트 아카이브</p>
    <div class="release-badge">
      <span class="dot"></span>
      <span>최종 업데이트: {{ site.release_id }}</span>
    </div>
  </header>

  <section class="search-section">
    <div class="search-row">
      <div class="search-input-wrapper">
        <input type="text" id="search-input" class="search-input" placeholder="검색어 입력 (제목, 내용, 종목...)" />
      </div>
      <select id="filter-type" class="filter-select">
        <option value="all">전체 유형</option>
      </select>
      <select id="filter-stock" class="filter-select">
        <option value="all">전체 종목</option>
      </select>
      <input type="date" id="date-from" class="date-input" />
      <input type="date" id="date-to" class="date-input" />
      <button id="search-btn" class="search-btn">검색</button>
    </div>
    <div class="result-count" id="result-count"></div>
  </section>

  <div id="search-results" class="results-container">
    {% assign current_session = "" %}
    
    {% for post in site.posts %}
      {% assign post_session = post.session_id %}
      {% if post_session == nil or post_session == "" %}
        {% assign post_session = post.date | date: "%Y-%m-%d-%H%M" %}
      {% endif %}
      
      {% if current_session != post_session %}
        {% if current_session != "" %}
          </div></div>
        {% endif %}
        <div class="session-group">
          <div class="session-header">
            <div class="session-info">
              <span class="session-id">{{ post_session }}</span>
              <span class="date">{{ post_session | slice: 11, 2 }}:{{ post_session | slice: 13, 2 }}</span>
            </div>
          </div>
          <div class="report-list">
        {% assign current_session = post_session %}
      {% endif %}
      
      <div class="report-item">
        <span class="report-seq">{{ post.session_order }}</span>
        <div class="report-title">
          <a class="report-link" href="{{ post.url | relative_url }}">{{ post.title | replace: "_", " " }}</a>
        </div>
        <span class="report-time">{{ post_session | slice: 11, 2 }}:{{ post_session | slice: 13, 2 }}</span>
      </div>
    {% endfor %}
    {% if current_session != "" %}
          </div>
        </div>
    {% endif %}
  </div>

  <footer class="footer">
    본 리포트는 투자 참고용이며, 모든 투자의 책임은 투자자 본인에게 있습니다.
  </footer>
</div>
