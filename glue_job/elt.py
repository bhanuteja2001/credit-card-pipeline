import pandas as pd
import s3fs
import pyarrow.parquet as pq
import pyarrow as pa

# Initialize S3 filesystem
s3_filesystem = s3fs.S3FileSystem()

# Constants
BUCKET = 'cashback-bucket'

def read_csv_from_s3(bucket, key):
    """
    Read a CSV file from S3 and return a pandas DataFrame.
    
    :param bucket: S3 bucket name
    :param key: S3 object key (file path)
    :return: pandas DataFrame
    """
    file_path = f's3://{bucket}/{key}'
    return pd.read_csv(file_path)

def write_df_to_parquet_s3(df, bucket, key):
    """
    Write a pandas DataFrame to a Parquet file in S3.
    
    :param df: pandas DataFrame to write
    :param bucket: S3 bucket name
    :param key: S3 object key (file path)
    """
    file_path = f's3://{bucket}/{key}'
    with s3_filesystem.open(file_path, 'wb') as f:
        table = pa.Table.from_pandas(df)
        pq.write_table(table, f, compression='snappy')

def calculate_plu_price(row):
    """
    Calculate PLU price based on transaction details.
    
    :param row: DataFrame row
    :return: Calculated PLU price
    """
    if row['rebate_rate'] == 0.0:
        return row['fiat_amount_rewarded'] / row['plu_amount']
    else:
        return ((abs(row['amount']) / 100) * row['rebate_rate']) / row['plu_amount']


# Load data from S3
rewards_df = read_csv_from_s3(BUCKET, 'staging/rewards.csv')
transactions_df = read_csv_from_s3(BUCKET, 'staging/transactions.csv')

# Merge datasets
joined_df = pd.merge(rewards_df, transactions_df, left_on='reference_id', right_on='transaction_id', how='left')

# Select and rename relevant fields
selected_fields = [
    "reward_id", "transaction_id", "description", "plu_amount", "date",
    "available", "reason", "createdAt", "updatedAt", "rebate_rate",
    "fiat_amount_rewarded", "currency", "reference_type", "reward_type", "amount"
]
selected_fields_df = joined_df[selected_fields]
selected_fields_df = selected_fields_df.rename(columns={
    'createdAt': 'created_at', 
    'updatedAt': 'updated_at',
    'date': 'transaction_date'
})

# Calculate PLU price
selected_fields_df['plu_price'] = selected_fields_df.apply(calculate_plu_price, axis=1)

# Calculate transaction amount
selected_fields_df['transaction_amount'] = selected_fields_df['amount'].apply(lambda x: abs(x) / 100)

# Convert data types
type_conversions = {
    'reward_id': str,
    'transaction_id': str,
    'amount': 'float64',
    'rebate_rate': 'float64',
    'reward_type': str,
    'reference_type': str,
    'available': bool,
    'reason': str,
    'fiat_amount_rewarded': str,
    'currency': str,
    'description': str,
    'plu_amount': 'float64',
    'transaction_amount': 'float64'
}

for column, dtype in type_conversions.items():
    selected_fields_df[column] = selected_fields_df[column].astype(dtype)

# Uncomment these lines if date parsing is needed
# selected_fields_df['created_at'] = pd.to_datetime(selected_fields_df['created_at'])
# selected_fields_df['updated_at'] = pd.to_datetime(selected_fields_df['updated_at'])
# selected_fields_df['transaction_date'] = pd.to_datetime(selected_fields_df['transaction_date'])

# Save processed data
selected_fields_df.to_csv('table.csv', index=False)

# Uncomment this line to write to S3 as Parquet
# write_df_to_parquet_s3(selected_fields_df, BUCKET, 'datawarehouse/transformed_data.parquet')
