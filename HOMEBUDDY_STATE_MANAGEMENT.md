# State Management & Data Flow Architecture

## State Management Pattern

Homebuddy uses a centralized state management approach with React hooks:

```typescript
// User State
const [userId, setUserId] = useState<string>('user-123');

// Appliances State
const [appliances, setAppliances] = useState<Appliance[]>([]);

// Repairs State
const [repairs, setRepairs] = useState<Repair[]>([]);

// Tasks State
const [maintenanceTasks, setMaintenanceTasks] = useState<Task[]>([]);

// Alerts State
const [alerts, setAlerts] = useState<Alert[]>([]);
```

## Data Flow

### Adding Appliance Flow
```
User Input
    ↓
Validate Data
    ↓
Create Appliance Object
    ↓
Generate Default Tasks
    ↓
Update State
    ↓
UI Re-render
```

### Logging Repair Flow
```
User Input
    ↓
Validate Data
    ↓
Create Repair Record
    ↓
Calculate Statistics
    ↓
Detect Patterns
    ↓
Generate Alerts
    ↓
Update State
    ↓
Display Notifications
```

### Maintenance Check Flow
```
Scheduled Check
    ↓
Compare nextDue with Today
    ↓
Identify Overdue Tasks
    ↓
Check Warranty Status
    ↓
Generate Alerts
    ↓
Update UI Badges
```

## Custom Hooks

### useApplianceManager
```typescript
const {
  appliances,
  addAppliance,
  removeAppliance,
  getApplianceStats
} = useApplianceManager(userId);
```

### useRepairHistory
```typescript
const {
  repairs,
  addRepair,
  getStatistics,
  identifyRecurringIssues
} = useRepairHistory(userId);
```

### useMaintenanceSchedule
```typescript
const {
  tasks,
  getOverdueTasks,
  markTaskComplete,
  generateAlerts
} = useMaintenanceSchedule(userId);
```

## Type Definitions

```typescript
interface ApplianceState {
  appliances: Appliance[];
  repairs: Repair[];
  tasks: MaintenanceTask[];
  alerts: Alert[];
}

interface ApplianceActions {
  ADD_APPLIANCE: Appliance;
  REMOVE_APPLIANCE: string;
  ADD_REPAIR: Repair;
  COMPLETE_TASK: string;
  GENERATE_ALERT: Alert;
  ACKNOWLEDGE_ALERT: string;
}
```

## Future Enhancement: Redux/Context API

For scaling, we can migrate to:
- Redux for centralized store
- Redux Thunk for async operations
- Redux DevTools for debugging
- Or Context API + useReducer

---

**Implementation Lead: unnatii14**
