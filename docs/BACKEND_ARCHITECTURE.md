# FastAPI Backend Architecture

## Backend Server Configuration

**Server:** FastAPI with Uvicorn  
**Port:** 8000  
**Language:** Python 3.11

### Key Endpoints

```python
POST /api/appliances - Add new appliance
GET /api/appliances - Get all appliances
DELETE /api/appliances/{id} - Remove appliance

POST /api/repairs - Log repair
GET /api/repairs - Get repair history
GET /api/repairs/statistics - Get repair stats

GET /api/maintenance - Get maintenance tasks
POST /api/maintenance/{taskId}/complete - Mark task complete
GET /api/alerts - Get active alerts

POST /api/auth/login - User authentication
POST /api/auth/signup - User registration
```

### Data Models

**Appliance Model:**
- id: UUID
- userId: string
- brand: string
- model: string
- type: 'washer' | 'dishwasher' | 'oven' | 'microwave' | 'vacuum'
- purchaseDate: Date
- warrantyExpiry: Optional[Date]
- maintenanceTasks: MaintenanceTask[]
- repairs: Repair[]

**Repair Model:**
- id: UUID
- applianceId: UUID
- date: Date
- issue: string
- symptoms: string[]
- resolution: string
- servicedBy: 'diy' | 'professional'
- cost: Optional[float]
- notes: Optional[string]

**MaintenanceTask Model:**
- id: UUID
- applianceId: UUID
- taskName: string
- description: string
- recommendedFrequency: int (days)
- nextDue: Date
- completed: boolean
- instructions: string[]
- difficulty: 'easy' | 'medium' | 'hard'
- estimatedTime: int (minutes)

### In-Memory Data Storage

Currently uses Python dictionaries for storage:
```python
users: Dict[str, User] = {}
appliances: Dict[str, List[Appliance]] = {}
repairs: Dict[str, List[Repair]] = {}
maintenanceTasks: Dict[str, List[MaintenanceTask]] = {}
alerts: Dict[str, List[Alert]] = {}
```

### Future Enhancements

- PostgreSQL/MongoDB integration
- JWT authentication
- WebSocket real-time updates
- Redis caching
- Background task scheduler
- Email notifications

---

**Backend Lead: Pearl 2**  
**Last Updated:** January 24, 2026
