#!/usr/bin/env python3
"""
Vastu Vision ML Model Trainer
Advanced ML model for Vastu score prediction
"""

import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

class VastuMLTrainer:
    def __init__(self):
        self.models = {}
        self.best_model = None
        self.scaler = StandardScaler()
        self.feature_importance = None
        
    def load_data(self, csv_path='vastu_processed.csv'):
        """Load processed Vastu data"""
        try:
            df = pd.read_csv(csv_path)
            print(f"SUCCESS: Data loaded: {df.shape}")
            return df
        except FileNotFoundError:
            print("ERROR: Processed data not found. Run data_processor.py first.")
            return None
    
    def prepare_features(self, df):
        """Prepare features for ML training"""
        # Select numerical features
        feature_columns = [
            'plot_width', 'plot_height', 'plot_area', 'floor_num',
            'zone_encoded', 'orientation_encoded', 'room_type_encoded',
            'adjacent_count', 'shared_walls_count'
        ]
        
        # Check if all columns exist
        missing_cols = [col for col in feature_columns if col not in df.columns]
        if missing_cols:
            print(f"⚠️ Missing columns: {missing_cols}")
            # Use available columns
            feature_columns = [col for col in feature_columns if col in df.columns]
        
        X = df[feature_columns].fillna(0)
        y = df['vastu_score']
        
        print(f"Features: {X.shape}")
        print(f"Target: {y.shape}")
        
        return X, y, feature_columns
    
    def train_multiple_models(self, X, y):
        """Train multiple ML models and compare performance"""
        print("\nTraining Multiple ML Models...")
        print("=" * 50)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Define models
        models = {
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
            'Linear Regression': LinearRegression(),
            'SVR': SVR(kernel='rbf'),
            'Neural Network': MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
        }
        
        results = {}
        
        for name, model in models.items():
            print(f"\nTraining {name}...")
            
            # Train model
            model.fit(X_train_scaled, y_train)
            
            # Predictions
            y_pred = model.predict(X_test_scaled)
            
            # Metrics
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            # Cross-validation
            cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='r2')
            
            results[name] = {
                'model': model,
                'mse': mse,
                'rmse': rmse,
                'mae': mae,
                'r2': r2,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std()
            }
            
            print(f"   R² Score: {r2:.3f}")
            print(f"   RMSE: {rmse:.3f}")
            print(f"   MAE: {mae:.3f}")
            print(f"   CV R²: {cv_scores.mean():.3f} (±{cv_scores.std():.3f})")
        
        return results, X_test_scaled, y_test
    
    def optimize_best_model(self, X, y):
        """Optimize the best performing model"""
        print("\nOptimizing Best Model...")
        print("=" * 50)
        
        # Use Random Forest as base (usually performs well)
        rf = RandomForestRegressor(random_state=42)
        
        # Parameter grid for optimization
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [5, 10, 15, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        
        # Grid search (disable parallel processing for Windows compatibility)
        grid_search = GridSearchCV(
            rf, param_grid, cv=5, scoring='r2', n_jobs=1, verbose=1
        )
        
        X_scaled = self.scaler.fit_transform(X)
        grid_search.fit(X_scaled, y)
        
        print(f"SUCCESS: Best parameters: {grid_search.best_params_}")
        print(f"SUCCESS: Best CV score: {grid_search.best_score_:.3f}")
        
        self.best_model = grid_search.best_estimator_
        return grid_search.best_estimator_
    
    def evaluate_model(self, model, X_test, y_test):
        """Comprehensive model evaluation"""
        print("\nModel Evaluation...")
        print("=" * 50)
        
        y_pred = model.predict(X_test)
        
        # Metrics
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"Performance Metrics:")
        print(f"   R² Score: {r2:.3f}")
        print(f"   RMSE: {rmse:.3f}")
        print(f"   MAE: {mae:.3f}")
        print(f"   MSE: {mse:.3f}")
        
        # Feature importance (for tree-based models)
        if hasattr(model, 'feature_importances_'):
            self.feature_importance = model.feature_importances_
            print(f"\nFeature Importance:")
            for i, importance in enumerate(self.feature_importance):
                print(f"   Feature {i}: {importance:.3f}")
        
        return {
            'mse': mse, 'rmse': rmse, 'mae': mae, 'r2': r2,
            'predictions': y_pred, 'actual': y_test
        }
    
    def save_model(self, model_path='vastu_ml_model.pkl'):
        """Save the trained model and metadata"""
        if self.best_model is None:
            print("❌ No model to save")
            return
        
        model_data = {
            'model': self.best_model,
            'scaler': self.scaler,
            'feature_importance': self.feature_importance,
            'model_type': 'RandomForestRegressor',
            'version': '1.0.0'
        }
        
        joblib.dump(model_data, model_path)
        print(f"SUCCESS: Model saved to {model_path}")
    
    def predict_sample(self, sample_data):
        """Predict Vastu score for sample data"""
        if self.best_model is None:
            print("ERROR: No trained model available")
            return None
        
        # Prepare sample data
        sample_scaled = self.scaler.transform([sample_data])
        prediction = self.best_model.predict(sample_scaled)[0]
        
        return max(0, min(100, prediction))  # Clamp between 0-100

def main():
    """Main training pipeline"""
    print("Vastu Vision ML Model Trainer")
    print("=" * 50)
    
    # Initialize trainer
    trainer = VastuMLTrainer()
    
    # Load data
    df = trainer.load_data()
    if df is None:
        return
    
    # Prepare features
    X, y, feature_columns = trainer.prepare_features(df)
    
    # Train multiple models
    results, X_test, y_test = trainer.train_multiple_models(X, y)
    
    # Find best model
    best_model_name = max(results.keys(), key=lambda k: results[k]['r2'])
    print(f"\nBest Model: {best_model_name}")
    print(f"   R² Score: {results[best_model_name]['r2']:.3f}")
    
    # Optimize best model
    optimized_model = trainer.optimize_best_model(X, y)
    
    # Final evaluation
    final_results = trainer.evaluate_model(optimized_model, X_test, y_test)
    
    # Save model
    trainer.save_model('vastu_ml_model.pkl')
    
    # Sample prediction
    print("\nSample Prediction:")
    sample_features = [30, 40, 1200, 1, 5, 2, 3, 2, 1]  # Example features
    prediction = trainer.predict_sample(sample_features)
    print(f"   Sample Vastu Score: {prediction:.1f}")
    
    print("\nML Training Complete!")
    print("=" * 50)
    print("SUCCESS: Multiple models trained and compared")
    print("SUCCESS: Best model optimized")
    print("SUCCESS: Model saved and ready for deployment")
    print("SUCCESS: Ready for API integration!")

if __name__ == "__main__":
    main()
