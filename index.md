---
layout: default
title: Trading Pulse Archive
---

<style>
  .session-group { margin-bottom: 2rem; border-bottom: 1px solid #f0f0f0; padding-bottom: 1rem; }
  .session-header { color: #007bff; font-size: 1.4rem; margin-bottom: 0.8rem; border-left: 5px solid #007bff; padding-left: 0.8rem; }
  .report-list { list-style: none; padding-left: 0.5rem; }
  .report-item { margin-bottom: 0.4rem; display: flex; align-items: center; }
  .report-title { font-size: 1.05rem; font-weight: normal; margin: 0; color: #333; }
  .report-date { font-size: 0.8rem; color: #999; margin-left: auto; padding-left: 1rem; }
  .report-link { text-decoration: none; color: inherit; }
  .report-link:hover { color: #007bff; text-decoration: underline; }
</style>

# 📈 Trading Pulse

{% assign posts_by_session = site.posts | group_by: "session_id" %}

{% for session in posts_by_session %}
  <div class="session-group">
    <h3 class="session-header">🗓️ 세션: {{ session.name }}</h3>
    <div class="report-list">
      {% assign sorted_items = session.items | sort: "session_order" %}
      {% for post in sorted_items %}
        <div class="report-item">
          <h4 class="report-title">
            <a class="report-link" href="{{ post.url | relative_url }}">
              [{{ post.session_order }}/{{ session.items.size }}] {{ post.title | escape }}
            </a>
          </h4>
          <span class="report-date">{{ post.date | date: "%H:%M" }}</span>
        </div>
      {% endfor %}
    </div>
  </div>
{% endfor %}
