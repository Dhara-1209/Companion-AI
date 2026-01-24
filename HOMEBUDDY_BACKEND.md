# FastAPI Backend - Homebuddy Server

## Server Configuration

**Framework:** FastAPI with Uvicorn  
**Port:** 8000  
**Python Version:** 3.11

## API Endpoints

### Appliance Management
```
POST   /api/appliances          - Add new appliance
GET    /api/appliances          - Get all appliances
GET    /api/appliances/{id}     - Get specific appliance
PUT    /api/appliances/{id}     - Update appliance
DELETE /api/appliances/{id}     - Remove appliance
```

### Repair Management
```
POST   /api/repairs             - Log new repair
GET    /api/repairs             - Get repair history
GET    /api/repairs/{id}        - Get specific repair
GET    /api/repairs/stats       - Get repair statistics
```

### Maintenance Scheduling
```
GET    /api/maintenance         - Get maintenance tasks
POST   /api/maintenance/{id}/done - Mark task complete
GET    /api/maintenance/overdue  - Get overdue tasks
```

### Alerts & Notifications
```
GET    /api/alerts              - Get active alerts
POST   /api/alerts/{id}/ack     - Acknowledge alert
GET    /api/alerts/summary      - Get alert summary
```

## Data Models

### Appliance
- id: UUID
- userId: string
- brand: string
- model: string
- type: string (washer, dishwasher, oven, microwave, vacuum)
- purchaseDate: date
- warrantyExpiry: date (optional)
- maintenanceTasks: List[Task]
- repairs: List[Repair]
- alerts: List[Alert]

### Repair
- id: UUID
- applianceId: UUID
- date: date
- issue: string
- symptoms: List[string]
- resolution: string
- cost: float (optional)
- servicedBy: string (diy/professional)

### MaintenanceTask
- id: UUID
- name: string
- frequency: int (days)
- nextDue: date
- completed: boolean
- instructions: List[string]
- difficulty: string
- estimatedTime: int (minutes)

## Server Features

✅ RESTful API design
✅ Data validation with Pydantic
✅ Error handling
✅ CORS support
✅ Async/await support
✅ In-memory data storage (expandable to database)

## Future Enhancements

- PostgreSQL database integration
- JWT authentication
- WebSocket real-time updates
- Email notifications
- Background task scheduler
- Caching with Redis

---

**Backend Lead: Krrishna-2210**
