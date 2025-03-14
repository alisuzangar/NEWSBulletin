#!/usr/bin/env python3
"""
Simple HTTP server for testing the News App locally.
This script starts a local web server to serve the PWA files.
"""

import http.server
import socketserver
import os
import webbrowser
import socket
import threading
import time

# Configuration
PORT = 8000

def get_local_ip():
    """Get the local IP address of the machine."""
    try:
        # Create a socket to determine the local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Doesn't need to be reachable
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'  # Fallback to localhost

def open_browser():
    """Open the browser to the app URL after a short delay."""
    time.sleep(1)
    local_ip = get_local_ip()
    url = f"http://{local_ip}:{PORT}"
    print(f"\nOpening browser to {url}")
    print(f"On your iPhone, open Safari and navigate to: {url}")
    print("Then tap the Share button and select 'Add to Home Screen'")
    
    # Try to open browser
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Could not open browser automatically: {e}")
        print(f"Please manually open {url} in your browser")

def main():
    """Start the HTTP server."""
    # Change to the directory containing this script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Create handler and server
    handler = http.server.SimpleHTTPRequestHandler
    
    # Try to create the server, handling potential port conflicts
    try:
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            local_ip = get_local_ip()
            print(f"Starting server at http://{local_ip}:{PORT}")
            print("Press Ctrl+C to stop the server")
            
            # Open browser in a separate thread
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
    main()
