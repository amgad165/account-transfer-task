# Account Transfer Project

This project is a Django-based web application for managing accounts, transferring money between accounts, and importing account data from CSV or Excel files. The application is dockerized for easy setup and deployment.

## Features

- **Import Accounts**: Import account data from CSV or Excel files.
- **View Accounts**: Display a list of all accounts.
- **Send Money**: Transfer money from one account to another.
- **Search Accounts**: Search for accounts by ID or name.

## Setup and Installation

### Prerequisites

- Docker
- Docker Compose

### Steps

1. **Clone the repository**:
    ```bash
    git clone https://github.com/amgad165/account-transfer-task.git

    ```

2. **Create the Docker image and start the containers**:
    ```bash
    docker-compose up --build
    ```

    This will build the Docker image and start the Django application on port 8000.

3. **Access the application**:

    Open your web browser and navigate to `http://127.0.0.1:8000/`.

## Usage

### Import Accounts

1. Navigate to the "Import Accounts" page.
2. Upload a CSV or Excel file containing account data with the following columns:
    - `ID`: The unique identifier for the account.
    - `Name`: The name of the account holder.
    - `Balance`: The initial balance of the account.

### View Accounts

Navigate to the "Accounts" page to see a list of all accounts.

### Send Money

1. click on "Send Money" button in Accounts page.
2. Select the sender and receiver accounts.
3. Enter the amount to transfer.
4. Click "Send Money" to complete the transaction.

### Search Accounts

Use the search functionality on the "Accounts" page to find accounts by ID or name.


## Models

- **Account**:
  - `id`: CharField (primary key)
  - `name`: CharField
  - `balance`: DecimalField

## Views

- **index**: Renders the home page.
- **account_transfer**: Renders the account transfer page with a list of accounts.
- **import_accounts**: Handles account import functionality.
- **send_money**: Handles money transfer between accounts.

## Unit Tests

Unit tests are provided to ensure the functionality of models and views. To run the tests, use the following command:

```bash
docker-compose exec django python manage.py test   
