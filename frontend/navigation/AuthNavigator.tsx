import React, { useState } from 'react';
import { View } from 'react-native';
import OnboardingScreen from '../screens/OnboardingScreen';
import LoginScreen from '../screens/LoginScreen';
import RegisterScreen from '../screens/RegisterScreen';

interface AuthNavigatorProps {
  onAuthComplete: () => void;
}

export default function AuthNavigator({ onAuthComplete }: AuthNavigatorProps) {
  const [showOnboarding, setShowOnboarding] = useState(true);
  const [authFlow, setAuthFlow] = useState<'login' | 'register'>('login');

  const handleOnboardingComplete = () => {
    setShowOnboarding(false);
  };

  const handleLogin = () => {
    onAuthComplete();
  };

  const handleRegister = () => {
    onAuthComplete();
  };

  const navigateToRegister = () => {
    setAuthFlow('register');
  };

  const navigateToLogin = () => {
    setAuthFlow('login');
  };

  if (showOnboarding) {
    return <OnboardingScreen onComplete={handleOnboardingComplete} />;
  }

  return (
      <View style={{ flex: 1 }}>
        {authFlow === 'login' ? (
            <LoginScreen
                onLogin={handleLogin}
                onNavigateToRegister={navigateToRegister}
            />
        ) : (
            <RegisterScreen
                onRegister={handleRegister}
                onNavigateToLogin={navigateToLogin}
            />
        )}
      </View>
  );
}