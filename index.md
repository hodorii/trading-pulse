---
layout: default
title: Trading Pulse Archive
---

<style>
  .session-group { margin-bottom: 1.5rem; }
  .session-header { color: #007bff; border-bottom: 1px solid #eee; padding-bottom: 0.3rem; margin-top: 1.5rem; }
  .report-list { list-style: none; padding-left: 0.5rem; margin-top: 0.5rem; }
  .report-item { margin-bottom: 0.3rem; display: flex; align-items: baseline; }
  .report-title { font-size: 1.1rem; font-weight: 600; margin: 0; display: inline; }
  .report-date { font-size: 0.85rem; color: #888; margin-left: 0.8rem; flex-shrink: 0; }
  .report-link { text-decoration: none; color: #333; }
  .report-link:hover { color: #007bff; text-decoration: underline; }
</style>

# 📈 Trading Pulse

{% assign sessions = site.posts | group_by: "session_id" %}

{% for session in sessions %}
  <div class="session-group">
    <h3 class="session-header">🗓️ 세션: {{ session.name }}</h3>
    <div class="report-list">
      {% assign sorted_posts = session.items | sort: "session_order" %}
      {% for post in sorted_posts %}
        <div class="report-item">
          <h4 class="report-title">
            <a class="report-link" href="{{ post.url | relative_url }}">
              {{ post.title | escape }}
            </a>
          </h4>
          <span class="report-date">{{ post.date | date: "%Y-%m-%d %H:%M" }}</span>
        </div>
      {% endfor %}
    </div>
  </div>
{% endfor %}
