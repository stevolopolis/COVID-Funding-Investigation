"""CBI deals data WebScraper

This file contains the WebScraper Object for scraping deals data from
CB-Insighted embedded funding table. Scraped data will be saved into
csv files under the sub-directory 'data'.
If all deal data from 2015 to 2021 are scraped, there should be around
67,000+ instances of data stored.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of interested personel
for investigating the funding data over the COVID-19 period. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2021 Steven T. S., Luo.
"""

import csv
import math
from typing import Optional, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Links to each year of deals data and their subsequent total number of deals
# 2013 -- https://app.cbinsights.com/top-search/kg7paa?companyView=table&isid=0-0a2898ca-c892-3562-b2da-956cdcbe6688&tab=companyDeal -- 5374
# 2014 -- https://app.cbinsights.com/top-search/kg7paa?companyView=table&isid=0-fcf5d344-5be1-3613-b6f4-2aca3b8876ce&tab=companyDeal -- 6633
# 2015 -- https://app.cbinsights.com/top-search/kg7paa?companyView=table&isid=0-f85da5b0-bd1c-3228-ac61-48063feff484&tab=companyDeal -- 8056
# 2016 -- https://app.cbinsights.com/top-search/kg7paa?companyView=table&isid=0-47e72abd-a74d-33f8-b72e-a80d82ad9d27&tab=companyDeal -- 8398
# 2017 -- https://app.cbinsights.com/top-search/kg7paa?companyView=table&isid=0-d8114bfb-f7bc-3690-8445-fcc9c54bcaa0&tab=companyDeal -- 9245
# 2018 -- https://app.cbinsights.com/top-search/kg7paa?companyView=table&isid=0-6639b78a-e353-3b4c-b799-2853b5c13d52&tab=companyDeal -- 10356
# 2019 -- https://app.cbinsights.com/top-search/kg7paa?companyView=table&isid=0-7694ef6d-5e05-3824-83e4-f6bb9872f655&tab=companyDeal -- 10052
# 2020 -- https://app.cbinsights.com/top-search/kg7paa?companyView=table&isid=0-20663eca-9f8c-38c0-81cb-c257f65f4c52&tab=companyDeal -- 9073
# 2021 -- https://app.cbinsights.com/top-search/kg7paa?companyView=table&isid=0-b06ad0b8-f322-3a34-9b2a-d15eea37b7e5&tab=companyDeal -- 11966

LINKS = ['https://app.cbinsights.com/top-search/kg7paa?companyView=table&isid=0-0a2898ca-c892-3562-b2da-956cdcbe6688&tab=companyDeal',
         'https://app.cbinsights.com/top-search/kg7paa?companyView=table&isid=0-fcf5d344-5be1-3613-b6f4-2aca3b8876ce&tab=companyDeal',
         'https://app.cbinsights.com/top-search/kg7paa?companyView=table&isid=0-f85da5b0-bd1c-3228-ac61-48063feff484&tab=companyDeal',
         'https://app.cbinsights.com/top-search/kg7paa?companyView=table&isid=0-47e72abd-a74d-33f8-b72e-a80d82ad9d27&tab=companyDeal',
         'https://app.cbinsights.com/top-search/kg7paa?companyView=table&isid=0-d8114bfb-f7bc-3690-8445-fcc9c54bcaa0&tab=companyDeal',
         'https://app.cbinsights.com/top-search/kg7paa?companyView=table&isid=0-6639b78a-e353-3b4c-b799-2853b5c13d52&tab=companyDeal',
         'https://app.cbinsights.com/top-search/kg7paa?companyView=table&isid=0-7694ef6d-5e05-3824-83e4-f6bb9872f655&tab=companyDeal',
         'https://app.cbinsights.com/top-search/kg7paa?companyView=table&isid=0-20663eca-9f8c-38c0-81cb-c257f65f4c52&tab=companyDeal',
         'https://app.cbinsights.com/top-search/kg7paa?companyView=table&isid=0-b06ad0b8-f322-3a34-9b2a-d15eea37b7e5&tab=companyDeal']

HEADER = ['Companies', 'Investment Stage', 'Deal Size', 'Deal Date', 'Round Investors',
          'Description', 'Industry', 'Country', 'Total Funding', 'All Investors']


class DataScraper:
    """A data scraper object that scrapes the deals data from specified CB-Insights webpages.
    Instance Attributes:
        - username: The username to log in to CB-Insights
        - password: The password to log in to CB-Insights
    """
    driver: webdriver.Chrome
    username: str
    password: str

    def __init__(self, username: str, password: str) -> None:
        self.driver = get_driver()
        self.username = username
        self.password = password

    def scrape_15_21(self) -> None:
        """Scrape the deals data from 2015 to 2021 and save the data to multiple csv file.
        The csv files are saved in a 'data' sub directory."""
        for year in range(15, 22):
            data_link = LINKS[year - 13]
            csv_save_path = 'data/scraped_deal_data_%s.csv' % year

            self.scrape_year(data_link, csv_save_path)

    def scrape_year(self, link: str, save_path: str) -> None:
        """Scrape the deals data for a year and save the data to a csv file."""
        n_pages = self.initialize_link(link)

        # Header of our chosen table of deals data
        save_data_to_csv(save_path, HEADER, file_exists=False)

        for page in range(1, n_pages + 1):
            print('Scraping page %s out of %s pages' % (page, n_pages))

            self.driver.implicitly_wait(10)  # wait for the webpage to load before searching for elements

            companies_ls = []  # companies_ls is a list containing 25 rows of deal data (1 page of data)

            for row in range(1, 26):
                # Two try-except blocks are used to make sure the code runs smoothly without interuptions.
                # Due to delays in loading the webpage, the drivers may not be able to find elements and
                # hence cause an error.
                # These try-except blocks would catch those errors and allow the code to run again.
                try:
                    company_ls = self.scrape_row(row)
                    companies_ls.append(company_ls)
                except:
                    try:
                        # company_ls = []
                        # c_name = driver.find_element(By.XPATH,
                        #                              '//*[@id="react-tabs-3"]/div/div/div[1]/div/div[2]/div[%s]/div/div[2]/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div/a' % row)
                        # company_ls.append(c_name.text)
                        company_ls = self.scrape_row(row)
                        companies_ls.append(company_ls)
                    except:
                        pass

            save_data_to_csv(save_path, companies_ls, file_exists=True)
            self.next_page()

    def scrape_row(self, row: int) -> list[Any]:
        """Return the list of company funding details as shown in the embedded table on CB-Insights.
        
        This code scrapes the data from each row in the embedded table using specific XPATHs.
        As XPATHs are specific to each webpage's own design, this code is only applicable to
        our particular selection of webpages.
        
        The columns of each row are in the following order:
        ['Companies', 'Investment Stage', 'Deal Size', 'Deal Date', 'Round Investors',
        'Description', 'Industry', 'Country', 'Total Funding', 'All Investors']

        Due inefficiencies in selenium's XPATH searching, data for the columns 'Round Investors'
        and 'All Investors'will not be scraped. They will be filled in as 'N/A' instead.
        Since these data are not essential for answering our main research question, it does not
        affect the analysis in the report and could be omitted for now.
        """
        company_ls = []
        for col in range(2, 12):
            # Scraping ['Companies']
            if col in [2]:
                c_col = self.driver.find_element(By.XPATH,
                                                 '//*[@id="react-tabs-5"]/div/div/div[1]/div/div[2]/div[%s]/div/div[%s]/div/div/div/div[1]/div/div/div/div' % (row, col))
                company_ls.append(c_col.text)
            # Scraping ['Investment Stage', 'Deal Size', 'Country', 'Total Funding']
            elif col in [3, 4, 9, 10]:
                c_col = self.driver.find_element(By.XPATH,
                                                 '//*[@id="react-tabs-5"]/div/div/div[1]/div/div[2]/div[%s]/div/div[%s]/div/div/div[1]/div/div/div' % (row, col))
                company_ls.append(c_col.text)
            # Scraping ['Round Investors', 'All Investors']
            elif col in [6, 11]:
                pass
                # Commented out due to efficiency issues.
                # sub_row_str_ls = []
                # more_rows = True
                # sub_row = 1
                # while more_rows:
                #     try:
                #         print(sub_row_str_ls)
                #         c_col = self.driver.find_element(By.XPATH,
                #                                          '//*[@id="react-tabs-5"]/div/div/div[1]/div/div[2]/div[%s]/div/div[%s]/div/div/div[1]/div/div/div/div/div[%s]/div/div/div/a' % (row, col, sub_row))
                #         sub_row_str_ls.append(c_col.text)
                #         sub_row += 1
                #     except:
                #         more_rows = False
                # sub_row_str = ' '.join(sub_row_str_ls)
                # company_ls.append(sub_row_str)
                # company_ls.append('N/A')
            # Scraping  ['Deal Date']
            elif col in [5]:
                c_col = self.driver.find_element(By.XPATH,
                                                 '//*[@id="react-tabs-5"]/div/div/div[1]/div/div[2]/div[%s]/div/div[%s]/div/div/div[1]/div/div/p' % (row, col))
                company_ls.append(c_col.text)
            # Scraping ['Description', 'Industry']
            elif col in [7, 8]:
                c_col = self.driver.find_element(By.XPATH,
                                                 '//*[@id="react-tabs-5"]/div/div/div[1]/div/div[2]/div[%s]/div/div[%s]/div/div/div[1]/div/div/div/div' % (row, col))
                company_ls.append(c_col.text)

        return company_ls

    def initialize_link(self, link: str) -> webdriver.Chrome:
        """Return chrome webdriver and initialize webpage."""
        self.driver.get(link)

        # Uncomment the log_in line when this is first time running this code.
        # log_in(self.driver, self.username, self.password)
        
        return self.get_n_pages()

    def log_in(self) -> None:
        """Log in to CB-Insights using my personal login credentials.
        Not required when your chrome has remembered the login credentials."""
        email = self.driver.find_element(By.NAME, 'email')
        pwd = self.driver.find_element(By.NAME, 'password')
        email.send_keys(self.username)
        pwd.send_keys(self.password)

        self.driver.find_element(By.XPATH,
                                 '//*[@id="hero"]/div/section/form/div[3]/button').click()

    def next_page(self) -> None:
        """Press the 'next' button on the embedded table.

        Will refresh the webpage and show a new set of deals data. """
        self.driver.implicitly_wait(10)
        next_page_button = self.driver.find_element(By.XPATH,
                                                    '//*[@id="react-tabs-5"]/div/div/div[2]/div/div/div[3]/div/div/button[12]')
        next_page_button.click()

    def get_n_pages(self) -> float:
        """Return the number of pages in the embedded table of deals data.

        By default on CB-Insight, there are 25 rows per page and a maximum of 10000 rows for
        filtered search. Hence, where there are more than 10000 deals in the filtered search,
        e.g. 2021 data, only the top funding 10000 deals will be scraped (this does not affect our
        analysis as most of the left out deals having funding less than 0.5M, if not 0 or N/A.
        
        Note, this function is only applicable for this project's specific filtered search."""
        n_deals_html = self.driver.find_element(By.XPATH,
                                                '//*[@id="react-tabs-5"]/div/div/div[2]/div/div/div[1]/div')
        n_deals = n_deals_html.text
        n_deals = n_deals.split(' ')[5]
        n_pages = math.ceil(int(n_deals) / 25)

        return n_pages


def get_driver() -> webdriver.Chrome:
    """Return the selenium chrome webdriver for accessing a webpage in Chrome.
    Code referenced from selenium documentation and StackOverFlow."""
    options = webdriver.chrome.options.Options()
    options.add_argument("user-data-dir=C:\\Users\\steve\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 2")
    options.add_argument("profile-directory=Profile 2")
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    return driver


def save_data_to_csv(save_path: str, row: list[str], file_exists: Optional[bool] = False) -> None:
    """Initializes a csv file at save_path and saves a row of data to the file.
    
    Sample Usage:
    
    >>> header_row = ['Company', 'Address', 'City', 'State', 'Zip']
    >>> file_path = 'scraped_data.csv'
    >>> save_data_to_csv(file_path, header_row, file_exists=False)
    Saving rows...
    """
    print('Saving rows...')
    if not file_exists:
        with open(save_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(row)
    else:
        with open(save_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(row)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
    'extra-imports': ['csv', 'math', 'typing', 'selenium', 'webdriver_manager'],  # the names (strs) of imported modules
    'allowed-io': [],     # the names (strs) of functions that call print/open/input
    'max-line-length': 100,
    'disable': ['R1705', 'C0200']
    })