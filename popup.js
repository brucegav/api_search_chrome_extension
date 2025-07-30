document.addEventListener('DOMContentLoaded', function() {
  // Load API data and display it
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

  function setupSearch(apis) {
    const searchInput = document.getElementById('search');
    searchInput.addEventListener('input', () => {
      const searchTerm = searchInput.value.toLowerCase();
      const filtered = apis.filter(api => 
        api.name.toLowerCase().includes(searchTerm) ||
        api.description.toLowerCase().includes(searchTerm) ||
        api.category.toLowerCase().includes(searchTerm)
      );
      displayAPIs(filtered);
    });
  }
});