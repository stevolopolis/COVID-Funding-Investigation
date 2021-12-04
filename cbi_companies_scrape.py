import csv
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


LINK = 'https://app.cbinsights.com/top-search?companyView=table&isid=0-dad24223-1f4a-383a-b4da-e6e83c9cc68b&page=17&tab=company'
USERNAME = 'stevents.luo@mail.utoronto.ca'
PASSWORD = 'rma.HF!v38N5*jq'
CSV_SAVE_PATH = 'scraped_data_small.csv'

try:
    driver = get_driver()
    driver.get(LINK)

    """Log in to CB-Insights"""
    """email = driver.find_element(By.NAME, 'email')
    pwd = driver.find_element(By.NAME, 'password')
    email.send_keys(USERNAME)
    pwd.send_keys(PASSWORD)

    driver.find_element(By.XPATH, '//*[@id="hero"]/div/section/form/div[3]/button').click()"""

    """Saving header"""
    # headers for "companies" tab
    header_ls = [['Companies', 'Description', 'Industry', 'Country', 'Total Funding', 'Founded Year', 'Latest Funding Data', 'Latest Funding Round', 'Latest Funding Amount']]
    save_data_to_csv(CSV_SAVE_PATH, header_ls, file_exists=False)

    for page in range(1):
        print('Scraping page %s' % page)

        """Scrape table values in current page"""
        driver.implicitly_wait(10)

        companies_ls = []

        for row in range(1, 26):
            #print('Collecting data for row %s' % row)
            try:
                company_ls = []
                c_name = driver.find_element(By.XPATH,
                                                    '//*[@id="react-tabs-3"]/div/div/div[1]/div/div[2]/div[%s]/div/div[2]/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div/a' % row)
                company_ls.append(c_name.text)

                for col in range(3, 12):
                    # Columns: [Descriptions, Industry, Country, Total Funding, All Investor, Founded Year, Latest Funding Date, Latest Funding Round, Latest Funding Amount, Latest Funding Investors]
                    # Specific colulmns [Country, Total Funding, Founded Year]
                    if col in [3, 4]:    
                        c_col = driver.find_element(By.XPATH, '//*[@id="react-tabs-3"]/div/div/div[1]/div/div[2]/div[%s]/div/div[%s]/div/div/div[1]/div/div/div/div' % (row, col))
                        company_ls.append(c_col.text)   
                    elif col in [5, 6, 8, 10, 11]:
                        c_col = driver.find_element(By.XPATH, '//*[@id="react-tabs-3"]/div/div/div[1]/div/div[2]/div[%s]/div/div[%s]/div/div/div[1]/div/div/div' % (row, col))
                        company_ls.append(c_col.text)
                    # Investor Column with hyperlinks to each investor
                    elif col in [7, 12]:
                        pass
                        # Commented out due to efficiency issue
                        """more_investor = True
                        investor_idx = 0
                        c_col = []
                        while more_investor:
                            try:
                                i_col = driver.find_element(By.XPATH, '//*[@id="react-tabs-3"]/div/div/div[1]/div/div[2]/div[%s]/div/div[%s]/div/div/div[1]/div/div/div/div/div[%s]/div/div/div/a' % (row, col, investor_idx))
                                c_col.append(i_col.text)
                                investor_idx += 1
                            except:
                                more_investor = False

                        company_ls.append(c_col)"""
                    elif col == 9:
                        c_col = driver.find_element(By.XPATH, '//*[@id="react-tabs-3"]/div/div/div[1]/div/div[2]/div[%s]/div/div[%s]/div/div/div[1]/div/div/p' % (row, col))
                        company_ls.append(c_col.text)
                        
                companies_ls.append(company_ls)
            except:
                try:
                    company_ls = []
                    c_name = driver.find_element(By.XPATH,
                                                        '//*[@id="react-tabs-3"]/div/div/div[1]/div/div[2]/div[%s]/div/div[2]/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div/a' % row)
                    company_ls.append(c_name.text)

                    for col in range(3, 12):
                        # Columns: [Descriptions, Industry, Country, Total Funding, All Investor, Founded Year, Latest Funding Date, Latest Funding Round, Latest Funding Amount, Latest Funding Investors]
                        # Specific colulmns [Counry, Total Funding, Founded Year]
                        if col in [3, 4]:    
                            c_col = driver.find_element(By.XPATH, '//*[@id="react-tabs-3"]/div/div/div[1]/div/div[2]/div[%s]/div/div[%s]/div/div/div[1]/div/div/div/div' % (row, col))
                            company_ls.append(c_col.text)   
                        elif col in [5, 6, 8, 10, 11]:
                            c_col = driver.find_element(By.XPATH, '//*[@id="react-tabs-3"]/div/div/div[1]/div/div[2]/div[%s]/div/div[%s]/div/div/div[1]/div/div/div' % (row, col))
                            company_ls.append(c_col.text)
                        # Investor Column with hyperlinks to each investor
                        elif col in [7, 12]:
                            pass
                            # Commented out due to efficiency issue
                            """more_investor = True
                            investor_idx = 0
                            c_col = []
                            while more_investor:
                                try:
                                    i_col = driver.find_element(By.XPATH, '//*[@id="react-tabs-3"]/div/div/div[1]/div/div[2]/div[%s]/div/div[%s]/div/div/div[1]/div/div/div/div/div[%s]/div/div/div/a' % (row, col, investor_idx))
                                    c_col.append(i_col.text)
                                    investor_idx += 1
                                except:
                                    more_investor = False

                            company_ls.append(c_col)"""
                        elif col == 9:
                            c_col = driver.find_element(By.XPATH, '//*[@id="react-tabs-3"]/div/div/div[1]/div/div[2]/div[%s]/div/div[%s]/div/div/div[1]/div/div/p' % (row, col))
                            company_ls.append(c_col.text)
                            
                    companies_ls.append(company_ls)
                except:
                    pass

        save_data_to_csv(CSV_SAVE_PATH, companies_ls, file_exists=True)


        """Move on to the next page"""
        driver.implicitly_wait(10)
        next_page_button = driver.find_element(By.XPATH, '//*[@id="react-tabs-3"]/div/div/div[2]/div/div/div[3]/div/div/button[12]/div')
        next_page_button.click()



finally:
    driver.quit()

#cell1 = driver.find_element_by_class_name('flexItem flexItem--shrink')

#print(len(cell1))

