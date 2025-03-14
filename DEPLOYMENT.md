# Deploying the News App to iPhone

This guide explains how to deploy the standalone news app to an iPhone.

## Option 1: Using GitHub Pages (Recommended)

GitHub Pages provides free hosting for static websites, making it perfect for this PWA.

1. Create a GitHub repository
2. Upload all the files in the `mobile_app` directory to the repository
3. Enable GitHub Pages in the repository settings
4. Access the app using the GitHub Pages URL (e.g., https://yourusername.github.io/news-app/)
5. On your iPhone, open Safari and navigate to this URL
6. Tap the Share button and select "Add to Home Screen"

## Option 2: Using a Web Server

If you have access to a web server:

1. Upload all the files in the `mobile_app` directory to your web server
2. Make sure the server is configured to serve static files
3. Access the app using your server's URL
4. On your iPhone, open Safari and navigate to this URL
5. Tap the Share button and select "Add to Home Screen"

## Option 3: Using a Local Server for Testing

For testing purposes, you can use a simple HTTP server:

1. Navigate to the `mobile_app` directory
2. Run a simple HTTP server:
   - Python 3: `python -m http.server 8000`
   - Python 2: `python -m SimpleHTTPServer 8000`
   - Node.js: `npx serve`
3. On your iPhone, make sure you're on the same network as your computer
4. Find your computer's IP address (e.g., 192.168.1.100)
5. On your iPhone, open Safari and navigate to http://YOUR_IP_ADDRESS:8000
6. Tap the Share button and select "Add to Home Screen"

## Important Notes

1. **HTTPS Requirement**: For full PWA functionality including service workers, you need HTTPS. GitHub Pages provides this automatically.

2. **CORS Issues**: The app uses a CORS proxy to fetch RSS feeds. If you encounter CORS issues, you might need to use a different CORS proxy or set up your own.

3. **Icon Files**: Replace the placeholder icon files in the `icons` directory with actual PNG images of the appropriate sizes.

4. **Testing on iPhone**: Make sure you're using Safari on iPhone, as other browsers might not support "Add to Home Screen" functionality.

5. **Offline Functionality**: The app is designed to work offline after the first load. Test this by enabling Airplane Mode after loading the app.
