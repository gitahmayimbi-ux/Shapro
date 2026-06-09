# Shapro API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication
Currently, the API is open. Future versions will implement JWT authentication.

## Endpoints

### Farms

#### Get All Farms
```
GET /farms
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Green Valley Farm",
    "location": "Nairobi, Kenya",
    "latitude": -1.2921,
    "longitude": 36.8219,
    "area_hectares": 50
  }
]
```

#### Create Farm
```
POST /farms
```

**Request Body:**
```json
{
  "name": "Green Valley Farm",
  "location": "Nairobi, Kenya",
  "latitude": -1.2921,
  "longitude": 36.8219,
  "area_hectares": 50
}
```

**Response:** Returns created farm object with ID

---

### Weather

#### Get Weather Data
```
GET /weather/{farm_id}
```

**Response:**
```json
[
  {
    "id": 1,
    "farm_id": 1,
    "temperature": 24.5,
    "humidity": 65,
    "rainfall": 2.5,
    "wind_speed": 3.2,
    "recorded_at": "2024-06-09T14:30:00"
  }
]
```

---

### Crops

#### Get All Crops
```
GET /crops
```

#### Create Crop
```
POST /crops
```

**Request Body:**
```json
{
  "farm_id": 1,
  "crop_name": "Maize",
  "planting_date": "2024-05-01T00:00:00",
  "expected_harvest": "2024-09-01T00:00:00",
  "area_planted": 20
}
```

---

### Recommendations

#### Get Smart Recommendations
```
GET /recommendations?farm_id=1
```

**Response:**
```json
[
  {
    "type": "planting",
    "crop": "Maize",
    "confidence": 0.85,
    "reason": "Optimal temperature and humidity detected"
  },
  {
    "type": "irrigation",
    "crop": "Tomato",
    "confidence": 0.92,
    "reason": "Soil moisture below recommended threshold"
  }
]
```

---

### Analytics

#### Get Analytics
```
GET /analytics?farm_id=1
```

**Response:**
```json
{
  "total_farms": 5,
  "total_crops": 12,
  "average_temperature": 24.5,
  "average_humidity": 65.2,
  "predicted_yield": 8500,
  "yield_unit": "kg/hectare"
}
```

---

## Error Handling

All errors return appropriate HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error

## Rate Limiting
Currently no rate limiting. Will be implemented in future versions.
