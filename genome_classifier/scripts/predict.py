# scripts/predict.py

import pandas as pd
import pickle
import numpy as np
import sys
def make_predictions(features_file, completeness_file, output_file):

    # Load completeness information
    try:
        completeness_df = pd.read_csv(completeness_file)
        completeness_df.set_index('Genome', inplace=True)
    except FileNotFoundError:
        raise FileNotFoundError("Completeness file not found.")

    # Load features
    try:
        features = pd.read_csv(features_file, index_col=0)
    except FileNotFoundError:
        raise FileNotFoundError("Features file not found.")

    # Merge features with completeness information
    features = features.join(completeness_df, how='left')

    # Check for any genomes without completeness info
    missing_completeness = features['Completeness'].isnull()
    if missing_completeness.any():
        missing_genomes = features.index[missing_completeness].tolist()
        print(f"{Fore.RED}Warning: Missing completeness information for genomes: {missing_genomes}")
        features = features[~missing_completeness]


    # Define the feature columns to use
    feature_columns = [
        'n_marker_spm_median',
        'p_marker_spm_median',
        'n_marker_num',
        'p_marker_num',
        'sigmoid(n_marker_spm_total-p_marker_spm_total)',
        'gene_num'
    ]

    # Prepare features DataFrame
    X = features[feature_columns]

    # Load models
    with open('genome_classifier/data/pre_trained_model_dt.pkl', 'rb') as model_file:
        model_dt = pickle.load(model_file)

    with open('genome_classifier/data/pre_trained_model_xgb.pkl', 'rb') as model_file:
        model_xgb = pickle.load(model_file)

    # Initialize results DataFrame
    results = pd.DataFrame(index=features.index)
    results['Completeness'] = features['Completeness']
    results['Model Used'] = ''
    results['Prediction'] = ''
    results['Probability'] = ''

    # Loop over each genome
    for genome in features.index:
        completeness = features.loc[genome, 'Completeness']
        feature_vector = X.loc[genome].to_frame().T  # Ensure feature names are included

        # Choose model based on completeness
        if completeness < 33.0:
            model = model_dt
            model_name = 'Decision Tree'
        else:
            model = model_xgb
            model_name = 'XGBoost'

        # Make prediction
        try:
            prediction = model.predict(feature_vector)[0]
            probability = model.predict_proba(feature_vector)[0, 1]
        except Exception as e:
            print(f"{Fore.RED}Error making prediction for genome {genome}: {e}{Style.RESET_ALL}")
            prediction = None
            probability = None

        # Store results
        results.loc[genome, 'Model Used'] = model_name
        results.loc[genome, 'Prediction'] = prediction
        results.loc[genome, 'Probability'] = probability

    # Save predictions
    results.to_csv(output_file)
    print(f"Predictions saved to {output_file}")
