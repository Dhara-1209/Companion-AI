import { useState, useRef, useEffect } from 'react';
import { Button } from '@/app/components/ui/button';
import { Textarea } from '@/app/components/ui/textarea';
import { Card } from '@/app/components/ui/card';
import { QRScanner } from '@/app/components/QRScanner';
import {
  Send,
  Mic,
  MicOff,
  QrCode,
  Image as ImageIcon,
  LogOut,
  Bot,
  User,
} from 'lucide-react';
import { toast } from 'sonner';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
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
      content: `Hello ${userName}! 👋 I'm Companion AI, your intelligent assistant. I can help you with various tasks. You can send me messages by typing, using voice input, uploading photos, or scanning QR codes!`,
      timestamp: new Date(),
    },
  ]);
  const [inputText, setInputText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [showQRScanner, setShowQRScanner] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const recognitionRef = useRef<any>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const addMessage = (role: 'user' | 'assistant', content: string) => {
    const newMessage: Message = {
      id: Date.now().toString(),
      role,
      content,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, newMessage]);
  };

  const generateAIResponse = (userMessage: string) => {
    // Simulate AI response
    setTimeout(() => {
      let response = '';
      
      if (userMessage.toLowerCase().includes('hello') || userMessage.toLowerCase().includes('hi')) {
        response = "Hello! How can I assist you today?";
      } else if (userMessage.toLowerCase().includes('help')) {
        response = "I'm here to help! You can ask me questions, share images, scan QR codes, or use voice input. What would you like to do?";
      } else if (userMessage.includes('http') || userMessage.includes('www')) {
        response = "I detected a URL in your message. I can help you analyze or work with web links!";
      } else if (userMessage.toLowerCase().includes('qr')) {
        response = "You mentioned QR codes! Click the QR code icon below to scan one, or I can help you generate QR codes too.";
      } else {
        response = `I received your message: "${userMessage}". As a demo chatbot, I'm showing you that I can process your input! In a real implementation, I would be connected to an AI service to provide intelligent responses.`;
      }

      addMessage('assistant', response);
    }, 500);
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

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
      toast.error('Please upload an image file');
      return;
    }

    const reader = new FileReader();
    reader.onload = () => {
      addMessage('user', `📷 Uploaded image: ${file.name}`);
      setTimeout(() => {
        addMessage(
          'assistant',
          `I received your image "${file.name}". In a full implementation, I would analyze this image using AI vision models to describe its contents, detect objects, read text, or answer questions about it!`
        );
      }, 500);
    };
    reader.readAsDataURL(file);
    e.target.value = '';
  };

  const handleQRScan = (result: string) => {
    setShowQRScanner(false);
    addMessage('user', `📱 Scanned QR code: ${result}`);
    setTimeout(() => {
      addMessage(
        'assistant',
        `I detected the following content from the QR code: "${result}". How would you like me to help you with this?`
      );
    }, 500);
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
            <h1 className="text-xl font-semibold">Companion AI</h1>
            <p className="text-sm text-gray-600">Always here to help</p>
          </div>
        </div>
        <Button variant="ghost" onClick={onLogout} className="gap-2">
          <LogOut className="w-4 h-4" />
          Logout
        </Button>
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
              <p className="whitespace-pre-wrap">{message.content}</p>
              <p
                className={`text-xs mt-2 ${
                  message.role === 'user' ? 'text-indigo-200' : 'text-gray-500'
                }`}
              >
                {message.timestamp.toLocaleTimeString()}
              </p>
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
            />
            <Button
              onClick={handleSendMessage}
              disabled={!inputText.trim()}
              className="bg-indigo-600 hover:bg-indigo-700"
              size="icon"
            >
              <Send className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </div>

      {/* QR Scanner Modal */}
      {showQRScanner && (
        <QRScanner onScan={handleQRScan} onClose={() => setShowQRScanner(false)} />
      )}
    </div>
  );
}
