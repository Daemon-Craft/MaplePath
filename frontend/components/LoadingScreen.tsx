import React from 'react';
import { View, ActivityIndicator, Text, StyleSheet } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { colors, fontSizes } from '../constants/theme';

export default function LoadingScreen() {
  return (
    <LinearGradient
      colors={[colors.primary, colors.secondary]}
      style={styles.container}
    >
      <View style={styles.content}>
        <Text style={styles.title}>MaplePath</Text>
        <Text style={styles.subtitle}>Your Canadian Journey Starts Here</Text>

        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="white" />
          <Text style={styles.loadingText}>Loading...</Text>
        </View>
      </View>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  content: {
    alignItems: 'center',
  },
  title: {
    fontSize: 36,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 8,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: fontSizes.lg,
    color: 'white',
    opacity: 0.9,
    textAlign: 'center',
    marginBottom: 50,
    paddingHorizontal: 40,
  },
  loadingContainer: {
    alignItems: 'center',
  },
  loadingText: {
    fontSize: fontSizes.md,
    color: 'white',
    marginTop: 15,
    opacity: 0.8,
  },
});