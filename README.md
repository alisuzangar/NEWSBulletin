# خبرنامه ایران - Mobile App

This is a Progressive Web App (PWA) for the Iran News Bulletin. It can be installed on iOS devices and provides a mobile app experience with offline capabilities.

## Features

- **Standalone App**: Works directly on iPhone without requiring a server
- **Direct RSS Feed Integration**: Fetches news directly from RSS feeds
- **Offline Support**: Works without internet connection after initial load
- **Mobile-Optimized Interface**: Designed specifically for mobile devices
- **PWA Capabilities**: Can be installed on iPhone home screen
- **Dark/Light Mode**: Toggle between dark and light themes
- **Category Filtering**: Filter news by different categories
- **Refresh Button**: Manually refresh news when needed
- **Responsive Design**: Works on all screen sizes

## How to Install on iPhone

1. **Deploy the app** (see DEPLOYMENT.md for options)
2. **On your iPhone**:
   - Open Safari and navigate to the deployed app URL
   - Tap the Share button (box with arrow) at the bottom of Safari
   - Scroll down and tap "Add to Home Screen"
   - Name the app and tap "Add"
   - The app will now appear on your home screen with its icon

## Using the App

- **Refresh News**: Tap the "بروزرسانی اخبار" button to fetch the latest news
- **Filter Categories**: Use the category buttons to filter news by topic
- **Toggle Theme**: Tap the light/dark mode button to change the theme
- **Read Articles**: Tap on article titles to read the full article
- **Offline Use**: The app will work offline, showing previously loaded news

## Technical Details

- **Progressive Web App**: Uses modern web technologies for an app-like experience
- **Service Worker**: Enables offline functionality and caching
- **Local Storage**: Stores news data for offline access
- **CORS Proxy**: Uses a proxy to fetch RSS feeds across domains
- **Responsive Design**: CSS designed for mobile-first experience

## Files

- `index.html` - The main app interface and functionality
- `manifest.json` - PWA configuration for installation
- `service-worker.js` - Handles offline functionality and caching
- `icons/` - Directory containing app icons (placeholders)
- `DEPLOYMENT.md` - Guide for deploying the app

## Customization

- **RSS Feeds**: Edit the `RSS_FEEDS` object in index.html to change news sources
- **Categories**: Modify the category buttons and corresponding feeds
- **Keywords**: Update the `PREDEFINED_KEYWORDS` object to change keyword extraction
- **Styling**: Customize the CSS variables in the `:root` selector to change colors

## Troubleshooting

- If buttons don't work on iPhone, ensure you're using the latest version of iOS
- If the app doesn't install, make sure you're using Safari browser
- If news doesn't load, check your internet connection or try a different CORS proxy
- For offline testing, load the app first, then enable Airplane Mode
