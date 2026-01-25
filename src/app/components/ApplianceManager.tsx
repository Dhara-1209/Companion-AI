import { useState, type ChangeEvent } from 'react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { Textarea } from './ui/textarea';
import {
  Plus,
  Trash2,
  History,
  AlertTriangle,
  CheckCircle,
  Clock,
  Settings,
  X,
} from 'lucide-react';
import { toast } from 'sonner';
import {
  addAppliance,
  getUserAppliances,
  removeAppliance,
  getApplianceStats,
  getPredictiveAlerts,
  getMaintenanceTasks,
  markTaskCompleted,
  type UserAppliance,
} from '../../config/userApplianceManager';

interface ApplianceManagerProps {
  userId: string;
  onApplianceSelect?: (appliance: UserAppliance) => void;
}

export function ApplianceManager({ userId, onApplianceSelect }: ApplianceManagerProps) {
  const [appliances, setAppliances] = useState<UserAppliance[]>(getUserAppliances(userId));
  const [showAddForm, setShowAddForm] = useState(false);
  const [selectedAppliance, setSelectedAppliance] = useState<UserAppliance | null>(null);
  const [formData, setFormData] = useState({
    brand: '',
    model: '',
    applianceType: 'washer' as const,
    serialNumber: '',
    purchaseDate: new Date().toISOString().split('T')[0],
  });

  const handleAddAppliance = () => {
    if (!formData.brand || !formData.model) {
      toast.error('Please fill in brand and model');
      return;
    }

    const newAppliance = addAppliance(userId, {
      brand: formData.brand,
      model: formData.model,
      applianceType: formData.applianceType,
      serialNumber: formData.serialNumber || undefined,
      purchaseDate: new Date(formData.purchaseDate),
    });

    setAppliances(getUserAppliances(userId));
    setShowAddForm(false);
    setFormData({
      brand: '',
      model: '',
      applianceType: 'washer',
      serialNumber: '',
      purchaseDate: new Date().toISOString().split('T')[0],
    });
    toast.success(`${newAppliance.brand} ${newAppliance.model} added!`);
  };

  const handleRemoveAppliance = (applianceId: string) => {
    removeAppliance(userId, applianceId);
    setAppliances(getUserAppliances(userId));
    setSelectedAppliance(null);
    toast.success('Appliance removed');
  };

  const handleSelectAppliance = (appliance: UserAppliance) => {
    setSelectedAppliance(appliance);
    if (onApplianceSelect) {
      onApplianceSelect(appliance);
    }
  };

  return (
    <div className="space-y-4">
      {/* Add Appliance Form */}
      {showAddForm && (
        <Card className="p-4 bg-blue-50 border-blue-200">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-semibold text-lg">Add New Appliance</h3>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setShowAddForm(false)}
            >
              <X className="w-4 h-4" />
            </Button>
          </div>

          <div className="space-y-3">
            <input
              type="text"
              placeholder="Brand (e.g., Samsung, LG)"
              value={formData.brand}
              onChange={(e: ChangeEvent<HTMLInputElement>) => setFormData({ ...formData, brand: e.target.value })}
              className="w-full px-3 py-2 border rounded-md text-sm"
            />
            <input
              type="text"
              placeholder="Model (e.g., WF42H5200)"
              value={formData.model}
              onChange={(e: ChangeEvent<HTMLInputElement>) => setFormData({ ...formData, model: e.target.value })}
              className="w-full px-3 py-2 border rounded-md text-sm"
            />
            <select
              value={formData.applianceType}
              onChange={(e: ChangeEvent<HTMLSelectElement>) => setFormData({ ...formData, applianceType: e.target.value as any })}
              className="w-full px-3 py-2 border rounded-md text-sm"
            >
              <option value="washer">Washing Machine</option>
              <option value="dishwasher">Dishwasher</option>
              <option value="oven">Oven</option>
              <option value="microwave">Microwave</option>
              <option value="vacuum">Vacuum</option>
            </select>
            <input
              type="text"
              placeholder="Serial Number (optional)"
              value={formData.serialNumber}
              onChange={(e: ChangeEvent<HTMLInputElement>) => setFormData({ ...formData, serialNumber: e.target.value })}
              className="w-full px-3 py-2 border rounded-md text-sm"
            />
            <input
              type="date"
              value={formData.purchaseDate}
              onChange={(e: ChangeEvent<HTMLInputElement>) => setFormData({ ...formData, purchaseDate: e.target.value })}
              className="w-full px-3 py-2 border rounded-md text-sm"
            />
            <Button
              onClick={handleAddAppliance}
              className="w-full bg-green-600 hover:bg-green-700"
            >
              Add Appliance
            </Button>
          </div>
        </Card>
      )}

      {/* Add Button */}
      {!showAddForm && (
        <Button
          onClick={() => setShowAddForm(true)}
          className="w-full gap-2 bg-blue-600 hover:bg-blue-700"
        >
          <Plus className="w-4 h-4" />
          Add Appliance
        </Button>
      )}

      {/* Appliances List */}
      <div className="space-y-2">
        {appliances.map((appliance: UserAppliance) => {
          const stats = getApplianceStats(userId, appliance.id);
          const alerts = getPredictiveAlerts(userId, appliance.id);
          const tasks = getMaintenanceTasks(userId, appliance.id);
          const overdueTasks = tasks.filter((t: any) => t.nextDue && t.nextDue <= new Date());

          return (
            <Card
              key={appliance.id}
              className={`p-3 cursor-pointer transition ${
                selectedAppliance?.id === appliance.id
                  ? 'border-blue-500 bg-blue-50'
                  : 'hover:border-gray-400'
              }`}
              onClick={() => handleSelectAppliance(appliance)}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h4 className="font-semibold text-sm">
                    {appliance.brand} {appliance.model}
                  </h4>
                  <p className="text-xs text-gray-600">
                    Added: {appliance.addedAt.toLocaleDateString()}
                  </p>

                  {/* Status Indicators */}
                  <div className="flex items-center gap-2 mt-2 flex-wrap">
                    {alerts.length > 0 && (
                      <span className="inline-flex items-center gap-1 px-2 py-1 bg-red-100 text-red-700 rounded text-xs font-medium">
                        <AlertTriangle className="w-3 h-3" />
                        {alerts.length} Alert{alerts.length !== 1 ? 's' : ''}
                      </span>
                    )}

                    {overdueTasks.length > 0 && (
                      <span className="inline-flex items-center gap-1 px-2 py-1 bg-orange-100 text-orange-700 rounded text-xs font-medium">
                        <Clock className="w-3 h-3" />
                        {overdueTasks.length} Overdue
                      </span>
                    )}

                    {stats.repairCount > 0 && (
                      <span className="inline-flex items-center gap-1 px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs">
                        <History className="w-3 h-3" />
                        {stats.repairCount} Repairs
                      </span>
                    )}

                    {stats.maintenanceStatus === 'all_current' && (
                      <span className="inline-flex items-center gap-1 px-2 py-1 bg-green-100 text-green-700 rounded text-xs font-medium">
                        <CheckCircle className="w-3 h-3" />
                        Current
                      </span>
                    )}
                  </div>
                </div>

                <Button
                  variant="ghost"
                  size="sm"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleRemoveAppliance(appliance.id);
                  }}
                  className="text-red-600 hover:text-red-700 hover:bg-red-50"
                >
                  <Trash2 className="w-4 h-4" />
                </Button>
              </div>
            </Card>
          );
        })}

        {appliances.length === 0 && !showAddForm && (
          <div className="text-center py-6 text-gray-500">
            <Settings className="w-8 h-8 mx-auto mb-2 opacity-50" />
            <p className="text-sm">No appliances added yet</p>
          </div>
        )}
      </div>

      {/* Selected Appliance Details */}
      {selectedAppliance && (
        <ApplianceDetails userId={userId} appliance={selectedAppliance} />
      )}
    </div>
  );
}

function ApplianceDetails({
  userId,
  appliance,
}: {
  userId: string;
  appliance: UserAppliance;
}) {
  const stats = getApplianceStats(userId, appliance.id);
  const alerts = getPredictiveAlerts(userId, appliance.id);
  const tasks = getMaintenanceTasks(userId, appliance.id);
  const overdueTasks = tasks.filter(t => t.nextDue && t.nextDue <= new Date());

  return (
    <div className="space-y-3 mt-4 border-t pt-4">
      {/* Alerts */}
      {alerts.length > 0 && (
        <div className="space-y-2">
          <h4 className="font-semibold text-sm flex items-center gap-2 text-orange-700">
            <AlertTriangle className="w-4 h-4" />
            Active Alerts
          </h4>
          {alerts.map((alert) => (
            <Card
              key={alert.id}
              className={`p-3 ${
                alert.severity === 'critical'
                  ? 'bg-red-50 border-red-200'
                  : 'bg-orange-50 border-orange-200'
              }`}
            >
              <div className="flex items-start gap-2">
                <AlertTriangle className="w-4 h-4 mt-0.5 text-orange-600 flex-shrink-0" />
                <div className="flex-1">
                  <p className="font-semibold text-sm">{alert.title}</p>
                  <p className="text-xs text-gray-700 mt-1">{alert.description}</p>
                  <p className="text-xs text-gray-600 mt-2 italic">{alert.recommendedAction}</p>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* Overdue Maintenance */}
      {overdueTasks.length > 0 && (
        <div className="space-y-2">
          <h4 className="font-semibold text-sm flex items-center gap-2 text-red-600">
            <Clock className="w-4 h-4" />
            Overdue Maintenance ({overdueTasks.length})
          </h4>
          {overdueTasks.map((task) => (
            <Card key={task.id} className="p-3 bg-red-50 border-red-200">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <p className="font-semibold text-sm">{task.taskName}</p>
                  <p className="text-xs text-gray-700">{task.description}</p>
                  <p className="text-xs text-red-600 mt-1">
                    Overdue since: {task.nextDue?.toLocaleDateString()}
                  </p>
                </div>
                <Button
                  size="sm"
                  onClick={() => {
                    markTaskCompleted(userId, task.id);
                    toast.success('Task marked as completed!');
                  }}
                  className="bg-green-600 hover:bg-green-700"
                >
                  Done
                </Button>
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* Repair Stats */}
      {stats.repairCount > 0 && (
        <Card className="p-3 bg-gray-50">
          <h4 className="font-semibold text-sm mb-2 flex items-center gap-2">
            <History className="w-4 h-4" />
            Repair History
          </h4>
          <div className="grid grid-cols-2 gap-2 text-sm">
            <div>
              <p className="text-gray-600">Total Repairs</p>
              <p className="font-semibold">{stats.repairCount}</p>
            </div>
            {stats.lastRepair && (
              <div>
                <p className="text-gray-600">Last Repair</p>
                <p className="font-semibold text-xs">{stats.lastRepair.toLocaleDateString()}</p>
              </div>
            )}
            {stats.averageTimesBetweenRepairs && (
              <div>
                <p className="text-gray-600">Avg. Days Between</p>
                <p className="font-semibold">{stats.averageTimesBetweenRepairs} days</p>
              </div>
            )}
            {stats.commonIssues.length > 0 && (
              <div className="col-span-2">
                <p className="text-gray-600">Common Issues</p>
                <p className="text-xs">{stats.commonIssues.join(', ')}</p>
              </div>
            )}
          </div>
        </Card>
      )}

      {/* Next Scheduled Maintenance */}
      {tasks.length > 0 && overdueTasks.length < tasks.length && (
        <div className="space-y-2">
          <h4 className="font-semibold text-sm flex items-center gap-2 text-green-600">
            <CheckCircle className="w-4 h-4" />
            Upcoming Maintenance
          </h4>
          {tasks
            .filter(t => !t.nextDue || t.nextDue > new Date())
            .slice(0, 3)
            .map((task) => (
              <Card key={task.id} className="p-3">
                <p className="font-semibold text-sm">{task.taskName}</p>
                <p className="text-xs text-gray-600">
                  Due: {task.nextDue?.toLocaleDateString() || 'Not scheduled'}
                </p>
              </Card>
            ))}
        </div>
      )}
    </div>
  );
}
