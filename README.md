# WebCrawler

# Faculty Web Scraper and Parser

This repository contains a Python-based web scraping and parsing tool designed to collect, process, and store information about faculty members from a university's website into a MongoDB database. The project leverages libraries like `BeautifulSoup` for HTML parsing and `PyMongo` for database interaction.

---

## Features

- **Web Scraping**: The `crawler.py` script fetches HTML content from the target university website and stores it in MongoDB.
- **Data Parsing**: The `parser.py` script processes the scraped HTML to extract structured faculty data, including:
  - Name
  - Title
  - Office
  - Phone
  - Email
  - Website
- **Database Storage**: The cleaned and structured data is stored in a MongoDB collection for further use.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/faculty-web-scraper.git
   cd faculty-web-scraper

2. Install the required Python libraries:
  pip install -r requirements.txt

3.  Set up a MongoDB instance (local or cloud-based) and ensure it's running.

---

## Usage

### Step 1: Web Crawling
Run the crawler.py script to scrape HTML pages and store them in the pages collection in MongoDB: `python crawler.py`

### Step 2: Step 2: Data Parsing
Run the parser.py script to parse the faculty data and store the structured data in the professors collection: `python parser.py`

---

## Project Structure

- `crawler.py`: Script for web scraping and storing raw HTML data.
- `parser.py`: Script for parsing faculty details from HTML and storing structured data.
- `requirements.txt`: List of required Python packages.
- `README.md`: Repository documentation.

---

## Database Details
- **Database Name**: `webcrawler`
- **Collections**:
-   `pages`: Stores raw HTML content of scraped web pages
-   `professors`: Stores parsed and cleaned faculty data

---

## Example Output
### MongoDB Data Format (`professors` collection):
{ <br />
  "name": "John Doe", <br />
  "title": "Associate Professor", <br />
  "office": "8-15", <br />
  "phone": "(909) 869-3441", <br />
  "email": "johndoe@university.edu", <br />
  "website": "https://www.university.edu/faculty/johndoe/" <br />
}

---

## Notes
- Ensure your MongoDB instance is running before executing the scripts.
- Update the `crawler.py` and `parser.py` scripts with the correct MongoDB connection string if necessary.
