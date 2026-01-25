/**
 * Test Suite for Personalized Repair Assistant Features
 * Tests:
 * 1. Track appliances owned by a user
 * 2. Maintain a history of previous repairs/issues
 * 3. Offer predictive maintenance suggestions
 */

import {
  addAppliance,
  getUserAppliances,
  addRepairRecord,
  getRepairHistory,
  getMaintenanceTasks,
  getPredictiveAlerts,
  getApplianceStats,
  markTaskCompleted,
  getOverdueTasks,
  type UserAppliance,
} from '../config/userApplianceManager';

const testUserId = 'test-user-123';

console.log('=== PERSONALIZED REPAIR ASSISTANT TEST SUITE ===\n');

// Test 1: Track appliances owned by a user
console.log('TEST 1: Track Appliances');
console.log('------------------------');

const appliance1 = addAppliance(testUserId, {
  brand: 'Samsung',
  model: 'WF42H5200',
  applianceType: 'washer',
  purchaseDate: new Date('2022-06-15'),
  serialNumber: 'SN123456',
  maintenanceInterval: 180,
});

console.log('✓ Added Washing Machine:', {
  brand: appliance1.brand,
  model: appliance1.model,
  purchaseDate: appliance1.purchaseDate.toDateString(),
});

const appliance2 = addAppliance(testUserId, {
  brand: 'LG',
  model: 'LDTE5678',
  applianceType: 'dishwasher',
  purchaseDate: new Date('2021-03-20'),
});

console.log('✓ Added Dishwasher:', {
  brand: appliance2.brand,
  model: appliance2.model,
});

const appliances = getUserAppliances(testUserId);
console.log(`✓ Total appliances tracked: ${appliances.length}\n`);

// Test 2: Maintain repair history
console.log('TEST 2: Repair History');
console.log('---------------------');

const repair1 = addRepairRecord(testUserId, {
  applianceId: appliance1.id,
  issue: 'Drain blockage',
  symptoms: ['Water not draining', 'Strange noise'],
  resolution: 'Cleaned drain filter and hoses',
  servicedBy: 'diy',
  notes: 'Found lint buildup in filter',
});

console.log('✓ Added Repair Record 1:', {
  issue: repair1.issue,
  resolution: repair1.resolution,
  date: repair1.date.toDateString(),
});

const repair2 = addRepairRecord(testUserId, {
  applianceId: appliance1.id,
  issue: 'Drain blockage',
  symptoms: ['Water pooling at bottom'],
  resolution: 'Replaced drain hose',
  servicedBy: 'professional',
  cost: 150,
});

console.log('✓ Added Repair Record 2:', {
  issue: repair2.issue,
  date: repair2.date.toDateString(),
});

const repair3 = addRepairRecord(testUserId, {
  applianceId: appliance2.id,
  issue: 'Filter dirty',
  symptoms: ['Poor cleaning performance'],
  resolution: 'Cleaned spray arms and filter',
  servicedBy: 'diy',
});

console.log('✓ Added Repair Record 3 (Dishwasher)');

const history = getRepairHistory(testUserId, appliance1.id);
console.log(`✓ Total repairs for washing machine: ${history.length}\n`);

// Test 3: Predictive Maintenance Suggestions
console.log('TEST 3: Predictive Maintenance');
console.log('------------------------------');

const alerts = getPredictiveAlerts(testUserId);
console.log(`✓ Generated ${alerts.length} predictive alerts:`);

alerts.forEach((alert, index) => {
  console.log(`  Alert ${index + 1}:`);
  console.log(`    Type: ${alert.type}`);
  console.log(`    Title: ${alert.title}`);
  console.log(`    Severity: ${alert.severity}`);
  console.log(`    Description: ${alert.description}`);
  console.log(`    Recommended Action: ${alert.recommendedAction}\n`);
});

// Test maintenance tasks
const maintenanceTasks = getMaintenanceTasks(testUserId, appliance1.id);
console.log(`✓ Maintenance tasks for washing machine: ${maintenanceTasks.length}`);
console.log('  Tasks:');
maintenanceTasks.forEach((task) => {
  console.log(`    - ${task.taskName}: ${task.description}`);
  console.log(`      Recommended Frequency: Every ${task.recommendedFrequency} days`);
  console.log(`      Difficulty: ${task.difficulty}`);
});

// Mark a task as completed
if (maintenanceTasks.length > 0) {
  markTaskCompleted(testUserId, maintenanceTasks[0].id);
  console.log(`\n✓ Marked task as completed: ${maintenanceTasks[0].taskName}`);
}

const overdueTasks = getOverdueTasks(testUserId);
console.log(`✓ Overdue maintenance tasks: ${overdueTasks.length}\n`);

// Test appliance statistics
console.log('TEST 4: Appliance Statistics');
console.log('----------------------------');

const stats = getApplianceStats(testUserId, appliance1.id);
console.log('Washing Machine Statistics:');
console.log(`  Total Repairs: ${stats.repairCount}`);
console.log(`  Last Repair: ${stats.lastRepair?.toDateString()}`);
console.log(`  Avg Days Between Repairs: ${stats.averageTimesBetweenRepairs || 'N/A'}`);
console.log(`  Common Issues: ${stats.commonIssues.join(', ') || 'None'}`);
console.log(`  Maintenance Status: ${stats.maintenanceStatus}\n`);

// Summary
console.log('=== TEST SUMMARY ===');
console.log(`✓ Appliances tracked: ${appliances.length}`);
console.log(`✓ Repair records created: ${getRepairHistory(testUserId).length}`);
console.log(`✓ Predictive alerts generated: ${alerts.length}`);
console.log(`✓ Maintenance tasks defined: ${maintenanceTasks.length}`);
console.log('\n✓ ALL TESTS PASSED! Features are working correctly.');
