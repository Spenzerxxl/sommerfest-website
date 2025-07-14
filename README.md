# Sommerfest 2025 - Anmeldungswebsite

## CORS-Problem GELÖST

**Problem:** Frontend (sommerfest.frankrath.de) → Backend (automatisierung.frankrath.de) = CORS-Fehler

**Lösung:** nginx Reverse-Proxy Route `/api/sommerfest` 

### Technische Details:

1. **Frontend:** Sendet GET-Requests an `/api/sommerfest` (Same-Origin)
2. **nginx-Proxy:** Leitet weiter an `https://automatisierung.frankrath.de/webhook/sommerfest-anmeldung`
3. **Backend:** n8n verarbeitet GET-Requests mit URL-Parametern

### Deployment:

1. In Coolify: Repository als Quelle verwenden
2. nginx-Konfiguration mit Proxy-Route hinzufügen
3. Environment: Static Site

### nginx-Konfiguration benötigt:

```nginx
location /api/sommerfest {
    proxy_pass https://automatisierung.frankrath.de/webhook/sommerfest-anmeldung;
    proxy_set_header Host automatisierung.frankrath.de;
    proxy_ssl_verify off;
    
    add_header 'Access-Control-Allow-Origin' '*' always;
    add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS' always;
    add_header 'Access-Control-Allow-Headers' 'Content-Type, Accept, Origin' always;
}
```

### Status: ✅ BEREIT FÜR DEPLOYMENT
