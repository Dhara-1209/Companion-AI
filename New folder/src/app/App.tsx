import { useState } from 'react';
import { Login } from '@/app/components/Login';
import { Signup } from '@/app/components/Signup';
import { Chat } from '@/app/components/Chat';
import { Toaster } from '@/app/components/ui/sonner';
import { toast } from 'sonner';

type Screen = 'login' | 'signup' | 'chat';

export default function App() {
  const [currentScreen, setCurrentScreen] = useState<Screen>('login');
  const [userName, setUserName] = useState('');

  const handleLogin = (email: string, password: string) => {
    // Mock authentication
    toast.success('Login successful!');
    setUserName(email.split('@')[0]);
    setCurrentScreen('chat');
  };

  const handleSignup = (name: string, email: string, password: string) => {
    // Mock registration
    toast.success('Account created successfully!');
    setUserName(name);
    setCurrentScreen('chat');
  };

  const handleLogout = () => {
    toast.info('Logged out successfully');
    setUserName('');
    setCurrentScreen('login');
  };

  return (
    <>
      {currentScreen === 'login' && (
        <Login
          onLogin={handleLogin}
          onSwitchToSignup={() => setCurrentScreen('signup')}
        />
      )}

      {currentScreen === 'signup' && (
        <Signup
          onSignup={handleSignup}
          onSwitchToLogin={() => setCurrentScreen('login')}
        />
      )}

      {currentScreen === 'chat' && (
        <Chat userName={userName} onLogout={handleLogout} />
      )}

      <Toaster position="top-center" richColors />
    </>
  );
}
