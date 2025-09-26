import React, { useEffect, useRef } from 'react';
import { View, Text, StyleSheet, Dimensions, Animated } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';

const { width, height } = Dimensions.get('window');

interface OnboardingSlideProps {
  title: string;
  subtitle: string;
  icon: keyof typeof Ionicons.glyphMap;
  color: string;
  isActive: boolean;
}

export default function OnboardingSlide({ title, subtitle, icon, color, isActive }: OnboardingSlideProps) {
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const scaleAnim = useRef(new Animated.Value(0.8)).current;
  const slideAnim = useRef(new Animated.Value(50)).current;

  useEffect(() => {
    if (isActive) {
      Animated.parallel([
        Animated.timing(fadeAnim, {
          toValue: 1,
          duration: 800,
          useNativeDriver: true,
        }),
        Animated.spring(scaleAnim, {
          toValue: 1,
          tension: 100,
          friction: 8,
          useNativeDriver: true,
        }),
        Animated.timing(slideAnim, {
          toValue: 0,
          duration: 600,
          useNativeDriver: true,
        }),
      ]).start();
    } else {
      fadeAnim.setValue(0);
      scaleAnim.setValue(0.8);
      slideAnim.setValue(50);
    }
  }, [isActive]);

  return (
    <View style={styles.slide}>
      <LinearGradient
        colors={['#f8f9fa', '#ffffff']}
        style={styles.gradient}
      >
        <Animated.View
          style={[
            styles.iconContainer,
            {
              opacity: fadeAnim,
              transform: [{ scale: scaleAnim }],
            },
          ]}
        >
          <View style={[styles.iconBackground, { backgroundColor: `${color}20` }]}>
            <Ionicons name={icon} size={80} color={color} />
          </View>
        </Animated.View>

        <Animated.View
          style={[
            styles.textContainer,
            {
              opacity: fadeAnim,
              transform: [{ translateY: slideAnim }],
            },
          ]}
        >
          <Text style={styles.title}>{title}</Text>
          <Text style={styles.subtitle}>{subtitle}</Text>
        </Animated.View>
      </LinearGradient>
    </View>
  );
}

const styles = StyleSheet.create({
  slide: {
    flex: 1,
    width,
  },
  gradient: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 40,
  },
  iconContainer: {
    marginBottom: 60,
  },
  iconBackground: {
    width: 160,
    height: 160,
    borderRadius: 80,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 10,
    },
    shadowOpacity: 0.1,
    shadowRadius: 20,
    elevation: 10,
  },
  textContainer: {
    alignItems: 'center',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#333',
    textAlign: 'center',
    marginBottom: 20,
    lineHeight: 40,
  },
  subtitle: {
    fontSize: 18,
    color: '#666',
    textAlign: 'center',
    lineHeight: 26,
    paddingHorizontal: 20,
  },
});
