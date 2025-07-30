document.addEventListener('DOMContentLoaded', function() {
  fetch('api_sources.json')
    .then(response => response.json())
    .then(data => {
      displayAPIs(data);
      setupSearch(data);
    });

  function displayAPIs(apis) {
    const apiList = document.getElementById('api-list');
    apiList.innerHTML = '';

    apis.forEach(api => {
      const div = document.createElement('div');
      div.className = 'api-item';
      div.innerHTML = `
        <div class="api-name">${api.name}</div>
        <div>${api.description}</div>
        <div class="api-category">${api.category} - ${api.requires_key ? 'API Key Required' : 'No Key Needed'}</div>
        <a href="${api.url}" target="_blank">View Documentation</a>
      `;
      apiList.appendChild(div);
    });
  }

  function calculateRelevanceScore(api, searchTerm) {
    const term = searchTerm.toLowerCase();
    let score = 0;

    // Category match (highest weight - 3x)
    if (api.category.toLowerCase().includes(term)) {
      score += 3;
    }

    // Search tags match (medium weight - 2x)
    if (api.search_tags && api.search_tags.toLowerCase().includes(term)) {
      score += 2;
    }

    // Description match (lower weight - 1x)
    if (api.description.toLowerCase().includes(term)) {
      score += 1;
    }

    // Name match (medium weight - 2x)
    if (api.name.toLowerCase().includes(term)) {
      score += 2;
    }

    return score;
  }

  function setupSearch(apis) {
    const searchInput = document.getElementById('search');
    searchInput.addEventListener('input', () => {
      const searchTerm = searchInput.value.toLowerCase().trim();

      if (searchTerm === '') {
        displayAPIs(apis);
        return;
      }

      // Calculate relevance scores and filter
      const scoredApis = apis.map(api => ({
        ...api,
        relevanceScore: calculateRelevanceScore(api, searchTerm)
      }))
      .filter(api => api.relevanceScore > 0)
      .sort((a, b) => b.relevanceScore - a.relevanceScore);

      displayAPIs(scoredApis);
    });
  }
});