import React, { useState, useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { StatusBar } from 'expo-status-bar';
import AsyncStorage from '@react-native-async-storage/async-storage';
import AuthNavigator from './navigation/AuthNavigator';
import TabNavigator from './navigation/TabNavigator';

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      // Check if user has completed onboarding and is authenticated
      const authToken = await AsyncStorage.getItem('authToken');
      const hasCompletedOnboarding = await AsyncStorage.getItem('hasCompletedOnboarding');

      if (authToken && hasCompletedOnboarding) {
        setIsAuthenticated(true);
      }
    } catch (error) {
      console.log('Error checking auth status:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAuthComplete = async () => {
    try {
      // Save authentication status
      await AsyncStorage.setItem('authToken', 'user_authenticated');
      await AsyncStorage.setItem('hasCompletedOnboarding', 'true');
      setIsAuthenticated(true);
    } catch (error) {
      console.log('Error saving auth status:', error);
    }
  };

  const handleLogout = async () => {
    try {
      await AsyncStorage.removeItem('authToken');
      setIsAuthenticated(false);
    } catch (error) {
      console.log('Error logging out:', error);
    }
  };

  if (isLoading) {
    // You can add a proper loading screen here
    return null;
  }

  return (
    <NavigationContainer>
      <StatusBar style="auto" />
      {isAuthenticated ? (
        <TabNavigator />
      ) : (
        <AuthNavigator onAuthComplete={handleAuthComplete} />
      )}
    </NavigationContainer>
  );
}
