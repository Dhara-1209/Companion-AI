/**
 * User Appliance Management & Repair History System
 * Tracks owned appliances and maintenance history
 */

export interface UserAppliance {
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

export interface RepairRecord {
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

export interface MaintenanceTask {
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

export interface PredictiveAlert {
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

// In-memory storage for demo (replace with database in production)
export const userAppliances: Map<string, UserAppliance[]> = new Map();
export const repairHistory: Map<string, RepairRecord[]> = new Map();
export const maintenanceTasks: Map<string, MaintenanceTask[]> = new Map();
export const predictiveAlerts: Map<string, PredictiveAlert[]> = new Map();

// Common maintenance tasks by appliance type
export const commonMaintenanceTasks: Record<string, Omit<MaintenanceTask, 'id' | 'applianceId'>> = {
  'washer-filter-clean': {
    taskName: 'Clean Filter',
    description: 'Clean the lint filter to prevent drainage issues',
    recommendedFrequency: 180, // 6 months
    priority: 'high',
    estimatedTime: '30 minutes',
    difficulty: 'easy',
    steps: [
      'Locate the drain filter (usually at the bottom front)',
      'Place towel underneath to catch water',
      'Turn the drain plug counterclockwise',
      'Remove debris and clean with water',
      'Replace the plug and tighten clockwise'
    ]
  },
  'washer-hose-inspect': {
    taskName: 'Inspect Hoses',
    description: 'Check inlet and outlet hoses for wear, cracks, or bulges',
    recommendedFrequency: 365, // 1 year
    priority: 'high',
    estimatedTime: '15 minutes',
    difficulty: 'easy',
    steps: [
      'Turn off water supply',
      'Inspect both inlet hoses for cracks, bulges, or leaks',
      'Check outlet hose for kinks or damage',
      'Replace if any damage is found',
      'Turn water supply back on and test'
    ]
  },
  'dishwasher-filter-clean': {
    taskName: 'Clean Spray Arms & Filter',
    description: 'Remove food particles and buildup from filter and spray arms',
    recommendedFrequency: 90, // 3 months
    priority: 'high',
    estimatedTime: '20 minutes',
    difficulty: 'easy',
    steps: [
      'Remove bottom rack',
      'Unscrew and remove filter',
      'Rinse filter thoroughly',
      'Check spray arm holes for debris',
      'Use toothpick to clear blocked holes',
      'Reinstall filter and rack'
    ]
  },
  'microwave-interior-clean': {
    taskName: 'Clean Interior',
    description: 'Clean microwave interior to maintain hygiene and performance',
    recommendedFrequency: 60, // 2 months
    priority: 'medium',
    estimatedTime: '15 minutes',
    difficulty: 'easy',
    steps: [
      'Unplug microwave',
      'Remove turntable',
      'Wipe interior with damp cloth',
      'Clean turntable with soap and water',
      'Wipe turntable bearings',
      'Reinstall turntable and plug in'
    ]
  },
  'oven-self-clean': {
    taskName: 'Self-Clean Cycle',
    description: 'Run self-cleaning cycle to remove buildup',
    recommendedFrequency: 180, // 6 months
    priority: 'medium',
    estimatedTime: '3-4 hours',
    difficulty: 'medium',
    steps: [
      'Remove racks if desired',
      'Close oven door',
      'Press self-clean button',
      'Set cycle time (usually 3-4 hours)',
      'Let cycle complete',
      'Wait for oven to cool',
      'Wipe out ash with damp cloth'
    ]
  },
  'vacuum-filter-clean': {
    taskName: 'Clean Filter',
    description: 'Clean or replace vacuum filter for optimal suction',
    recommendedFrequency: 90, // 3 months
    priority: 'high',
    estimatedTime: '10 minutes',
    difficulty: 'easy',
    steps: [
      'Unplug vacuum',
      'Locate filter access (usually on side or back)',
      'Remove filter',
      'Tap gently to remove dust',
      'Rinse under warm water if washable',
      'Let dry completely',
      'Reinstall filter'
    ]
  }
};

// User appliance management functions

export function addAppliance(
  userId: string,
  appliance: Omit<UserAppliance, 'id' | 'userId' | 'isActive' | 'addedAt'>
): UserAppliance {
  const newAppliance: UserAppliance = {
    ...appliance,
    id: `app-${Date.now()}`,
    userId,
    isActive: true,
    addedAt: new Date()
  };

  if (!userAppliances.has(userId)) {
    userAppliances.set(userId, []);
  }
  userAppliances.get(userId)!.push(newAppliance);

  // Create default maintenance tasks
  createDefaultMaintenanceTasks(userId, newAppliance.id, appliance.applianceType);

  return newAppliance;
}

export function getUserAppliances(userId: string): UserAppliance[] {
  return userAppliances.get(userId) || [];
}

export function getAppliance(userId: string, applianceId: string): UserAppliance | null {
  const appliances = userAppliances.get(userId) || [];
  return appliances.find(a => a.id === applianceId) || null;
}

export function updateAppliance(
  userId: string,
  applianceId: string,
  updates: Partial<UserAppliance>
): UserAppliance | null {
  const appliances = userAppliances.get(userId) || [];
  const appliance = appliances.find(a => a.id === applianceId);
  
  if (!appliance) return null;
  
  Object.assign(appliance, updates);
  return appliance;
}

export function removeAppliance(userId: string, applianceId: string): boolean {
  const appliances = userAppliances.get(userId) || [];
  const index = appliances.findIndex(a => a.id === applianceId);
  
  if (index === -1) return false;
  
  appliances.splice(index, 1);
  return true;
}

// Repair history functions

export function addRepairRecord(
  userId: string,
  repair: Omit<RepairRecord, 'id' | 'userId' | 'date'>
): RepairRecord {
  const newRecord: RepairRecord = {
    ...repair,
    id: `repair-${Date.now()}`,
    userId,
    date: new Date()
  };

  if (!repairHistory.has(userId)) {
    repairHistory.set(userId, []);
  }
  repairHistory.get(userId)!.push(newRecord);

  // Update appliance last maintenance date
  updateAppliance(userId, repair.applianceId, {
    lastMaintenance: new Date()
  });

  // Generate predictive alerts based on repair patterns
  generatePredictiveAlerts(userId, repair.applianceId);

  return newRecord;
}

export function getRepairHistory(userId: string, applianceId?: string): RepairRecord[] {
  const history = repairHistory.get(userId) || [];
  if (applianceId) {
    return history.filter(r => r.applianceId === applianceId);
  }
  return history;
}

export function getRecentRepairs(userId: string, days: number = 30): RepairRecord[] {
  const history = repairHistory.get(userId) || [];
  const cutoffDate = new Date();
  cutoffDate.setDate(cutoffDate.getDate() - days);
  
  return history.filter(r => r.date >= cutoffDate);
}

// Maintenance tasks functions

function createDefaultMaintenanceTasks(userId: string, applianceId: string, applianceType: string): void {
  const taskMap: Record<string, string[]> = {
    'washer': ['washer-filter-clean', 'washer-hose-inspect'],
    'dishwasher': ['dishwasher-filter-clean'],
    'microwave': ['microwave-interior-clean'],
    'oven': ['oven-self-clean'],
    'vacuum': ['vacuum-filter-clean']
  };

  const taskKeys = taskMap[applianceType] || [];
  const tasks: MaintenanceTask[] = taskKeys.map((key, index) => {
    const baseTask = commonMaintenanceTasks[key];
    return {
      id: `task-${applianceId}-${index}`,
      applianceId,
      ...baseTask
    };
  });

  if (!maintenanceTasks.has(userId)) {
    maintenanceTasks.set(userId, []);
  }
  maintenanceTasks.get(userId)!.push(...tasks);
}

export function getMaintenanceTasks(userId: string, applianceId?: string): MaintenanceTask[] {
  const tasks = maintenanceTasks.get(userId) || [];
  if (applianceId) {
    return tasks.filter(t => t.applianceId === applianceId);
  }
  return tasks;
}

export function markTaskCompleted(userId: string, taskId: string): MaintenanceTask | null {
  const tasks = maintenanceTasks.get(userId) || [];
  const task = tasks.find(t => t.id === taskId);
  
  if (!task) return null;
  
  const now = new Date();
  task.lastCompleted = now;
  task.nextDue = new Date(now.getTime() + task.recommendedFrequency * 24 * 60 * 60 * 1000);
  
  return task;
}

export function getOverdueTasks(userId: string): MaintenanceTask[] {
  const tasks = maintenanceTasks.get(userId) || [];
  const now = new Date();
  
  return tasks.filter(t => {
    const dueDate = t.nextDue || new Date();
    return dueDate <= now;
  });
}

// Predictive maintenance functions

function generatePredictiveAlerts(userId: string, applianceId: string): void {
  const appliance = getAppliance(userId, applianceId);
  if (!appliance) return;

  if (!predictiveAlerts.has(userId)) {
    predictiveAlerts.set(userId, []);
  }

  const alerts = predictiveAlerts.get(userId)!;
  
  // Check warranty expiry
  if (appliance.warrantyExpiry) {
    const daysUntilExpiry = Math.ceil(
      (appliance.warrantyExpiry.getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24)
    );

    if (daysUntilExpiry <= 30 && daysUntilExpiry > 0) {
      const existingAlert = alerts.find(a => 
        a.applianceId === applianceId && a.type === 'warranty_expiry'
      );

      if (!existingAlert) {
        alerts.push({
          id: `alert-${Date.now()}`,
          applianceId,
          userId,
          type: 'warranty_expiry',
          title: `Warranty expiring soon for ${appliance.brand} ${appliance.model}`,
          description: `Your warranty expires in ${daysUntilExpiry} days (${appliance.warrantyExpiry.toDateString()})`,
          severity: daysUntilExpiry <= 7 ? 'critical' : 'warning',
          recommendedAction: 'Consider backup plans or extended warranty before expiry',
          createdAt: new Date(),
          acknowledged: false
        });
      }
    }
  }

  // Check for common issues based on repair patterns
  const repairRecords = getRepairHistory(userId, applianceId);
  const issueCounts: Record<string, number> = {};
  
  repairRecords.forEach(record => {
    issueCounts[record.issue] = (issueCounts[record.issue] || 0) + 1;
  });

  Object.entries(issueCounts).forEach(([issue, count]) => {
    if (count >= 2) {
      const existingAlert = alerts.find(a =>
        a.applianceId === applianceId && 
        a.type === 'common_issue' && 
        a.title.includes(issue)
      );

      if (!existingAlert) {
        alerts.push({
          id: `alert-${Date.now()}`,
          applianceId,
          userId,
          type: 'common_issue',
          title: `Recurring issue detected: ${issue}`,
          description: `You've experienced "${issue}" ${count} times. Consider professional service or replacement parts.`,
          severity: count >= 3 ? 'critical' : 'warning',
          recommendedAction: 'Review past repairs for solutions or consult professional service',
          createdAt: new Date(),
          acknowledged: false
        });
      }
    }
  });
}

export function getPredictiveAlerts(userId: string, applianceId?: string): PredictiveAlert[] {
  const alerts = predictiveAlerts.get(userId) || [];
  if (applianceId) {
    return alerts.filter(a => a.applianceId === applianceId && !a.acknowledged);
  }
  return alerts.filter(a => !a.acknowledged);
}

export function acknowledgeAlert(userId: string, alertId: string): PredictiveAlert | null {
  const alerts = predictiveAlerts.get(userId) || [];
  const alert = alerts.find(a => a.id === alertId);
  
  if (!alert) return null;
  
  alert.acknowledged = true;
  return alert;
}

export function getApplianceStats(userId: string, applianceId: string): {
  repairCount: number;
  lastRepair?: Date;
  averageTimesBetweenRepairs?: number;
  commonIssues: string[];
  maintenanceStatus: 'all_current' | 'some_overdue' | 'all_overdue';
} {
  const repairs = getRepairHistory(userId, applianceId);
  const overdueTasks = getOverdueTasks(userId).filter(t => t.applianceId === applianceId);
  const allTasks = getMaintenanceTasks(userId, applianceId);

  const repairDates = repairs.map(r => r.date.getTime()).sort((a, b) => b - a);
  let averageTimesBetweenRepairs: number | undefined;
  
  if (repairDates.length > 1) {
    const intervals = [];
    for (let i = 0; i < repairDates.length - 1; i++) {
      intervals.push(repairDates[i] - repairDates[i + 1]);
    }
    averageTimesBetweenRepairs = Math.round(
      intervals.reduce((a, b) => a + b, 0) / intervals.length / (1000 * 60 * 60 * 24)
    );
  }

  const issueCounts: Record<string, number> = {};
  repairs.forEach(r => {
    issueCounts[r.issue] = (issueCounts[r.issue] || 0) + 1;
  });
  
  const commonIssues = Object.entries(issueCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 3)
    .map(([issue]) => issue);

  let maintenanceStatus: 'all_current' | 'some_overdue' | 'all_overdue';
  if (overdueTasks.length === 0) {
    maintenanceStatus = 'all_current';
  } else if (overdueTasks.length === allTasks.length) {
    maintenanceStatus = 'all_overdue';
  } else {
    maintenanceStatus = 'some_overdue';
  }

  return {
    repairCount: repairs.length,
    lastRepair: repairs[0]?.date,
    averageTimesBetweenRepairs,
    commonIssues,
    maintenanceStatus
  };
}
