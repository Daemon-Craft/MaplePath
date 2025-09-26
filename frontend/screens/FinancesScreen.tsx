import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

export default function FinancesScreen() {
  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Ionicons name="wallet" size={80} color="#c7372c" />
        <Text style={styles.title}>Finances</Text>
      </View>

      <View style={styles.balanceCard}>
        <Text style={styles.balanceLabel}>Total Balance</Text>
        <Text style={styles.balanceAmount}>$2,450.00 CAD</Text>
        <View style={styles.balanceChange}>
          <Ionicons name="trending-up" size={16} color="#28A745" />
          <Text style={styles.changeText}>+12.5% this month</Text>
        </View>
      </View>

      <View style={styles.actionsContainer}>
        <TouchableOpacity style={styles.actionCard}>
          <Ionicons name="add-circle" size={40} color="#28A745" />
          <Text style={styles.actionTitle}>Add</Text>
          <Text style={styles.actionDescription}>Income</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.actionCard}>
          <Ionicons name="remove-circle" size={40} color="#c7372c" />
          <Text style={styles.actionTitle}>Expenses</Text>
          <Text style={styles.actionDescription}>Outgoing</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.actionCard}>
          <Ionicons name="bar-chart" size={40} color="#c7372c" />
          <Text style={styles.actionTitle}>Reports</Text>
          <Text style={styles.actionDescription}>Analytics</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.actionCard}>
          <Ionicons name="card" size={40} color="#6F42C1" />
          <Text style={styles.actionTitle}>Cards</Text>
          <Text style={styles.actionDescription}>Payment methods</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.recentTransactions}>
        <Text style={styles.sectionTitle}>Recent Transactions</Text>
        <View style={styles.transaction}>
          <Ionicons name="restaurant" size={24} color="#FF6B35" />
          <View style={styles.transactionDetails}>
            <Text style={styles.transactionTitle}>Le Gourmet Restaurant</Text>
            <Text style={styles.transactionDate}>Today, 12:30</Text>
          </View>
          <Text style={styles.transactionAmount}>-$45.00</Text>
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
  balanceCard: {
    backgroundColor: 'white',
    margin: 10,
    padding: 20,
    borderRadius: 12,
    alignItems: 'center',
  },
  balanceLabel: {
    fontSize: 16,
    color: '#666',
  },
  balanceAmount: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#333',
    marginVertical: 5,
  },
  balanceChange: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  changeText: {
    fontSize: 14,
    color: '#28A745',
    marginLeft: 5,
  },
  actionsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    padding: 5,
  },
  actionCard: {
    backgroundColor: 'white',
    width: '47%',
    padding: 15,
    margin: '1.5%',
    borderRadius: 12,
    alignItems: 'center',
  },
  actionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginTop: 8,
    color: '#333',
  },
  actionDescription: {
    fontSize: 12,
    color: '#666',
    marginTop: 2,
  },
  recentTransactions: {
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
  transaction: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 10,
  },
  transactionDetails: {
    flex: 1,
    marginLeft: 15,
  },
  transactionTitle: {
    fontSize: 16,
    fontWeight: '500',
    color: '#333',
  },
  transactionDate: {
    fontSize: 14,
    color: '#666',
    marginTop: 2,
  },
  transactionAmount: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#DC3545',
  },
});
