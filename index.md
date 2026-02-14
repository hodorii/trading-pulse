---
layout: default
title: Trading Pulse Archive
---

<style>
  .session-group { margin-bottom: 2.5rem; border-left: 4px solid #007bff; padding-left: 1rem; }
  .session-header { color: #007bff; font-size: 1.4rem; margin-bottom: 1rem; font-weight: bold; background: #f8f9fa; padding: 0.5rem; }
  .report-list { list-style: none; padding: 0; }
  .report-item { margin-bottom: 0.5rem; display: flex; align-items: baseline; border-bottom: 1px solid #eee; padding: 0.2rem 0; }
  .report-seq { font-family: monospace; color: #999; margin-right: 0.8rem; width: 30px; }
  .report-title { font-size: 1.05rem; flex-grow: 1; }
  .report-time { font-size: 0.85rem; color: #666; }
  .report-link { text-decoration: none; color: #333; }
  .report-link:hover { color: #007bff; }
</style>

# 📈 Trading Pulse

{% assign posts_by_session = site.posts | group_by: "session_id" %}

{% for session in posts_by_session %}
  {% if session.name == "" or session.name == nil %}{% continue %}{% endif %}
  <div class="session-group">
    <div class="session-header">🗓️ {% assign date_p = session.name | slice: 0, 10 %}{% assign hh = session.name | slice: 11, 2 %}{% assign mm = session.name | slice: 13, 2 %}{{ date_p }} {{ hh }}:{{ mm }}</div>
    <div class="report-list">
      {% assign sorted_items = session.items | sort: "session_order" %}
      {% for post in sorted_items %}
        <div class="report-item">
          <span class="report-seq">[{{ post.session_order }}]</span>
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
