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

// Récupération des dimensions de l'écran pour calculer la largeur des slides
const { width, height } = Dimensions.get('window');

interface OnboardingScreenProps {
  // Callback appelé quand l'utilisateur termine l'onboarding (Skip ou Get Started)
  onComplete: () => void;
}

// Configuration des 3 slides d'onboarding
// Chaque slide a un titre, sous-titre, icône et couleur thématique
const slides = [
  {
    title: 'Welcome to Canada!',
    subtitle: 'Start your Canadian journey with confidence. We\'ll help you navigate every step of your new life in Canada.',
    icon: 'flag' as const, // Icône drapeau pour représenter le Canada
    color: '#c7372c', // Rouge du logo MaplePath
  },
  {
    title: 'Save Money with Local Deals',
    subtitle: 'Discover exclusive discounts and deals tailored for newcomers. Save on essentials while you settle in.',
    icon: 'wallet' as const, // Icône portefeuille pour l'aspect financier
    color: '#28A745', // Vert pour symboliser l'économie d'argent
  },
  {
    title: 'Build Your Canadian Career',
    subtitle: 'Access tools and resources to enhance your resume and find opportunities in the Canadian job market.',
    icon: 'briefcase' as const, // Icône porte-documents pour la carrière
    color: '#FF6B35', // Orange pour dynamiser l'aspect professionnel
  },
];

export default function OnboardingScreen({ onComplete }: OnboardingScreenProps) {
  // État pour suivre quel slide est actuellement visible (0, 1, ou 2)
  const [currentIndex, setCurrentIndex] = useState(0);

  // Référence pour contrôler programmatiquement le ScrollView horizontal
  const scrollViewRef = useRef<ScrollView>(null);

  // Animation pour l'effet de "pression" sur le bouton Next/Get Started
  const buttonScaleAnim = useRef(new Animated.Value(1)).current;

  // Tableau d'animations pour chaque indicateur de page (les petits points en bas)
  // Chaque indicateur a sa propre animation pour changer de taille et couleur
  const indicatorAnims = useRef(slides.map((_, index) => new Animated.Value(index === 0 ? 1 : 0))).current;

  // Fonction appelée quand l'utilisateur fait défiler manuellement les slides
  const handleScroll = (event: any) => {
    // Calcul de la position actuelle basée sur le scroll horizontal
    const scrollPosition = event.nativeEvent.contentOffset.x;
    // Conversion en index de slide (0, 1, ou 2)
    const index = Math.round(scrollPosition / width);

    // Mise à jour uniquement si on change vraiment de slide
    if (index !== currentIndex) {
      setCurrentIndex(index);
      animateIndicators(index); // Animation des petits points indicateurs
    }
  };

  // Animation des indicateurs de page (dots) quand on change de slide
  const animateIndicators = (activeIndex: number) => {
    indicatorAnims.forEach((anim, index) => {
      Animated.timing(anim, {
        toValue: index === activeIndex ? 1 : 0, // 1 = actif, 0 = inactif
        duration: 300, // Animation de 300ms
        useNativeDriver: false, // false car on anime width et backgroundColor
      }).start();
    });
  };

  // Navigation programmatique vers un slide spécifique
  // Utilisée quand l'utilisateur clique sur un indicateur
  const goToSlide = (index: number) => {
    // Scroll vers la position calculée (index * largeur de l'écran)
    scrollViewRef.current?.scrollTo({ x: index * width, animated: true });
    setCurrentIndex(index);
    animateIndicators(index);
  };

  // Gestion du bouton "Next" / "Get Started"
  const handleNext = () => {
    if (currentIndex < slides.length - 1) {
      // Si on n'est pas sur le dernier slide, passer au suivant
      goToSlide(currentIndex + 1);
    } else {
      // Sur le dernier slide, terminer l'onboarding avec une animation
      Animated.sequence([
        // Animation de "pression" du bouton
        Animated.timing(buttonScaleAnim, {
          toValue: 0.95, // Réduire légèrement
          duration: 100,
          useNativeDriver: true,
        }),
        Animated.timing(buttonScaleAnim, {
          toValue: 1, // Revenir à la taille normale
          duration: 100,
          useNativeDriver: true,
        }),
      ]).start(() => {
        // Une fois l'animation terminée, appeler le callback
        onComplete();
      });
    }
  };

  // Bouton "Skip" pour passer directement à la fin
  const handleSkip = () => {
    onComplete();
  };

  return (
    <View style={styles.container}>
      {/* ScrollView horizontal avec pagination pour les slides */}
      <ScrollView
        ref={scrollViewRef}
        horizontal // Défilement horizontal
        pagingEnabled // Snap automatique sur chaque page
        showsHorizontalScrollIndicator={false} // Masquer la barre de scroll
        onScroll={handleScroll} // Écouter les événements de scroll
        scrollEventThrottle={16} // Optimisation: 60fps (1000ms/60 ≈ 16ms)
        style={styles.scrollView}
      >
        {slides.map((slide, index) => (
          <OnboardingSlide
            key={index}
            title={slide.title}
            subtitle={slide.subtitle}
            icon={slide.icon}
            color={slide.color}
            // Passer si ce slide est actuellement actif pour déclencher ses animations
            isActive={index === currentIndex}
          />
        ))}
      </ScrollView>

      {/* Indicateurs de page (petits points en bas) */}
      <View style={styles.indicatorContainer}>
        {slides.map((_, index) => {
          // Animation interpolée pour la largeur: 10px (inactif) -> 30px (actif)
          const animatedWidth = indicatorAnims[index].interpolate({
            inputRange: [0, 1],
            outputRange: [10, 30],
          });

          // Animation interpolée pour la couleur: gris -> rouge MaplePath
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

      {/* Barre de navigation avec boutons Skip et Next */}
      <View style={styles.buttonContainer}>
        {/* Bouton Skip - toujours visible, permet de passer l'onboarding */}
        <TouchableOpacity style={styles.skipButton} onPress={handleSkip}>
          <Text style={styles.skipText}>Skip</Text>
        </TouchableOpacity>

        {/* Bouton Next/Get Started avec animation de scale */}
        <Animated.View style={{ transform: [{ scale: buttonScaleAnim }] }}>
          <TouchableOpacity style={styles.nextButton} onPress={handleNext}>
            <LinearGradient
              colors={['#c7372c', '#d44636']} // Dégradé rouge MaplePath
              style={styles.nextButtonGradient}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 1 }}
            >
              {/* Texte et icône changent sur le dernier slide */}
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
