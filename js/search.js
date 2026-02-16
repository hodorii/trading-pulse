---
layout: null
---
(function() {
  'use strict';

  const TYPES = [
    'IDR', 'MAD', 'TTO', 'TSM', 'Synthesis', 'Value', 'Market', 'Risk', 
    'Guide', 'Macro', 'Review', 'Supply', 'Tactical', 'Unified', 'Event',
    '매크로', '시장', '이벤트', '가치', '수급', '리스크', '결정', '가이드', 
    '통합', '시뮬', '스윙', '데이', '분석', '단기', '기관', '시나리오', 
    '복기', '애프터', '비교', '포트', '요약', '시스템', '리서치'
  ].sort();

  const STOCKS = [
    'SK하이닉스', '삼성전자', '미래에셋증권', '제룡전기', '두산에너빌리티',
    '한화', '우리기술', '현대차', '삼성바이오로직스', '우진', '에스피지',
    '현대위아', '삼현', '레인보우로보틱스', '에스오에스랩', '현대로템',
    '포스코인터내셔널', '포스코홀딩스', '한국조선해양', '한미반도체',
    '파크시스템즈', '솔브레인', 'HPSP', '와이투솔루션', '코스닥주도주',
    '두산밥캣', '한라캐스트', '삼천당제약', 'KB금융', '한글과컴퓨터',
    '기가비스'
  ].sort();

  let searchIndex = [];
  let fuse = null;

  function extractType(title) {
    if (!title) return '';
    const parts = title.split('_');
    return parts[0] || '';
  }

  function extractStock(title) {
    if (!title) return '';
    for (const stock of STOCKS) {
      if (title.includes(stock)) return stock;
    }
    return '';
  }

  async function loadIndex() {
    try {
      const response = await fetch('{{ "/search.json" | relative_url }}');
      searchIndex = await response.json();
      
      searchIndex = searchIndex.map(post => ({
        ...post,
        type: extractType(post.title),
        stock: extractStock(post.title)
      }));

      fuse = new Fuse(searchIndex, {
        keys: [
          { name: 'title', weight: 0.4 },
          { name: 'content', weight: 0.3 },
          { name: 'type', weight: 0.15 },
          { name: 'stock', weight: 0.15 }
        ],
        threshold: 0.3,
        includeScore: true,
        minMatchCharLength: 2
      });

      return true;
    } catch (error) {
      console.error('Failed to load search index:', error);
      return false;
    }
  }

  function search(query, filters = {}) {
    let results = searchIndex;

    if (query && query.trim()) {
      const fuseResults = fuse.search(query.trim());
      results = fuseResults.map(r => r.item);
    }

    if (filters.type && filters.type !== 'all') {
      results = results.filter(post => post.type === filters.type);
    }

    if (filters.stock && filters.stock !== 'all') {
      results = results.filter(post => post.stock === filters.stock);
    }

    if (filters.dateFrom) {
      results = results.filter(post => post.date >= filters.dateFrom);
    }

    if (filters.dateTo) {
      results = results.filter(post => post.date <= filters.dateTo);
    }

    return results;
  }

  function getSessionId(post) {
    const sid = post.session_id;
    if (sid && sid.trim() !== '') {
      return sid.trim();
    }
    if (post.path) {
      const match = post.path.match(/(\d{4}-\d{2}-\d{2}-\d{4})/);
      if (match) return match[1];
    }
    const d = new Date(post.date);
    const yy = d.getFullYear();
    const mm = String(d.getMonth() + 1).padStart(2, '0');
    const dd = String(d.getDate()).padStart(2, '0');
    const hh = String(d.getHours()).padStart(2, '0');
    const mm2 = String(d.getMinutes()).padStart(2, '0');
    return `${yy}-${mm}-${dd}-${hh}${mm2}`;
  }

  function groupBySession(results) {
    const groups = {};
    results.forEach(post => {
      const sessionId = getSessionId(post);
      if (!groups[sessionId]) {
        groups[sessionId] = {
          session_id: sessionId,
          date: post.date,
          posts: []
        };
      }
      groups[sessionId].posts.push(post);
    });

    return Object.values(groups).sort((a, b) => b.session_id.localeCompare(a.session_id));
  }

  function renderResults(groups) {
    const container = document.getElementById('search-results');
    if (!container) return;

    if (groups.length === 0) {
      container.innerHTML = '<p class="no-results">검색 결과가 없습니다.</p>';
      return;
    }

    let html = '';
    groups.forEach(group => {
      const sessionId = group.session_id;
      const dateStr = sessionId.slice(0, 10);
      const timeStr = sessionId.slice(11, 16);
      const dateObj = new Date(dateStr);
      const formattedDate = dateObj.toLocaleDateString('ko-KR', { 
        year: 'numeric', month: 'long', day: 'numeric' 
      });

      html += `<div class="session-group">
        <div class="session-header">
          <div class="session-info">
            <span class="session-id">${sessionId}</span>
            <span class="date">${timeStr}</span>
          </div>
        </div>
        <div class="report-list">`;

      const sortedPosts = group.posts.sort((a, b) => {
        const orderA = parseInt(a.session_order) || 0;
        const orderB = parseInt(b.session_order) || 0;
        return orderA - orderB;
      });

      sortedPosts.forEach(post => {
        const title = post.title.replace(/_/g, ' ');
        html += `<div class="report-item">
          <span class="report-seq">${post.session_order || ''}</span>
          <div class="report-title">
            <a class="report-link" href="${post.url}">${title}</a>
            ${post.type ? `<span class="report-type">${post.type}</span>` : ''}
            ${post.stock ? `<span class="report-stock">${post.stock}</span>` : ''}
          </div>
        </div>`;
      });

      html += '</div></div>';
    });

    container.innerHTML = html;
  }

  function initFilters() {
    const typeSelect = document.getElementById('filter-type');
    const stockSelect = document.getElementById('filter-stock');

    if (typeSelect) {
      TYPES.forEach(type => {
        const option = document.createElement('option');
        option.value = type;
        option.textContent = type;
        typeSelect.appendChild(option);
      });
    }

    if (stockSelect) {
      STOCKS.forEach(stock => {
        const option = document.createElement('option');
        option.value = stock;
        option.textContent = stock;
        stockSelect.appendChild(option);
      });
    }
  }

  function handleSearch() {
    const query = document.getElementById('search-input')?.value || '';
    const type = document.getElementById('filter-type')?.value || 'all';
    const stock = document.getElementById('filter-stock')?.value || 'all';
    const dateFrom = document.getElementById('date-from')?.value || '';
    const dateTo = document.getElementById('date-to')?.value || '';

    const filters = { type, stock, dateFrom, dateTo };
    const results = search(query, filters);
    const grouped = groupBySession(results);
    renderResults(grouped);

    const countEl = document.getElementById('result-count');
    if (countEl) {
      countEl.textContent = `${results.length}개 결과`;
    }
  }

  function debounce(func, wait) {
    let timeout;
    return function(...args) {
      clearTimeout(timeout);
      timeout = setTimeout(() => func.apply(this, args), wait);
    };
  }

  document.addEventListener('DOMContentLoaded', async () => {
    const loaded = await loadIndex();
    if (loaded) {
      initFilters();
      
      const searchInput = document.getElementById('search-input');
      const typeFilter = document.getElementById('filter-type');
      const stockFilter = document.getElementById('filter-stock');
      const dateFrom = document.getElementById('date-from');
      const dateTo = document.getElementById('date-to');
      const searchBtn = document.getElementById('search-btn');

      if (searchInput) searchInput.addEventListener('input', debounce(handleSearch, 300));
      if (typeFilter) typeFilter.addEventListener('change', handleSearch);
      if (stockFilter) stockFilter.addEventListener('change', handleSearch);
      if (dateFrom) dateFrom.addEventListener('change', handleSearch);
      if (dateTo) dateTo.addEventListener('change', handleSearch);
      if (searchBtn) searchBtn.addEventListener('click', handleSearch);
    }
  });

  window.TradingPulseSearch = { search, groupBySession, loadIndex };
})();
