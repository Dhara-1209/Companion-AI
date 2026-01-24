# 🎯 PERSONALIZED REPAIR ASSISTANT - VISUAL OVERVIEW

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      USER INTERFACE (React)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────┐  ┌──────────────────────────┐    │
│  │   Chat Component         │  │   Appliance Sidebar      │    │
│  │   ┌────────────────────┐ │  │  ┌──────────────────────┐│    │
│  │   │  Message History   │ │  │  │ My Appliances Button │    │
│  │   │ ┌────────────────┐ │ │  │  ├──────────────────────┤│    │
│  │   │ │ AI Response    │ │ │  │  │                      ││    │
│  │   │ └────────────────┘ │ │  │  │ [Add Form]           ││    │
│  │   │ ┌────────────────┐ │ │  │  │                      ││    │
│  │   │ │ User Message   │ │ │  │  │ [Appliance List]     ││    │
│  │   │ └────────────────┘ │ │  │  │                      ││    │
│  │   │                    │ │  │  │ [Repair History]     ││    │
│  │   │ [Message Input]    │ │  │  │                      ││    │
│  │   └────────────────────┘ │  │  │ [Statistics]         ││    │
│  │                          │  │  │                      ││    │
│  └──────────────────────────┘  │  └──────────────────────┘│    │
│                                │                           │    │
│                                └───────────────────────────┘    │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
         ↕ HTTP/JSON (TypeScript API Client)
┌─────────────────────────────────────────────────────────────────┐
│                     BACKEND API (FastAPI)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Appliance Management           Repair Management                │
│  ┌────────────────────────┐    ┌────────────────────────┐       │
│  │ POST /user/appliance   │    │ POST /user/repair      │       │
│  │ GET /user/appliances   │    │ GET /user/repair-hist  │       │
│  │ DELETE /user/appliance │    │                        │       │
│  └────────────────────────┘    └────────────────────────┘       │
│                                                                   │
│  Alert Management               Statistics                       │
│  ┌────────────────────────┐    ┌────────────────────────┐       │
│  │ GET /user/alerts       │    │ GET /user/stats        │       │
│  │ POST /user/alert/ack   │    │                        │       │
│  └────────────────────────┘    └────────────────────────┘       │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Internal Functions (No direct API)                          │ │
│  │ • Alert Generation (Recurring issues, warranty, overdue)   │ │
│  │ • Statistics Calculation                                    │ │
│  │ • Maintenance Task Management                              │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
         ↕ In-Memory Storage (Development)
┌─────────────────────────────────────────────────────────────────┐
│                      DATA STORAGE                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  In-Memory (Current - MVP)          Database (Planned)           │
│  ┌──────────────────────────┐      ┌──────────────────────────┐ │
│  │ user_appliances_store    │      │ PostgreSQL/MySQL         │ │
│  │ repair_history_store     │ ──→  │ Tables: users,           │ │
│  │ maintenance_alerts_store │      │ appliances, repairs,     │ │
│  │ maintenance_tasks_store  │      │ maintenance, alerts      │ │
│  └──────────────────────────┘      └──────────────────────────┘ │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

```
USER ACTION                 COMPONENT           STATE              BACKEND             STORAGE
    │                           │                 │                   │                   │
    │──Add Appliance───────────→│ ApplianceManager│                   │                   │
    │                           │──────State──────→│                   │                   │
    │                           │                 ├──Form Data───────→│ POST /appliance──→│
    │                           │ ←────Response────│←───JSON────────←  │                   │
    │                           │ ←──Add to List───│                   │                   │
    │  Display Updated List←────│                 │                   │                   │
    │                           │                 │                   │                   │
    │                           │                 │                   │                   │
    │──Click Appliance─────────→│ Set selected    │                   │                   │
    │                           ├─State Change────→│                   │                   │
    │                           │ Show RepairHistory                   │                   │
    │                           │                 │                   │                   │
    │                           │                 │                   │                   │
    │──Log Repair─────────────→│ RepairHistory   │                   │                   │
    │                           │──Form Data──────→│                   │                   │
    │                           │ Push to Array   ├──POST /repair────→│ Generate Alerts──→│
    │                           │                 │←───JSON────────←  │                   │
    │                           │ ←──New Repair────│                   │                   │
    │  Display History & Stats←─│ Calculate Stats │                   │                   │
    │                           │                 │                   │                   │
    │                           │                 │                   │                   │
    │──Toggle Sidebar──────────→│ showApplianceMgr│                   │                   │
    │                           ├─State Toggle────→│                   │                   │
    │  Sidebar Show/Hide←───────│                 │                   │                   │
    │                           │                 │                   │                   │
    └────────────────────────────────────────────────────────────────────────────────────→
                                                                                (time)
```

---

## Feature Implementation Map

```
PERSONALIZED REPAIR ASSISTANT (8 Features)
│
├─ 1. APPLIANCE TRACKING
│  ├─ Add Appliance
│  │  ├─ Form: brand, model, type, serial, date
│  │  ├─ Storage: userApplianceManager.addAppliance()
│  │  ├─ API: POST /user/appliance
│  │  └─ UI: ApplianceManager component
│  │
│  ├─ View Appliances
│  │  ├─ List display with cards
│  │  ├─ Status indicators (alerts, overdue, repairs)
│  │  ├─ Sortable/searchable
│  │  └─ Click to select for repairs
│  │
│  ├─ Remove Appliance
│  │  ├─ Delete button on each card
│  │  ├─ Confirmation dialog
│  │  ├─ API: DELETE /user/appliance/{id}
│  │  └─ Remove all associated repairs
│  │
│  └─ Track Warranty
│     ├─ Store warranty expiry date
│     ├─ Calculate days remaining
│     ├─ Alert if within 30 days
│     └─ Critical if within 7 days
│
├─ 2. REPAIR LOGGING
│  ├─ Log New Repair
│  │  ├─ Form: issue, symptoms, resolution, parts, cost, type
│  │  ├─ Multi-line symptoms
│  │  ├─ Optional parts and cost
│  │  ├─ DIY vs Professional dropdown
│  │  └─ API: POST /user/repair
│  │
│  ├─ View Repair History
│  │  ├─ List sorted by newest first
│  │  ├─ Show date, issue, solution, type, cost
│  │  ├─ Expandable details
│  │  └─ Filter by appliance
│  │
│  ├─ Track Costs
│  │  ├─ Store repair cost
│  │  ├─ Calculate total per appliance
│  │  ├─ Calculate aggregate total
│  │  └─ DIY vs Professional breakdown
│  │
│  └─ View Statistics
│     ├─ Total repairs per appliance
│     ├─ Average cost per repair
│     ├─ DIY vs Professional ratio
│     ├─ Cost by date range
│     └─ Common issues analysis
│
├─ 3. MAINTENANCE TRACKING
│  ├─ Auto-Generate Tasks
│  │  ├─ Washer: filter (6mo), hoses (1yr)
│  │  ├─ Dishwasher: filter (3mo)
│  │  ├─ Microwave: interior (2mo)
│  │  ├─ Oven: self-clean (6mo)
│  │  └─ Vacuum: filter (3mo)
│  │
│  ├─ Track Task Status
│  │  ├─ Next due date calculation
│  │  ├─ Last completed tracking
│  │  ├─ Overdue detection
│  │  └─ Priority levels
│  │
│  ├─ Mark Task Complete
│  │  ├─ "Mark Done" button
│  │  ├─ Update last completed date
│  │  ├─ Calculate next due (frequency + today)
│  │  └─ Clear overdue flag
│  │
│  └─ Task Management
│     ├─ View all tasks per appliance
│     ├─ Hide completed tasks
│     ├─ Show overdue prominent
│     └─ Difficulty and time estimates
│
├─ 4. PREDICTIVE ALERTS
│  ├─ Warranty Expiry Alert
│  │  ├─ Trigger: 30 days before expiry
│  │  ├─ Critical: Within 7 days
│  │  ├─ Show days remaining
│  │  └─ Recommend action
│  │
│  ├─ Recurring Issue Alert
│  │  ├─ Trigger: Same issue 2+ times
│  │  ├─ Show issue history
│  │  ├─ Recommend professional service
│  │  └─ Suggest parts replacement
│  │
│  ├─ Overdue Maintenance Alert
│  │  ├─ Trigger: Task past recommended date
│  │  ├─ Show days overdue
│  │  ├─ Recommend completion
│  │  └─ Show easy/medium/hard difficulty
│  │
│  ├─ Unusual Pattern Alert
│  │  ├─ Trigger: High repair frequency
│  │  ├─ Analyze repair intervals
│  │  ├─ Compare to appliance type average
│  │  └─ Recommend evaluation
│  │
│  └─ Alert Management
│     ├─ Acknowledge alerts
│     ├─ View acknowledged separately
│     ├─ Auto-clear resolved issues
│     └─ Severity badges (info/warn/critical)
│
├─ 5. STATISTICS & INSIGHTS
│  ├─ Per-Appliance Stats
│  │  ├─ Total repairs
│  │  ├─ Last repair date
│  │  ├─ Average days between repairs
│  │  ├─ Most common issues
│  │  ├─ Total spent on repairs
│  │  └─ DIY vs Professional count
│  │
│  ├─ Aggregate Statistics
│  │  ├─ Total appliances
│  │  ├─ Total repairs across all
│  │  ├─ Total spending
│  │  ├─ Average cost per repair
│  │  ├─ DIY vs Professional (aggregate)
│  │  └─ Top 5 common issues overall
│  │
│  ├─ Trend Analysis
│  │  ├─ Repairs per month
│  │  ├─ Cost trends
│  │  ├─ Issue frequency over time
│  │  └─ Maintenance completion rates
│  │
│  └─ Export & Reporting
│     ├─ API: GET /user/stats
│     ├─ JSON format
│     ├─ Filterable by appliance
│     └─ Date range filtering (future)
│
├─ 6. CHAT INTEGRATION
│  ├─ Sidebar Toggle
│  │  ├─ Button: "My Appliances" (gear icon)
│  │  ├─ Position: Right side
│  │  ├─ Width: 320px (w-80)
│  │  ├─ Smooth animation
│  │  └─ Close button (X)
│  │
│  ├─ Appliance Manager View
│  │  ├─ Show appliance list
│  │  ├─ Add appliance form
│  │  ├─ Status indicators
│  │  ├─ Delete buttons
│  │  └─ Click to select
│  │
│  ├─ Repair History View
│  │  ├─ Back button
│  │  ├─ Selected appliance info
│  │  ├─ Log repair form
│  │  ├─ Repair history list
│  │  └─ Statistics display
│  │
│  ├─ Chat Awareness (future)
│  │  ├─ Reference repair history
│  │  ├─ Suggest maintenance
│  │  ├─ Use repair patterns for advice
│  │  └─ Alert-aware responses
│  │
│  └─ User Experience
│     ├─ No chat disruption
│     ├─ Easy toggle on/off
│     ├─ Persistent state
│     ├─ Clear navigation
│     └─ Responsive design
│
├─ 7. API ENDPOINTS
│  ├─ Appliance APIs
│  │  ├─ POST /user/appliance
│  │  ├─ GET /user/appliances
│  │  └─ DELETE /user/appliance/{id}
│  │
│  ├─ Repair APIs
│  │  ├─ POST /user/repair
│  │  └─ GET /user/repair-history
│  │
│  ├─ Alert APIs
│  │  ├─ GET /user/alerts
│  │  └─ POST /user/alert/{id}/acknowledge
│  │
│  └─ Statistics API
│     └─ GET /user/stats
│
└─ 8. DATA MODELS
   ├─ UserAppliance
   │  ├─ id, userId, brand, model, type
   │  ├─ serialNumber, purchaseDate, warrantyExpiry
   │  ├─ addedAt, isActive
   │  └─ lastMaintenance (optional)
   │
   ├─ RepairRecord
   │  ├─ id, applianceId, userId, date
   │  ├─ issue, symptoms[], resolution
   │  ├─ partsReplaced[], servicedBy, cost
   │  └─ notes (optional)
   │
   ├─ MaintenanceTask
   │  ├─ id, applianceId, taskName, description
   │  ├─ recommendedFrequency, lastCompleted
   │  ├─ nextDue, priority, difficulty
   │  └─ estimatedTime, steps
   │
   └─ PredictiveAlert
      ├─ id, applianceId, userId, type
      ├─ title, description, severity
      ├─ recommendedAction, createdAt
      └─ acknowledged
```

---

## Component Hierarchy

```
APP
├── CHAT (Chat.tsx)
│   ├── ChatHeader
│   │   └── "My Appliances" Button ────────┐
│   ├── ChatMessages                        │
│   │   ├── AI Message                      │
│   │   └── User Message                    │
│   ├── ChatInput                           │
│   │   └── Message Input Area              │
│   │                                       │
│   └── Appliance Sidebar (if toggled)◄─────┘
│       ├── ApplianceManager
│       │   ├── Add Appliance Form
│       │   │   ├── Brand Input
│       │   │   ├── Model Input
│       │   │   ├── Type Dropdown
│       │   │   ├── Serial Input
│       │   │   ├── Date Picker
│       │   │   └── Add Button
│       │   │
│       │   ├── Appliance List
│       │   │   └── ApplianceCard (repeating)
│       │   │       ├── Name
│       │   │       ├── Status Badges
│       │   │       ├── Stats
│       │   │       ├── Delete Button
│       │   │       └── Click Handler
│       │   │
│       │   └── Stats Display
│       │
│       └── RepairHistory (if appliance selected)
│           ├── Back Button
│           ├── Appliance Info
│           │
│           ├── Repair Form
│           │   ├── Issue Input
│           │   ├── Symptoms Textarea
│           │   ├── Resolution Input
│           │   ├── Parts Input
│           │   ├── Service Type Dropdown
│           │   ├── Cost Input
│           │   └── Log Button
│           │
│           ├── Repair History List
│           │   └── RepairCard (repeating)
│           │       ├── Date
│           │       ├── Issue
│           │       ├── Solution
│           │       ├── Cost
│           │       └── Type Badge
│           │
│           └── Statistics
│               ├── Total Repairs
│               ├── DIY Count
│               ├── Professional Count
│               └── Total Spent
```

---

## State Management Flow

```
GLOBAL STATE (Chat Component)
│
├─ showApplianceManager (boolean)
│  ├─ true → Show sidebar
│  ├─ false → Hide sidebar
│  └─ Toggled by "My Appliances" button
│
└─ selectedAppliance (UserAppliance | null)
   ├─ null → Show ApplianceManager
   ├─ {appliance} → Show RepairHistory
   └─ Updated by clicking appliance name

COMPONENT STATE (ApplianceManager)
├─ appliances (UserAppliance[])
│  ├─ Fetched from backend
│  ├─ Updated on add/remove
│  └─ Displayed as list
│
└─ formData
   ├─ brand, model, type, serial, date
   ├─ Reset on submit
   └─ Validated before send

COMPONENT STATE (RepairHistory)
├─ repairs (RepairRecord[])
│  ├─ Fetched for selected appliance
│  ├─ Sorted by date
│  └─ Updated on add
│
├─ maintenanceTasks (MaintenanceTask[])
│  ├─ Auto-generated for appliance type
│  ├─ Updated on completion
│  └─ Shows overdue status
│
├─ alerts (PredictiveAlert[])
│  ├─ Fetched for appliance
│  ├─ Shows warnings
│  └─ Acknowledges available
│
└─ formData
   ├─ issue, symptoms, resolution, parts, cost
   ├─ Reset on submit
   └─ Validated before send
```

---

## Data Storage Schema

### In-Memory (Current)
```
user_appliances_store: {
  "user-123": [
    {
      id: "app-001",
      brand: "Samsung",
      model: "WF42H5200",
      applianceType: "washer",
      ...
    },
    ...
  ]
}

repair_history_store: {
  "user-123": [
    {
      id: "rep-001",
      applianceId: "app-001",
      issue: "Water not draining",
      ...
    },
    ...
  ]
}

maintenance_alerts_store: {
  "user-123": [
    {
      id: "alert-001",
      applianceId: "app-001",
      type: "warranty_expiry",
      ...
    },
    ...
  ]
}
```

### Future Database
```sql
users
├─ id
├─ username
└─ created_at

appliances
├─ id
├─ user_id (FK)
├─ brand
├─ model
├─ type
└─ ...

repairs
├─ id
├─ appliance_id (FK)
├─ user_id (FK)
├─ issue
├─ date
└─ ...

alerts
├─ id
├─ appliance_id (FK)
├─ type
├─ acknowledged
└─ ...
```

---

## User Journey

```
NEW USER
   │
   ├─ Discovers "My Appliances" button
   │  └─ Clicks Settings icon
   │     └─ Sidebar opens
   │
   ├─ Fills "Add Appliance" form
   │  └─ Brand: Samsung, Model: WF42H5200, Type: Washer
   │     └─ Clicks "Add Appliance"
   │
   ├─ Appliance appears in list
   │  └─ Shows status: 0 alerts, 0 repairs, no maintenance
   │     └─ Clicks appliance name
   │
   ├─ Switches to "Repair History" view
   │  └─ Fills "Log Repair" form
   │     └─ Issue: Water not draining, Cost: $45
   │        └─ Clicks "Log Repair"
   │
   ├─ Repair appears in history
   │  ├─ Statistics update (1 repair, $45 total)
   │  └─ Default maintenance tasks appear
   │     └─ Sees "Filter cleaning - 6 months"
   │        └─ Marks as complete (starts 6-month countdown)
   │
   └─ EXPERIENCED USER JOURNEY
      ├─ Regularly logs repairs and maintenance
      ├─ Monitors alerts (warranty, recurring issues)
      ├─ Views statistics to track spending
      └─ Stays proactive with maintenance alerts
```

---

## Error Handling & Validation

```
FORM VALIDATION
│
├─ ApplianceManager Add Form
│  ├─ Brand: Required, max 50 chars
│  ├─ Model: Required, max 50 chars
│  ├─ Type: Required, dropdown validation
│  ├─ Serial: Optional, max 50 chars
│  ├─ Date: Required, valid date format
│  └─ Submit: Validate all before send
│
├─ RepairHistory Log Form
│  ├─ Issue: Required, max 200 chars
│  ├─ Symptoms: Required, min 1, max 10
│  ├─ Resolution: Required, max 500 chars
│  ├─ Parts: Optional, max 10 items
│  ├─ Service Type: Required, enum validation
│  ├─ Cost: Optional, numeric validation
│  └─ Submit: Validate all before send
│
└─ API VALIDATION
   ├─ All parameters required
   ├─ Type checking enforced
   ├─ User ID validation
   ├─ Resource ownership verification
   └─ Error responses with clear messages
```

---

## Performance Considerations

```
OPTIMIZATION
├─ Frontend
│  ├─ React.memo for ApplianceCard
│  ├─ useMemo for statistics calculation
│  ├─ useCallback for event handlers
│  ├─ Lazy loading for large lists
│  └─ Virtual scrolling (future)
│
├─ Backend
│  ├─ In-memory storage (fast)
│  ├─ Indexed lookups
│  ├─ Filtered queries
│  └─ Database indexes (future)
│
└─ Network
   ├─ Batch operations (future)
   ├─ Pagination for large results
   ├─ Compression (gzip)
   └─ Caching strategies (future)

SCALABILITY
├─ Current: Single user, in-memory (MVP)
├─ Next: Multi-user, database
├─ Future: Distributed, cloud sync
└─ Estimated: Handles 1000+ appliances per user
```

---

**This Personalized Repair Assistant is built on a solid, scalable architecture!**
