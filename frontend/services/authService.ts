import apiClient from './api';
import AsyncStorage from '@react-native-async-storage/async-storage';

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  created_at: string;
}

class AuthService {
  /**
   * Connexion avec email et mot de passe
   */
  async login(email: string, password: string): Promise<AuthResponse> {
    try {
      const response = await apiClient.post<AuthResponse>('/auth/login', {
        email,
        password,
      });

      // Sauvegarder le token
      if (response.data.access_token) {
        await AsyncStorage.setItem('authToken', response.data.access_token);
      }

      return response.data;
    } catch (error: any) {
      if (error.response?.data?.detail) {
        throw new Error(error.response.data.detail);
      }
      throw new Error('Erreur de connexion. Veuillez réessayer.');
    }
  }

  /**
   * Inscription avec email et mot de passe
   */
  async register(data: RegisterRequest): Promise<User> {
    try {
      const response = await apiClient.post<User>('/auth/register', data);
      return response.data;
    } catch (error: any) {
      if (error.response?.data?.detail) {
        throw new Error(error.response.data.detail);
      }
      throw new Error('Erreur lors de l\'inscription. Veuillez réessayer.');
    }
  }

  /**
   * Connexion avec Google
   */
  async googleAuth(firebaseToken: string): Promise<AuthResponse> {
    try {
      const response = await apiClient.post<AuthResponse>('/auth/google-auth', {
        firebase_token: firebaseToken,
      });

      // Sauvegarder le token
      if (response.data.access_token) {
        await AsyncStorage.setItem('authToken', response.data.access_token);
      }

      return response.data;
    } catch (error: any) {
      if (error.response?.data?.detail) {
        throw new Error(error.response.data.detail);
      }
      throw new Error('Erreur d\'authentification Google. Veuillez réessayer.');
    }
  }

  /**
   * Récupérer le profil utilisateur actuel
   */
  async getCurrentUser(): Promise<User> {
    try {
      const token = await AsyncStorage.getItem('authToken');
      if (!token) {
        throw new Error('Non authentifié');
      }

      const response = await apiClient.get<User>('/auth/me', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      return response.data;
    } catch (error: any) {
      if (error.response?.data?.detail) {
        throw new Error(error.response.data.detail);
      }
      throw new Error('Erreur lors de la récupération du profil.');
    }
  }

  /**
   * Déconnexion
   */
  async logout(): Promise<void> {
    await AsyncStorage.removeItem('authToken');
  }

  /**
   * Vérifier si l'utilisateur est authentifié
   */
  async isAuthenticated(): Promise<boolean> {
    const token = await AsyncStorage.getItem('authToken');
    return !!token;
  }

  /**
   * Récupérer le token d'authentification
   */
  async getToken(): Promise<string | null> {
    return await AsyncStorage.getItem('authToken');
  }
}

export default new AuthService();