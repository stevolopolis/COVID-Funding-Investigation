from typing import Optional
from datetime import datetime
from data_loader import CompressedDeal
import statistics
import math

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def funding_per_category(categorized_deals_dict: dict[str, CompressedDeal], metric: Optional[str] = 'sum') -> dict[str, dict[str, int]]:
    """Return a dictionary mapping each category to a dictionary returned by funding_per_month().
    
    Used for generating monthly funding line graphs for each selected category.
    
    Sample Usage:
    
    >>> from data_loader import read_csv
    >>> deals = read_csv('scraped_deal_data_15.csv', compressed=True)
    >>> categorized_deals_dict = categorize_deals(deals, 'country')
    >>> funding_per_category(categorized_deals_dict, metric='sum')
    {'USA': {'Jan': 0, 'Feb: 0, ...}, 'China': {'Jan': 0, 'Feb: 0, ...}}
    """
    funding_per_cat = {}
    for cat in categorized_deals_dict:
        funding_per_cat[cat] = funding_per_month(categorized_deals_dict[cat], metric=metric)

    return funding_per_cat


def categorize_deals(deals: list[CompressedDeal], category: str) -> dict[str, CompressedDeal]:
    """Return a dictionary mapping each category to a list of CompressedDeals.
    
    Categories include: 'country', 'industry', 'stage', ('deal_size').

    Sample Usage:

    >>> from data_loader import read_csv
    >>> deals = read_csv('scraped_deal_data_15.csv', compressed=True)
    >>> categorize_deals(deals, 'country')
    {'USA': [slack_ipo, spotify_round_f], 'China': [didi_ipo, meituan_round_b]} # including pseudo lists of CompressedDeals
    """
    deals_dict = {}
    for deal in deals:
        if category == 'country':
            if deal.country in deals_dict:
                deals_dict[deal.country].append(deal)
            else:
                deals_dict[deal.country] = [deal]
        elif category == 'industry':
            if deal.industry in deals_dict:
                deals_dict[deal.industry].append(deal)
            else:
                deals_dict[deal.industry] = [deal]
        elif category == 'stage':
            if deal.stage in deals_dict:
                deals_dict[deal.stage].append(deal)
            else:
                deals_dict[deal.stage] = [deal]

    return deals_dict


def funding_per_month(deals: list[CompressedDeal], metric: Optional[str] = 'sum') -> dict[str, int]:
    """Return dictionary mapping month to funding amount based on a selected metric.
    
    Takes in a list of CompressedDeal generated from data_loader.py to created the corresponding dictionary.

    Metrics include: sum, mean, median, max, min
    
    Sample Usage:
    
    >>> from data_loader import read_csv
    >>> deals = read_csv('scraped_deal_data_15.csv', compressed=True)
    >>> funding_per_month(deals, metric='sum)
    {'Jan': ...}
    """
    yearly_deals = {month: [] for month in MONTHS}
    yearly_deals_metric = {month: 0 for month in MONTHS}
    for deal in deals:
        deal_date_month = datetime_to_month(deal.deal_date)
        yearly_deals[deal_date_month].append(deal.deal_size)
        
    for m in yearly_deals:
        if metric == 'sum':
            yearly_deals_metric[m] = sum(yearly_deals[m])
        elif metric == 'mean':
            yearly_deals_metric[m] = statistics.mean(yearly_deals[m])
        elif metric == 'median':
            yearly_deals_metric[m] = statistics.median(yearly_deals[m])
        elif metric == 'max':
            yearly_deals_metric[m] = max(yearly_deals[m])
        elif metric == 'min':
            yearly_deals_metric[m] = min(yearly_deals[m])

    return yearly_deals_metric


def datetime_to_month(date: datetime) -> str:
    month_int = datetime.strptime('%m')
    return MONTHS[month_int - 1]