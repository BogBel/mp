# Wool Price Comparison Portal
## Introduction

This repository contains my solution for a software development coding task focusing on web scraping and data aggregation. The primary objective of the task is to create a wool price comparison portal, initially featuring data extraction from "Wollplatz" (https://www.wollplatz.de/). The project aims to provide valuable insights for wool products by comparing various attributes like price, availability, needle size, and composition.
## Challenge Encountered: Cloudflare Protection

During the initial development phase, I noticed that Wollplatz's website appeared to implement more strict Cloudflare protection over the weekend. This change significantly affected the scraping process, as none of the requests to the product pages were successful.

## Workaround: Mocked Responses

To maintain progress, I implemented a workaround by mocking responses for some product pages. This approach involves reading pre-saved HTML content from files when direct scraping fails.

## Search Functionality

Notably, the search functionality of the portal remains operational. This was achieved by leveraging the Sooqr API, allowing effective retrieval of search results from Wollplatz.

## Overview of Process

The application is structured to perform the following actions:
  1. Upon receiving a request, background tasks are initiated to fetch results from the website.
  2. These results are then stored in Redis with a Time-To-Live (TTL), making the data temporarily cached for efficiency.
  3. The stored results can subsequently be accessed via another API call.

## Tech Stack

The technical components of the project include:
  1. FastAPI: For building the API, taking advantage of its performance, ease of use, and built-in support for asynchronous operations.
  2. Redis: Used as a caching layer to store the fetched data with a TTL.
  3. Docker and Docker-Compose: For containerizing the FastAPI and Redis services.
  4. Python 3.11: The programming language used, alongside pipenv for managing the virtual environment and dependencies.
  5. Pydantic: Employed for data validation.

## Setup and Running the Application

### To run the project:
  1. Ensure you have Docker and Docker Compose installed on your machine.
  2. Clone the repository to your local machine.
  3. Navigate to the root directory of the project in your terminal.
  4. Run docker-compose up -d.
  5. Access the API documentation and test the API calls at: http://0.0.0.0:8000/docs.

## Running Tests

To execute the tests after the Docker containers are up and running, follow these steps:

  ```bash
docker-compose exec app bash
```
Within the container, run the tests using pytest:

```bash
pipenv run pytest
```
This process allows you to run your test suite within the context of your application's Docker container environment.

## Decision-Making Process
1. Data Storage for Queries
    Implementation: Used a simple JSON file to store input queries.
    Alternative Considered: MongoDB, for its flexibility and scalability in handling structured data.

2. Data Storage for Results

    Implementation: Chose Redis due to the dynamic nature of data (frequent changes in availability and price). Stored data in a key-value format, where the key is **query:{query.id}:{crawler_name}** and the value is a JSON string of crawled data.
    Alternative Considered: Elasticsearch, which could be more efficient at scale, especially for search and analytics.

3. Approach to Testing

   Implementation: Some tests have been written to cover the logic of data converters. It's ideal to have all functions that parse data and do not rely on online sources covered with unit tests to ensure the correctness of the parsing logic.

## Suggestions for Improvement
1. Enhanced Data Storage System

    Details: The current data storage system can be upgraded to a more robust solution like a NoSQL or SQL database, which would provide better scalability, data integrity, and advanced query capabilities.

2. Logging Mechanism

    Details: Implementing a comprehensive logging system is crucial for monitoring the application's performance and debugging issues. Tools like loguru or Python's built-in logging module can be used to set up structured and informative logs.

3. Robust Error Handling

    Details: Expanding the error handling mechanism to cover a wider range of possible exceptions and edge cases. This could involve creating custom exceptions that are more descriptive of the specific errors the application might encounter.

4. Queue Management for Background Tasks

    Details: For scaling purposes, integrating a message broker like RabbitMQ for managing background tasks could significantly enhance performance and reliability, especially when dealing with large volumes of data or requests.

5. Advanced Anti-bot Mitigation Strategy

    Details: Developing Anti-Bot Countermeasures: An area for improvement involves developing more sophisticated techniques to bypass anti-bot protections. This is crucial for enabling real-time data access and retrieval from websites with strict bot-detection mechanisms.
6. Advanced Testing and Monitoring

    Details: In the future, more sophisticated testing strategies like black-box testing could be implemented. This would involve sending specific inputs and validating the outputs to assess the overall functionality and reliability of the application.

   
These suggestions aim to address some of the key areas where the project could be improved, enhancing its efficiency, scalability, and overall robustness. Each of these improvements would contribute significantly to the project's ability to handle larger scales and more complex scenarios.

## Sample API Requests and Responses
### Fetching Search Queries

Request:

```bash

curl -X 'GET' \
  'http://0.0.0.0:8000/api/search_queries' \
  -H 'accept: application/json'
```
Response:

```json

[
  {
    "id": 1,
    "brand_name": "DMC",
    "product_name": "Natura XL"
  },
  ... (additional items)
]
```

### Fetching Product Details

Request:

```bash

curl -X 'GET' \
  'http://0.0.0.0:8000/api/product/1' \
  -H 'accept: application/json'
```
Response:

```json

{
  "query_data": {
    "id": 1,
    "brand_name": "DMC",
    "product_name": "Natura XL"
  },
  "products": [
    {
      "url": "https://www.wollplatz.de/wolle/dmc/dmc-natura-xl",
      "product_name": "DMC Natura XL",
      "brand": "DMC",
      "price": {
        "value": 8.46,
        "currency": "EUR"
      },
      "availability": false
    }
    ... (additional items)
  ]
}
```
