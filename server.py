import http.server
import socketserver
import os
import json
import sys
import threading
import time
from datetime import datetime
import subprocess

# Import the update_news function
from update_news import update_news_json

# Configuration
PORT = 8000
UPDATE_INTERVAL = 3600  # Update news every hour (in seconds)

# Custom request handler
class NewsAppHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Set the directory to serve files from
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)
    
    def log_message(self, format, *args):
        # Override to add timestamp
        sys.stderr.write("[%s] %s - %s\n" %
                         (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                          self.address_string(),
                          format % args))
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def update_news_periodically():
    """Update news data periodically in the background."""
    while True:
        try:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Updating news data...")
            update_news_json()
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Next update in {UPDATE_INTERVAL} seconds.")
        except Exception as e:
            print(f"Error in update thread: {str(e)}")
        
        # Sleep until next update
        time.sleep(UPDATE_INTERVAL)

def open_browser():
    """Open the browser to the app URL after a short delay."""
    time.sleep(1)
    url = f"http://localhost:{PORT}"
    print(f"Opening browser to {url}")
    
    # Try to open browser based on platform
    try:
        import webbrowser
        webbrowser.open(url)
    except:
        if sys.platform.startswith('darwin'):  # macOS
            subprocess.call(['open', url])
        elif sys.platform.startswith('win'):   # Windows
            subprocess.call(['start', url], shell=True)
        elif sys.platform.startswith('linux'): # Linux
            subprocess.call(['xdg-open', url])

def main():
    # Create handler and server
    handler = NewsAppHandler
    
    # Try to create the server, handling potential port conflicts
    try:
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            print(f"Serving at http://localhost:{PORT}")
            print("Press Ctrl+C to stop the server")
            
            # Start background thread for news updates
            update_thread = threading.Thread(target=update_news_periodically, daemon=True)
            update_thread.start()
            
            # Open browser
            browser_thread = threading.Thread(target=open_browser, daemon=True)
            browser_thread.start()
            
            # Start server
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 98 or e.errno == 10048:  # Address already in use
            print(f"Port {PORT} is already in use. The app may already be running.")
            print(f"Try opening http://localhost:{PORT} in your browser.")
            open_browser()
        else:
            print(f"Error starting server: {e}")
    except KeyboardInterrupt:
        print("\nServer stopped by user")

if __name__ == "__main__":
    # Initial news update
    print("Performing initial news update...")
    update_news_json()
    
    # Start server
    main()
