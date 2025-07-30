import requests
import json


def download_public_apis():
    """Download and process the public APIs JSON"""
    json_url = "https://raw.githubusercontent.com/marcelscruz/public-apis/main/db/resources.json"

    try:
        print("Downloading APIs from GitHub...")
        response = requests.get(json_url)
        response.raise_for_status()

        data = response.json()

        # The APIs are in data['entries'], not data directly
        api_entries = data.get('entries', [])
        print(f"Downloaded {len(api_entries)} APIs")

        # Convert to our format
        converted_apis = []
        for api in api_entries:
            converted_apis.append({
                'name': api.get('API', 'Unknown'),
                'description': api.get('Description', ''),
                'url': api.get('Link', ''),
                'category': api.get('Category', 'Other'),
                'requires_key': api.get('Auth', '').lower() not in ['', 'no', 'none']
            })

        # Save directly as api_sources.json
        with open('api_sources.json', 'w', encoding='utf-8') as f:
            json.dump(converted_apis, f, indent=2, ensure_ascii=False)

        print(f"Successfully converted {len(converted_apis)} APIs to api_sources.json")
        return converted_apis

    except Exception as e:
        print(f"Error downloading APIs: {e}")
        return []


def generate_search_tags(api):
    """Auto-generate search tags based on category and description"""
    tags = []

    # Category-based tags
    category_tags = {
        'finance': ['money', 'trading', 'investment', 'market', 'stock', 'crypto', 'currency', 'banking'],
        'weather': ['climate', 'forecast', 'temperature', 'meteorology', 'atmospheric'],
        'sports': ['game', 'team', 'player', 'league', 'score', 'match', 'tournament'],
        'demographics': ['population', 'census', 'statistics', 'geographic', 'social']
    }

    category_lower = api['category'].lower()
    if category_lower in category_tags:
        tags.extend(category_tags[category_lower])

    # Extract common terms from description
    description_words = api['description'].lower().split()
    relevant_words = [word for word in description_words if len(word) > 3]
    tags.extend(relevant_words[:5])  # Add up to 5 relevant words

    return ' '.join(tags)


def generate_extension_files():
    # This will use the api_sources.json file that download_public_apis() creates
    try:
        with open('api_sources.json', 'r', encoding='utf-8') as f:
            api_sources = json.load(f)
    except FileNotFoundError:
        print("api_sources.json not found! Run download_public_apis() first.")
        return

    print(f"Loaded {len(api_sources)} APIs for extension")

def create_popup_html():
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>API Search</title>
    <style>
        body {width: 400px; padding 10px;}
        #search {width: 100%; padding: 5px; margin-bottom: 10px;}
        .api-item {border: 1px solid #ccc; margin: 5px 0; padding: 10px;}
        .api-category {color: #666; font-size: 12px;}
    </style>
</head>
</body>
    <input type="text" id="search" placeholder="Search APIs...">
    <div id="api-list"><div>
    <script src="popup.js"></script>
</body>
</html>"""

    with open('popup.html', 'w') as f:
        f.write(html_content)

    print("Generated popup.html successfully")


def create_popup_js():
    js_content = """document.addEventListener('DOMContentLoaded', function() {
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
});"""

    with open('popup.js', 'w') as f:
        f.write(js_content)

    print("Generated popup.js successfully!")


def create_manifest():
    manifest_content = """{
  "manifest_version": 3,
  "name": "API Data Source Finder",
  "version": "1.0",
  "description": "Find APIs and data sources for data analysis",
  "action": {
    "default_popup": "popup.html",
    "default_title": "API Finder"
  },
  "permissions": []
}"""

    with open('manifest.json', 'w') as f:
        f.write(manifest_content)

    print("Generated manifest.json successfully!")


if __name__ == "__main__":
    download_public_apis()
    generate_extension_files()
    create_popup_html()
    create_popup_js()
    create_manifest()









