import csv
import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def get_driver():
    options = webdriver.chrome.options.Options()
    options.add_argument("user-data-dir=C:\\Users\\steve\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 2")
    #options.add_argument("--disable-extensions")
    options.add_argument("profile-directory=Profile 2")
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    return driver


def save_data_to_csv(save_path, rows, file_exists=False):
    print('Saving rows...')
    if not file_exists:
        with open(save_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
    else:
        with open(save_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

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
LINK = 'https://app.cbinsights.com/top-search/kg7paa?companyView=table&isid=0-47e72abd-a74d-33f8-b72e-a80d82ad9d27&tab=companyDeal'
USERNAME = 'stevents.luo@mail.utoronto.ca'
PASSWORD = 'rma.HF!v38N5*jq'
CSV_SAVE_PATH = 'scraped_deal_data_15.csv'

for year in range(14, 15):
    LINK = LINKS[year - 13]
    CSV_SAVE_PATH = 'scraped_deal_data_%s.csv' % year
    driver = get_driver()
    driver.get(LINK)
    try:
        """Log in to CB-Insights"""
        """email = driver.find_element(By.NAME, 'email')
        pwd = driver.find_element(By.NAME, 'password')
        email.send_keys(USERNAME)
        pwd.send_keys(PASSWORD)

        driver.find_element(By.XPATH, '//*[@id="hero"]/div/section/form/div[3]/button').click()"""
        
        n_deals_html = driver.find_element(By.XPATH, '//*[@id="react-tabs-5"]/div/div/div[2]/div/div/div[1]/div')
        n_deals = n_deals_html.text
        n_deals = n_deals.split(' ')[5]
        n_pages = math.ceil(int(n_deals) / 25)

        """Saving header"""
        # headers for "deals" tab
        header_ls = [['Companies', 'Investment Stage', 'Deal Size', 'Deal Date', 'Round Investors', 'Description', 'Industry', 'Country', 'Total Funding', 'All Investors']]
        save_data_to_csv(CSV_SAVE_PATH, header_ls, file_exists=False)

        # Currently, you could only manualyl input the number of pages
        for page in range(1, n_pages + 1):
            print('Scraping page %s out of %s pages' % (page, n_pages))

            """Scrape table values in current page"""
            driver.implicitly_wait(10)

            companies_ls = []

            for row in range(1, 26):
                # print('Collecting data for row %s' % row)
                try:
                    company_ls = []
                    for col in range(2, 12):
                        # Columns: ['Companies', 'Investment Stage', 'Deal Size', 'Deal Date', 'Round Investors', 'Description', 'Industry', 'Country', 'Total  Funding', 'All Investors']
                        if col in [2]:
                            c_col = driver.find_element(By.XPATH, '//*[@id="react-tabs-5"]/div/div/div[1]/div/div[2]/div[%s]/div/div[%s]/div/div/div/div[1]/div/div/div/div' % (row, col))
                            company_ls.append(c_col.text)   
                        elif col in [3, 4, 9, 10]:
                            c_col = driver.find_element(By.XPATH, '//*[@id="react-tabs-5"]/div/div/div[1]/div/div[2]/div[%s]/div/div[%s]/div/div/div[1]/div/div/div' % (row, col))
                            company_ls.append(c_col.text)
                        # Investor Column with hyperlinks to each investor
                        elif col in [6, 11]:
                            # Commented out due to efficiency issues.
                            # These are investment info columns ("current-stage investors" and "all investors")
                            """sub_row_str_ls = []
                            more_rows = True
                            sub_row = 1
                            while more_rows:
                                try:
                                    print(sub_row_str_ls)
                                    c_col = driver.find_element(By.XPATH, '//*[@id="react-tabs-5"]/div/div/div[1]/div/div[2]/div[%s]/div/div[%s]/div/div/div[1]/div/div/div/div/div[%s]/div/div/div/a' % (row, col, sub_row))
                                    sub_row_str_ls.append(c_col.text)
                                    sub_row += 1
                                except:
                                    more_rows = False
                            sub_row_str = ' '.join(sub_row_str_ls)
                            company_ls.append(sub_row_str)"""
                            company_ls.append('N/A')
                        elif col in [5]:
                            c_col = driver.find_element(By.XPATH, '//*[@id="react-tabs-5"]/div/div/div[1]/div/div[2]/div[%s]/div/div[%s]/div/div/div[1]/div/div/p' % (row, col))
                            company_ls.append(c_col.text)
                        elif col in [7, 8]:
                            c_col = driver.find_element(By.XPATH, '//*[@id="react-tabs-5"]/div/div/div[1]/div/div[2]/div[%s]/div/div[%s]/div/div/div[1]/div/div/div/div' % (row, col))
                            company_ls.append(c_col.text)
                            
                    companies_ls.append(company_ls)
                except:
                    try:
                        company_ls = []
                        c_name = driver.find_element(By.XPATH,
                                                            '//*[@id="react-tabs-3"]/div/div/div[1]/div/div[2]/div[%s]/div/div[2]/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div/a' % row)
                        company_ls.append(c_name.text)

                        for col in range(2, 12):
                            # Columns: ['Companies', 'Investment Stage', 'Deal Size', 'Deal Date', 'Description', 'Industry', 'Country', 'Total  Funding', 'All Investors']
                            if col in [2]:    
                                c_col = driver.find_element(By.XPATH, '//*[@id="react-tabs-5"]/div/div/div[1]/div/div[2]/div[%s]/div/div[%s]/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div/a' % (row, col))
                                company_ls.append(c_col.text)   
                            elif col in [3, 4, 9, 10]:
                                c_col = driver.find_element(By.XPATH, '//*[@id="react-tabs-5"]/div/div/div[1]/div/div[2]/div[%s]/div/div[%s]/div/div/div[1]/div/div/div' % (row, col))
                                company_ls.append(c_col.text)
                            # Investor Column with hyperlinks to each investor
                            elif col in [6, 11]:
                                # Commented out due to efficiency issues.
                                # These are investment info columns ("current-stage investors" and "all investors")
                                """sub_row_str_ls = []
                                more_rows = True
                                sub_row = 1
                                while more_rows:
                                    try:
                                        print(sub_row_str_ls)
                                        c_col = driver.find_element(By.XPATH, '//*[@id="react-tabs-5"]/div/div/div[1]/div/div[2]/div[%s]/div/div[%s]/div/div/div[1]/div/div/div/div/div[%s]/div/div/div/a' % (row, col, sub_row))
                                        sub_row_str_ls.append(c_col.text)
                                        sub_row += 1
                                    except:
                                        more_rows = False
                                sub_row_str = ' '.join(sub_row_str_ls)
                                company_ls.append(sub_row_str)"""
                                company_ls.append('N/A')
                            elif col in [5]:
                                c_col = driver.find_element(By.XPATH, '//*[@id="react-tabs-5"]/div/div/div[1]/div/div[2]/div[%s]/div/div[%s]/div/div/div[1]/div/div/p' % (row, col))
                                company_ls.append(c_col.text)
                            elif col in [7, 8]:
                                c_col = driver.find_element(By.XPATH, '//*[@id="react-tabs-5"]/div/div/div[1]/div/div[2]/div[%s]/div/div[%s]/div/div/div[1]/div/div/div/div' % (row, col))
                                company_ls.append(c_col.text)
                                
                        companies_ls.append(company_ls)
                    except:
                        pass

            save_data_to_csv(CSV_SAVE_PATH, companies_ls, file_exists=True)
            """Move on to the next page"""
            driver.implicitly_wait(10)
            next_page_button = driver.find_element(By.XPATH, '//*[@id="react-tabs-5"]/div/div/div[2]/div/div/div[3]/div/div/button[12]')
            next_page_button.click()

    finally:
        #driver.quit()
        pass

    #cell1 = driver.find_element_by_class_name('flexItem flexItem--shrink')

    #print(len(cell1))

