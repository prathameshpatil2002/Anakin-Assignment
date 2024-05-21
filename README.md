# Approach

## Steps Taken:

### Cookie Management:

Cookies are crucial for autofilling input fields on the website.
Programmatically set cookies for the respective locations to simulate user input.

### Parallel Processing:

Used Python's multiprocessing module to handle restaurant data collection from multiple locations concurrently.

### Data Extraction Using Selenium:

Utilized Selenium WebDriver to automate browser interactions, including clicking and scrolling events, to ensure all data is loaded.
Extracted necessary details using CSS selectors to pinpoint relevant HTML elements.

### Data Formatting and Storage:

Formatted the extracted data into JSON format.
Stored the complete dataset as an NDJSON (Newline Delimited JSON) compressed file (ndjson.gz).

## Problems Faced and Solutions:
### Problem : Obtaining Latitude and Longitude
Issue: Latitude and Longitude data was not visible in the HTML elements.
Solution: Monitored network requests to identify the one returning geolocation data. Used URL `https://portal.grab.com/foodweb/v2/merchants/{}?latlng=1.396364,103.747462` and replaced the restaurant_id dynamically to fetch latitude and longitude information from the response.

## Execution Steps:
### Prerequisites:

Install Required Packages:

Install dependencies listed in requirements.txt:
`sh pip install -r requirements.txt`

Run the Program:
`sh python scraper.py`
