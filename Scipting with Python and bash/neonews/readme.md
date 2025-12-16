
# NeoNews CLI

![NeoNews Banner](https://user-images.githubusercontent.com/1287098/147876189-3f434a42-7c3e-4d8a-9883-7a4b640093d1.png)

A command-line interface for fetching the latest news from various countries and topics, and archiving them to AWS.

## Overview

This application allows users to select a country and a news topic. It then fetches relevant news articles from the [Newsdata.io](https://newsdata.io/) API and country information from [REST Countries](https://restcountries.com/). The fetched articles are then saved to an AWS DynamoDB table, and the full JSON content is stored in an S3 bucket.

The CLI provides an interactive experience using `rich` for beautiful terminal output and `questionary` for user prompts.

## File Structure

Here is a breakdown of the project's file structure and the purpose of each file:

- **`main.py`**: The main entry point for the application. It handles user interaction, fetches data, and orchestrates the saving of articles to AWS.

- **`Makefile`**: Contains a set of commands to streamline common development tasks like installation, running the app, cleaning the workspace, and managing AWS resources.

- **`requirements.txt`**: Lists all the Python dependencies required to run the project.

- **`src/`**: This directory contains the core logic of the application, separated into different modules:

    - **`api.py`**: Defines the `ApiClient` class, which is responsible for making HTTP requests to external APIs (`restcountries.com` and `newsdata.io`) to fetch country details and news articles.

    - **`config.py`**: Manages the application's configuration. It loads environment variables from a `.env` file, such as API keys and AWS resource names.

    - **`aws_handler.py`**: Contains the `AWSClient` class, which encapsulates all interactions with AWS services (DynamoDB and S3). This includes creating resources, saving articles, and deleting resources.

    - **`db_ops.py`**: A helper script that provides command-line functions to initialize or destroy the AWS resources used by the application. This script is called by the `Makefile`.

- **`.env.example`**: An example file showing the required environment variables. You should create your own `.env` file based on this example.

## Prerequisites

Before you can run this application, you will need the following:

- Python 3.7+
- An AWS account with credentials configured on your local machine.
- API key from [Newsdata.io](https://newsdata.io/).

## Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/neonews.git
    cd neonews
    ```

2.  **Create a `.env` file:**
    Create a file named `.env` in the root of the project and add the following environment variables. Replace the placeholder values with your actual credentials.
    ```
    NEWSDATA_API_KEY=your_newsdata_api_key
    AWS_REGION=your_aws_region
    DYNAMODB_TABLE=your_dynamodb_table_name
    S3_BUCKET_NAME=your_s3_bucket_name
    ```

3.  **Install the dependencies:**
    Use the `make install` command to create a virtual environment and install the required packages.
    ```bash
    make install
    ```

4.  **Initialize AWS Resources:**
    Run the `make init-cloud` command to create the DynamoDB table and S3 bucket in your AWS account.
    ```bash
    make init-cloud
    ```

## Usage

To run the application, use the `make run` command:

```bash
make run
```

This will launch the interactive CLI. You will be prompted to select a country, a news topic, and a language. The application will then fetch the news and save it to your AWS resources.

## Makefile Commands

The `Makefile` provides several commands to help you manage the application:

- **`make help`**: Displays a list of all available commands.

- **`make install`**: Sets up the development environment by creating a Python virtual environment and installing all the dependencies from `requirements.txt`.

- **`make run`**: Starts the NeoNews CLI application.

- **`make clean`**: Cleans the workspace by removing the virtual environment and any `__pycache__` directories.

- **`make init-cloud`**: Provisions the necessary AWS resources (DynamoDB table and S3 bucket) as defined in your `.env` file.

- **`make nuke-db`**: **(DANGEROUS)** This command will delete all data from the DynamoDB table and empty the S3 bucket. You will be prompted for confirmation before the operation proceeds.

Enjoy using NeoNews!
