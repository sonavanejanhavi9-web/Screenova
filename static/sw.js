/* ═══════════════════════════════════════════════════
   Screenova – sw.js  (Service Worker)
   Handles background push notifications
   ═══════════════════════════════════════════════════ */

const CACHE = "screenova-v1";

// Install: cache key assets
self.addEventListener("install", e => {
  self.skipWaiting();
});

self.addEventListener("activate", e => {
  self.clients.claim();
});

// Listen for push events from the server (future use with Web Push API)
self.addEventListener("push", e => {
  const data = e.data ? e.data.json() : {};
  const title = data.title || "Screenova Alert";
  const options = {
    body:  data.body  || "Check your screen time!",
    icon:  data.icon  || "/static/icon.png",
    badge: data.badge || "/static/icon.png",
    tag:   data.tag   || "screenova",
    renotify: true,
    actions: [
      { action: "open",    title: "Open App" },
      { action: "dismiss", title: "Dismiss"  }
    ]
  };
  e.waitUntil(self.registration.showNotification(title, options));
});

// Handle notification click
self.addEventListener("notificationclick", e => {
  e.notification.close();
  if (e.action === "open" || !e.action) {
    e.waitUntil(clients.openWindow("/dashboard"));
  }
});
