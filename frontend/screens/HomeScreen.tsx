import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

export default function HomeScreen() {
  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Ionicons name="home" size={80} color="#c7372c" />
        <Text style={styles.title}>Home</Text>
        <Text style={styles.subtitle}>Welcome to MaplePath</Text>
      </View>

      <View style={styles.quickActions}>
        <Text style={styles.sectionTitle}>Quick Actions</Text>
        <View style={styles.actionsRow}>
          <TouchableOpacity style={styles.quickActionCard}>
            <Ionicons name="camera" size={30} color="#c7372c" />
            <Text style={styles.quickActionText}>Scanner</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.quickActionCard}>
            <Ionicons name="wallet" size={30} color="#FFC107" />
            <Text style={styles.quickActionText}>Finances</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.quickActionCard}>
            <Ionicons name="briefcase" size={30} color="#FF6B35" />
            <Text style={styles.quickActionText}>Services</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.quickActionCard}>
            <Ionicons name="document-text" size={30} color="#28A745" />
            <Text style={styles.quickActionText}>CV</Text>
          </TouchableOpacity>
        </View>
      </View>

      <View style={styles.recentActivity}>
        <Text style={styles.sectionTitle}>Recent Activity</Text>
        <View style={styles.activityItem}>
          <Ionicons name="checkmark-circle" size={24} color="#28A745" />
          <View style={styles.activityContent}>
            <Text style={styles.activityTitle}>Document scanned</Text>
            <Text style={styles.activityTime}>2 hours ago</Text>
          </View>
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    alignItems: 'center',
    padding: 20,
    backgroundColor: 'white',
    marginBottom: 10,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginTop: 10,
    color: '#333',
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    marginTop: 5,
  },
  quickActions: {
    backgroundColor: 'white',
    margin: 10,
    padding: 20,
    borderRadius: 12,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#333',
  },
  actionsRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  quickActionCard: {
    alignItems: 'center',
    padding: 15,
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
    width: '22%',
  },
  quickActionText: {
    fontSize: 12,
    marginTop: 8,
    textAlign: 'center',
    color: '#333',
  },
  recentActivity: {
    backgroundColor: 'white',
    margin: 10,
    padding: 20,
    borderRadius: 12,
  },
  activityItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  activityContent: {
    marginLeft: 15,
  },
  activityTitle: {
    fontSize: 16,
    fontWeight: '500',
    color: '#333',
  },
  activityTime: {
    fontSize: 14,
    color: '#666',
    marginTop: 2,
  },
});
