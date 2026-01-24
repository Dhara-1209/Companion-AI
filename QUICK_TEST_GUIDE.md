# Quick Test Data & Scenarios

Use this guide for rapid feature verification.

---

## Scenario 1: Samsung Washer with Drain Issues (5 min demo)

### Step 1: Add Appliance (1 min)
```
Settings (⚙️) → ApplianceManager → Add Appliance

Brand: Samsung
Model: WF42H5200AW
Type: Washing Machine
Serial: SN-2022-001
Date: 06/15/2022

✅ Result: Appliance added, shows "✅ Current"
```

### Step 2: View Maintenance (1 min)
```
Click Samsung appliance → Scroll to "Upcoming Maintenance"

✅ Result: Shows
- Clean Filter (Due: 12/15/2022) [6 months from purchase]
- Inspect Hoses (Due: 06/15/2023) [1 year from purchase]
```

### Step 3: Log First Repair (1 min)
```
Repair History tab → Fill form:

Appliance: Samsung WF42H5200AW
Issue: Drain blockage
Symptoms: ☑ Water not draining, ☑ Strange noise
Resolution: Cleaned drain filter and hoses
DIY: ☑ (checked)
Cost: $0

✅ Result: 
- Repair added to history
- Stats show: "1 Repair", "Common Issues: None yet"
```

### Step 4: Log Same Issue Again (1 min)
```
Repair History tab → Fill form again:

Appliance: Samsung WF42H5200AW
Issue: Drain blockage (SAME!)
Symptoms: ☑ Water pooling at bottom
Resolution: Replaced drain hose
DIY: ☐ (unchecked)
Cost: $150

✅ Result:
- Second repair logged
- ApplianceManager shows "⚠️ 1 Alert" badge on Samsung
- Click appliance → Active Alerts section shows:
  Title: "Recurring issue detected: Drain blockage"
  Severity: WARNING (yellow)
  "Review past repairs for solutions..."
```

### Step 5: Verify Statistics (1 min)
```
Click Samsung appliance → Scroll to "Repair History"

✅ Result:
- Total Repairs: 2
- Last Repair: 01/24/2026
- Common Issues: Drain blockage
```

**Demo time: 5 minutes | Shows: All 3 features**

---

## Scenario 2: Warranty Expiry Alert (3 min demo)

### Step 1: Add Appliance with Warranty
```
Settings → ApplianceManager → Add Appliance

Brand: LG
Model: LSTE7669SS
Type: Dishwasher
Date: 12/24/2024 (1 year warranty = expires 12/24/2025)
Serial: SN-LG-2024-999

✅ Result: Appliance added
```

### Step 2: Check Alert (if within 30 days of expiry)
```
Click LG appliance → Scroll to "Active Alerts"

✅ Result (if warranty within 30 days):
- Red Alert: "Warranty expiring soon for LG LSTE7669SS"
- Severity: CRITICAL or WARNING (depends on days left)
- Shows exact expiry date
```

**Demo time: 3 minutes | Shows: Warranty alert feature**

---

## Scenario 3: Overdue Maintenance (3 min demo)

### Step 1: Add Old Appliance
```
Settings → ApplianceManager → Add Appliance

Brand: Whirlpool
Model: WED5090HW
Type: Washing Machine
Date: 01/01/2025 (1 month old, so lint cleaning overdue)

✅ Result: Appliance added
```

### Step 2: Mark Task Overdue
```
Maintenance frequency is 180 days (6 months)
Since 6 months have passed, task should show as overdue

Click Whirlpool appliance → ApplianceDetails

✅ Result:
- Red "⏱️ 1 Overdue" badge on appliance
- "Overdue Maintenance" section shows:
  - "Clean Filter" task in red background
  - "Overdue since: 01/24/2026"
  - Green "Done" button
```

### Step 3: Mark Task Complete
```
Click "Done" button on overdue task

✅ Result:
- Task marked complete
- lastCompleted: 01/24/2026
- nextDue: 07/24/2026 (6 months later)
- "⏱️ Overdue" badge disappears
- Task moves to "Upcoming Maintenance"
```

**Demo time: 3 minutes | Shows: Maintenance scheduling & task completion**

---

## Scenario 4: Full Feature Demonstration (10 min)

Combine all scenarios:

```
Timeline:
0:00-1:00  → Add Samsung washer (Feature 1)
1:00-2:00  → View maintenance tasks (Feature 3)
2:00-3:30  → Log first drain blockage repair (Feature 2)
3:30-5:00  → Log second drain blockage repair (Feature 3)
5:00-6:00  → Show predictive alert generated (Feature 3)
6:00-7:00  → Show repair statistics (Feature 2)
7:00-8:00  → Add dishwasher with warranty (Feature 3)
8:00-9:00  → Show warranty expiry alert (Feature 3)
9:00-10:00 → Complete maintenance task (Feature 1 & 3)

Covers all features in sequence!
```

---

## Test Data Library

### Appliance Data

**Washing Machines:**
```
1. Samsung WF42H5200AW (2022-06-15)
2. LG WM3900HW (2023-01-10)
3. Whirlpool WED5090HW (2024-06-20)
```

**Dishwashers:**
```
1. LG LSTE7669SS (2024-12-24)
2. Bosch SHPM88Z75N (2023-03-15)
3. KitchenAid KDPE334GPA (2022-09-01)
```

**Microwaves:**
```
1. Panasonic NNST651W (2024-02-14)
2. GE JES2051SNSS (2023-08-22)
```

**Ovens:**
```
1. GE JB645RKSS (2022-11-05)
2. Whirlpool WFE745H0FS (2023-07-18)
```

**Vacuums:**
```
1. Dyson V15 (2024-03-30)
2. Shark NV360 (2023-11-11)
```

### Repair Issues (Common)

```
"Drain blockage" (Washer)
  - Symptoms: Water not draining, Strange noise
  - Resolution: Cleaned filter, Replaced hose
  - DIY Cost: $0-30
  - Pro Cost: $150-200

"Filter dirty" (Dishwasher)
  - Symptoms: Poor cleaning, Water spots
  - Resolution: Cleaned spray arms, Replaced filter
  - DIY Cost: $20-50
  - Pro Cost: $100-150

"Won't heat" (Oven)
  - Symptoms: Food not cooking, Takes longer
  - Resolution: Replaced heating element
  - DIY Cost: $100-200
  - Pro Cost: $300-500

"Loud noise" (Washer)
  - Symptoms: Grinding sound, Vibration
  - Resolution: Inspected pump, Replaced bearing
  - DIY Cost: $50-100
  - Pro Cost: $200-400
```

---

## Keyboard Shortcuts (for demo)

```
Ctrl+Shift+C      → Open dev console (check for errors)
F5                → Refresh (resets in-memory data)
Ctrl+Shift+I      → Open inspector
Tab               → Navigate forms
Enter             → Submit form
Esc               → Close sidebars
```

---

## Browser DevTools Inspection

### Check Maintenance Tasks:
```javascript
// In browser console:
// The system stores data in memory, you can inspect:
localStorage.getItem('userAppliances') // (Will be null for now)

// To see if data persists, check if localStorage is being used
// Current version: In-memory only (no persistence)
```

### Verify Timestamps:
```javascript
// Check if dates are correctly formatted
new Date().toLocaleDateString() // Your current date
// Appliances added today should show today's date
```

---

## Common Issues & Solutions

### Issue: Appliance doesn't show in list
**Check:**
- Did you fill in Brand AND Model?
- Did you select an appliance Type?
- Did you click "Add Appliance" button?
**Solution:** Fill all required fields, click Add

### Issue: Maintenance tasks not appearing
**Check:**
- Is appliance selected (highlighted)?
- Scroll down in ApplianceDetails panel?
**Solution:** Click appliance, scroll to see tasks

### Issue: Alert not generating after second repair
**Check:**
- Is the issue name spelled exactly the same?
- Did you log the repair successfully?
- Check "Repair History" tab for both repairs
**Solution:** Spelling must match exactly (case-insensitive but must be same words)

### Issue: Previous data showing after refresh
**Expected:** Data disappears after page refresh (in-memory)
**Solution:** This is normal - current version doesn't persist data

---

## Feature Checklist for Demo

```
BEFORE YOU START:
☐ Frontend running (http://localhost:5175)
☐ Backend running (http://localhost:8000)
☐ Browser opened to frontend
☐ Console clear of errors

FEATURE 1: Track Appliances
☐ Click Settings (⚙️) icon
☐ See ApplianceManager sidebar
☐ Click "Add Appliance"
☐ Fill form with test data
☐ See appliance added to list
☐ See default maintenance tasks created

FEATURE 2: Repair History
☐ Click "Repair History" tab
☐ Fill repair form with test data
☐ See repair logged and added to history
☐ See statistics update (repairCount increases)
☐ Log same issue twice
☐ See "Common Issues" updated

FEATURE 3: Predictive Maintenance
☐ See maintenance tasks with 180-day (6 month) intervals
☐ See "Done" button on tasks
☐ Click "Done" - see nextDue date updates
☐ After logging issue twice, see alert appears
☐ See alert details with recommended action
☐ See overdue tasks highlighted in red
```

---

## Success Indicators

### Feature 1 ✅
- [x] Can add appliance
- [x] Appliance appears in list
- [x] Maintenance tasks auto-created
- [x] Shows correct appliance type in details

### Feature 2 ✅
- [x] Can log repairs
- [x] Repair history shows all entries
- [x] Statistics calculated correctly
- [x] Common issues identified after 2+ repairs

### Feature 3 ✅
- [x] Maintenance tasks show 180-day frequency
- [x] Tasks marked complete update next due
- [x] Overdue tasks highlighted in red
- [x] Alerts generated for recurring issues
- [x] Alerts have severity levels (warning/critical)

**If all above are checked: ✅ FEATURES WORKING CORRECTLY**

---

## Demo Script (Full Walkthrough)

```
"Good afternoon. Today I'm going to show you the Personalized 
Repair Assistant - an intelligent system that helps users track 
their appliances and predict maintenance needs.

[Show frontend on screen]

First, let's add an appliance. I'll click the Settings icon 
to open the Appliance Manager.

[Click Settings icon - sidebar appears]

Now I'll add my Samsung washing machine that I purchased about 
a year ago.

[Fill in form, click Add]

Great! The system has automatically created maintenance tasks. 
Notice it suggests cleaning the lint filter every 6 months - 
exactly the scenario mentioned in our requirements.

[Click appliance - show details]

Now, let's say I had a drain problem. I'll log a repair in the 
Repair History tab.

[Switch to Repair History tab]
[Log first drain blockage repair]

A few days later, the same issue happens again. Let's log it.

[Log second drain blockage repair]

Notice something important - the system detected this is a 
recurring issue and generated an alert. 

[Click appliance - show alert]

It's telling me that I've experienced this problem twice and 
recommending I either review solutions or get professional help.

This is the power of predictive maintenance - it learns from 
your history and warns you about patterns.

Finally, let me show the maintenance tracking. Once a task is 
complete, the next due date automatically updates 6 months out.

[Click Done on a task if available]

So in summary:
1. We track all your appliances
2. We keep a complete history of repairs
3. We predict maintenance needs and alert you to issues

Thank you!"

Duration: ~5 minutes
Covers: All 3 features
Impact: Demonstrates intelligent maintenance tracking
```

---

## Quick Reference

| Appliance Type | Maintenance Task | Frequency |
|---|---|---|
| Washer | Clean Filter | 180 days (6 mo) |
| Washer | Inspect Hoses | 365 days (1 yr) |
| Dishwasher | Clean Filter | 90 days (3 mo) |
| Microwave | Clean Interior | 60 days (2 mo) |
| Oven | Self-Clean | 180 days (6 mo) |
| Vacuum | Clean Filter | 30 days (1 mo) |

**Feature Status:**
- ✅ Appliance Tracking: WORKING
- ✅ Repair History: WORKING  
- ✅ Predictive Maintenance: WORKING
- ✅ 6-Month Recommendations: WORKING
- ✅ Pattern Detection: WORKING
- ✅ Alert Generation: WORKING

**Ready for presentation!**
