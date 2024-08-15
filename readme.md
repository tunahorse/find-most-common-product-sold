# Documentation for Odoo Sales Data Fetching Script

## Overview

This script is designed to connect to an Odoo server and retrieve product IDs from sales orders that have been completed within the last 90 days. It uses the `xmlrpc.client` module to communicate with the Odoo server via XML-RPC, allowing for secure and flexible data retrieval. The script is particularly useful for businesses or developers needing to analyze recent sales data.

## Prerequisites

- **Python 3.x**: Ensure that Python 3.x is installed on your system.
- **Odoo Server**: Access to an Odoo server with the appropriate credentials.
- **Python Libraries**: The script uses `xmlrpc.client`, `ssl`, and `datetime` modules, which are part of the Python standard library.

## Configuration

### Odoo Server Configuration

- **DB**: The name of the Odoo database you want to connect to.
- **URL**: The URL of the Odoo server, including the port number.
- **USERNAME**: The username of the account used to authenticate with the Odoo server.
- **PASSWORD**: The password associated with the provided username.

Example:
```python
DB = 'db'
URL = 'https://ip'
USERNAME = 'user
PASSWORD = 'pw'
```

### SSL Configuration

The script disables SSL verification to allow connections to servers with self-signed certificates or other non-standard SSL configurations. It achieves this by creating an SSL context that bypasses hostname checks and certificate verification.

Example:
```python
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
```

## Functions

### `connect_to_odoo()`

**Purpose**: Establishes a connection to the Odoo server and authenticates the user.

- **Returns**: 
  - `uid` (int): The user ID of the authenticated user.
  - `models` (xmlrpc.client.ServerProxy): A proxy object that allows interaction with the Odoo models.

- **Error Handling**:
  - Catches `xmlrpc.client.ProtocolError` for protocol-related issues.
  - Catches any other exceptions to handle unexpected errors.

**Example**:
```python
uid, models = connect_to_odoo()
if not uid or not models:
    return
```

### `fetch_sales_data(uid, models)`

**Purpose**: Fetches the product IDs from sales orders within the last 90 days that are either in the 'sale' or 'done' state.

- **Parameters**:
  - `uid` (int): The user ID of the authenticated user.
  - `models` (xmlrpc.client.ServerProxy): The proxy object for interacting with Odoo models.

- **Returns**: 
  - `product_ids` (list): A list of unique product IDs from the fetched sales orders.

- **Error Handling**:
  - Catches `xmlrpc.client.Fault` for XML-RPC-specific errors.

**Example**:
```python
product_ids = fetch_sales_data(uid, models)
if not product_ids:
    return
```

## Script Execution

The script is executed by calling the `main()` function. This function connects to the Odoo server, fetches the sales data, and prints the list of product IDs to the console.

### Example Execution

```python
if __name__ == "__main__":
    main()
```

Upon successful execution, the script will output a list of product IDs like so:

```python
[6780, 6782, 6783]
```

## Error Handling and Troubleshooting

- **Connection Errors**: If the script fails to connect to the Odoo server, ensure that the URL and credentials are correct and that the server is reachable.
- **SSL Verification Issues**: If SSL verification is required, modify the SSL context configuration accordingly.
- **No Data Returned**: If no product IDs are returned, verify that there are sales orders in the specified date range and that they match the defined criteria.

## Security Considerations

- **Credentials**: Store the username and password securely, and avoid hardcoding them in production environments. Consider using environment variables or a configuration file.
- **SSL Verification**: Disabling SSL verification is not recommended for production environments. Ensure secure connections by properly configuring SSL/TLS.

This documentation should help in understanding, using, and modifying the script as needed for different Odoo server configurations and requirements.
