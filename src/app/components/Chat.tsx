import { useState, useRef, useEffect } from 'react';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';
import { Card } from './ui/card';
import { QRScanner } from './QRScanner';
import { ApplianceManager } from './ApplianceManager';
import { RepairHistory } from './RepairHistory';
import {
  Send,
  Mic,
  MicOff,
  QrCode,
  Image as ImageIcon,
  LogOut,
  Bot,
  User,
  AlertTriangle,
  X,
  Settings,
} from 'lucide-react';
import { toast } from 'sonner';
import { apiService, AnswerResponse } from '../../services/api';
import { 
  type DeviceInfo 
} from '../../config/deviceRegistry';
import type { UserAppliance } from '@/config/userApplianceManager';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  safetyFlag?: boolean;
  safetyLevel?: string;
  safetyMessage?: string;
  sources?: any[];
  processingTime?: number;
}

interface ChatProps {
  userName: string;
  onLogout: () => void;
}

export function Chat({ userName, onLogout }: ChatProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: `Hello ${userName}! 👋 I'm HomeBuddy, your intelligent appliance troubleshooting assistant. I can help you diagnose problems, provide repair guidance, and ensure safety.

**💬 Multiple Input Methods:**
🎤 Voice Input - Speak your question
📱 QR Code - Scan your appliance QR code
📷 Upload Photo - Share images of your appliance
⌨️ Text Input - Type your question

**🔧 Features:**
🏠 Track your appliances and maintenance history
📊 Get predictive maintenance alerts
⚠️ Safety warnings and guidance
🔍 AI-powered diagnostics

How can I help you today?`,
      timestamp: new Date(),
    },
  ]);
  const [inputText, setInputText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [showQRScanner, setShowQRScanner] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [currentDevice, setCurrentDevice] = useState<DeviceInfo | null>(null);
  const [showApplianceManager, setShowApplianceManager] = useState(false);
  const [selectedAppliance, setSelectedAppliance] = useState<UserAppliance | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const recognitionRef = useRef<any>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Check backend health on mount
  useEffect(() => {
    checkBackendHealth();
  }, []);

  const checkBackendHealth = async () => {
    try {
      const health = await apiService.healthCheck();
      if (!health.home_buddy_loaded) {
        toast.warning('AI model is still loading. Responses may be delayed.');
      }
    } catch (error) {
      console.error('Backend health check failed:', error);
      toast.error('Unable to connect to backend. Please ensure the server is running.');
    }
  };

  const addMessage = (
    role: 'user' | 'assistant',
    content: string,
    metadata?: Partial<Message>
  ) => {
    const newMessage: Message = {
      id: Date.now().toString(),
      role,
      content,
      timestamp: new Date(),
      ...metadata,
    };
    setMessages((prev) => [...prev, newMessage]);
    return newMessage;
  };

  const generateAIResponse = async (userMessage: string) => {
    setIsLoading(true);
    try {
      const response: AnswerResponse = await apiService.getAnswer({
        query: userMessage,
        brand: currentDevice?.brand,
        model: currentDevice?.model,
      });

      addMessage('assistant', response.answer, {
        safetyFlag: response.safety_flag,
        safetyLevel: response.safety_level,
        safetyMessage: response.safety_message,
        sources: response.sources,
        processingTime: response.processing_time,
      });

      // Show safety warning if flagged
      if (response.safety_flag && response.safety_message) {
        toast.error(response.safety_message, {
          duration: 5000,
        });
      }
    } catch (error) {
      console.error('Failed to get AI response:', error);
      addMessage(
        'assistant',
        `I'm sorry, I encountered an error processing your request. Please try again or check if the backend server is running. Error: ${error instanceof Error ? error.message : 'Unknown error'}`
      );
      toast.error('Failed to get response from AI');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = () => {
    if (!inputText.trim()) return;

    addMessage('user', inputText);
    generateAIResponse(inputText);
    setInputText('');
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const toggleVoiceInput = () => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      toast.error('Speech recognition is not supported in your browser');
      return;
    }

    if (isRecording) {
      recognitionRef.current?.stop();
      setIsRecording(false);
      return;
    }

    const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition;
    const recognition = new SpeechRecognition();
    
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
      setIsRecording(true);
      toast.info('Listening... Speak now');
    };

    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      setInputText(transcript);
      toast.success('Speech captured!');
    };

    recognition.onerror = (event: any) => {
      console.error('Speech recognition error:', event.error);
      toast.error('Speech recognition error: ' + event.error);
      setIsRecording(false);
    };

    recognition.onend = () => {
      setIsRecording(false);
    };

    recognitionRef.current = recognition;
    recognition.start();
  };

  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
      toast.error('Please upload an image file');
      return;
    }

    setIsLoading(true);
    addMessage('user', `📷 Uploaded image: ${file.name}`);

    try {
      const result = await apiService.uploadFile(file);
      toast.success(`Image processed: ${result.chunks_processed} chunks extracted`);
      
      addMessage(
        'assistant',
        `I've analyzed your image "${file.name}". ${result.status}. How can I help you with this image?`
      );
    } catch (error) {
      console.error('Failed to upload image:', error);
      toast.error('Failed to process image');
      addMessage(
        'assistant',
        `Sorry, I couldn't process the image. Error: ${error instanceof Error ? error.message : 'Unknown error'}`
      );
    } finally {
      setIsLoading(false);
      e.target.value = '';
    }
  };

  const handleQRScan = async (result: DeviceInfo) => {
    setShowQRScanner(false);
    addMessage('user', `📱 Scanned QR code for ${result.brand} ${result.model}`);
    
    setIsLoading(true);
    try {
      const device = result as DeviceInfo;
      setCurrentDevice(device);

      // Show device info card
      const deviceInfoMessage = `✅ **Device Loaded Successfully!**\n\n📱 Brand: ${device.brand}\n🔧 Model: ${device.model}\n🏠 Type: ${device.applianceType}\n${device.serialNumber ? `📊 Serial: ${device.serialNumber}` : ''}\n${device.manufactureYear ? `📅 Year: ${device.manufactureYear}` : ''}\n\nI've loaded the manual for this specific device. Now I can provide targeted help for your ${device.brand} ${device.model}!`;
      
      addMessage('assistant', deviceInfoMessage);
      toast.success(`Loaded ${device.brand} ${device.model}! Ask me anything about this device.`);

    } catch (error) {
      console.error('Failed to process QR code:', error);
      toast.error('Failed to process QR code');
      addMessage(
        'assistant',
        `I encountered an error processing the QR code. Error: ${error instanceof Error ? error.message : 'Unknown error'}`
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="h-screen flex flex-col bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <div className="bg-white shadow-md p-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="bg-indigo-600 p-2 rounded-full">
            <Bot className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-semibold">HomeBuddy</h1>
            <p className="text-sm text-gray-600">Always here to help</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setShowApplianceManager(!showApplianceManager)}
            className="gap-2"
          >
            <Settings className="w-4 h-4" />
            My Appliances
          </Button>
          <Button variant="ghost" onClick={onLogout} className="gap-2">
            <LogOut className="w-4 h-4" />
            Logout
          </Button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex gap-3 ${
              message.role === 'user' ? 'flex-row-reverse' : 'flex-row'
            }`}
          >
            <div
              className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                message.role === 'user' ? 'bg-indigo-600' : 'bg-gray-300'
              }`}
            >
              {message.role === 'user' ? (
                <User className="w-5 h-5 text-white" />
              ) : (
                <Bot className="w-5 h-5 text-gray-700" />
              )}
            </div>
            <Card
              className={`max-w-[70%] p-4 ${
                message.role === 'user'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-white text-gray-900'
              }`}
            >
              {message.safetyFlag && (
                <div className="flex items-center gap-2 mb-2 text-red-600 font-semibold">
                  <AlertTriangle className="w-4 h-4" />
                  <span className="text-sm">Safety Alert: {message.safetyLevel?.toUpperCase()}</span>
                </div>
              )}
              <p className="whitespace-pre-wrap">{message.content}</p>
              {message.safetyMessage && (
                <div className="mt-2 p-2 bg-red-100 rounded text-sm text-red-800">
                  ⚠️ {message.safetyMessage}
                </div>
              )}
            </Card>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="bg-white border-t p-4">
        <div className="max-w-4xl mx-auto space-y-3">
          {/* Action Buttons */}
          <div className="flex gap-2 justify-center">
            <Button
              variant="outline"
              size="sm"
              onClick={toggleVoiceInput}
              className={isRecording ? 'bg-red-50 border-red-300' : ''}
            >
              {isRecording ? (
                <>
                  <MicOff className="w-4 h-4 mr-2" />
                  Stop Recording
                </>
              ) : (
                <>
                  <Mic className="w-4 h-4 mr-2" />
                  Voice Input
                </>
              )}
            </Button>

            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowQRScanner(true)}
            >
              <QrCode className="w-4 h-4 mr-2" />
              Scan QR
            </Button>

            <Button
              variant="outline"
              size="sm"
              onClick={() => fileInputRef.current?.click()}
            >
              <ImageIcon className="w-4 h-4 mr-2" />
              Upload Photo
            </Button>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              className="hidden"
              onChange={handleImageUpload}
            />
          </div>

          {/* Text Input */}
          <div className="flex gap-2">
            <Textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Type your message or use one of the input methods above..."
              className="resize-none min-h-[60px]"
              rows={2}
              disabled={isLoading}
            />
            <Button
              onClick={handleSendMessage}
              disabled={!inputText.trim() || isLoading}
              className="bg-indigo-600 hover:bg-indigo-700"
              size="icon"
            >
              {isLoading ? (
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
            </Button>
          </div>
        </div>
      </div>

      {/* QR Scanner Modal */}
      {showQRScanner && (
        <QRScanner onScan={handleQRScan} onClose={() => setShowQRScanner(false)} />
      )}

      {/* Appliance Manager Modal */}
      {showApplianceManager && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg p-6 max-w-2xl w-full max-h-[80vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-bold text-gray-900">My Appliances</h2>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setShowApplianceManager(false)}
              >
                <X className="w-5 h-5" />
              </Button>
            </div>
            {!selectedAppliance ? (
              <ApplianceManager
                userId={userName}
                onApplianceSelect={setSelectedAppliance}
              />
            ) : (
              <div className="space-y-4">
                <Button
                  variant="outline"
                  className="w-full"
                  onClick={() => setSelectedAppliance(null)}
                >
                  ← Back to Appliances
                </Button>
                <Card className="p-4 bg-indigo-50 border-indigo-200">
                  <h3 className="font-semibold text-gray-900">
                    {selectedAppliance?.brand} {selectedAppliance?.model}
                  </h3>
                  <p className="text-sm text-gray-600 mt-1">
                    Added: {selectedAppliance && new Date(selectedAppliance.addedAt).toLocaleDateString()}
                  </p>
                </Card>
                {selectedAppliance && (
                  <RepairHistory userId={userName} appliance={selectedAppliance} />
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
