from data_loader import read_csv
from data_analysis import funding_per_month, funding_per_category
from visualization import vis_funding_per_month, vis_category_line

sum_monthly_deals = {}
for year in range(15, 21):
    csv_filepath = 'scraped_deal_data_%s.csv' % year
    deals = read_csv(csv_filepath, compressed=True)
    monthly_deals = funding_per_month(deals, metric='sum')
    for month in monthly_deals:
        date = '%s-%s' % (year, month)
        sum_monthly_deals[date] = monthly_deals[month]

vis_funding_per_month(sum_monthly_deals, '2015-2020 Total Funding Graph')


"""# For categorized Visualization
csv_filepath = 'scraped_deal_data_15.csv'
deals = read_csv(csv_filepath, compressed=True)
categorized_deals = funding_per_category(deals, category='stage', metric='sum')
vis_category_line(categorized_deals, 'stage', 'Category: stage')"""
