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
  Zap,
  Settings,
  ChevronDown,
  ChevronUp,
} from 'lucide-react';
import { toast } from 'sonner';
import { apiService, AnswerResponse } from '../../services/api';
import { 
  parseQRCodeData, 
  isValidDeviceInfo, 
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

**New Features:**
🏠 Track your appliances and maintenance history
🔧 Log repairs and get repair patterns
⚠️ Get predictive maintenance alerts
📊 View repair statistics

You can scan a QR code from your appliance to load its specific manual and get customized help!`,
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

  const handleKeyPress = (e: React.KeyboardEvent) => {
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

  const handleClearDevice = () => {
    setCurrentDevice(null);
    addMessage('assistant', 'Device context cleared. You can now ask general appliance questions or scan a new QR code.');
  };

  return (
    <div className="h-screen flex bg-gray-50">
      {/* Main Content Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-white border-b px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-gradient-to-br from-purple-600 to-purple-700 p-2.5 rounded-xl shadow-md">
              <Bot className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">HomeBuddy</h1>
              <p className="text-sm text-gray-500">Smart Appliance Assistant</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Button
              variant="outline"
              onClick={() => setShowApplianceManager(!showApplianceManager)}
              className="gap-2 border-gray-200 hover:bg-gray-50"
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

        {/* Chat Area */}
        <div className="flex-1 overflow-y-auto px-6 py-6">
          <div className="max-w-5xl mx-auto space-y-6">
            {/* AI Assistant Header */}
            <div className="flex items-center justify-between bg-white rounded-xl p-4 shadow-sm border">
              <div className="flex items-center gap-3">
                <div className="bg-gradient-to-br from-purple-600 to-purple-700 p-2.5 rounded-full">
                  <Bot className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">AI Assistant</h3>
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    <span className="text-sm text-green-600">Online</span>
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-sm text-purple-600 font-medium">Smart Mode</span>
                <div className="w-10 h-5 bg-purple-600 rounded-full flex items-center px-0.5">
                  <div className="w-4 h-4 bg-white rounded-full ml-auto"></div>
                </div>
              </div>
            </div>

            {/* Current Device Info */}
            {currentDevice && (
              <div className="flex items-center gap-2 bg-gradient-to-r from-purple-100 to-blue-100 px-4 py-3 rounded-xl border border-purple-200">
                <Zap className="w-5 h-5 text-purple-600" />
                <div className="flex-1">
                  <p className="text-xs font-semibold text-purple-900">Active Device</p>
                  <p className="text-sm font-medium text-purple-800">
                    {currentDevice.brand} {currentDevice.model}
                  </p>
                </div>
                <button
                  onClick={handleClearDevice}
                  className="text-purple-600 hover:text-purple-800 p-1 rounded-lg hover:bg-purple-200 transition-colors"
                  title="Clear device"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            )}

            {/* Messages */}
            <div className="space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex gap-3 ${
                    message.role === 'user' ? 'flex-row-reverse' : 'flex-row'
                  }`}
                >
                  <div
                    className={`flex-shrink-0 w-9 h-9 rounded-full flex items-center justify-center ${
                      message.role === 'user' 
                        ? 'bg-gradient-to-br from-purple-600 to-purple-700' 
                        : 'bg-gradient-to-br from-purple-600 to-purple-700'
                    }`}
                  >
                    {message.role === 'user' ? (
                      <User className="w-5 h-5 text-white" />
                    ) : (
                      <Bot className="w-5 h-5 text-white" />
                    )}
                  </div>
                  <div
                    className={`max-w-[70%] rounded-2xl px-5 py-4 ${
                      message.role === 'user'
                        ? 'bg-gradient-to-br from-purple-600 to-purple-700 text-white'
                        : message.safetyFlag
                        ? 'bg-red-50 border-2 border-red-300 text-gray-900'
                        : 'bg-white text-gray-900 shadow-sm border border-gray-100'
                    }`}
                  >
                    {message.safetyFlag && (
                      <div className="flex items-center gap-2 mb-3 text-red-600 font-semibold">
                        <AlertTriangle className="w-4 h-4" />
                        <span className="text-sm">Safety Alert: {message.safetyLevel?.toUpperCase()}</span>
                      </div>
                    )}
                    <div className="whitespace-pre-wrap text-[15px] leading-relaxed">{message.content}</div>
                    {message.safetyMessage && (
                      <div className="mt-3 p-3 bg-red-100 rounded-lg text-sm text-red-800">
                        ⚠️ {message.safetyMessage}
                      </div>
                    )}
                    {message.sources && message.sources.length > 0 && (
                      <div className="mt-4 pt-4 border-t border-gray-200">
                        <p className="text-xs font-semibold text-gray-600 mb-2">Sources:</p>
                        <ul className="text-xs text-gray-500 space-y-1.5">
                          {message.sources.slice(0, 3).map((source: any, idx: number) => (
                            <li key={idx}>
                              📄 {source.filename} {source.page && `(p.${source.page})`}
                              {source.brand && ` - ${source.brand}`}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                    <p
                      className={`text-xs mt-3 ${
                        message.role === 'user' ? 'text-purple-200' : 'text-gray-400'
                      }`}
                    >
                      {message.timestamp.toLocaleTimeString()}
                      {message.processingTime && ` • ${message.processingTime.toFixed(2)}s`}
                    </p>
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
          </div>
        </div>

        {/* Input Area */}
        <div className="bg-white border-t px-6 py-4">
          <div className="max-w-5xl mx-auto space-y-4">
            {/* Action Buttons */}
            <div className="flex gap-3 justify-center">
              <Button
                variant="outline"
                size="sm"
                onClick={toggleVoiceInput}
                className={`gap-2 ${isRecording ? 'bg-red-50 border-red-300 text-red-600' : 'border-gray-200'}`}
              >
                {isRecording ? (
                  <>
                    <MicOff className="w-4 h-4" />
                    Voice Input
                  </>
                ) : (
                  <>
                    <Mic className="w-4 h-4" />
                    Voice Input
                  </>
                )}
              </Button>

              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowQRScanner(true)}
                className="gap-2 border-gray-200"
              >
                <QrCode className="w-4 h-4" />
                Scan QR
              </Button>

              <Button
                variant="outline"
                size="sm"
                onClick={() => fileInputRef.current?.click()}
                className="gap-2 border-gray-200"
              >
                <ImageIcon className="w-4 h-4" />
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
            <div className="flex gap-3">
              <Textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyDown={handleKeyPress}
                placeholder="Type your appliance question here..."
                className="resize-none rounded-xl border-gray-200 focus:border-purple-500 focus:ring-purple-500"
                rows={1}
                disabled={isLoading}
              />
              <Button
                onClick={handleSendMessage}
                disabled={!inputText.trim() || isLoading}
                className="bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800 text-white rounded-xl px-6 shadow-md"
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
      </div>

      {/* Right Sidebar - Quick Stats */}
      {!showApplianceManager && (
        <div className="w-80 bg-white border-l overflow-y-auto">
          <div className="p-6 space-y-6">
            {/* Quick Stats Header */}
            <div>
              <h3 className="text-lg font-bold text-gray-900 mb-4">Quick Stats</h3>
              
              <div className="space-y-3">
                <Card className="p-4 bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200 shadow-sm">
                  <div className="flex items-start gap-3">
                    <div className="bg-purple-100 p-2 rounded-lg">
                      <Zap className="w-5 h-5 text-purple-600" />
                    </div>
                    <div className="flex-1">
                      <p className="text-sm text-gray-600 mb-1">Quick Diagnostics</p>
                      <p className="text-2xl font-bold text-gray-900">{'< 2 min'}</p>
                    </div>
                  </div>
                </Card>

                <Card className="p-4 bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200 shadow-sm">
                  <div className="flex items-start gap-3">
                    <div className="bg-blue-100 p-2 rounded-lg">
                      <Settings className="w-5 h-5 text-blue-600" />
                    </div>
                    <div className="flex-1">
                      <p className="text-sm text-gray-600 mb-1">Warranty Tracking</p>
                      <p className="text-2xl font-bold text-gray-900">Auto</p>
                    </div>
                  </div>
                </Card>
              </div>
            </div>

            {/* Available Features */}
            <div>
              <h3 className="text-lg font-bold text-gray-900 mb-4">Available Features</h3>
              
              <Card className="p-4 bg-gradient-to-br from-purple-50 to-pink-50 border-purple-200">
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-purple-600 rounded-full"></div>
                    <p className="text-sm font-medium text-gray-700">Smart Features</p>
                  </div>
                  <ul className="text-sm text-gray-600 space-y-2 ml-4">
                    <li>• AI-Powered Diagnostics</li>
                    <li>• Error Code Database</li>
                    <li>• Repair History Tracking</li>
                    <li>• Predictive Maintenance</li>
                    <li>• Safety Alerts</li>
                  </ul>
                </div>
              </Card>
            </div>
          </div>
        </div>
      )}

      {/* Appliance Manager Sidebar */}
      {showApplianceManager && (
        <div className="w-96 bg-white border-l overflow-y-auto">
          <div className="p-6 space-y-4">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-bold text-gray-900">My Appliances</h2>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setShowApplianceManager(false)}
                className="hover:bg-gray-100"
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

                <Card className="p-4 bg-purple-50 border-purple-200">
                  <h3 className="font-semibold text-gray-900">
                    {selectedAppliance.brand} {selectedAppliance.model}
                  </h3>
                  <p className="text-sm text-gray-600 mt-1">
                    Added: {new Date(selectedAppliance.addedAt).toLocaleDateString()}
                  </p>
                </Card>

                <RepairHistory userId={userName} appliance={selectedAppliance} />
              </div>
            )}
          </div>
        </div>
      )}

      {/* QR Scanner Modal */}
      {showQRScanner && (
        <QRScanner onScan={handleQRScan} onClose={() => setShowQRScanner(false)} />
      )}
    </div>
  );
}
