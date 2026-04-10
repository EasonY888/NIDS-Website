import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
import socket
import struct
import sys

def analyzeContent(file_path):
    # 1. Define the Required Format
    REQUIRED_COLUMNS = [
        'IPV4_SRC_ADDR', 'L4_SRC_PORT', 'IPV4_DST_ADDR', 'L4_DST_PORT', 
        'PROTOCOL', 'L7_PROTO', 'IN_BYTES', 'OUT_BYTES', 'IN_PKTS', 
        'OUT_PKTS', 'TCP_FLAGS', 'FLOW_DURATION_MILLISECONDS'
    ]

    # 2. Load the NEW data
    file_path = 'media/files/cleaned_test_data.csv'  # Change this to your new CSV file path
    new_data = pd.read_csv(file_path)

    # 3. Validate Header Format
    # We convert both to lists and compare them
    if list(new_data.columns) != REQUIRED_COLUMNS:
        print("CRITICAL ERROR: This file does not have the format required.")
        print(f"Expected: {REQUIRED_COLUMNS}")
        print(f"Received: {list(new_data.columns)}")
        sys.exit() # Stop the script immediately
    else:
        print("File format validated successfully.")

    # 4. Preprocessing IP Addresses
    def ip_to_int(ip):
        try:
            return struct.unpack("!I", socket.inet_aton(ip))[0]
        except:
            return 0

    df_processed = new_data.copy()
    df_processed['IPV4_SRC_ADDR'] = df_processed['IPV4_SRC_ADDR'].apply(ip_to_int)
    df_processed['IPV4_DST_ADDR'] = df_processed['IPV4_DST_ADDR'].apply(ip_to_int)

    # 5. Label Mapping 
    class_names = ['Analysis', 'Backdoor', 'Benign', 'DoS', 'Exploits', 'Fuzzers', 'Generic', 'Reconnaissance', 'Shellcode', 'Worms']

    # 6. Feature Selection
    # Now we safely drop these because we verified they existed in step 3
    X_new = df_processed.drop(columns=['Label', 'Attack'], errors='ignore')

    # 7. Load the Saved Model
    model = xgb.XGBClassifier()
    model.load_model('network_model.json')
    print("Model loaded successfully.")

    # 8. Run Inference
    print("Running inference...")
    y_pred = model.predict(X_new)
    y_proba = model.predict_proba(X_new)

    # 9. Format and Show Results
    results = []
    for i in range(len(X_new)):
        predicted_label = class_names[y_pred[i]]
        probs = {class_names[j]: round(float(y_proba[i][j]), 4) for j in range(len(class_names))}
        
        results.append({
            'Source_IP': new_data.iloc[i]['IPV4_SRC_ADDR'],
            'Prediction': predicted_label,
            'Confidence': np.max(y_proba[i]),
            'Full_Probabilities': probs
        })

    results_df = pd.DataFrame(results)

    # print("\n--- Inference Results ---")
    # print(results_df[['Source_IP', 'Prediction', 'Confidence']].head(10))

    # print(f"\nDetailed breakdown for first row:")
    # for attack, p in results_df.iloc[0]['Full_Probabilities'].items():
    #     print(f"  {attack}: {p*100:.2f}%")

    # 10. Generate the Summary String
    counts = results_df['Prediction'].value_counts()
    counts_string = counts.to_string()

    # WRAP IT HERE: 
    # The \n is a newline, and the ``` creates the "code block" look
    final_output = f"### TOTAL ATTACK SUMMARY\n```text\n{counts_string}\n```"

    return final_output
