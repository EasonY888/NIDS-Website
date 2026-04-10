import pandas as pd

# 1. Load the data
df = pd.read_csv('base/utils/NF-UNSW-NB15.csv', low_memory=False)

# 2. Columns we want in the FINAL output (The "Expected" list)
expected_columns = [
    'IPV4_SRC_ADDR', 'L4_SRC_PORT', 'IPV4_DST_ADDR', 'L4_DST_PORT', 
    'PROTOCOL', 'L7_PROTO', 'IN_BYTES', 'OUT_BYTES', 
    'IN_PKTS', 'OUT_PKTS', 'TCP_FLAGS', 
    'FLOW_DURATION_MILLISECONDS'
]

# 3. Identify Benign vs Attacks (Using the 'Attack' column before we drop it)
# Adjust 'Benign' or 0 depending on your actual CSV values
is_benign = (df['Attack'] == 'Benign') | (df['Attack'] == 0) | (df['Attack'] == '0')

df_benign = df[is_benign]
df_attacks = df[~is_benign]

# 4. Reduce Benign rows (keep 10% of benign, 100% of attacks)
df_benign_reduced = df_benign.sample(frac=0.1, random_state=42)

# 5. Combine and filter down to ONLY the Expected columns
final_df = pd.concat([df_benign_reduced, df_attacks])
final_df = final_df[expected_columns]  # This removes the 'Attack' column

# 6. Shuffle
final_df = final_df.sample(frac=1, random_state=42)

# 7. Save
final_df.to_csv('media/files/cleaned_test_data.csv', index=False)

print("File created successfully with exactly 12 columns.")
print(f"Final Column Count: {len(final_df.columns)}")