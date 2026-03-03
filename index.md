---
layout: default
title: Trading Pulse Archive
---

<div class="container">
  <header class="header" style="margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 1px solid #eee;">
    <h1>Trading Pulse</h1>
    <p>AI 기반 정밀 실측 트레이딩 리포트 아카이브</p>
  </header>

  <div class="results-container">
    {% for post in site.posts %}
      <div class="post-item" style="margin-bottom: 1rem; padding: 0.5rem; border-bottom: 1px dashed #eee;">
        <span class="post-date" style="color: #666; font-family: monospace;">{{ post.date | date: "%Y-%m-%d %H:%M" }}</span>
        <span class="post-title" style="margin-left: 1rem; font-weight: bold;">
          <a href="{{ post.url | relative_url }}">{{ post.title | replace: "_", " " }}</a>
        </span>
      </div>
    {% endfor %}
  </div>

  <footer class="footer" style="margin-top: 2rem; font-size: 0.8rem; color: #888;">
    본 리포트는 투자 참고용이며, 모든 투자의 책임은 투자자 본인에게 있습니다.
  </footer>
</div>
