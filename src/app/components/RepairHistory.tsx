import { useState } from 'react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { Textarea } from './ui/textarea';
import {
  Plus,
  Calendar,
  Wrench,
  X,
} from 'lucide-react';
import { toast } from 'sonner';
import {
  addRepairRecord,
  getRepairHistory,
  type UserAppliance,
} from '../../config/userApplianceManager';

interface RepairHistoryProps {
  userId: string;
  appliance: UserAppliance;
}

export function RepairHistory({ userId, appliance }: RepairHistoryProps) {
  const [showAddForm, setShowAddForm] = useState(false);
  const [repairs, setRepairs] = useState(getRepairHistory(userId, appliance.id));
  const [formData, setFormData] = useState({
    issue: '',
    symptoms: '',
    resolution: '',
    partsReplaced: '',
    servicedBy: 'diy' as const,
    cost: '',
  });

  const handleAddRepair = () => {
    if (!formData.issue || !formData.symptoms || !formData.resolution) {
      toast.error('Please fill in issue, symptoms, and resolution');
      return;
    }

    addRepairRecord(userId, {
      applianceId: appliance.id,
      issue: formData.issue,
      symptoms: formData.symptoms.split('\n').filter(s => s.trim()),
      resolution: formData.resolution,
      partsReplaced: formData.partsReplaced
        ? formData.partsReplaced.split('\n').filter(p => p.trim())
        : undefined,
      servicedBy: formData.servicedBy,
      cost: formData.cost ? parseFloat(formData.cost) : undefined,
    });

    setRepairs(getRepairHistory(userId, appliance.id));
    setShowAddForm(false);
    setFormData({
      issue: '',
      symptoms: '',
      resolution: '',
      partsReplaced: '',
      servicedBy: 'diy',
      cost: '',
    });
    toast.success('Repair record added!');
  };

  return (
    <div className="space-y-4">
      {/* Add Repair Form */}
      {showAddForm && (
        <Card className="p-4 bg-blue-50 border-blue-200">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-semibold text-lg">Log Repair/Issue</h3>
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
              placeholder="Issue (e.g., Water not draining)"
              value={formData.issue}
              onChange={(e) => setFormData({ ...formData, issue: e.target.value })}
              className="w-full px-3 py-2 border rounded-md text-sm"
            />

            <Textarea
              placeholder="Symptoms (one per line)&#10;e.g., &#10;- Water pooling at bottom&#10;- Beeping noise&#10;- Slow spin cycle"
              value={formData.symptoms}
              onChange={(e) => setFormData({ ...formData, symptoms: e.target.value })}
              className="text-sm"
            />

            <Textarea
              placeholder="Resolution/Fix Applied"
              value={formData.resolution}
              onChange={(e) => setFormData({ ...formData, resolution: e.target.value })}
              className="text-sm"
            />

            <Textarea
              placeholder="Parts Replaced (one per line, optional)"
              value={formData.partsReplaced}
              onChange={(e) => setFormData({ ...formData, partsReplaced: e.target.value })}
              className="text-sm"
            />

            <div className="grid grid-cols-2 gap-2">
              <select
                value={formData.servicedBy}
                onChange={(e) => setFormData({ ...formData, servicedBy: e.target.value as any })}
                className="px-3 py-2 border rounded-md text-sm"
              >
                <option value="diy">DIY</option>
                <option value="professional">Professional</option>
              </select>

              <input
                type="number"
                placeholder="Cost ($, optional)"
                value={formData.cost}
                onChange={(e) => setFormData({ ...formData, cost: e.target.value })}
                className="px-3 py-2 border rounded-md text-sm"
              />
            </div>

            <Button
              onClick={handleAddRepair}
              className="w-full bg-green-600 hover:bg-green-700"
            >
              Log Repair
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
          Log Repair/Issue
        </Button>
      )}

      {/* Repairs List */}
      <div className="space-y-2">
        {repairs.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <Wrench className="w-8 h-8 mx-auto mb-2 opacity-50" />
            <p className="text-sm">No repair history yet</p>
          </div>
        ) : (
          repairs.map((repair) => (
            <Card key={repair.id} className="p-3">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <h4 className="font-semibold text-sm">{repair.issue}</h4>
                    <span
                      className={`px-2 py-0.5 rounded text-xs font-medium ${
                        repair.servicedBy === 'diy'
                          ? 'bg-blue-100 text-blue-700'
                          : 'bg-purple-100 text-purple-700'
                      }`}
                    >
                      {repair.servicedBy === 'diy' ? '🔧 DIY' : '👨‍🔧 Pro'}
                    </span>
                  </div>

                  <p className="text-xs text-gray-600 flex items-center gap-1 mt-1">
                    <Calendar className="w-3 h-3" />
                    {repair.date.toLocaleDateString()}
                  </p>

                  {repair.symptoms.length > 0 && (
                    <div className="mt-2 text-xs">
                      <p className="font-semibold text-gray-700">Symptoms:</p>
                      <ul className="list-disc list-inside text-gray-600 ml-1">
                        {repair.symptoms.map((symptom, idx) => (
                          <li key={idx}>{symptom}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  <div className="mt-2 text-xs">
                    <p className="font-semibold text-gray-700">Resolution:</p>
                    <p className="text-gray-600">{repair.resolution}</p>
                  </div>

                  {repair.partsReplaced && repair.partsReplaced.length > 0 && (
                    <div className="mt-2 text-xs">
                      <p className="font-semibold text-gray-700">Parts Replaced:</p>
                      <ul className="list-disc list-inside text-gray-600 ml-1">
                        {repair.partsReplaced.map((part, idx) => (
                          <li key={idx}>{part}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {repair.cost && (
                    <p className="text-xs font-semibold text-orange-600 mt-2">
                      Cost: ${repair.cost.toFixed(2)}
                    </p>
                  )}
                </div>
              </div>
            </Card>
          ))
        )}
      </div>

      {/* Summary Stats */}
      {repairs.length > 0 && (
        <Card className="p-3 bg-gray-50">
          <h4 className="font-semibold text-sm mb-2">Summary</h4>
          <div className="grid grid-cols-2 gap-2 text-sm">
            <div>
              <p className="text-gray-600 text-xs">Total Repairs</p>
              <p className="font-semibold">{repairs.length}</p>
            </div>
            <div>
              <p className="text-gray-600 text-xs">DIY vs Professional</p>
              <p className="font-semibold">
                {repairs.filter(r => r.servicedBy === 'diy').length} /{' '}
                {repairs.filter(r => r.servicedBy === 'professional').length}
              </p>
            </div>
            {repairs.some(r => r.cost) && (
              <div className="col-span-2">
                <p className="text-gray-600 text-xs">Total Spent</p>
                <p className="font-semibold">
                  $
                  {repairs
                    .filter(r => r.cost)
                    .reduce((sum, r) => sum + (r.cost || 0), 0)
                    .toFixed(2)}
                </p>
              </div>
            )}
          </div>
        </Card>
      )}
    </div>
  );
}
