---
layout: default
title: Trading Pulse Archive
---

<style>
  /* 보고서 내부 제목 크기 축소 */
  .post-content h1, .markdown-body h1 { font-size: 1.5rem !important; margin-top: 1.2rem; }
  .post-content h2, .markdown-body h2 { font-size: 1.3rem !important; margin-top: 1rem; border-bottom: 1px solid #eee; padding-bottom: 0.3rem; }
  .post-content h3, .markdown-body h3 { font-size: 1.1rem !important; margin-top: 0.8rem; }
  
  /* 리스트 간격 및 스타일 최적화 */
  .session-group { margin-bottom: 1.5rem; border-left: 3px solid #007bff; padding-left: 0.8rem; }
  .session-header { color: #007bff; font-size: 1.2rem; margin-bottom: 0.5rem; font-weight: bold; background: #f8f9fa; padding: 0.3rem 0.6rem; border-radius: 4px; }
  .report-list { list-style: none; padding: 0; }
  .report-item { margin-bottom: 0.2rem; display: flex; align-items: baseline; border-bottom: 1px solid #f9f9f9; padding: 0.1rem 0; }
  .report-seq { font-family: monospace; color: #bbb; margin-right: 0.5rem; width: 25px; font-size: 0.85rem; }
  .report-title { font-size: 0.95rem; flex-grow: 1; line-height: 1.4; }
  .report-time { font-size: 0.8rem; color: #888; margin-left: 0.5rem; }
  .report-link { text-decoration: none; color: #333; }
  .report-link:hover { color: #007bff; background: #f0f7ff; }
</style>

{% assign posts_by_session = site.posts | group_by: "session_id" %}

{% for session in posts_by_session %}
  {% if session.name == "" or session.name == nil %}{% continue %}{% endif %}
  <div class="session-group">
    <div class="session-header">🗓️ {% assign date_p = session.name | slice: 0, 10 %}{% assign hh = session.name | slice: 11, 2 %}{% assign mm = session.name | slice: 13, 2 %}{{ date_p }} {{ hh }}:{{ mm }}</div>
    <div class="report-list">
      {% assign sorted_items = session.items | sort: "session_order" %}
      {% for post in sorted_items %}
        <div class="report-item">
          <span class="report-seq">{{ post.session_order }}</span>
          <div class="report-title">
            <a class="report-link" href="{{ post.url | relative_url }}">
              {{ post.title | replace: "_", " " }}
            </a>
          </div>
          <span class="report-time">{{ hh }}:{{ mm }}</span>
        </div>
      {% endfor %}
    </div>
  </div>
{% endfor %}
