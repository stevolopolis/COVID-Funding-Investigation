from data_loader import read_csv
from data_analysis import funding_per_month, funding_per_interval, funding_per_quarter
from visualization import vis_funding_per_interval, vis_category_line
from typing import Optional
import matplotlib.pyplot as plt


def concat_monthly_deals(monthly_deals: dict[str, dict[str, int]]) -> dict[str, int]:
    cat_monthly_deals = {}
    for year in range(15, 21):
        for month in monthly_deals[year]:
            date = '%s-%s' % (year, month)
            cat_monthly_deals[date] = monthly_deals[year][month]

    return cat_monthly_deals

# For visualizing raw fundings per month over 2015-2020
def visualize_raw_funding(metric: Optional[str] = 'sum', interval: Optional[str] = 'month') -> None:
    multi_interval_deals = {}
    for year in range(15, 21):
        csv_filepath = 'scraped_deal_data_%s.csv' % year
        deals = read_csv(csv_filepath, compressed=True)
        if interval == 'month':
            interval_deals = funding_per_month(deals, metric=metric)
        elif interval == 'quarter':
            interval_deals = funding_per_quarter(deals, metric=metric)
        multi_interval_deals[year] = interval_deals

    v_interval_deals = concat_monthly_deals(multi_interval_deals)
    vis_funding_per_interval(v_interval_deals, '2015-2020 Total Funding Graph', 'Sum of Funds')
    plt.legend()
    plt.show()

# For visualizing selected categories
def visualize_categories(category: Optional[str] = 'stage',
                         metric: Optional[str] = 'sum',
                         interval: Optional[str] = 'quarter') -> None:
    visualize = True
    fig, ax = plt.subplots(1, 1)
    while visualize:
        sum_monthly_deals = {}
        for year in range(15, 21):
            csv_filepath = 'scraped_deal_data_%s.csv' % year
            deals = read_csv(csv_filepath, compressed=True)
            categorized_deals = funding_per_interval(deals, category=category, metric=metric, interval=interval)
            for sub_category in categorized_deals:
                if sub_category not in sum_monthly_deals:
                    sum_monthly_deals[sub_category] = {}
                sum_monthly_deals[sub_category][year] = categorized_deals[sub_category]

        print(categorized_deals.keys())
        selected_category = input('Select a category: ')
        if selected_category == 'q':
            visualize = False
        elif selected_category in sum_monthly_deals:
            v_monthly_deals = concat_monthly_deals(sum_monthly_deals[selected_category])
            vis_funding_per_interval(v_monthly_deals, '2015-2020 Total Funding Graph For %s' % selected_category, selected_category, ax=ax)
        elif selected_category == 'show':
            visualize = False
            plt.legend()
            plt.show()


def visualize_multi_categories(metric: Optional[str] = 'sum', interval: Optional[str] = 'quarter') -> None:
    visualize = True
    while visualize:
        sum_monthly_deals = {}
        for year in range(15, 21):
            csv_filepath = 'scraped_deal_data_%s.csv' % year
            deals = read_csv(csv_filepath, compressed=True)
            categorized_deals = funding_per_interval(deals, category=category, metric=metric, interval=interval)
            for sub_category in categorized_deals:
                if sub_category not in sum_monthly_deals:
                    sum_monthly_deals[sub_category] = {}
                sum_monthly_deals[sub_category][year] = categorized_deals[sub_category]

        for cat in sum_monthly_deals:
            v_monthly_deals = concat_monthly_deals(sum_monthly_deals[cat])
            vis_funding_per_interval(v_monthly_deals, '2015-2020 Total Funding Graph For %s' % selected_category)


if __name__ == '__main__':
    visualize_raw_funding(metric='mean', interval='quarter')
    #visualize_categories(category='stage', metric='sum', interval='quarter')
