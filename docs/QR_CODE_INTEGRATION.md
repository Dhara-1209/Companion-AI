# QR Code Integration Guide for CompanionAI

## Overview

The QR code integration system allows users to scan QR codes on appliances to automatically load device-specific manuals and provide targeted troubleshooting guidance. The system scans the QR code, extracts device information (brand, model, serial number), and uses that context to provide more accurate answers.

## System Architecture

```
QR Code (on appliance)
        ↓
   [QR Scanner Component]
        ↓
   [parseQRCodeData]
        ↓
   [Device Registry Lookup]
        ↓
   [Load Device Context: Brand, Model, Manual Path]
        ↓
   [Device-Specific Queries with AI]
        ↓
   [Filtered Answers from Device Manual]
```

## Components

### 1. Device Registry (`src/config/deviceRegistry.ts`)

Maintains a mapping of QR codes to device information.

**DeviceInfo Interface:**
```typescript
interface DeviceInfo {
  qrCode: string;
  brand: string;
  model: string;
  applianceType: 'washer' | 'dishwasher' | 'oven' | 'microwave' | 'vacuum';
  serialNumber?: string;
  manufactureYear?: number;
  manualPath?: string;
  errorCodes?: string[];
  commonIssues?: string[];
}
```

**Key Functions:**
- `getDeviceByQRCode(qrCode)` - Direct QR code lookup
- `parseQRCodeData(qrData)` - Parse multiple QR code formats
- `isValidDeviceInfo(device)` - Validate device information
- `getDevicesByBrand(brand)` - Get all devices by brand
- `getDevicesByCategory(category)` - Get devices by appliance type

### 2. QR Scanner Component (`src/app/components/QRScanner.tsx`)

Real-time QR code scanning using device camera.

**Features:**
- Live video feed with QR code highlighting
- Automatic device info extraction
- Error handling for camera access
- Validation before returning data

**Usage:**
```tsx
<QRScanner 
  onScan={(device) => handleQRScan(device)}
  onClose={() => setShowQRScanner(false)}
/>
```

### 3. Chat Integration (`src/app/components/Chat.tsx`)

Main chat interface with QR scanning support.

**Device Context Display:**
- Shows active device information in header
- Displays brand, model, serial number, manufacture year
- One-click device clearing

**Device-Specific Queries:**
- Automatically includes brand and model in API requests
- Receives filtered answers from device-specific manual
- Shows relevant error codes and common issues

### 4. API Service (`src/services/api.ts`)

Frontend API client with device-specific endpoints.

**New Methods:**
```typescript
async getDeviceSpecificAnswer(
  query: string,
  brand: string,
  model: string,
  k?: number
): Promise<AnswerResponse>
```

Automatically passes device context to backend.

### 5. Backend Endpoints (`src/backend/main.py`)

**POST /device/answer** - Device-specific query endpoint
- Validates brand and model are provided
- Enhances query with device context
- Returns answers filtered to device manual
- Includes source attribution

## QR Code Format Support

The system supports multiple QR code formats:

### Format 1: Direct QR Code Mapping
```
QR Code Content: SAMSUNG-WF42H5200-001
```
Maps directly to registry entry.

### Format 2: JSON Format
```json
{
  "qrCode": "SAMSUNG-WF42H5200-001",
  "brand": "Samsung",
  "model": "WF42H5200",
  "applianceType": "washer",
  "serialNumber": "WF42H5200001",
  "manufactureYear": 2021
}
```

### Format 3: Colon-Separated
```
Samsung:WF42H5200:washer:WF42H5200001:2021
```
Format: `Brand:Model:Type:Serial:Year`

### Format 4: Space-Separated
```
Samsung WF42H5200 washer
```
Format: `Brand Model Type`

## How It Works

### Step 1: User Scans QR Code
1. User taps "Scan QR Code" button in chat
2. QRScanner component opens with camera feed
3. User positions appliance QR code in frame

### Step 2: QR Code Processing
1. QR Scanner detects QR code
2. Extracts raw data from QR code
3. `parseQRCodeData()` converts to DeviceInfo
4. `isValidDeviceInfo()` validates the data

### Step 3: Device Loading
1. Device context stored in Chat component state
2. Device info displayed in header with brand/model
3. User can now ask device-specific questions

### Step 4: Device-Specific Queries
1. User asks question about their device
2. Chat sends query + brand + model to backend
3. Backend enhances search context with device info
4. AI searches device-specific manual chunks
5. Returns targeted answer with relevant sources

### Step 5: Device Clearing
1. User clicks "Clear Device" button
2. Device context removed from state
3. Returns to general appliance troubleshooting

## Adding New Devices

### To register a new device:

```typescript
// In src/config/deviceRegistry.ts
deviceRegistry.set('BRAND-MODEL-###', {
  qrCode: 'BRAND-MODEL-###',
  brand: 'Brand Name',
  model: 'Model Number',
  applianceType: 'washer', // or dishwasher, oven, microwave, vacuum
  serialNumber: 'OPTIONAL-SERIAL',
  manufactureYear: 2024,
  manualPath: 'manuals/brand-model.pdf',
  errorCodes: ['E1', 'E2', 'E3'],
  commonIssues: ['Issue 1', 'Issue 2']
});

// Or use the addDevice function:
import { addDevice } from '@/config/deviceRegistry';
addDevice('NEW-QR-CODE', deviceInfo);
```

## Error Codes Support

The registry includes common error codes for each device:

```typescript
errorCodes: ['E1', 'E2', 'E3', 'E4', 'E5'],
commonIssues: [
  'Not draining',
  'Spinning issue',
  'Water leakage',
  'Door lock problem'
]
```

When users report an error code, the system:
1. Checks if code is in device's error list
2. Filters manual chunks to error-related content
3. Provides device-specific troubleshooting steps

## Safety Features

The device context enhances safety:
1. **Model-specific hazards**: Different models have different safety concerns
2. **Error code matching**: Quickly identifies dangerous situations
3. **Manual accuracy**: Provides solutions from correct manual, not generic advice
4. **Source attribution**: Always shows which manual provided the answer

## Performance Optimizations

1. **Instant QR parsing**: No network call needed for QR processing
2. **Cached device info**: Registry is in-memory for O(1) lookup
3. **Filtered search**: Device context reduces search space
4. **Faster results**: Fewer, more relevant manual chunks to process

## Testing QR Codes

### Test Scanner:
1. Go to Chat interface
2. Click "Scan QR Code" button
3. Use browser's developer tools to enter test data:
```javascript
// In browser console, simulate QR scan
document.querySelector('[data-testid="qr-scan-input"]').value = "SAMSUNG-WF42H5200-001"
```

### Generate QR Codes:
Use any QR code generator:
1. [QR-Server.com](https://qr-server.com/)
2. [QRCode.tech](https://www.qrcode.tech/)
3. Print and test with phone camera

**Example QR code content:**
```
SAMSUNG-WF42H5200-001
```

## Troubleshooting

### QR Code Not Recognized
- Ensure QR code contains registered device format
- Check if device is in deviceRegistry
- Try manual entry (Brand + Model)

### Camera Access Denied
- Check browser permissions
- Try different browser
- Ensure HTTPS connection (required for camera)

### Device Info Not Loading
- Verify DeviceInfo has required fields (brand, model)
- Check console for parse errors
- Try different QR code format

### No Relevant Answers
- Verify device manual chunks are indexed
- Check if device brand/model matches manual content
- Try general query without device context

## Future Enhancements

1. **Cloud Registry**: Move device registry to database
2. **User Manuals Upload**: Allow uploading custom manuals
3. **OCR Integration**: Extract text from appliance photos
4. **Barcode Support**: Support non-QR barcodes
5. **Multi-language**: Translate manuals to user language
6. **Voice Input**: Ask about error codes verbally
7. **Historical Context**: Remember previously scanned devices
8. **Offline Mode**: Cache device manuals locally

## API Examples

### Scan QR Code in Chat
```bash
# Frontend detects QR code, calls:
POST /device/answer
{
  "query": "My washing machine won't drain",
  "brand": "Samsung",
  "model": "WF42H5200",
  "k": 10
}

# Response includes device-specific sources and safety checks
{
  "answer": "Based on your Samsung WF42H5200 manual...",
  "safety_flag": false,
  "safety_level": "safe",
  "sources": [
    {
      "filename": "samsung-wf42h5200-manual.pdf",
      "page": 45,
      "brand": "Samsung",
      "model": "WF42H5200",
      "relevance_score": 0.95
    }
  ],
  "processing_time": 1.23,
  "confidence_score": 0.89
}
```

## Database Schema (Future)

```sql
CREATE TABLE devices (
  id INT PRIMARY KEY,
  qr_code VARCHAR(100) UNIQUE,
  brand VARCHAR(50),
  model VARCHAR(50),
  appliance_type VARCHAR(20),
  serial_number VARCHAR(100),
  manufacture_year INT,
  manual_path VARCHAR(255),
  error_codes JSON,
  common_issues JSON,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TABLE device_manuals (
  id INT PRIMARY KEY,
  device_id INT,
  manual_file VARCHAR(255),
  page_count INT,
  indexed_chunks INT,
  uploaded_at TIMESTAMP,
  FOREIGN KEY (device_id) REFERENCES devices(id)
);
```

## Conclusion

The QR code integration provides a seamless way for users to get device-specific appliance troubleshooting. By scanning a QR code on their appliance, users instantly load the correct manual and receive targeted, accurate solutions to their problems.
