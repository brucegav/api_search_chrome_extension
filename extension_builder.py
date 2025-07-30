import requests
import json
from pathlib import Path


class ExtensionBuilder:
    """Chrome extension builder for API search tool"""

    def __init__(self):
        self.api_url = "https://raw.githubusercontent.com/marcelscruz/public-apis/main/db/resources.json"
        self.output_dir = Path(".")
        self.category_tags = {
            'finance': ['money', 'trading', 'investment', 'market', 'stock', 'crypto', 'currency', 'banking'],
            'weather': ['climate', 'forecast', 'temperature', 'meteorology', 'atmospheric'],
            'sports': ['game', 'team', 'player', 'league', 'score', 'match', 'tournament'],
            'demographics': ['population', 'census', 'statistics', 'geographic', 'social'],
            'health': ['medical', 'fitness', 'nutrition', 'wellness', 'disease'],
            'entertainment': ['movie', 'music', 'video', 'game', 'media']
        }

    def download_and_process_apis(self):
        """Download APIs and convert to extension format"""
        try:
            print("Downloading APIs from GitHub...")
            response = requests.get(self.api_url, timeout=30)
            response.raise_for_status()

            data = response.json()
            api_entries = data.get('entries', [])

            if not api_entries:
                raise ValueError("No API entries found in response")

            print(f"Downloaded {len(api_entries)} APIs")

            # Process APIs with enhanced data
            processed_apis = [self._process_api(api) for api in api_entries]

            # Save to file
            output_file = self.output_dir / 'api_sources.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(processed_apis, f, indent=2, ensure_ascii=False)

            print(f"Successfully processed {len(processed_apis)} APIs")
            return processed_apis

        except requests.RequestException as e:
            print(f"Network error downloading APIs: {e}")
            return []
        except (ValueError, KeyError) as e:
            print(f"Data processing error: {e}")
            return []

    def _process_api(self, api):
        """Process individual API entry"""
        processed = {
            'name': api.get('API', 'Unknown').strip(),
            'description': api.get('Description', '').strip(),
            'url': api.get('Link', '').strip(),
            'category': api.get('Category', 'Other').strip(),
            'requires_key': self._determine_auth_requirement(api.get('Auth', '')),
            'search_tags': self._generate_search_tags(api)
        }
        return processed

    def _determine_auth_requirement(self, auth_field):
        """Determine if API requires authentication"""
        auth_lower = auth_field.lower().strip()
        return auth_lower not in ['', 'no', 'none', 'null']

    def _generate_search_tags(self, api):
        """Generate search tags for enhanced searchability"""
        tags = set()

        # Add category-based tags
        category_lower = api.get('Category', '').lower()
        if category_lower in self.category_tags:
            tags.update(self.category_tags[category_lower])

        # Extract meaningful words from description
        description = api.get('Description', '').lower()
        words = [word.strip('.,!?()[]') for word in description.split()]
        meaningful_words = [word for word in words if len(word) > 3 and word.isalpha()]
        tags.update(meaningful_words[:5])

        return ' '.join(sorted(tags))

    def generate_files(self):
        """Generate all Chrome extension files"""
        files_generated = []

        try:
            self._create_popup_html()
            files_generated.append('popup.html')

            self._create_popup_js()
            files_generated.append('popup.js')

            self._create_manifest()
            files_generated.append('manifest.json')

            print(f"Generated files: {', '.join(files_generated)}")

        except Exception as e:
            print(f"Error generating files: {e}")

    def _create_popup_html(self):
        """Generate popup HTML with improved styling"""
        html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>API Search</title>
    <style>
        body { width: 450px; padding: 15px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
        #search { width: 100%; padding: 8px; margin-bottom: 12px; border: 1px solid #ddd; border-radius: 4px; }
        .api-item { border: 1px solid #e0e0e0; margin: 8px 0; padding: 12px; border-radius: 6px; }
        .api-item:hover { background-color: #f8f9fa; }
        .api-name { font-weight: 600; font-size: 14px; margin-bottom: 4px; }
        .api-description { font-size: 13px; color: #333; margin-bottom: 6px; }
        .api-category { font-size: 11px; color: #666; margin-bottom: 8px; }
        .api-link { font-size: 12px; color: #1a73e8; text-decoration: none; }
        .api-link:hover { text-decoration: underline; }
        .no-results { text-align: center; color: #666; padding: 20px; }
    </style>
</head>
<body>
    <input type="text" id="search" placeholder="Search APIs (e.g., weather, finance, crypto)...">
    <div id="api-list"></div>
    <script src="popup.js"></script>
</body>
</html>"""

        with open(self.output_dir / 'popup.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

    def _create_popup_js(self):
        """Generate popup JavaScript with optimized search"""
        js_content = """document.addEventListener('DOMContentLoaded', function() {
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
});"""

        with open(self.output_dir / 'popup.js', 'w', encoding='utf-8') as f:
            f.write(js_content)

    def _create_manifest(self):
        """Generate Chrome extension manifest"""
        manifest = {
            "manifest_version": 3,
            "name": "API Data Source Finder",
            "version": "1.0",
            "description": "Find APIs and data sources for data analysis and development",
            "action": {
                "default_popup": "popup.html",
                "default_title": "API Finder"
            },
            "permissions": [],
            "icons": {
                "16": "icon16.png",
                "48": "icon48.png",
                "128": "icon128.png"
            }
        }

        with open(self.output_dir / 'manifest.json', 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)

    def build(self):
        """Build complete Chrome extension"""
        apis = self.download_and_process_apis()
        if apis:
            self.generate_files()
            print(f"\n✅ Extension built successfully with {len(apis)} APIs!")
            print("Load the extension in Chrome at chrome://extensions/")
        else:
            print("❌ Failed to build extension - no APIs downloaded")


def main():
    """Main entry point"""
    builder = ExtensionBuilder()
    builder.build()


if __name__ == "__main__":
    main()