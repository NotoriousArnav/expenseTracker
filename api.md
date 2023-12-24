# Expense Tracker API Documentation

## Overview

Expense Tracker is a simple Flask-based web application that allows users to track and manage their expenses. This API documentation provides information on the available endpoints and their functionalities.

### Base URL

The base URL for the API is `http://localhost:5000/` when running the application locally.

## Endpoints

### 1. Get All Expenses

#### Endpoint

- **URL**: `/expenses`
- **Method**: `GET`
- **Description**: Get a list of all expenses.

#### Request

- **Parameters**: None

#### Response

- **Status Code**: 200 OK
- **Content-Type**: JSON
- **Body Example**:

```json
[
  {
    "currency": "INR",
    "id": "e8b5e9bd-546d-4b61-8fe5-5bd416da7e21",
    "note": "Dinner",
    "amount": 30.0,
    "timestamp": 1677834482
  },
  {
    "currency": "INR",
    "id": "c0f4657f-2a46-46b5-b163-4ac5e372ef6f",
    "note": "Groceries",
    "amount": 50.0,
    "timestamp": 1677834571
  }
  // ... other expenses
]
```

### 2. Get Expense Details

#### Endpoint

- **URL**: `/expenses/<expense_id>`
- **Method**: `GET`
- **Description**: Get details of a specific expense.

#### Request

- **Parameters**:
  - `expense_id` (path parameter): ID of the expense.

#### Response

- **Status Code**:
  - 200 OK: Successful request.
  - 404 Not Found: Expense with the specified ID not found.

- **Content-Type**: JSON
- **Body Example**:

```json
{
  "currency": "INR",
  "id": "e8b5e9bd-546d-4b61-8fe5-5bd416da7e21",
  "note": "Dinner",
  "amount": 30.0,
  "timestamp": 1677834482
}
```

### 3. Add Expense

#### Endpoint

- **URL**: `/expenses`
- **Method**: `POST`
- **Description**: Add a new expense.

#### Request

- **Parameters**:
  - `note` (form parameter): Note/description of the expense.
  - `amount` (form parameter): Amount spent.
  - `date` (form parameter): Date and time of the expense in the format `YYYY-MM-DDTHH:mm`.

#### Response

- **Status Code**:
  - 302 Found: Successful creation, redirects to the home page.
  - 400 Bad Request: Invalid request parameters.

### Error Handling

In case of an error, the API will return a JSON response with an `"error"` field and an appropriate status code.

- **Status Code**: 404 Not Found
- **Content-Type**: JSON
- **Body Example**:

```json
{
  "error": "Expense not found"
}
```

## Example Usage

### Curl Example

1. Get all expenses:

```bash
curl http://localhost:5000/expenses
```

2. Get expense details:

```bash
curl http://localhost:5000/expenses/e8b5e9bd-546d-4b61-8fe5-5bd416da7e21
```

3. Add a new expense:

```bash
curl -X POST -d "note=Dinner&amount=30&date=2023-01-15T19:30" http://localhost:5000/expenses
```

## Conclusion

The Expense Tracker API provides simple and straightforward endpoints for managing expenses. Feel free to use the provided endpoints according to your requirements. If you encounter any issues or have further questions, please refer to the API documentation or contact the developer.

*Author: Arnav Ghosh*