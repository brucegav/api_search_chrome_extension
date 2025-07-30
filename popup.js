document.addEventListener('DOMContentLoaded', function() {
  let allApis = [];

  fetch('api_sources.json')
    .then(response => response.json())
    .then(data => {
      allApis = data;
      displayAPIs(data.slice(0, 50)); // Show first 50 initially for performance
    })
    .catch(error => {
      console.error('Error loading APIs:', error);
      document.getElementById('api-list').innerHTML = '<div class="no-results">Error loading APIs</div>';
    });

  function displayAPIs(apis) {
    const apiList = document.getElementById('api-list');

    if (apis.length === 0) {
      apiList.innerHTML = '<div class="no-results">No APIs found matching your search</div>';
      return;
    }

    apiList.innerHTML = apis.map(api => `
      <div class="api-item">
        <div class="api-name">${escapeHtml(api.name)}</div>
        <div class="api-description">${escapeHtml(api.description)}</div>
        <div class="api-category">${escapeHtml(api.category)} • ${api.requires_key ? 'API Key Required' : 'No Key Needed'}</div>
        <a href="${escapeHtml(api.url)}" target="_blank" class="api-link">View Documentation →</a>
      </div>
    `).join('');
  }

  function calculateRelevanceScore(api, searchTerm) {
    const term = searchTerm.toLowerCase();
    let score = 0;

    // Exact name match (highest priority)
    if (api.name.toLowerCase() === term) score += 10;
    else if (api.name.toLowerCase().includes(term)) score += 5;

    // Category match
    if (api.category.toLowerCase().includes(term)) score += 4;

    // Search tags match
    if (api.search_tags && api.search_tags.toLowerCase().includes(term)) score += 3;

    // Description match
    if (api.description.toLowerCase().includes(term)) score += 2;

    return score;
  }

  function setupSearch() {
    const searchInput = document.getElementById('search');
    let searchTimeout;

    searchInput.addEventListener('input', () => {
      clearTimeout(searchTimeout);
      searchTimeout = setTimeout(() => {
        const searchTerm = searchInput.value.toLowerCase().trim();

        if (searchTerm === '') {
          displayAPIs(allApis.slice(0, 50));
          return;
        }

        if (searchTerm.length < 2) return;

        const scoredApis = allApis
          .map(api => ({ ...api, relevanceScore: calculateRelevanceScore(api, searchTerm) }))
          .filter(api => api.relevanceScore > 0)
          .sort((a, b) => b.relevanceScore - a.relevanceScore)
          .slice(0, 100); // Limit results for performance

        displayAPIs(scoredApis);
      }, 150);
    });
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  setupSearch();
});