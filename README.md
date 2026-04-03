# Irrigation API Endpoints

A FastAPI-based irrigation management system with AI-powered decision making, anomaly detection, and moisture prediction.

## Base URL

```
http://localhost:8000/api/v1
```

---

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/irrigate` | Main AI pipeline - process sensor data through classification, prediction, anomaly detection, and decision making |
| POST | `/plants` | Create a new plant profile |
| GET | `/plants` | List all plant profiles |
| GET | `/plants/{plant_id}` | Get a specific plant profile by ID |
| DELETE | `/plants/{plant_id}` | Delete a plant profile |
| GET | `/history` | Get sensor reading history with trend statistics |
| GET | `/anomalies` | List recent anomaly events |
| PATCH | `/anomalies/{anomaly_id}/resolve` | Mark an anomaly as resolved |
| GET | `/predictions` | List recent moisture predictions |

---

## Authentication

Currently, no authentication is required. All endpoints are publicly accessible.

---

## Endpoints Detail

### 1. POST /irrigate

**Summary:** Process sensor data through AI pipeline

**Description:** This is the main pipeline endpoint that orchestrates the entire AI decision-making flow:
1. Stores raw sensor reading to database
2. Classifies plant type based on sensor data
3. Predicts future moisture levels (1h, 3h, 6h)
4. Detects anomalies in sensor data
5. Makes irrigation decision
6. Persists all results and returns enriched response

**Request Body:**

```json
{
  "sensor": {
    "moisture_percent": 45.5,
    "soil_status": "moist",
    "rain_percent": 0,
    "rain_status": "no_rain",
    "temp_celsius": 25.0,
    "humidity_percent": 60,
    "tank_status": "filled",
    "tank_fill_percent": 85,
    "last_pump_command": "OFF",
    "last_pump_command_at": "2024-01-15T10:30:00Z"
  },
  "weather": {
    "temp_current": 24.5,
    "humidity_current": 55,
    "precipitation_now": 0,
    "wind_speed": 12,
    "description": "partly cloudy",
    "rain_probability_next_6h": 20,
    "temp_next_6h": 26
  },
  "context": {
    "moisture_threshold": 30,
    "last_pump_command": "OFF",
    "last_pump_command_at": "2024-01-15T10:30:00Z"
  },
  "plant_id": 1
}
```

**Sensor Object Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `moisture_percent` | float | Current soil moisture percentage (0-100) |
| `soil_status` | string | Current soil status: "dry", "moist", "wet" |
| `rain_percent` | float | Rain sensor reading (0-100) |
| `rain_status` | string | Rain status: "no_rain", "light_rain", "heavy_rain" |
| `temp_celsius` | float | Current temperature in Celsius |
| `humidity_percent` | float | Ambient humidity percentage (0-100) |
| `tank_status` | string | Water tank status: "empty", "low", "filled", "overflowing" |
| `tank_fill_percent` | float | Water tank fill percentage (0-100) |
| `last_pump_command` | string | Last pump command: "ON", "OFF" |
| `last_pump_command_at` | string (datetime) | Timestamp of last pump command |

**Weather Object Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `temp_current` | float | Current temperature |
| `humidity_current` | float | Current humidity |
| `precipitation_now` | float | Current precipitation |
| `wind_speed` | float | Wind speed |
| `description` | string | Weather description |
| `rain_probability_next_6h` | float | Rain probability for next 6 hours (0-100) |
| `temp_next_6h` | float | Predicted temperature for next 6 hours |

**Context Object Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `moisture_threshold` | float | Minimum moisture threshold for irrigation decision |
| `last_pump_command` | string | Last pump command: "ON", "OFF" |
| `last_pump_command_at` | string (datetime) | Timestamp of last pump command |

**Response:**

```json
{
  "reading_id": 123,
  "classification": {
    "plant_type": "vegetable",
    "water_need": "high",
    "growth_stage": "mature",
    "decay_rate": 2.5
  },
  "prediction": {
    "predicted_moisture_1h": 42.3,
    "predicted_moisture_3h": 35.1,
    "predicted_moisture_6h": 25.8,
    "predicted_dry_at": "2024-01-15T16:30:00Z",
    "confidence_score": 0.85,
    "model_type": "linear_regression"
  },
  "anomalies": [
    {
      "anomaly_type": "rapid_moisture_drop",
      "severity": "medium",
      "description": "Moisture dropped 15% in last hour"
    }
  ],
  "decision": {
    "pump_command": "ON",
    "reason": "Moisture below threshold and no rain expected",
    "duration_seconds": 300
  },
  "insights": [
    "High water need plant detected",
    "Rain expected in next 6 hours: 20%"
  ],
  "recorded_at": "2024-01-15T12:00:00Z"
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `reading_id` | int | ID of the stored sensor reading |
| `classification` | object | Plant classification results |
| `prediction` | object | Moisture prediction results |
| `anomalies` | array | List of detected anomalies |
| `decision` | object | Irrigation decision |
| `insights` | array | List of insight messages |
| `recorded_at` | string | Timestamp of the reading |

**Classification Object:**

| Field | Type | Description |
|-------|------|-------------|
| `plant_type` | string | Type of plant: "vegetable", "fruit", "flower", "herb", "tree", "grass", "shrub", "succulent", "unknown" |
| `water_need` | string | Water requirement level: "low", "medium", "high" |
| `growth_stage` | string | Plant growth stage: "seedling", "vegetative", "flowering", "mature", "dormant" |
| `decay_rate` | float | Moisture decay rate per hour |

**Prediction Object:**

| Field | Type | Description |
|-------|------|-------------|
| `predicted_moisture_1h` | float | Predicted moisture after 1 hour |
| `predicted_moisture_3h` | float | Predicted moisture after 3 hours |
| `predicted_moisture_6h` | float | Predicted moisture after 6 hours |
| `predicted_dry_at` | string (datetime) | Predicted time when soil will become dry |
| `confidence_score` | float | Model confidence score (0-1) |
| `model_type` | string | Type of prediction model used |

**Anomaly Object:**

| Field | Type | Description |
|-------|------|-------------|
| `anomaly_type` | string | Type of anomaly detected |
| `severity` | string | Severity level: "low", "medium", "high", "critical" |
| `description` | string | Description of the anomaly |

**Decision Object:**

| Field | Type | Description |
|-------|------|-------------|
| `pump_command` | string | Pump command: "ON" or "OFF" |
| `reason` | string | Explanation for the decision |
| `duration_seconds` | int | Recommended pump duration in seconds |

---

### 2. POST /plants

**Summary:** Create a new plant profile

**Description:** Creates and stores a new plant profile in the database.

**Request Body:**

```json
{
  "name": "Tomato",
  "species": "Solanum lycopersicum",
  "plant_type": "vegetable",
  "water_need": "high",
  "optimal_moisture_min": 40,
  "optimal_moisture_max": 80,
  "optimal_temp_min": 18,
  "optimal_temp_max": 30,
  "growth_stage": "mature",
  "location": "greenhouse_a",
  "notes": "Requires regular pruning"
}
```

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Common name of the plant |
| `species` | string | No | Scientific species name |
| `plant_type` | string | No | Type: "vegetable", "fruit", "flower", "herb", "tree", "grass", "shrub", "succulent" |
| `water_need` | string | No | Water requirement: "low", "medium", "high" |
| `optimal_moisture_min` | float | No | Minimum optimal moisture percentage |
| `optimal_moisture_max` | float | No | Maximum optimal moisture percentage |
| `optimal_temp_min` | float | No | Minimum optimal temperature (Celsius) |
| `optimal_temp_max` | float | No | Maximum optimal temperature (Celsius) |
| `growth_stage` | string | No | Growth stage: "seedling", "vegetative", "flowering", "mature", "dormant" |
| `location` | string | No | Physical location of the plant |
| `notes` | string | No | Additional notes |

**Response:** Returns the created plant profile with assigned ID.

**Status Code:** 201 Created

---

### 3. GET /plants

**Summary:** List all plant profiles

**Description:** Retrieves all plant profiles stored in the database, ordered alphabetically by name.

**Query Parameters:** None

**Response:**

```json
[
  {
    "id": 1,
    "name": "Tomato",
    "species": "Solanum lycopersicum",
    "plant_type": "vegetable",
    "water_need": "high",
    "optimal_moisture_min": 40,
    "optimal_moisture_max": 80,
    "optimal_temp_min": 18,
    "optimal_temp_max": 30,
    "growth_stage": "mature",
    "location": "greenhouse_a",
    "notes": "Requires regular pruning",
    "created_at": "2024-01-15T10:00:00Z"
  }
]
```

---

### 4. GET /plants/{plant_id}

**Summary:** Get a plant profile by ID

**Description:** Retrieves a specific plant profile by its unique identifier.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `plant_id` | int | Unique identifier of the plant |

**Response:** Returns the plant profile if found.

**Status Codes:**
- 200 OK: Success
- 404 Not Found: Plant profile not found

---

### 5. DELETE /plants/{plant_id}

**Summary:** Delete a plant profile

**Description:** Removes a plant profile from the database.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `plant_id` | int | Unique identifier of the plant |

**Status Codes:**
- 204 No Content: Successfully deleted
- 404 Not Found: Plant profile not found

---

### 6. GET /history

**Summary:** Get sensor reading history and trend stats

**Description:** Retrieves historical sensor readings with aggregated statistics.

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `plant_id` | int | null (optional) | Filter by specific plant ID |
| `limit` | int | 50 | Number of records to return (1-500) |

**Response:**

```json
{
  "readings": [
    {
      "id": 123,
      "moisture_percent": 45.5,
      "temp_celsius": 25.0,
      "humidity_percent": 60,
      "rain_percent": 0,
      "tank_fill_percent": 85,
      "tank_status": "filled",
      "last_pump_command": "OFF",
      "recorded_at": "2024-01-15T12:00:00Z"
    }
  ],
  "avg_moisture": 48.25,
  "min_moisture": 30.5,
  "max_moisture": 65.0,
  "total_anomalies": 5,
  "pump_on_count": 12
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `readings` | array | List of sensor readings |
| `avg_moisture` | float | Average moisture percentage |
| `min_moisture` | float | Minimum moisture percentage |
| `max_moisture` | float | Maximum moisture percentage |
| `total_anomalies` | int | Total anomaly count |
| `pump_on_count` | int | Total number of pump ON commands |

---

### 7. GET /anomalies

**Summary:** List recent anomaly events

**Description:** Retrieves recent anomaly events detected by the system.

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `plant_id` | int | null (optional) | Filter by specific plant ID |
| `resolved` | bool | null (optional) | Filter by resolved status |
| `limit` | int | 50 | Number of records to return (1-200) |

**Response:**

```json
[
  {
    "id": 1,
    "plant_id": 1,
    "reading_id": 123,
    "anomaly_type": "rapid_moisture_drop",
    "severity": "medium",
    "description": "Moisture dropped 15% in last hour",
    "resolved": false,
    "detected_at": "2024-01-15T12:00:00Z"
  }
]
```

---

### 8. PATCH /anomalies/{anomaly_id}/resolve

**Summary:** Mark an anomaly as resolved

**Description:** Updates the resolved status of an anomaly event.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `anomaly_id` | int | Unique identifier of the anomaly |

**Response:**

```json
{
  "id": 1,
  "resolved": true
}
```

**Status Codes:**
- 200 OK: Success
- 404 Not Found: Anomaly not found

---

### 9. GET /predictions

**Summary:** List recent moisture predictions

**Description:** Retrieves recent moisture predictions from the AI prediction engine.

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `plant_id` | int | null (optional) | Filter by specific plant ID |
| `limit` | int | 20 | Number of records to return (1-100) |

**Response:**

```json
[
  {
    "id": 1,
    "plant_id": 1,
    "reading_id": 123,
    "predicted_moisture_1h": 42.3,
    "predicted_moisture_3h": 35.1,
    "predicted_moisture_6h": 25.8,
    "predicted_dry_at": "2024-01-15T16:30:00Z",
    "confidence_score": 0.85,
    "model_type": "linear_regression",
    "created_at": "2024-01-15T12:00:00Z"
  }
]
```

---

## Error Responses

All endpoints may return the following error responses:

| Status Code | Description |
|-------------|-------------|
| 400 | Bad Request - Invalid input data |
| 404 | Not Found - Resource not found |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error |

**Error Response Format:**

```json
{
  "detail": "Error message description"
}
```

---

## Rate Limiting

Currently, no rate limiting is enforced.

---

## Data Models

### SensorReading

Stores raw sensor data from irrigation system:
- moisture_percent, soil_status, rain_percent, rain_status
- temp_celsius, humidity_percent
- tank_status, tank_fill_percent
- Weather data (temp, humidity, precipitation, wind, description)
- Context data (last_pump_command, moisture_threshold)

### PlantProfile

Stores plant information:
- name, species, plant_type, water_need
- optimal_moisture_min/max, optimal_temp_min/max
- growth_stage, location, notes

### MoisturePrediction

Stores AI prediction results:
- predicted_moisture_1h, predicted_moisture_3h, predicted_moisture_6h
- predicted_dry_at, confidence_score, model_type

### AnomalyEvent

Stores detected anomalies:
- anomaly_type, severity, description, resolved status

### IrrigationDecision

Stores irrigation decisions:
- pump_command (ON/OFF), reason, duration_seconds

---

## Example Usage

### Using curl

```bash
# Create a plant profile
curl -X POST http://localhost:8000/api/v1/plants \
  -H "Content-Type: application/json" \
  -d '{"name": "Tomato", "plant_type": "vegetable", "water_need": "high"}'

# Get all plants
curl http://localhost:8000/api/v1/plants

# Run irrigation AI pipeline
curl -X POST http://localhost:8000/api/v1/irrigate \
  -H "Content-Type: application/json" \
  -d '{
    "sensor": {
      "moisture_percent": 45.5,
      "soil_status": "moist",
      "rain_percent": 0,
      "rain_status": "no_rain",
      "temp_celsius": 25.0,
      "humidity_percent": 60,
      "tank_status": "filled",
      "tank_fill_percent": 85,
      "last_pump_command": "OFF",
      "last_pump_command_at": "2024-01-15T10:30:00Z"
    },
    "weather": {
      "temp_current": 24.5,
      "humidity_current": 55,
      "precipitation_now": 0,
      "wind_speed": 12,
      "description": "partly cloudy",
      "rain_probability_next_6h": 20,
      "temp_next_6h": 26
    },
    "context": {
      "moisture_threshold": 30,
      "last_pump_command": "OFF",
      "last_pump_command_at": "2024-01-15T10:30:00Z"
    },
    "plant_id": 1
  }'

# Get history
curl "http://localhost:8000/api/v1/history?limit=10&plant_id=1"

# Get anomalies
curl "http://localhost:8000/api/v1/anomalies?resolved=false"
```

### Using Python (requests)

```python
import requests

base_url = "http://localhost:8000/api/v1"

# Create plant
plant_data = {
    "name": "Tomato",
    "species": "Solanum lycopersicum",
    "plant_type": "vegetable",
    "water_need": "high",
    "optimal_moisture_min": 40,
    "optimal_moisture_max": 80
}
response = requests.post(f"{base_url}/plants", json=plant_data)

# Run irrigation pipeline
irrigate_data = {
    "sensor": {
        "moisture_percent": 45.5,
        "soil_status": "moist",
        "rain_percent": 0,
        "rain_status": "no_rain",
        "temp_celsius": 25.0,
        "humidity_percent": 60,
        "tank_status": "filled",
        "tank_fill_percent": 85,
        "last_pump_command": "OFF",
        "last_pump_command_at": "2024-01-15T10:30:00Z"
    },
    "weather": {
        "temp_current": 24.5,
        "humidity_current": 55,
        "precipitation_now": 0,
        "wind_speed": 12,
        "description": "partly cloudy",
        "rain_probability_next_6h": 20,
        "temp_next_6h": 26
    },
    "context": {
        "moisture_threshold": 30,
        "last_pump_command": "OFF",
        "last_pump_command_at": "2024-01-15T10:30:00Z"
    },
    "plant_id": 1
}
response = requests.post(f"{base_url}/irrigate", json=irrigate_data)
```

---

## OpenAPI/Swagger Documentation

Once the server is running, interactive API documentation is available at:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | sqlite+aiosql:///./irrigation.db |
| `HOST` | Server host | 0.0.0.0 |
| `PORT` | Server port | 8000 |

---

## Dependencies

- **FastAPI** - Web framework
- **SQLAlchemy** - ORM (async)
- **aiosqlite** - Async SQLite driver
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server