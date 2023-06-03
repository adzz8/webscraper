# Generic Table Scraper

This is a simple and generic web scraper script which uses Selenium and BeautifulSoup to extract data from tables on web pages. You can use this script to scrape any website that has data organized in a table within a container.

## Prerequisites

To run the script, you need to have the following installed:

- Python (3.x recommended)
- Selenium (`pip install selenium`)
- BeautifulSoup (`pip install beautifulsoup4`)
- ChromeDriver (https://sites.google.com/chromium.org/driver/)

Ensure ChromeDriver is installed in a directory that's included in your PATH system variable.

## Configuration

You can set up the script by providing the following arguments when running the script:

- `chromedriver_path`: This should be the path to your ChromeDriver executable.
- `input_file`: Path to a text file containing your list of items. The file should contain a list of items formatted as a Python list.
- `output_file`: The path and name of the CSV file where the scraped data will be saved.
- `url_template`: This should be the base URL for your web pages, with `{}` in the place where your item name will be inserted.
- `table_container_class`: The class name of the div containing the table(s) you want to scrape.
- `min_sleep_time`: The number of seconds to wait for each page to load.
- `max_sleep_time` : The maximum number of seconds to wait for each page to load.
- `max_workers`: The maximum number of threads to use for concurrent scraping.

You should also update the `fieldnames` in the `writer` setup to reflect the headers for your CSV file. This should match with the keys in your `data_list`.

## Usage

```python main.py --chromedriver_path "/usr/local/bin/chromedriver" --input_file "items.txt" --output_file "output.csv" --url_template "http://example.com/{}" --table_container_class "table-class" --min_sleep_time 1 --max_sleep_time 5 --max_workers 5



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
- `min_sleep_time`: `1`
- `max_sleep_time` : `5`
- `max_workers`: `5`

And you would set up the `fieldnames` and `data_list` like this:

```python
fieldnames = ['Author', 'Title', 'ISBN', 'URL']
...
data_list.append({'Author': item, 'Title': td.text.strip(), 'ISBN': td.find('span', class_='isbn').text.strip(), 'URL': a['href']})


## 🛠️ To-Do List

stuff to add after exams

- [x] **anti-fart** - seperate files for log handling, preventing crashes when program fails.
- [x] **slow down** - add delays between request so don't get flagged
- [x] **speed up** - utilize processor by multithreading
- [x] **interface?** - Command line interface for easy navigation and use.

# at this point the project would be pushing actual software, so focusing on other projects and might return later

- [ ] **cleanliness is half of faith** - data cleaning
- [ ] **spider** - web crawling, super effective scraper
- [ ] **spy games** - User agent rotation, switch up disguises to avoid getting caught.
- [ ] **container** - Containerizing the scraper with Docker, everyone loves an easy setup!
- [ ] **testing** - Unit tests to make sure everything's working as expected.
- [ ] **ELI5** - Clear instructions and documentation so people can use 

