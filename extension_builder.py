import json
import csv


def load_apis_from_csv():
    api_sources = []
    try:
        with open('api_list.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                api = {
                    "name": row['name'],
                    "description": row['description'],
                    "url": row['url'],
                    "category": row['category'],
                    "requires_key": row['requires_key'].lower() == 'true'
                }
                # Auto-generate searchable tags
                api['search_tags'] = generate_search_tags(api)
                api_sources.append(api)
    except FileNotFoundError:
        print("api_list.csv not found! Please create it first.")
        return []

    return api_sources


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
    api_sources = load_apis_from_csv()
    if not api_sources:
        return

    # Create the JSON file for our Chrome extension
    with open('api_sources.json', 'w') as f:
        json.dump(api_sources, f, indent=2)

    print(f"Generated api_sources.json with {len(api_sources)} APIs successfully!")

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
    generate_extension_files()
    create_popup_html()
    create_popup_js()
    create_manifest()









