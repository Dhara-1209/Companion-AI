# Personalized Repair Assistant - Integration Guide

## 🎯 Overview

The Personalized Repair Assistant adds comprehensive appliance tracking, maintenance history, and predictive maintenance features to CompanionAI. Users can now:

- 📱 Track all appliances they own
- 🔧 Log repairs and issues with detailed histories
- ⚠️ Receive predictive maintenance alerts
- 📊 View repair patterns and statistics
- 💾 Maintain complete service records

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React)                          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ApplianceManager (src/components/ApplianceManager.tsx)     │
│  ├─ Add/remove appliances                                    │
│  ├─ View appliance list                                      │
│  ├─ Display status indicators                                │
│  └─ Show maintenance tasks                                   │
│                                                               │
│  RepairHistory (src/components/RepairHistory.tsx)           │
│  ├─ Log repairs & issues                                     │
│  ├─ View repair records                                      │
│  ├─ Track repair costs                                       │
│  └─ Show repair patterns                                     │
│                                                               │
│  Chat Component (integration)                                │
│  ├─ Sidebar toggle for appliance manager                     │
│  ├─ Show predictive alerts                                   │
│  └─ Device-specific suggestions                              │
│                                                               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   Backend (FastAPI)                          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  POST /user/appliance                                        │
│  GET /user/appliances                                        │
│  DELETE /user/appliance/{id}                                 │
│                                                               │
│  POST /user/repair                                           │
│  GET /user/repair-history                                    │
│                                                               │
│  GET /user/alerts                                            │
│  POST /user/alert/{id}/acknowledge                           │
│                                                               │
│  GET /user/stats                                             │
│                                                               │
│  Internal: Predictive alert generation                       │
│                                                               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   Data Storage                               │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  user_appliances_store (in-memory)                           │
│  repair_history_store (in-memory)                            │
│  maintenance_alerts_store (in-memory)                        │
│                                                               │
│  [Future: Migration to database]                             │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Data Models

### UserAppliance
```typescript
interface UserAppliance {
  id: string;
  userId: string;
  qrCode?: string;
  brand: string;
  model: string;
  applianceType: 'washer' | 'dishwasher' | 'oven' | 'microwave' | 'vacuum';
  serialNumber?: string;
  purchaseDate: Date;
  warrantyExpiry?: Date;
  lastMaintenance?: Date;
  maintenanceInterval?: number; // days
  notes?: string;
  isActive: boolean;
  addedAt: Date;
}
```

### RepairRecord
```typescript
interface RepairRecord {
  id: string;
  applianceId: string;
  userId: string;
  date: Date;
  issue: string;
  symptoms: string[];
  resolution: string;
  partsReplaced?: string[];
  servicedBy: 'diy' | 'professional';
  cost?: number;
  notes?: string;
  preventiveSteps?: string[];
}
```

### MaintenanceTask
```typescript
interface MaintenanceTask {
  id: string;
  applianceId: string;
  taskName: string;
  description: string;
  recommendedFrequency: number; // days
  lastCompleted?: Date;
  nextDue?: Date;
  priority: 'low' | 'medium' | 'high';
  estimatedTime?: string;
  difficulty: 'easy' | 'medium' | 'hard';
  steps?: string[];
}
```

### PredictiveAlert
```typescript
interface PredictiveAlert {
  id: string;
  applianceId: string;
  userId: string;
  type: 'maintenance' | 'warranty_expiry' | 'common_issue' | 'unusual_pattern';
  title: string;
  description: string;
  severity: 'info' | 'warning' | 'critical';
  recommendedAction: string;
  createdAt: Date;
  acknowledged: boolean;
}
```

---

## 🎯 Key Features

### 1. Appliance Tracking
- Add new appliances with brand, model, serial number
- Track purchase date and warranty expiry
- View all tracked appliances
- Remove appliances from tracking
- Status indicators (alerts, overdue maintenance, repairs)

### 2. Repair Logging
- Log detailed repair records
- Track symptoms and resolutions
- Record parts replaced
- Specify DIY vs professional service
- Track repair costs
- View repair history with timestamps

### 3. Predictive Maintenance
- Track when each appliance needs maintenance
- Auto-generated maintenance tasks per appliance type
- Mark tasks as complete
- Overdue task notifications
- Maintenance patterns based on appliance type

### 4. Intelligent Alerts
- **Warranty expiry**: Alerts when warranty is ending (30 days before)
- **Recurring issues**: Detects patterns (e.g., "won't drain" 2+ times)
- **Maintenance due**: Notifies of overdue tasks
- **Unusual patterns**: Identifies abnormal repair frequencies

### 5. Statistics & Insights
- Total repairs per appliance
- DIY vs professional service breakdown
- Total amount spent on repairs
- Average cost per repair
- Common issues by appliance
- Last repair date
- Average days between repairs

### 6. Integration with Chat
- Show alerts in chat context
- Suggest maintenance when asking about appliance
- Use repair history for troubleshooting
- Predict issues based on patterns

---

## 🚀 Usage Examples

### Add an Appliance
```typescript
const appliance = addAppliance(userId, {
  brand: 'Samsung',
  model: 'WF42H5200',
  applianceType: 'washer',
  serialNumber: 'WF42H5200001',
  purchaseDate: new Date('2021-06-15'),
  warrantyExpiry: new Date('2024-06-15')
});
```

### Log a Repair
```typescript
const repair = addRepairRecord(userId, {
  applianceId: appliance.id,
  issue: 'Water not draining',
  symptoms: ['Water pooling at bottom', 'Beeping noise'],
  resolution: 'Cleaned filter and drain pump',
  partsReplaced: ['Drain pump seal'],
  servicedBy: 'diy',
  cost: 45.00
});
```

### Get Predictive Alerts
```typescript
const alerts = getPredictiveAlerts(userId, applianceId);
// Returns active alerts for this appliance
// Types: maintenance, warranty_expiry, common_issue, unusual_pattern
```

### Get Statistics
```typescript
const stats = getApplianceStats(userId, applianceId);
// Returns:
// - repairCount
// - lastRepair
// - averageTimesBetweenRepairs
// - commonIssues
// - maintenanceStatus
```

### Mark Task Completed
```typescript
markTaskCompleted(userId, taskId);
// Updates task completion date
// Calculates next due date
// Generates alerts if needed
```

---

## 📚 Components

### ApplianceManager Component
**File**: `src/app/components/ApplianceManager.tsx`

**Features**:
- List all user appliances
- Add new appliances via form
- Remove appliances
- View appliance details
- Show status indicators
- Display alerts & overdue tasks
- Show repair history stats

**Props**:
```typescript
interface ApplianceManagerProps {
  userId: string;
  onApplianceSelect?: (appliance: UserAppliance) => void;
}
```

**Example**:
```tsx
<ApplianceManager
  userId={userName}
  onApplianceSelect={(appliance) => setSelectedAppliance(appliance)}
/>
```

### RepairHistory Component
**File**: `src/app/components/RepairHistory.tsx`

**Features**:
- Log new repairs with detailed info
- View repair history by date
- Track DIY vs professional repairs
- Show parts replaced
- Track repair costs
- Display repair summary stats

**Props**:
```typescript
interface RepairHistoryProps {
  userId: string;
  appliance: UserAppliance;
}
```

**Example**:
```tsx
<RepairHistory
  userId={userName}
  appliance={selectedAppliance}
/>
```

---

## 🔌 API Endpoints

### Add Appliance
```
POST /user/appliance
Body: {
  "brand": "Samsung",
  "model": "WF42H5200",
  "appliance_type": "washer",
  "serial_number": "optional",
  "purchase_date": "2021-06-15"
}
Query: user_id

Response: {
  "status": "success",
  "appliance_id": "app-1234567890",
  "message": "Added Samsung WF42H5200"
}
```

### Get User Appliances
```
GET /user/appliances?user_id={user_id}

Response: {
  "status": "success",
  "appliances": [...],
  "count": 5
}
```

### Remove Appliance
```
DELETE /user/appliance/{appliance_id}?user_id={user_id}

Response: {
  "status": "success",
  "message": "Appliance removed"
}
```

### Log Repair
```
POST /user/repair?user_id={user_id}
Body: {
  "appliance_id": "app-xxx",
  "issue": "Water not draining",
  "symptoms": ["pooling", "noise"],
  "resolution": "Cleaned filter",
  "parts_replaced": ["seal"],
  "serviced_by": "diy",
  "cost": 45.00
}

Response: {
  "status": "success",
  "repair_id": "repair-xxx",
  "message": "Repair record added"
}
```

### Get Repair History
```
GET /user/repair-history?user_id={user_id}&appliance_id={appliance_id}

Response: {
  "status": "success",
  "repairs": [...],
  "count": 5
}
```

### Get Alerts
```
GET /user/alerts?user_id={user_id}

Response: {
  "status": "success",
  "alerts": [...],
  "count": 3
}
```

### Acknowledge Alert
```
POST /user/alert/{alert_id}/acknowledge?user_id={user_id}

Response: {
  "status": "success",
  "message": "Alert acknowledged"
}
```

### Get User Statistics
```
GET /user/stats?user_id={user_id}

Response: {
  "status": "success",
  "stats": {
    "total_appliances": 5,
    "total_repairs": 12,
    "diy_repairs": 8,
    "professional_repairs": 4,
    "total_spent": 850.50,
    "common_issues": ["water not draining", "noise"],
    "average_cost_per_repair": 70.88
  }
}
```

---

## 🎨 UI Integration

### Chat Sidebar
- New "My Appliances" button in header
- Sidebar slides in from right
- Shows appliance manager & repair history
- Can toggle on/off

### Status Indicators
- 🔴 Red alert badge: Active alerts
- 🟠 Orange clock: Overdue maintenance
- 📋 Gray history: Repair count
- ✅ Green check: All current

### Maintenance Tasks
Common tasks pre-populated by appliance type:

**Washing Machine**:
- Clean filter (6 months)
- Inspect hoses (1 year)

**Dishwasher**:
- Clean spray arms & filter (3 months)

**Microwave**:
- Clean interior (2 months)

**Oven**:
- Self-clean cycle (6 months)

**Vacuum**:
- Clean filter (3 months)

---

## 🔍 Predictive Alert Examples

### Warranty Expiry Alert
```
⚠️ Warranty expiring soon for Samsung WF42H5200
Your warranty expires in 7 days (June 15, 2024)
Action: Consider backup plans or extended warranty before expiry
Severity: CRITICAL (within 7 days)
```

### Recurring Issue Alert
```
⚠️ Recurring issue detected: Water not draining
You've experienced "Water not draining" 3 times.
Consider professional service or replacement parts.
Action: Review past repairs or consult professional service
Severity: CRITICAL (3+ occurrences)
```

### Overdue Maintenance Alert
```
⏰ Overdue maintenance for Samsung WF42H5200
Task: Clean Filter
Overdue since: January 15, 2024
Action: Complete this maintenance task to prevent issues
```

---

## 💾 Data Persistence

### Current (In-Memory)
- Data stored in Python dictionaries
- Lost when server restarts
- Suitable for development/demo

### Future (Database)
```sql
-- Suggested schema for production

CREATE TABLE users (
  id VARCHAR(50) PRIMARY KEY,
  username VARCHAR(100),
  email VARCHAR(100),
  created_at TIMESTAMP
);

CREATE TABLE appliances (
  id VARCHAR(50) PRIMARY KEY,
  user_id VARCHAR(50),
  brand VARCHAR(100),
  model VARCHAR(100),
  appliance_type VARCHAR(50),
  serial_number VARCHAR(100),
  purchase_date DATE,
  warranty_expiry DATE,
  added_at TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE repair_records (
  id VARCHAR(50) PRIMARY KEY,
  appliance_id VARCHAR(50),
  user_id VARCHAR(50),
  issue VARCHAR(255),
  symptoms JSON,
  resolution TEXT,
  parts_replaced JSON,
  serviced_by VARCHAR(20),
  cost DECIMAL(10, 2),
  date TIMESTAMP,
  FOREIGN KEY (appliance_id) REFERENCES appliances(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE maintenance_tasks (
  id VARCHAR(50) PRIMARY KEY,
  appliance_id VARCHAR(50),
  task_name VARCHAR(100),
  description TEXT,
  recommended_frequency INT,
  last_completed DATE,
  next_due DATE,
  FOREIGN KEY (appliance_id) REFERENCES appliances(id)
);

CREATE TABLE alerts (
  id VARCHAR(50) PRIMARY KEY,
  appliance_id VARCHAR(50),
  user_id VARCHAR(50),
  type VARCHAR(50),
  title VARCHAR(255),
  description TEXT,
  severity VARCHAR(20),
  acknowledged BOOLEAN,
  created_at TIMESTAMP,
  FOREIGN KEY (appliance_id) REFERENCES appliances(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## 🔐 Security Considerations

- User data segregated by user_id
- No sensitive personal information stored
- Warranty dates optional
- Serial numbers optional
- Repair history private to user
- Cost data not shared
- Alerts user-specific

---

## 📊 Analytics & Insights

### What We Can Track
- Most common appliance issues
- DIY vs professional service trends
- Average repair costs
- Warranty expiry patterns
- Maintenance completion rates
- Preventive vs reactive repairs

### Privacy
- All data is user-specific
- No cross-user analytics
- Optional sharing/privacy settings

---

## 🚀 Future Enhancements

1. **Database Migration**: Move from in-memory to persistent storage
2. **Cloud Sync**: Sync appliance data across devices
3. **Mobile App**: Dedicated mobile app for appliance tracking
4. **Warranty Tracking**: Integration with manufacturer warranty databases
5. **Parts Store**: Link to replacement parts for common issues
6. **Service Provider Integration**: Find local repair shops
7. **Community Repairs**: Share repair solutions with other users
8. **AI Recommendations**: ML-based maintenance predictions
9. **IoT Integration**: Connect smart appliances for automatic issue detection
10. **Export Reports**: PDF reports of repair history for insurance/resale

---

## 🧪 Testing

### Manual Testing Checklist
- [ ] Add a new appliance
- [ ] View appliance in list
- [ ] Log a repair for appliance
- [ ] View repair history
- [ ] Check maintenance tasks
- [ ] Mark task as complete
- [ ] Trigger alert condition (e.g., log 2nd repair of same issue)
- [ ] View alerts
- [ ] Acknowledge alert
- [ ] View statistics
- [ ] Remove appliance
- [ ] Verify data consistency

### Test Scenarios
1. **New User**: Add first appliance, log repairs, view stats
2. **Recurring Issue**: Log same issue multiple times, verify alert
3. **Warranty Expiry**: Add appliance with near-expiry warranty, check alert
4. **Maintenance**: Create maintenance tasks, mark complete, verify dates
5. **Cost Tracking**: Log repairs with costs, view total spent

---

## 🎓 Learning Resources

- Check `src/config/userApplianceManager.ts` for data management logic
- Review `src/app/components/ApplianceManager.tsx` for UI components
- See `src/backend/main.py` for API endpoints
- Test with sample data in ChatPT

---

## 📞 Support & Troubleshooting

### Data Not Persisting
- In-memory storage used (resets on server restart)
- Solution: Implement database for production

### Alerts Not Generating
- Check repair records are being logged
- Ensure `_generate_alerts()` is called
- Verify alert conditions are met

### Performance Issues
- Current in-memory storage is efficient
- Consider indexing for large datasets
- Optimize queries when migrating to database

---

**Status**: ✅ Complete and Integrated  
**Version**: 1.0  
**Last Updated**: January 24, 2026
