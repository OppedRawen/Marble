# Rappi Product Search Scraper

This project contains a Python script that performs product searches on Rappi (a Chilean delivery platform) and returns search results from Líder or Líder Express stores. The script accesses Rappi's API directly rather than parsing HTML, as requested in the challenge requirements.

## Features

- Searches for products on Rappi within Líder/Líder Express stores
- Returns results in JSON format with the required schema
- Uses a proxy for all requests
- Handles cookies automatically
- Object-oriented design for better maintainability
- Includes functionality to estimate cookie expiration (bonus feature)
- Allows searching from specific stores (bonus feature)

## Prerequisites

- Python 3.6 or higher
- `requests` library

## Installation

1. Clone this repository or download the script:

```bash
git clone <repository-url>
```

2. Install the required dependencies:

```bash
pip install requests
```

## Usage

### Basic Usage

Run the script with Python:

```bash
python rappi_scraper.py
```

The script will prompt you for:
- A search term (e.g., "pan", "arroz", "leche")
- A store ID (default is 900020469 for Express Líder)

### Programmatic Usage

You can also import the `RappiScraper` class in your own code:

```python
from rappi_scraper import RappiScraper

# Initialize the scraper
scraper = RappiScraper()

# Search for products
products = scraper.search_products("pan", "900020469")

# Display results
print(products)
```

### Output Format

The script returns a list of products with the following structure:

```json
[
  {
    "name": "Product Name",
    "product_link": "URL to product page",
    "image": "URL to product image",
    "price": 1000,
    "promotion_price": 800,
    "promotion_details": "buy 2 get 1 for free"
  },
  ...
]
```

## Approach to the Challenge

### 1. Understanding the Requirements

First, I carefully analyzed the challenge requirements, identifying the key tasks:
- Create a scraper for Rappi focusing on Líder stores
- Access Rappi's API instead of parsing HTML
- Extract specific product fields according to the schema
- Use a proxy for requests
- Implement cookie handling

### 2. API Endpoint Discovery

The most challenging part was discovering Rappi's API endpoints. I approached this methodically:

1. Used browser developer tools to monitor network requests
2. Filtered requests to focus on API calls related to product searches
3. Analyzed request patterns to identify the main search endpoint
4. Found the key endpoint: `https://services.rappi.cl/api/cpgs/search/v2/store/{store_id}/products`

### 3. Understanding Request/Response Structure

After finding the endpoint, I studied:
- The request method (POST)
- Required headers
- Payload structure
- Response format and how it maps to the required schema

### 4. Implementation Strategy

I chose an object-oriented approach because:
- It encapsulates functionality in a clean, modular way
- Makes the code more maintainable and testable
- Provides a clear interface for users

The main components of the implementation:
- `RappiScraper` class to handle all functionality
- Methods for cookie management, making requests, and parsing results
- Helper functions to extract specific data points

### 5. Challenges and Solutions

#### Challenge: Cookie Management
- **Solution**: Added automatic cookie retrieval and a method to refresh cookies

#### Challenge: Mapping API Response to Required Schema
- **Solution**: Created a parser that extracts and transforms the data according to the schema

#### Challenge: Promotion Details
- **Solution**: Implemented logic to analyze different promotion fields and construct meaningful descriptions

## Bonus Features Implemented

### 1. Store-Specific Search

The script allows searching from any Líder or Líder Express store by providing the store ID. The default is 900020469 for Express Líder.

### 2. Cookie Management

The script implements cookie handling in three ways:
- Automatic cookie retrieval when initializing the scraper
- A `refresh_cookies()` method to get new cookies if needed
- An `estimate_cookie_expiration()` method to determine how many requests can be made before cookies expire

## Future Improvements

1. Add error retries with exponential backoff
2. Implement pagination to handle large result sets
3. Add caching to reduce API requests
4. Create a command-line interface with more options
5. Add unit tests for better code reliability

## References

- [Rappi Chile](https://www.rappi.cl/)
- [Requests Library Documentation](https://docs.python-requests.org/en/latest/)