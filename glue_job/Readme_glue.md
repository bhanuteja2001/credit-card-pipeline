# Glue Jobs for Cashback Pipeline

This folder contains the AWS Glue job scripts used in the Cashback Pipeline project.

## Overview

The Glue jobs in this folder are responsible for ETL (Extract, Transform, Load) processes in the Cashback Pipeline. They process data from various sources, transform it, and prepare it for analysis in the data warehouse.

## Files

- `glue_script.py`: The main Glue job script for data transformation.
- `elt.py`: An alternative ELT (Extract, Load, Transform) script, possibly for different data processing needs.

## glue_script.py

This script is the primary Glue job used in the pipeline. It performs the following tasks:

- Reads data from S3 buckets (rewards and transactions data)
- Joins the datasets
- Performs various transformations including:
  - Calculating transaction amounts
  - Computing PLU prices
  - Renaming and selecting relevant fields
- Converts data types for consistency
- Writes the processed data to a Parquet file in S3

## elt.py

This script provides an alternative ELT approach:

- Reads CSV files from S3
- Performs data joining and transformation
- Calculates PLU prices and transaction amounts
- Converts data types
- Outputs the processed data to a CSV file (with an option to write to Parquet)

## Usage

These scripts are intended to be run as AWS Glue jobs. They are typically triggered by the Step Functions state machine defined in the infrastructure setup.

To modify or update these jobs:

1. Make changes to the relevant Python script.
2. Update the S3 object in the Glue job definition (in `../infra/glue.tf`).
3. Redeploy the infrastructure using Terraform.

## Dependencies

- `pyspark`: For distributed data processing
- `awsglue`: AWS Glue libraries
- Other standard Python libraries like `pandas`

## Important Notes

- Ensure that the IAM roles associated with these Glue jobs have the necessary permissions to read from and write to the specified S3 buckets.
- The scripts assume specific data formats and column names. Ensure any changes to input data structures are reflected in these scripts.
- Performance tuning may be necessary for large datasets. Consider adjusting Glue job parameters in the Terraform configuration as needed.

## Customization

To customize the Glue jobs:

1. Modify the Python scripts as needed.
2. Update the Glue job definitions in the Terraform files if there are changes to job parameters or resource requirements.
3. Ensure any new dependencies are properly handled in the Glue job environment.

For any questions or issues, please contact the data engineering team.