# Generic Scraper

This is a simple and generic web scraper script which uses Selenium and BeautifulSoup to extract data from tables on web pages. You can use this script to scrape any website that has data organized in a table within a container.

## Prerequisites

To run the script, you need to have the following installed:

- Python (3.x recommended)
- Selenium (`pip install selenium`)
- BeautifulSoup (`pip install beautifulsoup4`)
- ChromeDriver (https://sites.google.com/chromium.org/driver/)

Ensure ChromeDriver is installed in a directory that's included in your PATH system variable.

## Configuration

You can set up the script by editing the following items in the `config` dictionary at the top of the script:

- `chromedriver_path`: This should be the path to your ChromeDriver executable.
- `input_file`: Path to a text file containing your list of items. The file should contain a list of items formatted as a Python list.
- `output_file`: The path and name of the CSV file where the scraped data will be saved.
- `url_template`: This should be the base URL for your web pages, with `{}` in the place where your item name will be inserted.
- `table_container_class`: The class name of the div containing the table(s) you want to scrape.
- `sleep_time`: The number of seconds to wait for each page to load.

You should also update the `fieldnames` in the `writer` setup to reflect the headers for your CSV file. This should match with the keys in your `data_list`.

## Usage

Just run the script in Python. The script will read your items, scrape each page, extract the data, and write it to your output file. 

## Error Handling

The script will print out a message if it encounters an error with a specific item, but it will continue to run for the rest of the items.

## Example Use Case

Let's say you want to scrape a list of books from a bookseller's website where the books are organized by author. Each author's page has a table listing their books, including details like title and ISBN.

You would set up the script like this:

- `chromedriver_path`: `'path/to/your/chromedriver'`
- `input_file`: `'authors.txt'` (a list of authors, e.g. `['Agatha Christie', 'J.K. Rowling', 'George Orwell']`)
- `output_file`: `'books.csv'`
- `url_template`: `'https://www.bookseller.com/authors/{}'`
- `table_container_class`: `'book-list'`
- `sleep_time`: `3`

And you would set up the `fieldnames` and `data_list` like this:

```python
fieldnames = ['Author', 'Title', 'ISBN', 'URL']
...
data_list.append({'Author': item, 'Title': td.text.strip(), 'ISBN': td.find('span', class_='isbn').text.strip(), 'URL': a['href']})

# have fun scraping in accordance with privacy policies etc.
