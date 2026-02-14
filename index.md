---
layout: default
title: Home
---

# 📈 Trading Pulse: 세션별 분석 리포트

{% assign sessions = site.posts | group_by: "session_id" %}

{% for session in sessions %}
  <div class="session-group" style="margin-bottom: 2rem; border-left: 4px solid #007bff; padding-left: 1rem;">
    <h3 style="color: #007bff;">🗓️ 분석 세션: {{ session.name }}</h3>
    <ul class="post-list">
      {% assign sorted_posts = session.items | sort: "title" %}
      {% for post in sorted_posts %}
        <li>
          <span class="post-meta">{{ post.date | date: "%b %d, %Y %H:%M" }}</span>
          <a class="post-link" href="{{ post.url | relative_url }}">
            {{ post.title | escape }}
          </a>
        </li>
      {% endfor %}
    </ul>
  </div>
{% endfor %}
