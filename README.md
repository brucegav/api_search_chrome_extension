# API Data Source Finder

A Chrome extension that helps data analysts and data scientists discover APIs and data sources easily. Built with a comprehensive database of 1,500+ curated APIs.

## Features
- **Smart Search** - Weighted search algorithm prioritizing relevant results
- **Comprehensive Database** - 1,500+ APIs across multiple categories
- **Enhanced Filtering** - Search by category, description, name, and tags
- **Performance Optimized** - Debounced search with result limiting
- **Modern UI** - Clean interface with hover effects and responsive design
- **API Requirements** - Clear indication of authentication needs
- **Direct Links** - Quick access to API documentation

## Categories Included
Finance • Weather • Sports • Health • Government • Entertainment • Social Media • Transportation • Cryptocurrency • Machine Learning • and many more!

## How It Works
1. **Data Source**: Automatically downloads latest API data from the public-apis repository
2. **Processing**: Converts and enhances API data with searchable tags
3. **Search**: Weighted algorithm ranks results by relevance
4. **Display**: Shows top matches with key information and documentation links

## Installation
1. Clone this repository
2. Run the extension builder: `python extension_builder.py`
3. Open Chrome and go to `chrome://extensions/`
4. Enable "Developer mode"
5. Click "Load unpacked" and select the project folder
6. Start searching for APIs!

## Development

### Prerequisites
- Python 3.7+
- `requests` library: `pip install requests`
- `pillow` library for icon generation: `pip install pillow`

### File Structure
```
api_search_chrome_extension/
├── extension_builder.py    # Main build script (OOP design)
├── create_icons.py        # Icon generator script
├── popup.html            # Extension popup interface
├── popup.js              # Search functionality with weighted scoring
├── manifest.json         # Chrome extension configuration
├── api_sources.json      # Generated API database
├── icon16.png           # Extension icons
├── icon48.png
├── icon128.png
└── README.md
```

### Build Process
The `ExtensionBuilder` class handles:
- Downloading API data from external source
- Converting to optimized format with search tags
- Generating all Chrome extension files
- Creating professional icons

### Customization
- **Add Categories**: Extend `category_tags` in the `ExtensionBuilder` class
- **Modify Search**: Adjust weights in the `calculateRelevanceScore` function
- **UI Changes**: Update the HTML/CSS in `_create_popup_html` method
- **Icons**: Run `create_icons.py` to generate new icon variations

## Technical Details
- **Architecture**: Object-oriented Python build system
- **Data Processing**: JSON-based API database with enhanced metadata
- **Search Algorithm**: Multi-field weighted scoring with debouncing
- **Performance**: Lazy loading, result limiting, and caching
- **Security**: HTML escaping and XSS prevention

## Recent Updates
- Refactored to object-oriented design
- Added comprehensive error handling
- Implemented custom icon system
- Enhanced search performance
- Improved UI/UX with modern styling
- Added security best practices

## Future Enhancements
- Favorites system for bookmarking APIs
- Advanced filtering by authentication type
- API usage examples and code snippets
- Export functionality for API lists
- Chrome Web Store publication

## Contributing
This project started as a learning exercise and continues to evolve. Feel free to suggest APIs to add, report bugs, or propose improvements!

## License
Open source - feel free to use and modify for your own projects.

---

**Built for data professionals who need quick access to quality APIs and data sources.**