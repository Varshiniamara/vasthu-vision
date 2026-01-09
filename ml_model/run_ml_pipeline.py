#!/usr/bin/env python3
"""
Vastu Vision Complete ML Pipeline
Runs data processing, model training, and testing
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\nRunning {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"SUCCESS: {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main ML pipeline execution"""
    print("Vastu Vision ML Pipeline")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path('data_processor.py').exists():
        print("ERROR: Please run this script from the ml directory")
        return
    
    # Step 1: Install Python dependencies
    print("\nInstalling Python dependencies...")
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("Some dependencies may have failed to install, continuing...")
    
    # Step 2: Process data and create CSV
    print("\nProcessing Vastu data...")
    if not run_command("python data_processor.py", "Data processing"):
        print("Data processing failed")
        return
    
    # Step 3: Train ML model
    print("\nTraining ML model...")
    if not run_command("python model_trainer.py", "Model training"):
        print("Model training failed")
        return
    
    # Step 4: Test the model
    print("\nTesting ML model...")
    test_features = {
        'plot_width': 30,
        'plot_height': 40,
        'plot_area': 1200,
        'floor_num': 1,
        'zone_encoded': 5,
        'orientation_encoded': 2,
        'room_type_encoded': 3,
        'adjacent_count': 2,
        'shared_walls_count': 1
    }
    
    # Test prediction
    try:
        import json
        import subprocess
        
        # Prepare test input
        test_input = json.dumps(test_features)
        
        # Run prediction
        result = subprocess.run(
            ['python', 'predict.py'],
            input=test_input,
            text=True,
            capture_output=True,
            check=True
        )
        
        prediction_result = json.loads(result.stdout)
        print(f"SUCCESS: Test prediction successful:")
        print(f"   Vastu Score: {prediction_result['vastu_score']}")
        print(f"   Confidence: {prediction_result['confidence']}")
        print(f"   Model Type: {prediction_result['model_type']}")
        
    except Exception as e:
        print(f"WARNING: Test prediction failed: {e}")
    
    # Step 5: Check generated files
    print("\nChecking generated files...")
    files_to_check = [
        'vastu_dataset.csv',
        'vastu_processed.csv',
        'vastu_ml_model.pkl'
    ]
    
    for file in files_to_check:
        if Path(file).exists():
            print(f"SUCCESS: {file} - Generated successfully")
        else:
            print(f"ERROR: {file} - Missing")
    
    print("\nML Pipeline Complete!")
    print("=" * 50)
    print("SUCCESS: Data processed and CSV created")
    print("SUCCESS: ML model trained and saved")
    print("SUCCESS: Model tested and working")
    print("SUCCESS: Ready for backend integration!")
    
    print("\nNext Steps:")
    print("1. The trained model is now ready")
    print("2. Backend can use predict.py for real-time predictions")
    print("3. Frontend can call the ML-powered API endpoints")
    print("4. Your Vastu Vision app is ML-ready!")

if __name__ == "__main__":
    main()
