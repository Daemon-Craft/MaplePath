import React, { useState } from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import OnboardingScreen from '../screens/OnboardingScreen';
import LoginScreen from '../screens/LoginScreen';
import RegisterScreen from '../screens/RegisterScreen';

const Stack = createStackNavigator();

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
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      {authFlow === 'login' ? (
        <Stack.Screen name="Login">
          {() => (
            <LoginScreen
              onLogin={handleLogin}
              onNavigateToRegister={navigateToRegister}
            />
          )}
        </Stack.Screen>
      ) : (
        <Stack.Screen name="Register">
          {() => (
            <RegisterScreen
              onRegister={handleRegister}
              onNavigateToLogin={navigateToLogin}
            />
          )}
        </Stack.Screen>
      )}
    </Stack.Navigator>
  );
}
