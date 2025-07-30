# API Search Chrome Extension

A Chrome extension that helps data analysts and data scientists discover APIs and data sources easily.

## Features
- Search through curated APIs by category, description, and keywords
- Weighted search algorithm prioritizing relevant results
- Categories include Finance, Weather, Demographics, Sports, Healthcare, and more
- Displays API requirements (whether API key needed)
- Direct links to API documentation

## Current Status
- [x] Chrome extension structure
- [x] Weighted search functionality  
- [x] Python script to generate extension files
- [ ] Complete API database (in progress)

## Files
- `extension_builder.py` - Python script that generates all Chrome extension files
- `popup.html` - Extension popup interface
- `popup.js` - Search functionality with weighted scoring
- `manifest.json` - Chrome extension configuration
- `api_sources.json` - API database (generated from CSV)
- `api_list.csv` - Source data for APIs (work in progress)

## Usage
1. Run `python extension_builder.py` to generate extension files
2. Load the extension in Chrome developer mode
3. Use the search box to find relevant APIs

## Contributing
This is a learning project. Feel free to suggest APIs to add or improvements!