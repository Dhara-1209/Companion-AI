# Predictive Maintenance & Feature Implementation Details

## Core Features Implementation

### Feature 1: Appliance Tracking System
**Location:** `src/config/userApplianceManager.ts` (lines 1-100)

The system maintains a registry of user appliances with complete lifecycle management:

```typescript
// Data Structure
interface Appliance {
  id: string;
  userId: string;
  brand: string;
  model: string;
  applianceType: 'washer' | 'dishwasher' | 'oven' | 'microwave' | 'vacuum';
  purchaseDate: Date;
  warrantyExpiry?: Date;
  lastMaintenance?: Date;
  maintenanceTasks: MaintenanceTask[];
  repairRecords: Repair[];
  alerts: Alert[];
}
```

**Key Functions:**
- `addAppliance()` - Registers new appliance with auto-generated maintenance schedule
- `getAppliances()` - Retrieves all appliances for user
- `removeAppliance()` - Deletes appliance and associated data
- `getApplianceStats()` - Calculates comprehensive statistics

---

### Feature 2: Repair History & Pattern Detection
**Location:** `src/config/userApplianceManager.ts` (lines 200-300)

Comprehensive repair tracking with intelligent pattern analysis:

```typescript
interface Repair {
  id: string;
  applianceId: string;
  date: Date;
  issue: string;
  symptoms: string[];
  resolution: string;
  servicedBy: 'diy' | 'professional';
  cost?: number;
  notes?: string;
}
```

**Key Functions:**
- `addRepairRecord()` - Logs repair with auto-alert generation
- `getRepairHistory()` - Retrieves complete repair records
- `calculateRepairStats()` - Computes statistics (count, avg days between, common issues)
- `identifyRecurringIssues()` - Detects patterns (triggers at 2+ occurrences)

**Pattern Detection Logic:**
```typescript
// After 2nd occurrence of same issue → WARNING alert
// After 3rd+ occurrence → CRITICAL alert with recommendation
```

---

### Feature 3: Predictive Maintenance with 6-Month Scheduling
**Location:** `src/config/userApplianceManager.ts` (lines 300-400)

Intelligent maintenance scheduling with automatic reminders:

**Maintenance Task Frequency (Washers):**
| Task | Frequency | Days |
|------|-----------|------|
| Clean Lint Filter | Every 6 months | 180 |
| Inspect Hoses | Annually | 365 |
| Check Seals | Annually | 365 |

**Implementation:**
```typescript
// When appliance added → Tasks auto-created with 180-day intervals
const commonTasks = {
  washer: [
    {
      name: 'Clean Filter',
      frequency: 180,  // 6 months
      instructions: ['Remove lint trap...', 'Clean thoroughly...']
    },
    // ... more tasks
  ]
};
```

**Key Functions:**
- `getMaintenanceTasks()` - Returns scheduled tasks with status
- `markTaskCompleted()` - Updates completion and recalculates nextDue
- `getOverdueTasks()` - Returns tasks past due date
- `generatePredictiveAlerts()` - Creates alerts for:
  - Overdue maintenance (> nextDue date)
  - Warranty expiry (≤ 30 days)
  - Recurring issues (pattern detected)

**Alert System:**
```typescript
interface Alert {
  id: string;
  type: 'MAINTENANCE_OVERDUE' | 'WARRANTY_EXPIRY' | 'RECURRING_ISSUE';
  severity: 'WARNING' | 'CRITICAL';
  message: string;
  recommendation: string;
  acknowledged: boolean;
}
```

---

## Data Flow Architecture

```
User Action
    ↓
Component (React)
    ↓
State Update (useState)
    ↓
userApplianceManager Function
    ↓
Business Logic (Pattern Detection, Scheduling)
    ↓
Alert Generation
    ↓
UI Update (Display Badges, Notifications)
```

---

## Example: 6-Month Lint Filter Maintenance

**Scenario:**
User adds Samsung Washer on Jan 1, 2024

**System Response:**
1. Creates "Clean Lint Filter" task
2. Sets frequency: 180 days
3. Sets nextDue: Jul 1, 2024

**On Jul 2, 2024:**
1. Task becomes OVERDUE
2. Alert generated: "Maintenance Overdue"
3. UI Badge shows: "⏱️ 1 Overdue" (RED)

**User marks "Done" on Jul 2:**
1. Task marked complete
2. nextDue recalculated: Jan 1, 2025 (180 days later)
3. Alert dismissed
4. Badge removed from UI

---

## Business Logic Highlights

### Recurring Issue Detection
```typescript
if (issueCount >= 2) {
  severity = issueCount >= 3 ? 'CRITICAL' : 'WARNING';
  alert.type = 'RECURRING_ISSUE';
  alert.recommendation = "Review past repairs and seek professional help";
}
```

### Warranty Tracking
```typescript
const daysUntilExpiry = (warrantyDate - today) / (1000 * 60 * 60 * 24);
if (daysUntilExpiry <= 30 && daysUntilExpiry > 0) {
  // Generate WARNING alert
}
if (daysUntilExpiry <= 7) {
  // Generate CRITICAL alert
}
```

### Maintenance Task Rescheduling
```typescript
// When task marked complete
task.completed = true;
task.lastCompleted = today;
task.nextDue = new Date(today.getTime() + (recommendedFrequency * 24 * 60 * 60 * 1000));
```

---

## Performance Characteristics

- **Add Appliance:** O(1) - Direct Map insertion
- **Log Repair:** O(n) - Linear scan for pattern detection (n = repair count)
- **Generate Alerts:** O(n) - Single pass through appliances
- **Get Statistics:** O(n) - Complete aggregation

**Optimization for Scale:**
- Pattern detection indexed by issue type
- Alerts cached until acknowledged
- Tasks indexed by nextDue date

---

**Feature Implementation Lead: Pearl 3**  
**Last Updated:** January 24, 2026
