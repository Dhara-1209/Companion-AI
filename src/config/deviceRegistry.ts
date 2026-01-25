/**
 * Device Registry for QR Code Mapping
 * Maps QR codes to device information (brand, model, manual, etc.)
 */

export interface DeviceInfo {
  qrCode: string;
  brand: string;
  model: string;
  applianceType: 'washer' | 'dishwasher' | 'oven' | 'microwave' | 'vacuum';
  serialNumber?: string;
  manufactureYear?: number;
  manualPath?: string;
  errorCodes?: string[];
  commonIssues?: string[];
}

// Device registry - maps QR codes to device information
// In production, this would come from a database or external service
export const deviceRegistry: Map<string, DeviceInfo> = new Map([
  // Samsung Washers
  [
    'SAMSUNG-WF42H5200-001',
    {
      qrCode: 'SAMSUNG-WF42H5200-001',
      brand: 'Samsung',
      model: 'WF42H5200',
      applianceType: 'washer',
      serialNumber: 'WF42H5200001',
      manufactureYear: 2021,
    },
  ],
  // LG Microwaves
  [
    'LG-MS2595DIS-001',
    {
      qrCode: 'LG-MS2595DIS-001',
      brand: 'LG',
      model: 'MS2595DIS',
      applianceType: 'microwave',
      serialNumber: 'LG20210001',
      manufactureYear: 2021,
    },
  ],
  // Bosch Dishwashers
  [
    'BOSCH-SMI68TS06E-001',
    {
      qrCode: 'BOSCH-SMI68TS06E-001',
      brand: 'Bosch',
      model: 'SMI68TS06E',
      applianceType: 'dishwasher',
      serialNumber: 'BOSCH001',
      manufactureYear: 2020,
    },
  ],
  // Whirlpool Ovens
  [
    'WHIRLPOOL-WFE725H0HV-001',
    {
      qrCode: 'WHIRLPOOL-WFE725H0HV-001',
      brand: 'Whirlpool',
      model: 'WFE725H0HV',
      applianceType: 'oven',
      serialNumber: 'WP20210001',
      manufactureYear: 2021,
    },
  ],
]);

/**
 * Get device info by QR code
 */
export function getDeviceByQRCode(qrCode: string): DeviceInfo | null {
  return deviceRegistry.get(qrCode) || null;
}

/**
 * Parse QR code data - supports multiple formats:
 * 1. Direct QR code mapping: "SAMSUNG-WF42H5200-001"
 * 2. JSON format: {"brand":"Samsung","model":"WF42H5200","type":"washer"}
 * 3. Colon-separated: "Samsung:WF42H5200:washer"
 */
export function parseQRCodeData(
  qrData: string
): Partial<DeviceInfo> | null {
  try {
    // Check if it's a registered QR code
    const registered = getDeviceByQRCode(qrData);
    if (registered) {
      return registered;
    }

    // Try parsing as JSON
    if (qrData.startsWith('{')) {
      const parsed = JSON.parse(qrData);
      return {
        qrCode: parsed.qrCode || qrData,
        brand: parsed.brand || parsed.manufacturer,
        model: parsed.model || parsed.modelNumber,
        applianceType: parsed.applianceType || parsed.type,
        serialNumber: parsed.serialNumber || parsed.serial,
        manufactureYear: parsed.manufactureYear || parsed.year,
      };
    }

    // Try parsing as colon-separated format
    if (qrData.includes(':')) {
      const parts = qrData.split(':');
      if (parts.length >= 3) {
        return {
          qrCode: qrData,
          brand: parts[0].trim(),
          model: parts[1].trim(),
          applianceType: (parts[2].trim().toLowerCase() as DeviceInfo['applianceType']) || undefined,
          serialNumber: parts[3]?.trim(),
        };
      }
    }

    // Try parsing as space-separated format
    if (qrData.includes(' ')) {
      const parts = qrData.split(/\s+/);
      if (parts.length >= 2) {
        return {
          qrCode: qrData,
          brand: parts[0],
          model: parts[1],
          applianceType: (parts[2]?.toLowerCase() as DeviceInfo['applianceType']) || undefined,
        };
      }
    }

    // Last resort: treat as "Brand Model" format
    const spacedParts = qrData.trim().split(/\s+/);
    if (spacedParts.length >= 2) {
      return {
        qrCode: qrData,
        brand: spacedParts[0],
        model: spacedParts.slice(1).join('-'),
      };
    }
  } catch (error) {
    console.error('Error parsing QR code:', error);
  }

  return null;
}

/**
 * Validate device info has required fields
 */
export function isValidDeviceInfo(device: Partial<DeviceInfo>): device is DeviceInfo {
  return !!(device.brand && device.model);
}
