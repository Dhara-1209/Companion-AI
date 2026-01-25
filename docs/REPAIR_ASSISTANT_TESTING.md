# Personalized Repair Assistant - Testing Guide

## 🧪 Test Environment Setup

### Prerequisites
- CompanionAI running (frontend: `npm run dev`, backend: `python src/backend/main.py`)
- Browser with access to `http://localhost:5173`
- Test user account available (use default "John" or create new)

### Test Data Appliances

Pre-configured test appliances:
- **Samsung WF42H5200** (Washing Machine) - Common issues: water not draining, noises
- **LG LDT5678** (Dishwasher) - Common issues: not cleaning, leaking
- **Bosch HBI5500** (Oven) - Common issues: temperature not holding, door stuck
- **Whirlpool WMH78019** (Microwave) - Common issues: won't heat, display dark

---

## ✅ Test Scenarios

### Test 1: Add New Appliance

**Objective**: Verify appliance can be added with all fields

**Steps**:
1. Click "My Appliances" button (settings icon in header)
2. Sidebar opens on right showing appliance manager
3. Fill in form:
   - Brand: `Samsung`
   - Model: `WM6000`
   - Type: `Washer`
   - Serial: `ABC123456`
   - Purchase Date: `01/15/2022`
4. Click "Add Appliance" button
5. Verify appliance appears in list below form

**Expected Result**: 
- ✅ New appliance added to list
- ✅ Toast notification shows success
- ✅ Form clears for next entry
- ✅ Appliance shows in "My Appliances" list

**Failure Scenarios**:
- ❌ Missing required fields → Form validation shows error
- ❌ Invalid date format → Date picker shows error
- ❌ Server error → Toast shows error message

---

### Test 2: View Appliance Status Indicators

**Objective**: Verify status badges display correctly

**Steps**:
1. With appliances in list, check each appliance card
2. Look for status indicators:
   - Alert badge (red, if active)
   - Overdue maintenance badge (orange, if tasks overdue)
   - Repair count
   - Maintenance status

**Expected Result**:
- ✅ New appliance shows no alerts (0 repairs, no maintenance due)
- ✅ Icons are color-coded
- ✅ Counts are accurate

---

### Test 3: Log a Repair

**Objective**: Verify repair records can be logged with all details

**Steps**:
1. Click on appliance name to select it
2. Sidebar switches to "Repair History" view for selected appliance
3. Fill in repair form:
   - Issue: `Water not draining properly`
   - Symptoms:
     - `Pooling water at bottom`
     - `Beeping error code E3`
   - Resolution: `Cleaned filter and drain pump`
   - Parts Replaced: `Drain seal`
   - Serviced By: `DIY`
   - Cost: `45.00`
4. Click "Log Repair" button
5. Verify repair appears in history list

**Expected Result**:
- ✅ Repair added to history (newest first)
- ✅ All fields displayed correctly
- ✅ Date automatically set to today
- ✅ Toast confirmation shown

**Data Validation**:
- Symptoms should be multi-line with bullet points
- Cost should be optional but validated as number if provided
- Repair type (DIY/Professional) affects badge color

---

### Test 4: View Repair History

**Objective**: Verify repair records display in correct order

**Steps**:
1. With appliance selected, view repairs in history
2. Verify at least 2 repairs are logged (from previous tests)
3. Check that:
   - Newest repairs appear first
   - Date format is readable (e.g., "Jan 15, 2024")
   - Repair type shows correct badge (DIY in blue, Professional in purple)

**Expected Result**:
- ✅ Repairs sorted by date (newest first)
- ✅ All fields visible and readable
- ✅ Expandable details for each repair

---

### Test 5: View Repair Statistics

**Objective**: Verify stats calculate correctly

**Steps**:
1. After logging 2+ repairs, scroll to bottom of repair history
2. View summary statistics:
   - Total Repairs: [count]
   - DIY Repairs: [count]
   - Professional Repairs: [count]
   - Total Spent: [sum of costs]
3. Verify calculations match logged repairs

**Expected Result**:
- ✅ Numbers match logged repairs
- ✅ Costs sum correctly
- ✅ DIY/Professional split is accurate

**Example**:
```
Logged repairs:
1. DIY - $45
2. Professional - $120
3. DIY - $30

Expected stats:
- Total: 3
- DIY: 2
- Professional: 1
- Total Spent: $195
```

---

### Test 6: View Maintenance Tasks

**Objective**: Verify default maintenance tasks load for appliance

**Steps**:
1. Appliance Manager shows list of appliances
2. Click on appliance name
3. Look for "Maintenance Tasks" section
4. Verify tasks appear for appliance type:
   - Washing Machine: Clean filter (6 months), Inspect hoses (1 year)
   - Dishwasher: Clean filter (3 months)
   - Microwave: Clean interior (2 months)
   - Oven: Self-clean (6 months)
   - Vacuum: Clean filter (3 months)

**Expected Result**:
- ✅ Default tasks populate automatically
- ✅ Next due date calculated correctly
- ✅ Can be marked as complete

---

### Test 7: Mark Maintenance Task Complete

**Objective**: Verify task completion updates dates

**Steps**:
1. In ApplianceManager, find maintenance section
2. Find overdue task (if any)
3. Click "Mark Done" or checkmark button
4. Verify:
   - Task marked as complete
   - Last completed date updates
   - Next due date recalculates (e.g., 6 months from today)
   - Overdue badge disappears from appliance

**Expected Result**:
- ✅ Task completion recorded
- ✅ Dates update correctly
- ✅ Status badges refresh immediately

---

### Test 8: Trigger Recurring Issue Alert

**Objective**: Verify alert generates when issue repeats

**Steps**:
1. Log first repair with issue: `Water not draining`
2. Log second repair with same issue: `Water not draining`
3. Check for alert in appliance status or sidebar
4. Alert should show:
   - Title: "Recurring issue detected"
   - Description: Mentions issue repeats (2+ times)
   - Severity: CRITICAL

**Expected Result**:
- ✅ Alert appears after 2nd occurrence
- ✅ Alert title mentions "recurring"
- ✅ Alert recommends action (professional service, etc.)

---

### Test 9: Warranty Expiry Alert

**Objective**: Verify warranty alert triggers

**Steps**:
1. Add appliance with warranty date set to tomorrow
2. Check alerts
3. Alert should appear:
   - Title: "Warranty expiring soon"
   - Days remaining shown
   - Severity: CRITICAL (within 7 days)

**Expected Result**:
- ✅ Alert triggers for near-expiry warranties
- ✅ Expires old alerts when warranty passes
- ✅ Severity increases as expiry approaches

**Test Data**: `Warranty Expiry: tomorrow's date`

---

### Test 10: Acknowledge Alert

**Objective**: Verify alerts can be dismissed

**Steps**:
1. Active alert visible in appliance status
2. Click on alert or acknowledge button
3. Alert moves to acknowledged status
4. No longer shows in active alerts

**Expected Result**:
- ✅ Alert marked as acknowledged
- ✅ Disappears from active list
- ✅ Can be unacknowledged if needed

---

### Test 11: Delete Appliance

**Objective**: Verify appliance can be removed

**Steps**:
1. In ApplianceManager, find appliance to remove
2. Click delete/trash icon
3. Confirm removal
4. Verify:
   - Appliance removed from list
   - All repairs still in history (optional backup)
   - Status indicators update

**Expected Result**:
- ✅ Appliance deleted from list
- ✅ Associated repairs deleted (if designed that way)
- ✅ No orphaned records

---

### Test 12: View User Statistics

**Objective**: Verify stats aggregate across all appliances

**Steps**:
1. Add 2+ appliances
2. Log repairs across different appliances
3. Click on user stats (if available in UI)
4. View aggregated statistics:
   - Total appliances: [count]
   - Total repairs: [sum]
   - DIY vs Professional split
   - Total spent
   - Common issues across all appliances

**Expected Result**:
- ✅ Stats aggregate correctly
- ✅ Numbers match sum of individual appliances
- ✅ Common issues ranked by frequency

**Example Data**:
```
Appliance 1 (Washer):
- Repair 1: "Water not draining" - DIY - $45
- Repair 2: "Water not draining" - Professional - $120

Appliance 2 (Dishwasher):
- Repair 1: "Not cleaning" - DIY - $30

Expected stats:
- Total appliances: 2
- Total repairs: 3
- DIY repairs: 2 ($75)
- Professional: 1 ($120)
- Common issues: ["Water not draining" (2x), "Not cleaning" (1x)]
```

---

## 🔄 Integration Tests

### Test 13: QR Code + Repair Assistant Integration

**Objective**: Verify QR code device context works with repair assistant

**Steps**:
1. Scan device QR code (or simulate with test code)
2. Device name appears in header
3. Click "My Appliances"
4. Find appliance in list (should match scanned device)
5. Log repair with device context
6. Later, when asking about appliance, system shows repair history

**Expected Result**:
- ✅ QR code identifies appliance correctly
- ✅ Repair history available for that specific device
- ✅ Chat can reference past repairs in responses

---

### Test 14: Chat Integration - Show Alerts

**Objective**: Verify alerts display in chat interface

**Steps**:
1. Create appliance with active alert
2. Engage in chat about the appliance
3. Verify alert shows in:
   - Header when appliance selected
   - Chat context for responses
   - Sidebar status badge

**Expected Result**:
- ✅ Alerts visible in chat interface
- ✅ Chat responses reference alerts when relevant
- ✅ Visual prominence of critical alerts

---

### Test 15: Sidebar Show/Hide

**Objective**: Verify sidebar toggles smoothly

**Steps**:
1. Click "My Appliances" button
2. Sidebar slides in from right
3. Chat adjusts width
4. Click button again or X button
5. Sidebar closes
6. Chat returns to full width

**Expected Result**:
- ✅ Smooth animation
- ✅ Chat messages don't reflow awkwardly
- ✅ Can toggle freely without errors
- ✅ Chat state preserved when sidebar closes

---

## 🧠 Advanced Test Scenarios

### Scenario A: First-Time User Flow

**Steps**:
1. Open app (new user "Jane")
2. See "Get started" or prompt to add appliances
3. Add 3 appliances (washer, dishwasher, oven)
4. View each appliance's default maintenance tasks
5. Scroll through chat asking about appliances
6. Log one repair for each appliance
7. View statistics showing 3 appliances, 3 repairs
8. Check for overdue maintenance alerts

**Success Criteria**:
- Complete flow takes <2 minutes
- No errors at any step
- Data accurate throughout

---

### Scenario B: Power User - Repair Detective

**Steps**:
1. User with existing appliances
2. Has multiple repairs for same appliance
3. Logs 3 repairs with "not heating" issue
4. System detects pattern (recurring issue)
5. Alert generated: "Recurring issue detected"
6. User acknowledges alert
7. Chat helps diagnose root cause using repair history
8. User logs one more repair with resolution

**Success Criteria**:
- Alert triggers on 3rd occurrence
- System references past repairs
- Chat provides context-aware assistance

---

### Scenario C: Warranty Management

**Steps**:
1. User adds appliances with various warranty dates
2. Some warranties expiring soon (within 30 days)
3. Some warranties already expired
4. System generates alerts for near-expiry
5. User acknowledges alerts
6. When asking about appliance, chat mentions warranty status
7. User can extend warranty or take preventive action

**Success Criteria**:
- Alerts sorted by days remaining
- Critical (< 7 days) shown prominently
- Chat provides helpful warranty guidance

---

## 📊 Performance Tests

### Load Test: Add Many Appliances

**Steps**:
1. Add 50 appliances (via API or UI)
2. Switch between appliances
3. Load repair history
4. View statistics
5. Measure performance

**Success Criteria**:
- Switching appliances < 200ms
- History loads < 500ms
- Statistics calculate < 100ms
- No memory leaks
- UI remains responsive

---

## 🐛 Known Issues & Workarounds

### Issue 1: Data Lost on Restart
**Cause**: In-memory storage  
**Workaround**: Implement database (see PERSONALIZED_REPAIR_ASSISTANT.md)  
**Status**: Planned for future release

### Issue 2: Large Repair Histories Slow Down
**Cause**: Frontend renders all repairs at once  
**Workaround**: Add pagination (25 repairs per page)  
**Status**: To be implemented

### Issue 3: Alerts Not Generating
**Cause**: Frontend not calling /user/stats to trigger generation  
**Workaround**: Make backend generate alerts on repair logging  
**Status**: Implemented in backend

---

## 📋 Test Checklist

- [ ] Create test account or use default user
- [ ] Add 3-5 test appliances
- [ ] Log 2+ repairs for each appliance
- [ ] Complete maintenance task
- [ ] Verify statistics are accurate
- [ ] Trigger recurring issue alert
- [ ] Acknowledge alerts
- [ ] Delete appliance
- [ ] Test sidebar toggle
- [ ] Test with QR code scanning
- [ ] Test chat integration
- [ ] Verify data consistency
- [ ] Performance acceptable (< 1s load times)
- [ ] No console errors
- [ ] Responsive on mobile (if applicable)

---

## 🚀 Test Data Script

To quickly populate test data, use this JavaScript in browser console:

```javascript
// Add test appliances
const appliances = [
  { brand: 'Samsung', model: 'WF42H5200', type: 'washer', serial: 'WF001', cost: 1200 },
  { brand: 'LG', model: 'LDT5678', type: 'dishwasher', serial: 'LG001', cost: 1500 },
  { brand: 'Bosch', model: 'HBI5500', type: 'oven', serial: 'BOSCH001', cost: 3000 }
];

appliances.forEach(app => {
  console.log(`Added ${app.brand} ${app.model}`);
  // Would call ApplianceManager.addAppliance() API
});

// Log test repairs
const repairs = [
  { issue: 'Water not draining', symptom: 'Pooling water', resolved: 'Cleaned filter', cost: 45 },
  { issue: 'Water not draining', symptom: 'Beeping error', resolved: 'Replaced seal', cost: 120 },
  { issue: 'Leaking', symptom: 'Water under door', resolved: 'Replaced door gasket', cost: 80 }
];

repairs.forEach(repair => {
  console.log(`Logged repair: ${repair.issue} - $${repair.cost}`);
  // Would call RepairHistory.addRepair() API
});
```

---

## 📞 Troubleshooting

### Appliances not showing in list
- Clear browser cache
- Restart server
- Check browser console for errors
- Verify user_id is set correctly

### Repairs not saving
- Check network tab (should see POST /user/repair)
- Verify all required fields filled
- Check backend logs for errors
- Ensure server is running

### Stats showing wrong numbers
- Refresh page
- Verify repair cost values are numbers
- Check backend /user/stats endpoint response
- Clear and re-add test data

### Alerts not appearing
- Log at least 2 repairs with same issue
- Click refresh or switch appliances
- Check /user/alerts endpoint directly
- Verify alert generation logic runs

---

**Last Updated**: January 24, 2026  
**Status**: Complete  
**Coverage**: 15 test scenarios + performance + integration + advanced flows
