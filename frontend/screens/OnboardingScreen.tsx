import React, { useState, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Dimensions,
  ScrollView,
  TouchableOpacity,
  Animated
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import OnboardingSlide from '../components/OnboardingSlide';

const { width, height } = Dimensions.get('window');

interface OnboardingScreenProps {
  onComplete: () => void;
}

const slides = [
  {
    title: 'Welcome to Canada!',
    subtitle: 'Start your Canadian journey with confidence. We\'ll help you navigate every step of your new life in Canada.',
    icon: 'flag' as const,
    color: '#c7372c',
  },
  {
    title: 'Save Money with Local Deals',
    subtitle: 'Discover exclusive discounts and deals tailored for newcomers. Save on essentials while you settle in.',
    icon: 'wallet' as const,
    color: '#28A745',
  },
  {
    title: 'Build Your Canadian Career',
    subtitle: 'Access tools and resources to enhance your resume and find opportunities in the Canadian job market.',
    icon: 'briefcase' as const,
    color: '#FF6B35',
  },
];

export default function OnboardingScreen({ onComplete }: OnboardingScreenProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const scrollViewRef = useRef<ScrollView>(null);
  const buttonScaleAnim = useRef(new Animated.Value(1)).current;
  const indicatorAnims = useRef(slides.map((_, index) => new Animated.Value(index === 0 ? 1 : 0))).current;

  const handleScroll = (event: any) => {
    const scrollPosition = event.nativeEvent.contentOffset.x;
    const index = Math.round(scrollPosition / width);
    if (index !== currentIndex) {
      setCurrentIndex(index);
      animateIndicators(index);
    }
  };

  const animateIndicators = (activeIndex: number) => {
    indicatorAnims.forEach((anim, index) => {
      Animated.timing(anim, {
        toValue: index === activeIndex ? 1 : 0,
        duration: 300,
        useNativeDriver: false,
      }).start();
    });
  };

  const goToSlide = (index: number) => {
    scrollViewRef.current?.scrollTo({ x: index * width, animated: true });
    setCurrentIndex(index);
    animateIndicators(index);
  };

  const handleNext = () => {
    if (currentIndex < slides.length - 1) {
      goToSlide(currentIndex + 1);
    } else {
      // Animate button press
      Animated.sequence([
        Animated.timing(buttonScaleAnim, {
          toValue: 0.95,
          duration: 100,
          useNativeDriver: true,
        }),
        Animated.timing(buttonScaleAnim, {
          toValue: 1,
          duration: 100,
          useNativeDriver: true,
        }),
      ]).start(() => {
        onComplete();
      });
    }
  };

  const handleSkip = () => {
    onComplete();
  };

  return (
    <View style={styles.container}>
      <ScrollView
        ref={scrollViewRef}
        horizontal
        pagingEnabled
        showsHorizontalScrollIndicator={false}
        onScroll={handleScroll}
        scrollEventThrottle={16}
        style={styles.scrollView}
      >
        {slides.map((slide, index) => (
          <OnboardingSlide
            key={index}
            title={slide.title}
            subtitle={slide.subtitle}
            icon={slide.icon}
            color={slide.color}
            isActive={index === currentIndex}
          />
        ))}
      </ScrollView>

      {/* Page Indicators */}
      <View style={styles.indicatorContainer}>
        {slides.map((_, index) => {
          const isActive = index === currentIndex;
          const animatedWidth = indicatorAnims[index].interpolate({
            inputRange: [0, 1],
            outputRange: [10, 30],
          });
          const animatedColor = indicatorAnims[index].interpolate({
            inputRange: [0, 1],
            outputRange: ['#ddd', '#c7372c'],
          });

          return (
            <TouchableOpacity key={index} onPress={() => goToSlide(index)}>
              <Animated.View
                style={[
                  styles.indicator,
                  {
                    backgroundColor: animatedColor,
                    width: animatedWidth,
                  },
                ]}
              />
            </TouchableOpacity>
          );
        })}
      </View>

      {/* Navigation Buttons */}
      <View style={styles.buttonContainer}>
        <TouchableOpacity style={styles.skipButton} onPress={handleSkip}>
          <Text style={styles.skipText}>Skip</Text>
        </TouchableOpacity>

        <Animated.View style={{ transform: [{ scale: buttonScaleAnim }] }}>
          <TouchableOpacity style={styles.nextButton} onPress={handleNext}>
            <LinearGradient
              colors={['#c7372c', '#d44636']}
              style={styles.nextButtonGradient}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 1 }}
            >
              <Text style={styles.nextText}>
                {currentIndex === slides.length - 1 ? 'Get Started' : 'Next'}
              </Text>
              <Ionicons
                name={currentIndex === slides.length - 1 ? 'checkmark' : 'arrow-forward'}
                size={20}
                color="white"
                style={styles.buttonIcon}
              />
            </LinearGradient>
          </TouchableOpacity>
        </Animated.View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ffffff',
  },
  scrollView: {
    flex: 1,
  },
  indicatorContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 20,
  },
  indicator: {
    height: 10,
    borderRadius: 5,
    marginHorizontal: 5,
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 30,
    paddingBottom: 40,
  },
  skipButton: {
    paddingVertical: 15,
    paddingHorizontal: 20,
  },
  skipText: {
    fontSize: 16,
    color: '#666',
    fontWeight: '500',
  },
  nextButton: {
    borderRadius: 25,
    shadowColor: '#c7372c',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
  nextButtonGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 15,
    paddingHorizontal: 30,
    borderRadius: 25,
  },
  nextText: {
    fontSize: 16,
    color: 'white',
    fontWeight: 'bold',
    marginRight: 8,
  },
  buttonIcon: {
    marginLeft: 5,
  },
});
