import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

export default function ServicesScreen() {
  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Ionicons name="briefcase" size={80} color="#c7372c" />
        <Text style={styles.title}>Services</Text>
      </View>

      <View style={styles.servicesContainer}>
        <TouchableOpacity style={styles.serviceCard}>
          <Ionicons name="camera" size={40} color="#c7372c" />
          <Text style={styles.serviceTitle}>OCR Scanner</Text>
          <Text style={styles.serviceDescription}>Digitize your documents</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.serviceCard}>
          <Ionicons name="location" size={40} color="#28A745" />
          <Text style={styles.serviceTitle}>Location Services</Text>
          <Text style={styles.serviceDescription}>Location-based services</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.serviceCard}>
          <Ionicons name="analytics" size={40} color="#DC3545" />
          <Text style={styles.serviceTitle}>Analytics</Text>
          <Text style={styles.serviceDescription}>Reports and analysis</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.serviceCard}>
          <Ionicons name="cloud" size={40} color="#6F42C1" />
          <Text style={styles.serviceTitle}>Cloud Storage</Text>
          <Text style={styles.serviceDescription}>Online storage</Text>
        </TouchableOpacity>
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
  servicesContainer: {
    padding: 10,
  },
  serviceCard: {
    backgroundColor: 'white',
    padding: 20,
    margin: 5,
    borderRadius: 12,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 5,
  },
  serviceTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginTop: 10,
    color: '#333',
  },
  serviceDescription: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
    marginTop: 5,
  },
});
