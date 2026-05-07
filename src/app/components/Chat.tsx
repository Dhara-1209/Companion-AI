import { useState, useRef, useEffect } from 'react';
import { Button } from '@/app/components/ui/button';
import { Textarea } from '@/app/components/ui/textarea';
import { Card } from '@/app/components/ui/card';
import {
  Send,
  Mic,
  MicOff,
  LogOut,
  Bot,
  User,
  AlertTriangle,
} from 'lucide-react';
import { toast } from 'sonner';
import { apiService, AnswerResponse } from '@/services/api';

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
      content: `Hello ${userName}! 👋 I'm Companion AI, your intelligent appliance troubleshooting assistant. I can help you diagnose problems, provide repair guidance, and ensure safety. Ask me about any appliance issue you're experiencing!`,
      timestamp: new Date(),
    },
  ]);
  const [inputText, setInputText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
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
      if (!health.companion_ai_loaded) {
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
                  : message.safetyFlag
                  ? 'bg-red-50 border-2 border-red-300 text-gray-900'
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
              {message.sources && message.sources.length > 0 && (
                <div className="mt-3 pt-3 border-t border-gray-200">
                  <p className="text-xs font-semibold text-gray-600 mb-1">Sources:</p>
                  <ul className="text-xs text-gray-500 space-y-1">
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
                className={`text-xs mt-2 ${
                  message.role === 'user' ? 'text-indigo-200' : 'text-gray-500'
                }`}
              >
                {message.timestamp.toLocaleTimeString()}
                {message.processingTime && ` • ${message.processingTime.toFixed(2)}s`}
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
          </div>

          {/* Text Input */}
          <div className="flex gap-2">
            <Textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder={
                isLoading
                  ? 'Processing your request...'
                  : 'Type your appliance question here...'
              }
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


    </div>
  );
}
