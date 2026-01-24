# How to Test Personalized Repair Assistant Features

This guide walks you through testing all three core features of the Personalized Repair Assistant.

---

## Prerequisites

✅ Frontend running on http://localhost:5175
✅ Backend running on http://localhost:8000
✅ Both servers started successfully

---

## Test Scenario: Samsung Washing Machine with Recurring Drain Issues

### Step 1: Add an Appliance

1. Open http://localhost:5175 in browser
2. Click "Settings" (⚙️) icon in Chat header
3. The **ApplianceManager** sidebar should appear
4. Click **"Add Appliance"** button

**Fill in the form:**
- Brand: `Samsung`
- Model: `WF42H5200AW`
- Type: `Washing Machine`
- Serial Number: `SN123ABC456`
- Purchase Date: `2022-06-15`
- Click **"Add Appliance"**

**Expected Result:**
✅ Appliance appears in the list
✅ Status shows "✅ Current" (no issues yet)
✅ Default maintenance tasks created automatically

---

### Step 2: View Maintenance Tasks

1. Click on the Samsung washer in the appliances list
2. The **ApplianceDetails** panel shows on the right side
3. Scroll down to see **"Upcoming Maintenance"** section

**You should see:**
- ✅ "Clean Filter" - Due: [6 months from purchase]
- ✅ "Inspect Hoses" - Due: [12 months from purchase]
- Each task shows recommended frequency

**Task Details:**
- Clean Filter: Every 180 days (6 months) - Easy - 30 minutes
- Inspect Hoses: Every 365 days (1 year) - Easy - 15 minutes

---

### Step 3: Mark a Maintenance Task Complete

1. If a task is showing as overdue (next due date is past), click **"Done"** button
2. Task should mark complete and next due date updates

**Expected Result:**
✅ Task status updates
✅ "Done" button becomes available again for next cycle

---

### Step 4: Log a Repair (First Occurrence)

1. In Chat interface, click on **"Repair History"** tab at the top right
2. The **RepairHistory** component appears

**Fill in repair form:**
- Appliance: `Samsung WF42H5200AW` (should show in dropdown)
- Issue: `Drain blockage`
- Symptoms: Check "Water not draining" and "Strange noise"
- Resolution: `Cleaned drain filter and hoses`
- Who fixed it: `DIY`
- Cost: `$0`
- Click **"Add Repair"**

**Expected Result:**
✅ Repair appears in history list
✅ Statistics update showing 1 repair
✅ No alert yet (only one occurrence)

---

### Step 5: Log Same Issue Again (Trigger Predictive Alert)

1. Fill in repair form again:
   - Issue: `Drain blockage` (SAME as before)
   - Symptoms: Check "Water pooling at bottom"
   - Resolution: `Replaced drain hose`
   - Who fixed it: `Professional`
   - Cost: `$150`
   - Click **"Add Repair"**

**Expected Result:**
✅ Second repair logged
✅ Statistics now show 2 repairs
✅ **⚠️ ALERT GENERATED!** Check ApplianceManager:
   - Red "⚠️ 1 Alert" badge appears on appliance
   - Click appliance to see ApplianceDetails
   - **Active Alerts** section shows:
     - Title: "Recurring issue detected: Drain blockage"
     - Description: "You've experienced 'Drain blockage' 2 times..."
     - Severity: WARNING
     - Recommended Action: "Review past repairs or consult professional"

---

### Step 6: View Repair Statistics

1. Click on Samsung washer in ApplianceManager
2. Scroll to **"Repair History"** section in ApplianceDetails

**You should see:**
- Total Repairs: `2`
- Last Repair: [today's date]
- Avg. Days Between: [calculated]
- Common Issues: `Drain blockage`

---

### Step 7: Test Warranty Expiry Alert

1. Go back to ApplianceManager
2. Click **"Add Appliance"** again

**Add appliance with warranty expiring soon:**
- Brand: `LG`
- Model: `LDDE1111`
- Type: `Dishwasher`
- Purchase Date: `2023-12-24`
- Click **"Add Appliance"**

3. Click on LG appliance
4. If warranty expiry is set within 30 days:
   - **⚠️ "Warranty expiring soon"** alert should appear in Active Alerts

---

### Step 8: Test Overdue Maintenance

1. Add another appliance with a past purchase date
2. Let the system calculate if any maintenance tasks are overdue
3. If a task's nextDue date is in the past:
   - Red "⏱️ X Overdue" badge appears
   - Task shows in **"Overdue Maintenance"** section
   - Click **"Done"** to mark complete

---

## Feature Validation Checklist

### ✅ Feature 1: Track Appliances
- [ ] Successfully added washing machine
- [ ] Appliance appears in list
- [ ] Can see brand, model, type
- [ ] Default maintenance tasks auto-created
- [ ] Can add another appliance
- [ ] Can remove appliance

### ✅ Feature 2: Repair History
- [ ] Logged first repair successfully
- [ ] Repair appears in history
- [ ] Statistics show 1 repair
- [ ] Logged second repair (same issue)
- [ ] Statistics updated to 2 repairs
- [ ] Can see common issues identified
- [ ] Can see repair costs tracked

### ✅ Feature 3: Predictive Maintenance
- [ ] Maintenance tasks visible for appliance
- [ ] Tasks show recommended frequency (6 months, 1 year, etc.)
- [ ] After second same-issue repair, alert generated
- [ ] Alert severity shows as WARNING
- [ ] Alert includes recommended action
- [ ] Can see recurring issue details
- [ ] Task completion updates next due date
- [ ] Overdue tasks highlighted in red

---

## Expected Behavior Summary

| Feature | Action | Expected Result |
|---------|--------|-----------------|
| **Track Appliances** | Add washer | Appliance list updated, tasks created |
| **Track Appliances** | Click appliance | Details panel shows, maintenance visible |
| **Repair History** | Log repair | Appears in history, stats update |
| **Repair History** | Log same issue twice | Statistics show pattern |
| **Predictive Alerts** | Issue logged 2x | ⚠️ Alert generated for recurring issue |
| **Predictive Alerts** | Task overdue | Red "⏱️ Overdue" badge, task highlighted |
| **Maintenance** | Click "Done" on task | Task marked complete, next due updates |
| **Maintenance** | View upcoming tasks | Shows scheduled maintenance with dates |

---

## Troubleshooting

### Issue: Appliance not appearing in list
- **Solution:** Refresh page, ensure brand and model are filled in

### Issue: No maintenance tasks created
- **Solution:** Ensure appliance type is selected (washer, dishwasher, etc.)

### Issue: Alert not appearing after second repair
- **Solution:** Make sure issue name is spelled exactly the same both times

### Issue: Frontend/Backend not running
- **Solution:** 
  ```bash
  # Terminal 1: Backend
  cd c:\Companion-AI-master
  python src/backend/main.py
  
  # Terminal 2: Frontend
  cd c:\Companion-AI-master
  npm run dev
  ```

---

## Example Workflow Video Guide

For detailed walkthrough, follow this sequence:

1. **1:00 - Add Appliance**
   - Click Settings
   - Add Samsung washer
   - See maintenance tasks created

2. **2:30 - View Maintenance Schedule**
   - Click appliance
   - See 6-month lint filter cleaning task
   - Show "Inspect hoses" yearly task

3. **4:00 - Log First Repair**
   - Go to Repair History
   - Log "Drain blockage" issue
   - See statistics update

4. **5:30 - Log Recurring Issue**
   - Log same "Drain blockage" issue again
   - Watch alert appear
   - Show recurring issue detection

5. **7:00 - View Predictive Alerts**
   - Click appliance
   - Show active alerts section
   - Highlight recommended actions

6. **8:00 - Complete Maintenance Task**
   - Click "Done" on task
   - Show next due date updates
   - Explain 6-month recurring schedule

---

## Key Features Demonstrated

✅ **Appliance Tracking:** User manages multiple appliances in one place
✅ **Repair History:** Every repair logged with symptoms and costs
✅ **Pattern Detection:** System identifies recurring issues (e.g., drain blockage twice)
✅ **Predictive Alerts:** Automatic warnings when issues recur
✅ **Maintenance Scheduling:** 6-month reminder for lint trap cleaning
✅ **Task Management:** Mark tasks complete, get updated schedules
✅ **Statistics:** View repair patterns and common issues

---

## Data Reset

To start fresh testing:

1. Refresh browser (Ctrl+F5 to clear cache)
2. Or open DevTools → Application → Clear Site Data
3. This will reset all in-memory data

Note: Currently data is not persisted, so page refresh resets everything.
(Future enhancement: LocalStorage or database persistence)

---

## Success Criteria

✅ **All features working if:**
1. Can add appliances and see them tracked
2. Can log repairs and see history
3. Can see predictive alerts after recording similar issues
4. Maintenance tasks show 6-month intervals
5. System identifies patterns (e.g., drain blockage recurring)
6. UI shows status badges and alerts properly colored
