<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *'); 
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

// Handle preflight OPTIONS request
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// 1. Read the incoming JSON payload from your frontend
$inputData = json_decode(file_get_contents('php://input'), true);

if (!isset($inputData['userImage']) || !isset($inputData['garmentImage'])) {
    http_response_code(400);
    echo json_encode(["message" => "Missing user or garment image data."]);
    exit();
}

// 2. Prepare the payload for the AI API
// Note: You will need to replace 'YOUR_AI_API_ENDPOINT' and 'YOUR_API_KEY' 
// with the actual credentials of the try-on API you choose to route this through.
$aiApiEndpoint = 'YOUR_AI_API_ENDPOINT'; 
$apiKey = 'YOUR_API_KEY';

$payload = json_encode([
    "user_image" => $inputData['userImage'],
    "garment_image" => $inputData['garmentImage'],
    "category" => "upper_body"
]);

// 3. Initialize cURL to send the request securely
$ch = curl_init($aiApiEndpoint);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Authorization: Bearer ' . $apiKey
]);

// 4. Execute the request and handle the response
$response = curl_exec($ch);
$httpStatusCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$curlError = curl_error($ch);
curl_close($ch);

if ($curlError) {
    http_response_code(500);
    echo json_encode(["message" => "Server connection error: " . $curlError]);
    exit();
}

if ($httpStatusCode === 200) {
    // Assuming the AI API returns a JSON object with a 'generated_image_url' key
    $responseData = json_decode($response, true);
    
    if (isset($responseData['generated_image_url'])) {
        echo json_encode(["generated_image_url" => $responseData['generated_image_url']]);
    } else {
        http_response_code(500);
        echo json_encode(["message" => "Unexpected response format from AI API."]);
    }
} else {
    http_response_code($httpStatusCode);
    echo json_encode(["message" => "AI Generation Failed. Status Code: " . $httpStatusCode]);
}
?>