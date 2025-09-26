import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

export default function CVScreen() {
  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Ionicons name="document-text" size={80} color="#c7372c" />
        <Text style={styles.title}>Curriculum Vitae</Text>
      </View>
      <View style={styles.content}>
        <Text style={styles.sectionTitle}>My CV</Text>
        <Text style={styles.text}>View and manage your curriculum vitae</Text>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Work Experience</Text>
          <Text style={styles.text}>Add your work experiences</Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Education</Text>
          <Text style={styles.text}>Your degrees and education</Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Skills</Text>
          <Text style={styles.text}>List your technical skills</Text>
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
  content: {
    backgroundColor: 'white',
    padding: 20,
    margin: 10,
    borderRadius: 8,
  },
  section: {
    marginTop: 20,
    paddingTop: 20,
    borderTopWidth: 1,
    borderTopColor: '#eee',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#333',
  },
  text: {
    fontSize: 16,
    color: '#666',
    lineHeight: 24,
  },
});
