import time
import logging
import random
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
import argparse

# setup argument parser
parser = argparse.ArgumentParser(description='Web scraper')
parser.add_argument('--chromedriver_path', type=str, required=True, help='Path to ChromeDriver')
parser.add_argument('--input_file', type=str, required=True, help='Input file path')
parser.add_argument('--output_file', type=str, required=True, help='Output file path')
parser.add_argument('--url_template', type=str, required=True, help='URL template')
parser.add_argument('--table_container_class', type=str, required=True, help='HTML class for the table container')
parser.add_argument('--min_sleep_time', type=float, required=True, help='Minimum sleep time between requests')
parser.add_argument('--max_sleep_time', type=float, required=True, help='Maximum sleep time between requests')
parser.add_argument('--max_workers', type=int, required=True, help='Maximum number of threads')
args = parser.parse_args()

# configuration settings
config = {
    "chromedriver_path": args.chromedriver_path,  
    "input_file": args.input_file, 
    "output_file": args.output_file,  
    "url_template": args.url_template,  
    "table_container_class": args.table_container_class,
    "min_sleep_time": args.min_sleep_time,  
    "max_sleep_time": args.max_sleep_time,  
    "max_workers": args.max_workers,
}

# rest of your code


# setup logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

def scrape_item(item):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(config["chromedriver_path"], options=chrome_options)
    item_url = item.replace(' ', '%20')
    url = config["url_template"].format(item_url)

    try:
        print(f"Scraping: {item}")
        driver.get(url)
        time.sleep(random.uniform(config["min_sleep_time"], config["max_sleep_time"]))

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        table_container = soup.find('div', class_=config["table_container_class"])

        data_list = []

        if table_container:
            tables = table_container.find_all('table')
            if tables:
                for table in tables:
                    table_body = table.find('tbody')
                    if table_body:
                        rows = table_body.find_all('tr')
                        for row in rows:
                            td = row.find('td')
                            if td and td.text.strip() != "�":
                                a = td.find('a')
                                if a:
                                    data_list.append({'Item': item, 'Data1': td.text.strip(), 'Data2': a['href']})
    except Exception as e:
        error_message = f"Error with {item}. Error: {e}"
        print(error_message)
        logging.error(error_message)
    finally:
        driver.quit()

    return data_list

# fetch items
try:
    with open(config["input_file"], 'r') as file:
        items = eval(file.read())
except FileNotFoundError:
    logging.error(f'File {config["input_file"]} not found')
    items = []

# setup CSV file
try:
    with open(config["output_file"], 'w', newline='') as csvfile:
        fieldnames = ['Item', 'Data1', 'Data2']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        with concurrent.futures.ThreadPoolExecutor(max_workers=config["max_workers"]) as executor:
            future_to_item = {executor.submit(scrape_item, item): item for item in items}
            for future in concurrent.futures.as_completed(future_to_item):
                item = future_to_item[future]
                try:
                    data = future.result()
                    for row in data:
                        writer.writerow(row)
                except Exception as e:
                    logging.error(f"Error while writing {item} data to CSV. Error: {e}")
except Exception as e:
    logging.error(f'Error while setting up CSV file or during scraping: {e}')
