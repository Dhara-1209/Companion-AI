import { useEffect, useRef, useState } from 'react';
import QrScanner from 'qr-scanner';
import { Button } from '@/app/components/ui/button';
import { X } from 'lucide-react';
import { parseQRCodeData, isValidDeviceInfo, type DeviceInfo } from '@/config/deviceRegistry';

interface QRScannerProps {
  onScan: (result: DeviceInfo) => void;
  onClose: () => void;
}

export function QRScanner({ onScan, onClose }: QRScannerProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [scanner, setScanner] = useState<QrScanner | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!videoRef.current) return;

    const qrScanner = new QrScanner(
      videoRef.current,
      (result) => {
        // Parse QR code data to extract device information
        const deviceData = parseQRCodeData(result.data);
        if (deviceData && isValidDeviceInfo(deviceData)) {
          onScan(deviceData);
          qrScanner.stop();
        } else {
          console.warn('Invalid device information in QR code:', result.data);
          setError('QR code does not contain valid device information. Please try again.');
          // Restart scanner for another attempt
          setTimeout(() => {
            setError(null);
            qrScanner.start().catch(err => console.error('Failed to restart scanner:', err));
          }, 2000);
        }
      },
      {
        highlightScanRegion: true,
        highlightCodeOutline: true,
      }
    );

    setScanner(qrScanner);

    qrScanner.start().catch((err) => {
      console.error('QR Scanner error:', err);
      setError('Failed to access camera. Please check permissions.');
    });

    return () => {
      qrScanner.stop();
      qrScanner.destroy();
    };
  }, [onScan]);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg p-6 max-w-md w-full relative">
        <Button
          variant="ghost"
          size="icon"
          className="absolute top-2 right-2"
          onClick={() => {
            scanner?.stop();
            onClose();
          }}
        >
          <X className="w-5 h-5" />
        </Button>

        <h3 className="text-xl font-semibold mb-4">Scan QR Code</h3>

        {error ? (
          <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-md">
            {error}
          </div>
        ) : (
          <>
            <video
              ref={videoRef}
              className="w-full rounded-lg bg-black max-h-96"
            />
            <p className="text-sm text-gray-600 mt-4 text-center">
              Position the QR code within the frame
            </p>
          </>
        )}
      </div>
    </div>
  );
}
