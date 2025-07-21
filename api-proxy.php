<?php
/**
 * Sommerfest API Proxy - CORS-Problem Lösung
 * Proxied n8n-Webhooks um CORS-Preflight-Issues zu umgehen
 */

// CORS-Headers setzen (für alle Requests)
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With');
header('Access-Control-Allow-Credentials: true');

// OPTIONS-Preflight sofort beantworten
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Content-Type für JSON-Responses
header('Content-Type: application/json');

// n8n Base-URL
define('N8N_BASE_URL', 'https://automatisierung.frankrath.de/webhook');

// API-Endpunkt-Mapping
$endpoints = [
    'participants' => N8N_BASE_URL . '/get-participants',
    'preferences' => N8N_BASE_URL . '/get-preferences', 
    'buffet' => N8N_BASE_URL . '/buffet-uebersicht',
    'helfer' => N8N_BASE_URL . '/helfer-statistik',
    'login' => N8N_BASE_URL . '/orga-login'
];

// Gewünschten Endpunkt aus URL-Parameter lesen
$endpoint = $_GET['endpoint'] ?? '';

// Validierung: Existiert der Endpunkt?
if (!isset($endpoints[$endpoint])) {
    http_response_code(400);
    echo json_encode([
        'error' => 'Invalid endpoint',
        'available_endpoints' => array_keys($endpoints)
    ]);
    exit();
}

// n8n-URL aufbauen
$n8n_url = $endpoints[$endpoint];

// Für Login: URL-Parameter weiterleiten
if ($endpoint === 'login') {
    $username = $_GET['username'] ?? '';
    $password = $_GET['password'] ?? '';
    
    if ($username && $password) {
        $n8n_url .= '?username=' . urlencode($username) . '&password=' . urlencode($password);
    }
}

// cURL-Request an n8n
$curl = curl_init();

curl_setopt_array($curl, [
    CURLOPT_URL => $n8n_url,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT => 30,
    CURLOPT_FOLLOWLOCATION => true,
    CURLOPT_SSL_VERIFYPEER => true,
    CURLOPT_HTTPHEADER => [
        'User-Agent: Sommerfest-API-Proxy/1.0'
    ]
]);

// Request ausführen
$response = curl_exec($curl);
$http_code = curl_getinfo($curl, CURLINFO_HTTP_CODE);
$curl_error = curl_error($curl);

curl_close($curl);

// Fehlerbehandlung
if ($curl_error) {
    http_response_code(502);
    echo json_encode([
        'error' => 'Proxy error: ' . $curl_error,
        'endpoint' => $endpoint,
        'n8n_url' => $n8n_url
    ]);
    exit();
}

// HTTP-Status Code weiterleiten
http_response_code($http_code);

// Response weiterleiten
if ($response === false || $http_code >= 400) {
    echo json_encode([
        'error' => 'n8n API error',
        'http_code' => $http_code,
        'endpoint' => $endpoint
    ]);
} else {
    // Erfolgreiche Response weiterleiten
    echo $response;
}

// Debug-Info (nur bei Bedarf)
if (isset($_GET['debug'])) {
    error_log("Sommerfest API Proxy - Endpoint: $endpoint, HTTP: $http_code, URL: $n8n_url");
}
?>
