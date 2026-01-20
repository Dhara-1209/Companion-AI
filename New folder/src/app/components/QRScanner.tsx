import { useEffect, useRef, useState } from 'react';
import QrScanner from 'qr-scanner';
import { Button } from '@/app/components/ui/button';
import { X } from 'lucide-react';

interface QRScannerProps {
  onScan: (result: string) => void;
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
        onScan(result.data);
        qrScanner.stop();
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
              className="w-full rounded-lg bg-black"
              style={{ maxHeight: '400px' }}
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
