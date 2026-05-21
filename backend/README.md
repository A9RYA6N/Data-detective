# Web Scraper Backend

This project is a web scraping backend built with FastAPI, Playwright, and SQLAlchemy. Currently, it serves as an API that accepts Amazon product URLs, asynchronously scrapes the webpage using headless browsers to extract product details, and stores the extracted data in a PostgreSQL database.

## Prerequisites

- Python
- PostgreSQL

## Installation

1. Clone the repository:
   git clone <repository-url>
   cd web-scraper/backend

2. Create and activate a virtual environment:
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

3. Install the required dependencies:
   pip install -r requirements.txt

4. Install Playwright browser binaries:
   playwright install

5. Configure your environment variables:
   Create a `.env` file in the root directory and add your database configuration:
   DATABASE_URL=postgresql://user:password@localhost:5432/dbname

6. Run database migrations:
   alembic upgrade head

## Usage

1. Start the FastAPI server:
   uvicorn main:app --reload

2. Access the API documentation:
   Open your browser and navigate to `http://127.0.0.1:8000/docs` to test the scraping endpoints via the interactive Swagger UI.

## Future Plans

The project is designed to be scaled significantly. Future updates will include:

- Universal Link Handling: Expanding the scraper's logic to dynamically handle and parse links from almost any ecommerce website.
- Price Timeline: Tracking and visualizing price changes over time for specific products.
- Historical Data: Storing and displaying past sale events and pricing data.
- Advanced Analytics: Providing detailed insights and trends based on aggregated product data.
