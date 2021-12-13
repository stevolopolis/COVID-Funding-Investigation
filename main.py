"""Main

This file provides an interactive session in the terminal when ran. 
Based on the users inputs, this file will do webscraping, data loading,
data analysis, and data visualization accordingly.

If you are running this file in its native directory, input "n" when
the program asks you whether you have scraped the data already. Inputing "y"
may change the data files originally saved in the 'data' sub directory.

You may choose to visualize pie graphs or line graphs to your liking.
While the pie graphs show you the top fund receivers of each chosen category,
the line graphs show you the trend of the funding amounts of each chosen
category over the covid period.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of interested personel
for investigating the funding data over the COVID-19 period. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2021 Steven T. S., Luo.
"""

from cbi_deal_scrape import DataScraper
from visualization import visualize_raw_funding, visualize_categories, visualize_multi_year_pie, visualize_covid_pie

# My Personal logins for CB-insights using UofT account.
# Do not disclose this information to other people.
USERNAME = 'stevents.luo@mail.utoronto.ca'
PASSWORD = 'rma.HF!v38N5*jq'
CSV_SAVE_DIR = 'data'  # directory containing / to save webscraped csv files
N_PIE_WEDGES = 4  # number of wedges in the pie graphs. Default = 4 for clarity

if __name__ == '__main__':
    user_input_scrape = input('Have you scraped the data? ("y" or "n")\n')
    if user_input_scrape == 'n':
        data_scraper = DataScraper(USERNAME, PASSWORD, CSV_SAVE_DIR)
        data_scraper.scrape_15_21()

    user_input_visualize = input('Start visualizing? ("y" or "n")\n')
    while user_input_visualize == 'y':
        user_input_graph_type = input('Would you like to visualize pie graphs or line graphs? ("p" or "l")\n')
        if user_input_graph_type == 'l':
            user_input_line_cat = input('What category would you like to visualize? ("sum", "country", "industry", "stage")\n')
            user_input_metric = input('What statistical metric would you like to use? ("sum", "mean", "median", "max", "min")\n')
            user_input_fund_metric = input('What funding metric would you like to use? ("abs" or "rel")\n')
            if user_input_fund_metric == 'abs':
                user_input_rel = False
            elif user_input_fund_metric == 'rel':
                user_input_rel = True

            user_input_interval = input('What interval of data would you like to display? ("month" or "quarter")\n')
            if user_input_line_cat == 'sum':
                visualize_raw_funding(CSV_SAVE_DIR, metric=user_input_metric, interval=user_input_interval, rel=user_input_rel)
            else:
                visualize_categories(CSV_SAVE_DIR, category=user_input_line_cat, metric=user_input_metric, interval=user_input_interval, rel=user_input_rel)
        elif user_input_graph_type == 'p':
            user_input_pie_cat = input('What category would you like to visualize? ("company", "country", "industry", "stage")\n')
            user_input_multi_year = input('Would you like to visualize multiple years of pie graph? ("y" or "n")\n')
            if user_input_multi_year == 'y':
                visualize_multi_year_pie(CSV_SAVE_DIR, category=user_input_pie_cat, top_n=N_PIE_WEDGES, start_year='18', end_year='21')
            elif user_input_multi_year == 'n':
                visualize_covid_pie(CSV_SAVE_DIR, category=user_input_pie_cat, top_n=N_PIE_WEDGES)

        user_input_visualize = input('Continue visualizing? ("y" or "n")\n')
