#!/usr/bin/env python3
"""
Vastu Vision ML Data Processor
Converts Vastu dataset to CSV format for ML training
"""

import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

class VastuDataProcessor:
    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.model = None
        
    def create_sample_data(self):
        """Create sample Vastu dataset based on the provided structure"""
        data = []
        
        # Sample data based on the table structure you provided
        sample_records = [
            {
                'layout_id': 'VASTU_001DEVTA-MARKING',
                'source_pdf': 'https://www.scribd.com/document/583698234/LAYOUT-PLAN-WITH-VASTU_001DEVTA-MARKING',
                'plot_size_orientation': '30x40 East',
                'floor_number': '0Room',
                'room_name': 'BrahmasthanKitchen',
                'room_zone': 'SW',
                'adjacent_rooms': 'Bathroom',
                'shared_walls': 'Bedroom',
                'vastu_score': 75
            },
            {
                'layout_id': 'VASTU_002Design-and-Plans-PDF',
                'source_pdf': 'https://www.scribd.com/presentation/250817942/Vastu',
                'plot_size_orientation': '35x45 West',
                'floor_number': '1Kitchen',
                'room_name': 'BedroomKitchen',
                'room_zone': 'SE',
                'adjacent_rooms': 'Dining Room',
                'shared_walls': 'Dining Room',
                'vastu_score': 85
            },
            {
                'layout_id': 'VASTU_003Layout-Plan',
                'source_pdf': 'https://www.scribd.com/document/583698235/LAYOUT-PLAN-VASTU_003',
                'plot_size_orientation': '40x50 North',
                'floor_number': '0Bedroom',
                'room_name': 'Living',
                'room_zone': 'NW',
                'adjacent_rooms': 'Bedroom',
                'shared_walls': 'Bedroom',
                'vastu_score': 90
            },
            {
                'layout_id': 'VASTU_004Modern-House',
                'source_pdf': 'https://www.scribd.com/document/583698236/LAYOUT-PLAN-VASTU_004',
                'plot_size_orientation': '25x35 South',
                'floor_number': '1Bedroom',
                'room_name': 'Bathroom,Living',
                'room_zone': 'SW',
                'adjacent_rooms': 'BrahmasthanKitchen,BedroomKitchen',
                'shared_walls': 'Dining Room',
                'vastu_score': 80
            },
            {
                'layout_id': 'VASTU_005Traditional-Home',
                'source_pdf': 'https://www.scribd.com/document/583698237/LAYOUT-PLAN-VASTU_005',
                'plot_size_orientation': '30x40 East',
                'floor_number': '1Bathroom',
                'room_name': 'Room',
                'room_zone': 'SE',
                'adjacent_rooms': 'Dining Room',
                'shared_walls': 'Bedroom',
                'vastu_score': 88
            },
            {
                'layout_id': 'VASTU_006Apartment-Design',
                'source_pdf': 'https://www.scribd.com/document/583698238/LAYOUT-PLAN-VASTU_006',
                'plot_size_orientation': '35x45 West',
                'floor_number': '1Room',
                'room_name': 'Dining',
                'room_zone': 'NW',
                'adjacent_rooms': 'Bedroom',
                'shared_walls': 'Dining Room',
                'vastu_score': 82
            },
            {
                'layout_id': 'VASTU_007Villa-Plan',
                'source_pdf': 'https://www.scribd.com/document/583698239/LAYOUT-PLAN-VASTU_007',
                'plot_size_orientation': '40x50 North',
                'floor_number': '0Room',
                'room_name': 'Bedroom',
                'room_zone': 'SW',
                'adjacent_rooms': 'Bathroom',
                'shared_walls': 'Bedroom',
                'vastu_score': 92
            },
            {
                'layout_id': 'VASTU_008Duplex-House',
                'source_pdf': 'https://www.scribd.com/document/583698240/LAYOUT-PLAN-VASTU_008',
                'plot_size_orientation': '25x35 South',
                'floor_number': '1Kitchen',
                'room_name': 'BrahmasthanKitchen',
                'room_zone': 'SE',
                'adjacent_rooms': 'Dining Room',
                'shared_walls': 'Bedroom',
                'vastu_score': 78
            },
            {
                'layout_id': 'VASTU_009Bungalow-Design',
                'source_pdf': 'https://www.scribd.com/document/583698241/LAYOUT-PLAN-VASTU_009',
                'plot_size_orientation': '30x40 East',
                'floor_number': '1Bedroom',
                'room_name': 'BedroomKitchen',
                'room_zone': 'NW',
                'adjacent_rooms': 'Bedroom',
                'shared_walls': 'Dining Room',
                'vastu_score': 86
            },
            {
                'layout_id': 'VASTU_010Penthouse-Plan',
                'source_pdf': 'https://www.scribd.com/document/583698242/LAYOUT-PLAN-VASTU_010',
                'plot_size_orientation': '35x45 West',
                'floor_number': '1Bathroom',
                'room_name': 'Living',
                'room_zone': 'SW',
                'adjacent_rooms': 'BrahmasthanKitchen,BedroomKitchen',
                'shared_walls': 'Bedroom',
                'vastu_score': 94
            }
        ]
        
        # Generate more synthetic data for better training
        for i in range(11, 101):  # Generate 90 more records
            orientations = ['East', 'West', 'North', 'South', 'Northeast', 'Northwest', 'Southeast', 'Southwest']
            zones = ['SW', 'SE', 'NW', 'NE', 'N', 'S', 'E', 'W']
            room_types = ['Kitchen', 'Bedroom', 'Living', 'Bathroom', 'Dining', 'Study', 'Master Bedroom', 'Guest Room']
            floor_types = ['0Room', '1Kitchen', '1Bedroom', '1Bathroom', '1Room', '2Room']
            
            # Extract plot dimensions
            width = np.random.randint(20, 60)
            height = np.random.randint(25, 70)
            orientation = np.random.choice(orientations)
            
            data.append({
                'layout_id': f'VASTU_{i:03d}Sample-Layout',
                'source_pdf': f'https://www.scribd.com/document/583698{240+i}/LAYOUT-PLAN-VASTU_{i:03d}',
                'plot_size_orientation': f'{width}x{height} {orientation}',
                'floor_number': np.random.choice(floor_types),
                'room_name': np.random.choice(room_types),
                'room_zone': np.random.choice(zones),
                'adjacent_rooms': np.random.choice(['Bathroom', 'Dining Room', 'Bedroom', 'Living Room']),
                'shared_walls': np.random.choice(['Bedroom', 'Dining Room', 'Kitchen', 'Living Room']),
                'vastu_score': np.random.randint(60, 100)  # Score between 60-100
            })
        
        return pd.DataFrame(sample_records + data)
    
    def extract_features(self, df):
        """Extract and engineer features from the raw data"""
        df_processed = df.copy()
        
        # Extract plot dimensions
        df_processed['plot_width'] = df_processed['plot_size_orientation'].str.extract(r'(\d+)x').astype(float)
        df_processed['plot_height'] = df_processed['plot_size_orientation'].str.extract(r'x(\d+)').astype(float)
        df_processed['plot_area'] = df_processed['plot_width'] * df_processed['plot_height']
        
        # Extract orientation
        df_processed['orientation'] = df_processed['plot_size_orientation'].str.extract(r'([A-Za-z]+)$')
        
        # Extract floor number
        df_processed['floor_num'] = df_processed['floor_number'].str.extract(r'(\d+)').fillna(0).astype(int)
        
        # Room type encoding
        df_processed['room_type'] = df_processed['room_name'].str.split(',').str[0]
        
        # Zone encoding (convert to numerical)
        zone_mapping = {
            'N': 0, 'NE': 1, 'E': 2, 'SE': 3, 'S': 4, 'SW': 5, 'W': 6, 'NW': 7
        }
        df_processed['zone_encoded'] = df_processed['room_zone'].map(zone_mapping)
        
        # Orientation encoding
        orientation_mapping = {
            'North': 0, 'Northeast': 1, 'East': 2, 'Southeast': 3,
            'South': 4, 'Southwest': 5, 'West': 6, 'Northwest': 7
        }
        df_processed['orientation_encoded'] = df_processed['orientation'].map(orientation_mapping)
        
        # Room type encoding
        room_type_mapping = {
            'Kitchen': 1, 'Bedroom': 2, 'Living': 3, 'Bathroom': 4,
            'Dining': 5, 'Study': 6, 'Master Bedroom': 7, 'Guest Room': 8,
            'BrahmasthanKitchen': 9, 'BedroomKitchen': 10, 'Room': 11
        }
        df_processed['room_type_encoded'] = df_processed['room_type'].map(room_type_mapping)
        
        # Adjacent rooms count
        df_processed['adjacent_count'] = df_processed['adjacent_rooms'].str.count(',') + 1
        
        # Shared walls count
        df_processed['shared_walls_count'] = df_processed['shared_walls'].str.count(',') + 1
        
        return df_processed
    
    def prepare_training_data(self, df):
        """Prepare data for ML training"""
        # Select features for training
        feature_columns = [
            'plot_width', 'plot_height', 'plot_area', 'floor_num',
            'zone_encoded', 'orientation_encoded', 'room_type_encoded',
            'adjacent_count', 'shared_walls_count'
        ]
        
        X = df[feature_columns].fillna(0)
        y = df['vastu_score']
        
        return X, y
    
    def train_model(self, X, y):
        """Train the ML model"""
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train Random Forest model
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"Model Performance:")
        print(f"Mean Squared Error: {mse:.2f}")
        print(f"R² Score: {r2:.2f}")
        
        return X_test_scaled, y_test, y_pred
    
    def save_model(self, model_path='vastu_model.pkl'):
        """Save the trained model"""
        if self.model is not None:
            joblib.dump({
                'model': self.model,
                'scaler': self.scaler,
                'feature_columns': [
                    'plot_width', 'plot_height', 'plot_area', 'floor_num',
                    'zone_encoded', 'orientation_encoded', 'room_type_encoded',
                    'adjacent_count', 'shared_walls_count'
                ]
            }, model_path)
            print(f"Model saved to {model_path}")
    
    def predict_vastu_score(self, features):
        """Predict Vastu score for new data"""
        if self.model is None:
            raise ValueError("Model not trained yet")
        
        # Prepare features
        features_scaled = self.scaler.transform([features])
        prediction = self.model.predict(features_scaled)[0]
        
        return max(0, min(100, prediction))  # Clamp between 0-100

def main():
    """Main function to process data and train model"""
    print("Vastu Vision ML Data Processor")
    print("=" * 50)
    
    # Initialize processor
    processor = VastuDataProcessor()
    
    # Create sample data
    print("Creating Vastu dataset...")
    df = processor.create_sample_data()
    
    # Save raw data to CSV
    csv_path = 'vastu_dataset.csv'
    df.to_csv(csv_path, index=False)
    print(f"SUCCESS: Dataset saved to {csv_path}")
    print(f"Dataset shape: {df.shape}")
    
    # Process features
    print("\nProcessing features...")
    df_processed = processor.extract_features(df)
    
    # Save processed data
    processed_csv_path = 'vastu_processed.csv'
    df_processed.to_csv(processed_csv_path, index=False)
    print(f"SUCCESS: Processed dataset saved to {processed_csv_path}")
    
    # Prepare training data
    print("\nPreparing ML training data...")
    X, y = processor.prepare_training_data(df_processed)
    print(f"Features shape: {X.shape}")
    print(f"Target shape: {y.shape}")
    
    # Train model
    print("\nTraining ML model...")
    X_test, y_test, y_pred = processor.train_model(X, y)
    
    # Save model
    print("\nSaving trained model...")
    processor.save_model('vastu_model.pkl')
    
    print("\nML Pipeline Complete!")
    print("=" * 50)
    print("SUCCESS: Dataset created and saved")
    print("SUCCESS: Features engineered")
    print("SUCCESS: Model trained and saved")
    print("SUCCESS: Ready for integration!")

if __name__ == "__main__":
    main()
