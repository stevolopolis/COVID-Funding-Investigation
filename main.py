from data_loader import read_csv
from data_analysis import funding_per_month
from visualization import vis_funding_per_month
from pprint import pprint

csv_filepath = 'scraped_deal_data_15.csv'
deals = read_csv(csv_filepath, compressed=True)
pprint(deals[:10])
monthly_deals = funding_per_month(deals, metric='sum')
print(monthly_deals)
vis_funding_per_month(monthly_deals, '2015 Total Funding Graph')
