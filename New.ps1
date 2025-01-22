import pandas as pd
from datetime import datetime, timedelta

def load_transaction_data(file_path):
    return pd.read_excel(file_path)

def detect_fraudulent_transactions(data):
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    fraud_transactions = []
    for index, row in data.iterrows():
        customer_id = row['Customer_ID']
        transaction_time = row['Timestamp']
        amount = row['Amount']
        location = row['Location']
        if amount > 50000:
            fraud_transactions.append(row)
            continue
        recent_transactions = data[
            (data['Customer_ID'] == customer_id) &
            (data['Timestamp'] >= transaction_time - timedelta(minutes=5)) &
            (data['Timestamp'] <= transaction_time)
        ]
        if len(recent_transactions) > 3:
            fraud_transactions.append(row)
            continue
        daily_transactions = data[
            (data['Customer_ID'] == customer_id) &
            (data['Timestamp'].dt.date == transaction_time.date())
        ]
        if len(daily_transactions) > 10:
            fraud_transactions.append(row)
            continue
        prev_transaction = data[
            (data['Customer_ID'] == customer_id) &
            (data['Timestamp'] < transaction_time)
        ].sort_values(by='Timestamp').tail(1)
        if not prev_transaction.empty and prev_transaction.iloc[0]['Location'] != location:
            fraud_transactions.append(row)
    return pd.DataFrame(fraud_transactions).drop_duplicates()

def save_fraudulent_transactions(fraud_data, output_file):
    fraud_data.to_excel(output_file, index=False)
    print(f"Fraudulent transactions saved to {output_file}")

def main():
    input_file = input("Enter the path to the input Excel file: ")
    output_file = input("Enter the path to save the fraudulent transactions: ")
    data = load_transaction_data(input_file)
    fraud_data = detect_fraudulent_transactions(data)
    if fraud_data.empty:
        print("No fraudulent transactions detected.")
    else:
        print(f"Detected {len(fraud_data)} fraudulent transactions.")
        save_fraudulent_transactions(fraud_data, output_file)

if __name__ == "__main__":
    main()
