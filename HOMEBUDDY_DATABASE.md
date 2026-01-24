# Database & API Optimization Guide

## Database Design

### Tables

**Appliances Table**
```sql
CREATE TABLE appliances (
  id UUID PRIMARY KEY,
  user_id VARCHAR(255) NOT NULL,
  brand VARCHAR(255) NOT NULL,
  model VARCHAR(255) NOT NULL,
  type VARCHAR(50) NOT NULL,
  purchase_date DATE NOT NULL,
  warranty_expiry DATE,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

**Repairs Table**
```sql
CREATE TABLE repairs (
  id UUID PRIMARY KEY,
  appliance_id UUID NOT NULL,
  date DATE NOT NULL,
  issue VARCHAR(255) NOT NULL,
  symptoms TEXT,
  resolution TEXT NOT NULL,
  cost DECIMAL(10,2),
  serviced_by VARCHAR(50),
  created_at TIMESTAMP,
  FOREIGN KEY (appliance_id) REFERENCES appliances(id)
);
```

**Maintenance Tasks Table**
```sql
CREATE TABLE maintenance_tasks (
  id UUID PRIMARY KEY,
  appliance_id UUID NOT NULL,
  name VARCHAR(255) NOT NULL,
  frequency INT NOT NULL,
  next_due DATE NOT NULL,
  completed BOOLEAN DEFAULT FALSE,
  instructions TEXT,
  difficulty VARCHAR(50),
  estimated_time INT,
  created_at TIMESTAMP,
  FOREIGN KEY (appliance_id) REFERENCES appliances(id)
);
```

## API Response Optimization

### Caching Strategy
- Cache appliance list (5 min TTL)
- Cache repair statistics (10 min TTL)
- Cache maintenance tasks (5 min TTL)

### Pagination
```
GET /api/appliances?page=1&limit=10
GET /api/repairs?page=1&limit=20
```

### Filtering
```
GET /api/repairs?issue=drain_blockage
GET /api/maintenance?status=overdue
```

## Performance Improvements

✅ Database indexing on user_id
✅ API response compression
✅ Client-side caching
✅ Pagination for large datasets
✅ Query optimization

---

**Backend Lead: Krrishna-2210**
