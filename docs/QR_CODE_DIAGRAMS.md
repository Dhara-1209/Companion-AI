# QR Code Integration - Visual Diagrams

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER INTERFACE (React)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Chat Component                                          │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │ Header                                           │   │   │
│  │  │ ┌────────────────────────────────────────────┐  │   │   │
│  │  │ │ 📱 Active Device: Samsung WF42H5200       │  │   │   │
│  │  │ │ (if device scanned)                        │  │   │   │
│  │  │ └────────────────────────────────────────────┘  │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  │                                                          │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │ Toolbar                                          │   │   │
│  │  │  [Send] [Record] [Upload] [QR Scan] [Logout]    │   │   │
│  │  │                    ↑                             │   │   │
│  │  │                   Click                          │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  │                                                          │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │ Messages                                         │   │   │
│  │  │ [Chat messages with device context]             │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  │                                                          │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │ Input Box                                        │   │   │
│  │  │ [Enter your question...] [Send]                 │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  QRScanner Component (Modal)                            │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │ Scan QR Code                              [X]    │   │   │
│  │  ├──────────────────────────────────────────────────┤   │   │
│  │  │                                                  │   │   │
│  │  │          📹 Live Camera Feed                     │   │   │
│  │  │                                                  │   │   │
│  │  │     [QR Code Detected - Samsung WF42H5200]      │   │   │
│  │  │                                                  │   │   │
│  │  ├──────────────────────────────────────────────────┤   │   │
│  │  │ Position the QR code within the frame           │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   QR Scanner Library (qr-scanner)                │
├─────────────────────────────────────────────────────────────────┤
│  • Detects QR code from camera feed                             │
│  • Extracts raw data: "SAMSUNG-WF42H5200-001"                   │
│  • Returns data to Chat component via onScan callback           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                  Device Registry Parser                          │
├─────────────────────────────────────────────────────────────────┤
│  parseQRCodeData(rawData)                                       │
│  • Try direct lookup: SAMSUNG-WF42H5200-001                     │
│  • Try JSON parsing                                             │
│  • Try colon-separated format                                   │
│  • Try space-separated format                                   │
│  • Return: DeviceInfo object or null                            │
│                                                                  │
│  DeviceInfo: {                                                  │
│    qrCode: "SAMSUNG-WF42H5200-001",                             │
│    brand: "Samsung",                                            │
│    model: "WF42H5200",                                          │
│    applianceType: "washer",                                     │
│    serialNumber: "WF42H5200001",                                │
│    manufactureYear: 2021                                        │
│  }                                                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                  Chat Component State                            │
├─────────────────────────────────────────────────────────────────┤
│  currentDevice = {                                              │
│    brand: "Samsung",                                            │
│    model: "WF42H5200",                                          │
│    applianceType: "washer"                                      │
│  }                                                              │
│                                                                  │
│  Display in header:                                             │
│  "Active Device: Samsung WF42H5200"                             │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┴──────────────────────┐
        │                                            │
        ↓                                            ↓
    [Clear Device]                           [Ask Questions]
        │                                            │
        ↓                                            ↓
  Remove context                          User types query
  Remove from header                      │
                                          ↓
                                  Include device context:
                                  Query: "My washer won't drain"
                                  Brand: "Samsung"
                                  Model: "WF42H5200"
```

---

## Query Processing Flow

```
User Query (with Device Context)
│
├─ Query: "My washing machine won't drain"
├─ Brand: "Samsung"
└─ Model: "WF42H5200"
│
↓
┌─────────────────────────────────────────────────────────────────┐
│                    API Service (Frontend)                        │
├─────────────────────────────────────────────────────────────────┤
│  apiService.getDeviceSpecificAnswer(                            │
│    query: "My washing machine won't drain",                     │
│    brand: "Samsung",                                            │
│    model: "WF42H5200"                                           │
│  )                                                              │
└─────────────────────────────────────────────────────────────────┘
│
↓ POST /answer
│
┌─────────────────────────────────────────────────────────────────┐
│                  FastAPI Backend (Python)                       │
├─────────────────────────────────────────────────────────────────┤
│  1. Safety Check                                                │
│     └─ Is this a safe question? (Emergency detection)           │
│                                                                  │
│  2. Query Enhancement                                           │
│     └─ Enhanced: "[Device: Samsung WF42H5200] won't drain"      │
│                                                                  │
│  3. Vector Search (FAISS)                                       │
│     └─ Search for relevant manual chunks                        │
│     └─ Filter by brand "Samsung" (if metadata available)        │
│     └─ Top-K results (default: 10)                              │
│                                                                  │
│  Returned Chunks:                                               │
│  ┌────────────────────────────────────────┐                     │
│  │ Chunk 1: "Drainage troubleshooting"    │                     │
│  │ Score: 0.95                             │                     │
│  │ Source: Samsung WF42H5200 manual       │                     │
│  │ Page: 45                                │                     │
│  ├────────────────────────────────────────┤                     │
│  │ Chunk 2: "Filter maintenance"          │                     │
│  │ Score: 0.89                             │                     │
│  │ Source: Samsung WF42H5200 manual       │                     │
│  │ Page: 52                                │                     │
│  └────────────────────────────────────────┘                     │
│                                                                  │
│  4. LLM Generation                                              │
│     Input: Query + Top chunks + Brand/Model context            │
│     Model: Ollama/NIM/Template Mode                            │
│     Output: Device-specific answer                             │
│                                                                  │
│  5. Response Assembly                                           │
│     └─ Answer                                                   │
│     └─ Safety flags                                             │
│     └─ Sources (with device info)                               │
│     └─ Confidence score                                         │
│     └─ Processing metrics                                       │
└─────────────────────────────────────────────────────────────────┘
│
↓ JSON Response
│
┌─────────────────────────────────────────────────────────────────┐
│                     Response JSON                               │
├─────────────────────────────────────────────────────────────────┤
│  {                                                              │
│    "answer": "Based on your Samsung WF42H5200...",              │
│    "safety_flag": false,                                        │
│    "safety_level": "safe",                                      │
│    "sources": [                                                 │
│      {                                                          │
│        "filename": "samsung-wf42h5200-manual.pdf",              │
│        "page": 45,                                              │
│        "brand": "Samsung",                                      │
│        "model": "WF42H5200",                                    │
│        "relevance_score": 0.95                                  │
│      }                                                          │
│    ],                                                           │
│    "processing_time": 1.23,                                     │
│    "confidence_score": 0.89                                     │
│  }                                                              │
└─────────────────────────────────────────────────────────────────┘
│
↓ API Service (Frontend)
│
┌─────────────────────────────────────────────────────────────────┐
│                   Chat Component Display                        │
├─────────────────────────────────────────────────────────────────┤
│  Assistant Message:                                             │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Based on your Samsung WF42H5200 manual...             │    │
│  │                                                        │    │
│  │  Step 1: Check the filter...                           │    │
│  │  Step 2: Verify water level...                         │    │
│  │                                                        │    │
│  │  ⚠️ Safety Level: SAFE                                 │    │
│  │  📚 Sources:                                           │    │
│  │     • Samsung WF42H5200 Manual - Page 45              │    │
│  │       (Relevance: 95%)                                 │    │
│  │     • Samsung WF42H5200 Manual - Page 52              │    │
│  │       (Relevance: 89%)                                 │    │
│  │  ⏱️  Response Time: 1.23s                              │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
│  User can now:                                                  │
│  • Ask follow-up questions                                      │
│  • Click on sources to view manual                              │
│  • Clear device to ask general questions                        │
│  • Scan another device                                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Interaction Diagram

```
                      ┌──────────────────┐
                      │  React App       │
                      │  (App.tsx)       │
                      └────────┬─────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ↓                     ↓
          ┌──────────────────┐   ┌──────────────────┐
          │  Login Component │   │  Chat Component  │
          └──────────────────┘   └────────┬─────────┘
                                          │
                ┌─────────────────────────┼─────────────────────────┐
                │                         │                         │
                ↓                         ↓                         ↓
        ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
        │ QRScanner Comp   │   │ Toolbar Comp     │   │ Messages Area    │
        │                  │   │                  │   │                  │
        │ • Camera access  │   │ • Scan button    │   │ • Chat display   │
        │ • QR detection   │   │ • Clear device   │   │ • Device context │
        │ • Data parsing   │   │ • Logout button  │   │ • Sources show   │
        └────────┬─────────┘   └──────────────────┘   └──────────────────┘
                 │
                 ↓
        ┌──────────────────┐
        │ Device Registry  │
        │                  │
        │ parseQRCodeData()│
        │ isValidDeviceInfo│
        │ getDeviceByQRCode│
        └────────┬─────────┘
                 │
                 ↓
        ┌──────────────────┐
        │ API Service      │
        │                  │
        │ getAnswer()      │
        │ getDeviceSpecific│
        │ uploadFile()     │
        └────────┬─────────┘
                 │
                 ↓
        ┌──────────────────────────────────────┐
        │     Backend FastAPI Server           │
        │                                      │
        │ • /health                            │
        │ • /answer                            │
        │ • /device/answer                     │
        │ • /upload                            │
        │ • /metrics                           │
        └────────┬─────────────────────────────┘
                 │
    ┌────────────┼────────────┬────────────┐
    │            │            │            │
    ↓            ↓            ↓            ↓
┌────────┐ ┌──────────┐ ┌─────────┐ ┌──────────┐
│Safety  │ │Vector DB │ │AI Model │ │Metadata  │
│Checker │ │(FAISS)   │ │(Ollama) │ │Registry  │
│        │ │          │ │(NIM)    │ │          │
└────────┘ └──────────┘ └─────────┘ └──────────┘
```

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    QR CODE DATA FLOW                             │
└─────────────────────────────────────────────────────────────────┘

Physical Device
│
├─ QR Code Label
│  └─ Contains encoded data
│
↓
Camera (Smartphone/Laptop)
│
├─ Captures image
├─ Sends to QRScanner library
│
↓
QR Scanner Library (qr-scanner.js)
│
├─ Detects QR code region
├─ Decodes data
├─ Returns: "SAMSUNG-WF42H5200-001"
│
↓
QRScanner Component (React)
│
├─ Receives raw QR data
├─ Calls: parseQRCodeData(data)
├─ Validates: isValidDeviceInfo()
├─ Returns: DeviceInfo object
│
↓
Chat Component (React)
│
├─ Receives DeviceInfo
├─ Stores: currentDevice state
├─ Displays: Device header
├─ Updates: Queries with context
│
↓
API Service (Frontend)
│
├─ Constructs request:
│  ├─ query: "My washer won't drain"
│  ├─ brand: "Samsung"
│  └─ model: "WF42H5200"
│
↓
POST /answer (Backend)
│
├─ Receives: {query, brand, model}
├─ Enhances: Query with device context
├─ Searches: FAISS vector DB
├─ Filters: Device-specific chunks
├─ Generates: Answer using AI
├─ Packages: Response with sources
│
↓
Response JSON (Backend)
│
├─ answer: "Based on your device..."
├─ sources: [{brand, model, page, score}]
├─ safety_level: "safe"
├─ processing_time: 1.23
│
↓
Chat Component Display (Frontend)
│
├─ Renders: Answer text
├─ Shows: Device attribution
├─ Displays: Source references
├─ Shows: Safety warnings
│
↓
User sees:
│
├─ Full answer
├─ Device-specific content
├─ Manual references
├─ Solution steps
```

---

## Device Registry Data Structure

```
Device Registry (Map<string, DeviceInfo>)
│
├─ "SAMSUNG-WF42H5200-001" → {
│  ├─ qrCode: "SAMSUNG-WF42H5200-001"
│  ├─ brand: "Samsung"
│  ├─ model: "WF42H5200"
│  ├─ applianceType: "washer"
│  ├─ serialNumber: "WF42H5200001"
│  ├─ manufactureYear: 2021
│  ├─ manualPath: "manuals/samsung-wf42h5200.pdf"
│  ├─ errorCodes: ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8"]
│  └─ commonIssues: ["Not draining", "Spinning issue", "Water leakage"]
│
├─ "LG-MS2595DIS-001" → {
│  ├─ qrCode: "LG-MS2595DIS-001"
│  ├─ brand: "LG"
│  ├─ model: "MS2595DIS"
│  ├─ applianceType: "microwave"
│  └─ ...
│
├─ "BOSCH-SMI68TS06E-001" → {
│  ├─ qrCode: "BOSCH-SMI68TS06E-001"
│  ├─ brand: "Bosch"
│  ├─ model: "SMI68TS06E"
│  ├─ applianceType: "dishwasher"
│  └─ ...
│
└─ ... more devices
```

---

## QR Code Format Parsing Flow

```
Raw QR Data: Input
│
├─ Try Format 1: Direct Lookup
│  ├─ Check if data is in registry keys
│  ├─ If found → Return DeviceInfo
│  └─ If not → Continue
│
├─ Try Format 2: JSON
│  ├─ Check if starts with "{"
│  ├─ Parse JSON.parse()
│  ├─ Extract {brand, model, applianceType}
│  ├─ If valid → Return DeviceInfo
│  └─ If not → Continue
│
├─ Try Format 3: Colon-Separated
│  ├─ Split by ":"
│  ├─ Check if 3+ parts
│  ├─ Map: [brand, model, type, serial, year]
│  ├─ If valid → Return DeviceInfo
│  └─ If not → Continue
│
├─ Try Format 4: Space-Separated
│  ├─ Split by space
│  ├─ Check if 2+ parts
│  ├─ Map: [brand, model, type]
│  ├─ If valid → Return DeviceInfo
│  └─ If not → Continue
│
├─ Try Fuzzy Matching
│  ├─ Check registry keys for partial matches
│  ├─ Case-insensitive search
│  ├─ If match found → Return DeviceInfo
│  └─ If not → Continue
│
└─ Return null (Invalid QR code)
```

---

## Safety & Validation Flow

```
QR Code Data
│
├─ Syntax Validation
│  ├─ Check if valid format
│  ├─ Parse without errors
│  └─ Extract required fields
│
├─ Data Validation
│  ├─ Has brand? (required)
│  ├─ Has model? (required)
│  ├─ Validate appliance type
│  └─ Optional: serial, year
│
├─ Registry Validation
│  ├─ Device exists in registry? (optional)
│  ├─ Metadata available? (optional)
│  └─ Manual chunks indexed? (optional)
│
└─ UI Validation
   ├─ Display clear error if invalid
   ├─ Allow retry on QR scanner
   ├─ Suggest manual entry
   └─ Show guidance
```

---

## Integration Points

```
Frontend (React) ↔ Backend (FastAPI)
│
├─ QRScanner Component
│  └─ Sends: DeviceInfo object
│     Receives: (no backend call needed for QR parsing)
│
├─ API Service
│  ├─ Sends: {query, brand, model}
│  └─ Receives: {answer, sources, safety_level, ...}
│
├─ Chat Component
│  ├─ Stores: currentDevice state
│  ├─ Sends: Enhanced queries
│  └─ Displays: Device-specific responses
│
└─ Backend Endpoints
   ├─ /health → Check system status
   ├─ /answer → Process general queries
   └─ /device/answer → Process device-specific queries
```

---

This visual documentation complements the text documentation in:
- `docs/QR_CODE_INTEGRATION.md`
- `docs/QR_CODE_TESTING.md`
- `IMPLEMENTATION_COMPLETE.md`
