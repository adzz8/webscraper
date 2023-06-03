import time
import logging
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv

# configuration settings
config = {
    "chromedriver_path": "",  
    "input_file": "", 
    "output_file": "",  
    "url_template": "",  
    "table_container_class": "",
    "min_sleep_time": '',  
    "max_sleep_time": '',  
}

# setup logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

# fetch items
try:
    with open(config["input_file"], 'r') as file:
        items = eval(file.read())
except FileNotFoundError:
    logging.error(f'File {config["input_file"]} not found')
    items = []

# ninja mode chrome
chrome_options = Options()
chrome_options.add_argument("--headless")

# setup CSV file
try:
    with open(config["output_file"], 'w', newline='') as csvfile:
        fieldnames = ['Item', 'Data1', 'Data2']  
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for item in items:
            item_url = item.replace(' ', '%20')
            url = config["url_template"].format(item_url)
            driver = webdriver.Chrome(config["chromedriver_path"], options=chrome_options)

            try:
                print(f"Scraping: {item}") 
                driver.get(url)
                time.sleep(random.uniform(config["min_sleep_time"], config["max_sleep_time"]))

                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                table_container = soup.find('div', class_=config["table_container_class"])

                if table_container:
                    tables = table_container.find_all('table')
                    if tables:
                        for table in tables:
                            table_body = table.find('tbody')
                            if table_body:
                                rows = table_body.find_all('tr')
                                data_list = []
                                for row in rows:
                                    td = row.find('td')
                                    if td and td.text.strip() != "�":
                                        a = td.find('a')
                                        if a:
                                            data_list.append({'Data1': td.text.strip(), 'Data2': a['href']})
                                for data in data_list:
                                    writer.writerow({'Item': item, 'Data1': data['Data1'], 'Data2': data['Data2']})
            except Exception as e:
                error_message = f"Error with {item}. Error: {e}"
                print(error_message)
                logging.error(error_message)

            finally:
                driver.quit()

            time.sleep(random.uniform(config["min_sleep_time"], config["max_sleep_time"]))
except Exception as e:
    logging.error(f'Error while setting up CSV file or during scraping: {e}')
