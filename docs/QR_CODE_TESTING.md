# QR Code Testing Guide

## Quick Start

To test the QR code integration, you can use any of the example QR codes below.

## Pre-Registered Test QR Codes

These QR codes are already in the device registry and will work immediately:

### 1. Samsung Washing Machine
**QR Code Content:**
```
SAMSUNG-WF42H5200-001
```
**Device Info:**
- Brand: Samsung
- Model: WF42H5200
- Type: Washing Machine
- Serial: WF42H5200001
- Year: 2021

**Test Questions:**
- "My washing machine won't drain water"
- "What does error E3 mean on my Samsung?"
- "How do I clean the filter?"
- "The door won't lock"

---

### 2. LG Microwave
**QR Code Content:**
```
LG-MS2595DIS-001
```
**Device Info:**
- Brand: LG
- Model: MS2595DIS
- Type: Microwave
- Serial: LG20210001
- Year: 2021

**Test Questions:**
- "The turntable isn't spinning"
- "Why isn't my microwave heating?"
- "How do I set the timer?"
- "Display malfunction"

---

### 3. Bosch Dishwasher
**QR Code Content:**
```
BOSCH-SMI68TS06E-001
```
**Device Info:**
- Brand: Bosch
- Model: SMI68TS06E
- Type: Dishwasher
- Serial: BOSCH001
- Year: 2020

**Test Questions:**
- "Water isn't draining from my dishwasher"
- "No water inlet"
- "Pump noise"
- "Error codes"

---

### 4. Whirlpool Oven
**QR Code Content:**
```
WHIRLPOOL-WFE725H0HV-001
```
**Device Info:**
- Brand: Whirlpool
- Model: WFE725H0HV
- Type: Oven
- Serial: WP20210001
- Year: 2021

**Test Questions:**
- "Oven not heating"
- "Temperature sensor issue"
- "Door lock problem"
- "How do I calibrate the temperature?"

---

## How to Generate Your Own QR Codes

### Option 1: Use Online Generator (Recommended)

1. Go to [https://qr-server.com/](https://qr-server.com/)
2. In "Your text:" field, enter one of the formats below
3. Click "Genereate QR Code"
4. Print or display on screen
5. Scan with phone/webcam

### Option 2: Using Python

```python
import qrcode

# Generate QR code for Samsung washer
qr = qrcode.QRCode()
qr.add_data('SAMSUNG-WF42H5200-001')
qr.make()
img = qr.make_image()
img.save('samsung_washer.png')
```

### Option 3: Using Command Line

```bash
# Using qrencode (Linux/Mac)
echo 'SAMSUNG-WF42H5200-001' | qrencode -o samsung.png

# Using python one-liner
python3 -c "import qrcode; qr = qrcode.QRCode(); qr.add_data('SAMSUNG-WF42H5200-001'); qr.make().make_image().save('samsung.png')"
```

## QR Code Format Examples

### Format 1: Standard Format (Easiest)
```
SAMSUNG-WF42H5200-001
LG-MS2595DIS-001
BOSCH-SMI68TS06E-001
```
✅ Direct lookup in registry

### Format 2: JSON Format
```json
{"brand":"Samsung","model":"WF42H5200","applianceType":"washer","serialNumber":"WF42H5200001"}
```
✅ Parsed into object

### Format 3: Colon-Separated
```
Samsung:WF42H5200:washer
LG:MS2595DIS:microwave:LG20210001:2021
Bosch:SMI68TS06E:dishwasher
```
✅ Parsed into parts

### Format 4: Space-Separated
```
Samsung WF42H5200 washer
LG MS2595DIS microwave
Bosch SMI68TS06E dishwasher
```
✅ Parsed into parts

## Testing Procedure

### Step 1: Start the Application
```bash
# Terminal 1 - Backend
python src/backend/main.py

# Terminal 2 - Frontend
npm run dev
```

### Step 2: Open in Browser
```
http://localhost:5173
```

### Step 3: Navigate to Chat
1. Login/Signup if needed
2. Enter chat interface

### Step 4: Test QR Scanning

**Method A: With Real QR Code**
1. Print or display a QR code on phone
2. Click "Scan QR Code" button
3. Allow camera access
4. Point at QR code

**Method B: With Test Data**
1. Click "Scan QR Code" button
2. Open browser DevTools (F12)
3. Go to Console
4. Paste test code below:

```javascript
// Simulate QR scan for Samsung washer
const deviceInfo = {
  qrCode: "SAMSUNG-WF42H5200-001",
  brand: "Samsung",
  model: "WF42H5200",
  applianceType: "washer",
  serialNumber: "WF42H5200001",
  manufactureYear: 2021
};

// Trigger the scan handler
// (This depends on how Chat component is structured)
console.log("Test device:", deviceInfo);
```

### Step 5: Ask Device-Specific Questions

After scanning:
1. Notice device appears in header
2. Type a question like: "My washing machine won't drain"
3. AI responds with device-specific answer
4. Answers include sources from device manual

## Expected Behavior

### Successful Scan
```
✅ QR Code detected
✅ Device info extracted (Brand: Samsung, Model: WF42H5200)
✅ Device shown in header with active indicator
✅ Queries now include device context
✅ Answers are device-specific with manual sources
```

### Failed Scan
```
❌ Camera access denied
  → Check browser permissions
  → Try HTTPS connection
  → Try different browser

❌ QR code not recognized
  → Check QR code content
  → Try different format
  → Ensure QR code is properly generated

❌ Device not found in registry
  → Register device first in deviceRegistry.ts
  → Use supported format
  → Check spelling of brand/model
```

## Sample Test Scenarios

### Scenario 1: Drainage Issue
```
Device: Samsung WF42H5200 (Washer)
Question: "My washing machine won't drain water"

Expected Response:
- Should mention Samsung-specific drainage system
- Provide step-by-step troubleshooting
- Reference page number from manual
- Suggest checking filter (common Samsung issue)
- Include safety warnings if applicable
```

### Scenario 2: Error Code Query
```
Device: LG MS2595DIS (Microwave)
Question: "What does error E1 mean?"

Expected Response:
- If E1 is in device's error codes
- Provide LG-specific error meaning
- Suggest solutions from LG manual
- Reference manual page
- Offer next steps
```

### Scenario 3: Generic Question
```
Device: Bosch SMI68TS06E (Dishwasher)
Question: "How do I clean the filter?"

Expected Response:
- Device-specific cleaning procedure
- Bosch-specific component names
- Step-by-step with safety considerations
- Reference to manual page numbers
- Attach safety level (safe/caution)
```

### Scenario 4: Safety Issue
```
Device: Whirlpool WFE725H0HV (Oven)
Question: "I smell gas from the oven"

Expected Response:
- Immediate safety alert ⚠️
- Mark as DANGER level
- Recommend professional service
- DO NOT attempt DIY
- Include emergency contacts
- Reference safety section of manual
```

## Troubleshooting Test Issues

### Issue: Camera not working
**Solution:**
- Check browser console for permission errors
- Ensure HTTPS (required for camera)
- Try `http://localhost:5173` for dev
- Check system camera permissions

### Issue: QR code not scanning
**Solution:**
- Ensure QR code is in focus
- Good lighting conditions
- Not blurry or damaged
- Try moving closer/farther
- Use different QR code format

### Issue: Device not recognized
**Solution:**
- Check device is in deviceRegistry.ts
- Verify QR code content matches key
- Try manual format: `Brand Model Type`
- Check console for parse errors

### Issue: No device-specific answer
**Solution:**
- Verify device manual is indexed
- Check that chunks contain answer
- Try without device context first
- Check backend logs

## Performance Testing

### Load Testing QR Scanner
1. Generate 100 QR codes
2. Scan rapidly
3. Check for performance degradation
4. Monitor memory usage

### Test Device Context
1. Load 10 devices sequentially
2. Verify correct device displayed
3. Check query accuracy
4. Monitor response times

### Test with Large Manuals
1. Add device with 1000+ manual pages
2. Test search performance
3. Verify results are still relevant
4. Check response time

## Expected Response Times

| Operation | Time |
|-----------|------|
| QR Scanning | < 100ms |
| Device Lookup | < 10ms |
| Query with Context | 2-3 seconds |
| Source Attribution | < 500ms |
| Device Context Switch | < 50ms |

## Advanced Testing

### Test Multiple Devices
```javascript
// Test switching between devices
const devices = [
  'SAMSUNG-WF42H5200-001',
  'LG-MS2595DIS-001',
  'BOSCH-SMI68TS06E-001'
];

devices.forEach(qrCode => {
  console.log(`Testing: ${qrCode}`);
  // Simulate scan
});
```

### Test Invalid QR Codes
```javascript
const invalidCodes = [
  'INVALID-CODE',
  '12345',
  'Samsung',
  '',
  'null',
  undefined
];

invalidCodes.forEach(code => {
  console.log(`Testing invalid: ${code}`);
  // Should gracefully handle
});
```

### Test JSON QR Codes
```javascript
const jsonQR = JSON.stringify({
  brand: 'Samsung',
  model: 'WF42H5200',
  applianceType: 'washer'
});

console.log('JSON QR:', jsonQR);
// Should parse correctly
```

## Conclusion

The QR code integration is now fully testable. Use these guides to verify functionality across different devices and scenarios. All pre-registered devices should work immediately!

Happy testing! 🚀
