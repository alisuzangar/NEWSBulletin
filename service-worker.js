const CACHE_NAME = 'news-app-v1';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './manifest.json',
  'https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap'
];

// Install event - cache assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Caching app assets');
        return cache.addAll(ASSETS_TO_CACHE);
      })
      .then(() => self.skipWaiting())
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch event - serve from cache, fall back to network
self.addEventListener('fetch', event => {
  // Skip CORS proxy requests - we don't want to cache these
  if (event.request.url.includes('api.allorigins.win')) {
    return;
  }
  
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Cache hit - return the response from the cached version
        if (response) {
          return response;
        }
        
        // Not in cache - return the result from the live server
        // and cache it for future
        return fetch(event.request)
          .then(networkResponse => {
            // Don't cache if not a valid response or if it's a CORS request
            if (!networkResponse || networkResponse.status !== 200 || 
                networkResponse.type !== 'basic' || 
                event.request.url.includes('api.allorigins.win')) {
              return networkResponse;
            }

            // IMPORTANT: Clone the response. A response is a stream
            // and can only be consumed once. Since we want to return
            // the response to the browser and also cache it, we need to clone it.
            const responseToCache = networkResponse.clone();

            caches.open(CACHE_NAME)
              .then(cache => {
                cache.put(event.request, responseToCache);
              });

            return networkResponse;
          })
          .catch(error => {
            // Can't access the network at all
            console.log('Fetch failed:', error);
            
            // For font requests, return a fallback
            if (event.request.url.includes('fonts.googleapis.com') || 
                event.request.url.includes('fonts.gstatic.com')) {
              // Just fail gracefully for font requests
              return;
            }
            
            // For other requests, return a simple offline page if we can't match from cache
            if (event.request.mode === 'navigate') {
              return caches.match('./index.html');
            }
          });
      })
  );
});

// Listen for messages from the client
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

// Background sync for news updates when coming back online
self.addEventListener('sync', event => {
  if (event.tag === 'sync-news') {
    event.waitUntil(
      self.clients.matchAll().then(clients => {
        clients.forEach(client => {
          client.postMessage({
            type: 'REFRESH_NEWS'
          });
        });
      })
    );
  }
});
