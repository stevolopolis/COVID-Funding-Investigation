from matplotlib import use
from data_loader import read_csv
from data_analysis import funding_per_month, funding_per_interval, funding_per_quarter, funding_per_company, funding_per_country
from visualization import vis_funding_per_interval, vis_category_line, vis_covid_line, vis_category_pie
from typing import Optional
import matplotlib.pyplot as plt


def concat_monthly_deals(monthly_deals: dict[str, dict[str, int]]) -> dict[str, int]:
    """Return a dictionary mapping dates in the form of '<year>-<month>' to the corresponding fundings.
    Takes in a dictionary mapping years to a dictionary of monthly deals."""
    cat_monthly_deals = {}
    for year in range(15, 22):
        for month in monthly_deals[year]:
            date = '%s-%s' % (year, month)
            cat_monthly_deals[date] = monthly_deals[year][month]

    return cat_monthly_deals

# For visualizing raw fundings per month over 2015-2020
def visualize_raw_funding(metric: Optional[str] = 'sum', interval: Optional[str] = 'month', rel: Optional[bool] = False) -> None:
    """Visualize line graph of raw funding amounts from 2015 to 2020.
    Includes options to select metrics (as mentioned in data_analysis.py) and intervals ('month', 'quarter')."""
    fig, ax = plt.subplots(figsize=(10, 6))

    multi_interval_deals = {}
    for year in range(15, 22):
        csv_filepath = 'scraped_deal_data_%s.csv' % year
        deals = read_csv(csv_filepath, compressed=True)
        if interval == 'month':
            interval_deals = funding_per_month(deals, metric=metric, rel=rel)
        elif interval == 'quarter':
            interval_deals = funding_per_quarter(deals, metric=metric, rel=rel)
        multi_interval_deals[year] = interval_deals

    v_interval_deals = concat_monthly_deals(multi_interval_deals)
    vis_funding_per_interval(v_interval_deals, '2015-2021 Total Funding Graph', '%s of Funds' % metric, ax=ax)
    vis_covid_line(interval)
    plt.legend()
    plt.show()


# For visualizing selected categories
def visualize_categories(category: Optional[str] = 'stage',
                         metric: Optional[str] = 'sum',
                         interval: Optional[str] = 'quarter',
                         rel: Optional[bool] = False) -> None:
    """VIsualize line graphs of funding amounts based on the selected category.
    Takes in inference-time user input for the sub-categories to be visualized."""
    visualize = True
    fig, ax = plt.subplots(figsize=(10, 6))
    while visualize:
        sum_monthly_deals = {}
        for year in range(15, 22):
            csv_filepath = 'scraped_deal_data_%s.csv' % year
            deals = read_csv(csv_filepath, compressed=True)
            categorized_deals = funding_per_interval(deals, category=category, metric=metric, interval=interval, rel=rel)
            for sub_category in categorized_deals:
                if sub_category not in sum_monthly_deals:
                    sum_monthly_deals[sub_category] = {}
                sum_monthly_deals[sub_category][year] = categorized_deals[sub_category]

        print(list(categorized_deals.keys()))
        selected_category = input('Select a sub-category or "q" to exit or "show" to visualize.\n')
        if selected_category == 'q':
            visualize = False
        elif selected_category in sum_monthly_deals:
            v_monthly_deals = concat_monthly_deals(sum_monthly_deals[selected_category])
            vis_funding_per_interval(v_monthly_deals, '2015-2021 Total Funding Graph For %s' % selected_category, selected_category, ax=ax)
        elif selected_category == 'show':
            visualize = False
            vis_covid_line(interval)
            plt.legend()
            plt.show()


def visualize_multi_year_pie(category: Optional[str] = 'country', start_year: Optional[str] = '18', end_year: Optional[str] = '21') -> None:
    """"""
    fig, ax = plt.subplots(2, 2, figsize=(9, 7))

    multi_year_deals = []
    for year in range(15, 22):
        csv_filepath = 'scraped_deal_data_%s.csv' % year
        deals = read_csv(csv_filepath, compressed=True)
        multi_year_deals += deals

    for selected_year in range(int(start_year), int(end_year) + 1):
        category_fundings = funding_per_country(multi_year_deals, year=str(selected_year))
        vis_category_pie(category_fundings, '%s Total Funding Pie Chart' % selected_year, ax=ax[(selected_year - 18) // 2, (selected_year - 18) % 2])
    plt.show()


def visualize_covid_pie(category: Optional[str] = 'country', top_n: Optional[int] = 4) -> None:
    """"""
    fig, ax = plt.subplots(figsize=(9, 7))

    multi_year_deals = []
    for year in range(15, 22):
        csv_filepath = 'scraped_deal_data_%s.csv' % year
        deals = read_csv(csv_filepath, compressed=True)
        multi_year_deals += deals

    if category == 'country':
        category_fundings = funding_per_country(multi_year_deals, year='20')
        vis_category_pie(category_fundings, 'COVID Period Total Funding Pie Chart For Country', top_n=top_n, ax=ax)
    elif category == 'company':
        category_fundings = funding_per_company(multi_year_deals, year='20')
        vis_category_pie(category_fundings, 'COVID Period Total Funding Pie Chart For Companies', top_n=top_n, ax=ax)
    plt.show()


if __name__ == '__main__':
    """user_input_visualize = input('Start visualizing? ("y" or "n")\n')
    while user_input_visualize == 'y':
        user_input_cat = input('What category would you like to visualize? ("sum", "country", "industry", "stage")\n')
        user_input_metric = input('What statistical metric would you like to use? ("sum", "mean", "median", "max", "min")\n')
        if input('What funding metric would you like to use? ("abs" or "rel")\n') == 'abs':
            user_input_rel = False
        else:
            user_input_rel = True

        user_input_interval = input('What interval of data would you like to display? ("month", "quarter")\n')
        if user_input_cat == 'sum':
            visualize_raw_funding(metric=user_input_metric, interval=user_input_interval, rel=user_input_rel)
        else:
            visualize_categories(category=user_input_cat, metric=user_input_metric, interval=user_input_interval, rel=user_input_rel)

        user_input_visualize = input('Continue visualizing? ("y" or "n")\n')"""

    #visualize_multi_year_pie(category='country', start_year='18', end_year='21')
    visualize_covid_pie(category='country', top_n=5)
