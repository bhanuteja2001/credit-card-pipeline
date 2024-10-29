# Credit Card Rewards Pipeline

### Introduction

Credit card issuers frequently offer cashback incentives as a key selling point for their products. This initiative aims to create a streamlined and dependable data infrastructure for examining information related to credit card cashback rewards. The system is designed to gather, refine, and archive data obtained from payment cards through an API interface. Its primary objective is to uncover trends in spending habits and reward accumulation, providing valuable insights for both cardholders and issuers alike.



## Architecture
![img.png](static/img.png)

The pipeline consists of the following components:
1. Data extraction from Plutus API
2. Data storage in AWS S3
3. Data transformation using AWS Glue and Lambda
4. Data loading into AWS Redshift
5. Data visualization using Google Data Studio Dashboard

The entire process is orchestrated using AWS Step Functions and deployed using Terraform and Docker.

## Key Components

- `api.py`: Handles authentication and data retrieval from the Plutus API
- `pull_data_glue_job_lambda.py`: Lambda function for pulling data and triggering Glue jobs
- `glue_script.py`: Glue job for data transformation
- `load_to_redshift_lambda.py`: Lambda function for loading data into Redshift
- `infra/`: Terraform configurations for AWS infrastructure
- Dockerfiles: For containerizing Lambda functions


## Data Flow

1. The Plutus API is queried for transaction and reward data
2. Raw data is stored in S3 as CSV files
3. Glue jobs process and transform the data
4. Transformed data is stored back in S3 as Parquet files
5. A Glue crawler updates the data catalog
6. Data is loaded into Redshift for analysis
7. Looker Studio connects to Redshift for visualization



### Dashboard
A comprehensive dashboard is available in Looker Studio, providing insights into spending patterns and reward accumulation.

![dashboard.png](static/dashboard.png)


## Architecture Overview

### Workflow Orchestration
![step_function.png](static/step_function.png)
- step_functions are used to orchestrate the workflow of the data pipeline.

### Data Transformation
- Two datasets are pulled from the Open Banking API. Rewards and Transactions data. 
A left join is performed on the two datasets matching each reward with its transaction. 
This is because rewards are missing key information such as the merchant name and transaction amount.
- Performed cleaning, updated schema and created new variables such as `reward_amount` and `plu_price` for analysis downstream.


### Data Warehouse

Redshift is used as the data warehouse for the project.

![redshift.png](static/redshift.png)



## Setup

### Prerequisites

- AWS Account
- AWS CLI configured with appropriate credentials
- Docker
- Terraform (version ~> 1.7.5)
- Python 3.12
- LookerStudio

### Deployment

1. Clone the repository
2. Update the `Makefile` with your AWS Account ID and ECR region
3. Run `make terraform/plan` to preview the infrastructure changes
4. Run `make terraform/apply` to create the AWS resources
5. Use the AWS Console to run the Step Functions state machine
6. Get the Redshift endpoint and credentials from the AWS Console and sign into Looker to create a connection to Redshift



### Tear Down
`make terraform/plan-destroy` then `make terraform/destroy`
