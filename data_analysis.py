"""Deals Data Analysis

This file contains functions that analyses the deals data
from lists of CompressedDeals. Each function returns the funding
data in varying metrics such as funding per month, per country, or
per industry. Each function also takes in varying analysis metrics
such as whether relative or absolute values are reported, or whether
the mean, median, sum, etc. of funding amounts are reported. 

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of interested personel
for investigating the funding data over the COVID-19 period. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2021 Steven T. S., Luo.
"""

import statistics
from typing import Optional
from datetime import datetime
from data_loader import CompressedDeal

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def funding_per_interval(deals: list[CompressedDeal],
                         category: str,
                         metric: Optional[str] = 'sum',
                         interval: Optional[str] = 'month',
                         rel: Optional[bool] = False) -> dict[str, dict[str, int]]:
    """Return a dictionary mapping each category to a dictionary returned by funding_per_month().
    
    Used for generating monthly funding line graphs for each selected category.
    
    Sample Usage:
    
    >>> from data_loader import read_csv
    >>> deals = read_csv('data/sample_deal_data_15.csv', compressed=True)
    >>> funding_per_category(deals, metric='sum')
    {'USA': {'Jan': 5000000, 'Feb': 3000000, ...}, 'China': {'Jan': 3000000, 'Feb': 5000000, ...}}
    """
    categorized_deals_dict = categorize_deals(deals, category)
    funding_per_cat = {}
    for cat in categorized_deals_dict:
        if interval == 'month':
            funding_per_cat[cat] = funding_per_month(categorized_deals_dict[cat],
                                                     metric=metric,
                                                     rel=rel)
        elif interval == 'quarter':
            funding_per_cat[cat] = funding_per_quarter(categorized_deals_dict[cat],
                                                       metric=metric,
                                                       rel=rel)

    return funding_per_cat


def categorize_deals(deals: list[CompressedDeal], category: str) -> dict[str, CompressedDeal]:
    """Return a dictionary mapping each category to a list of CompressedDeals.
    
    Categories include: 'country', 'industry', 'stage', ('deal_size').

    Sample Usage:

    >>> from data_loader import read_csv
    >>> deals = read_csv('data/sample_deal_data_15.csv', compressed=True)
    >>> categorize_deals(deals, 'country')
    {'USA': [slack_ipo, spotify_round_f], 'China': [didi_ipo, meituan_round_b]}  # pseudo lists of CompressedDeals
    """
    deals_dict = {}
    for deal in deals:
        if category == 'country':
            if deal.deal_size == 0 or deal.country == '':
                continue
            elif deal.country in deals_dict:
                deals_dict[deal.country].append(deal)
            else:
                deals_dict[deal.country] = [deal]
        elif category == 'industry':
            if deal.deal_size == 0 or deal.industry == '':
                continue
            elif deal.industry in deals_dict:
                deals_dict[deal.industry].append(deal)
            else:
                deals_dict[deal.industry] = [deal]
        elif category == 'stage':
            if deal.deal_size == 0 or deal.stage == '':
                continue
            elif deal.stage in deals_dict:
                deals_dict[deal.stage].append(deal)
            else:
                deals_dict[deal.stage] = [deal]
        elif category == 'company':
            if deal.deal_size == 0 or deal.company == '':
                continue
            elif deal.company in deals_dict:
                deals_dict[deal.company].append(deal)
            else:
                deals_dict[deal.company] = [deal]
    return deals_dict


def funding_per_category(deals: list[CompressedDeal], year: str, category: str) -> dict[str, int]:
    """Return a dictionary mapping groups of a category to their
    total funding amounts during covid.
    
    The covid period is defined to start from 20-Jan to 20-Dec. 
    (Optional: create slider to control the definition of 'covid period'.)

    Precondition:
        - year in ['15', '16', '17', '18', '19', '20', '21']
        - category in ['country', 'company']
    
    Sample Usage:
    >>> from data_loader import read_csv
    >>> deals = read_csv('data/sample_deal_data_15.csv, compressed=True)
    >>> funding_per_category(deals, '20', 'country')
    {'United States': 55000000, 'China': 20000000}
    """
    cat_deals_dict = categorize_deals(deals, category)
    cat_deal_sum_dict = {c: 0 for c in cat_deals_dict}
    for cat in cat_deals_dict:
        for deal in cat_deals_dict[cat]:
            deal_year = datetime_to_year(deal.deal_date)
            if deal_year == year:
                cat_deal_sum_dict[cat] += deal.deal_size
    
    return cat_deal_sum_dict


def funding_per_quarter(deals: list[CompressedDeal],
                        metric: Optional[str] = 'sum',
                        rel: Optional[bool] = False) -> dict[str, int]:
    """Return dictionary mapping quarters to funding amount based on a selected metric.
    
    Takes in a list of CompressedDeal generated from data_loader.py to
    create the corresponding dictionary.

    Metrics include: sum, mean, median, max, min
    
    Sample Usage:
    
    >>> from data_loader import read_csv
    >>> deals = read_csv('data/sample_deal_data_15.csv', compressed=True)
    >>> funding_per_month(deals, metric='sum)
    {'Q1': 12000000, 'Q2': 15000000, 'Q3': 9000000, 'Q4': 25000000}
    """
    quarterly_deals = {'Q1': [], 'Q2': [], 'Q3': [], 'Q4': []}
    quarterly_deals_metrics = {'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0}
    for deal in deals:
        deal_date_month = datetime_to_month(deal.deal_date)
        if deal_date_month in ['Jan', 'Feb', 'Mar']:
            if rel:
                quarterly_deals['Q1'].append(get_rel_deal_size(deal))
            else:
                quarterly_deals['Q1'].append(deal.deal_size)
        elif deal_date_month in ['Apr', 'May', 'Jun']:
            if rel:
                quarterly_deals['Q2'].append(get_rel_deal_size(deal))
            else:
                quarterly_deals['Q2'].append(deal.deal_size)
        elif deal_date_month in ['Jul', 'Aug', 'Sep']:
            if rel:
                quarterly_deals['Q3'].append(get_rel_deal_size(deal))
            else:
                quarterly_deals['Q3'].append(deal.deal_size)
        elif deal_date_month in ['Oct', 'Nov', 'Dec']:
            if rel:
                quarterly_deals['Q4'].append(get_rel_deal_size(deal))
            else:
                quarterly_deals['Q4'].append(deal.deal_size)
        
    for m in quarterly_deals:
        if metric == 'sum':
            quarterly_deals_metrics[m] = sum(quarterly_deals[m])
        elif metric == 'mean':
            quarterly_deals_metrics[m] = get_mean(quarterly_deals[m])
        elif metric == 'median':
            quarterly_deals_metrics[m] = get_median(quarterly_deals[m])
        elif metric == 'max':
            quarterly_deals_metrics[m] = max(quarterly_deals[m])
        elif metric == 'min':
            quarterly_deals_metrics[m] = min(quarterly_deals[m])

    return quarterly_deals_metrics


def funding_per_month(deals: list[CompressedDeal],
                      metric: Optional[str] = 'sum',
                      rel: Optional[bool] = False) -> dict[str, int]:
    """Return dictionary mapping month to funding amount based on a selected metric.
    
    Takes in a list of CompressedDeal generated from data_loader.py to created the corresponding dictionary.

    Metrics include: sum, mean, median, max, min
    
    Sample Usage:
    
    >>> from data_loader import read_csv
    >>> deals = read_csv('data/sample_deal_data_15.csv', compressed=True)
    >>> funding_per_month(deals, metric='sum)
    {'Jan': 15000000, 'Feb': 25000000, ...}
    """
    monthly_deals = {month: [] for month in MONTHS}
    monthly_deals_metric = {month: 0 for month in MONTHS}
    for deal in deals:
        deal_date_month = datetime_to_month(deal.deal_date)
        if rel:
            monthly_deals[deal_date_month].append(get_rel_deal_size(deal))
        else:
            monthly_deals[deal_date_month].append(deal.deal_size)
        
    for m in monthly_deals:
        if metric == 'sum':
            monthly_deals_metric[m] = sum(monthly_deals[m])
        elif metric == 'mean':
            monthly_deals_metric[m] = get_mean(monthly_deals[m])
        elif metric == 'median':
            monthly_deals_metric[m] = get_median(monthly_deals[m])
        elif metric == 'max':
            monthly_deals_metric[m] = max(monthly_deals[m])
        elif metric == 'min':
            monthly_deals_metric[m] = min(monthly_deals[m])

    return monthly_deals_metric


def datetime_to_month(date: datetime) -> str:
    """Return CBI-format month string from datetime object
    
    Sample Usage:
    >>> datetime_to_month(datetime(2020, 10, 23))
    'Oct'
    >>> datetime_to_month(datetime(2019, 1 23))
    'Jan'
    """
    month_int = int(date.strftime('%m'))
    return MONTHS[month_int - 1]


def datetime_to_year(date: datetime) -> str:
    """Return CBI-format year string from datetime object
    
    Sample Usage:
    >>> datetime_to_month(datetime(2020, 10, 23))
    '20'
    >>> datetime_to_month(datetime(2009, 1 23))
    '09'
    """
    year_int = int(date.strftime('%y'))
    return str(year_int)


def get_mean(data_ls: list[int]) -> int:
    """Return mean of a list of integers.

    Returns 0 if the list is empty.
    """
    if len(data_ls) == 0:
        return 0
    else:
        return statistics.mean(data_ls)


def get_median(data_ls: list[int]) -> int:
    """Return median of a list of integers.

    Returns 0 if the list is empty.
    """
    if len(data_ls) == 0:
        return 0
    else:
        return statistics.median(data_ls)


def get_rel_deal_size(deal: CompressedDeal) -> float:
    """Return relative deal size of a CompressedDeal object.
    
    Relative deal size is defined to be the ratio of the
    deal size to the total funding size.

    Return 1 if CompressedDeal.total_funding is zero.

    Sample Usage:
    >>> deal = CompressedDeal('Shopify', 'Stage A', 1000000, datetime(2020, 10, 23), 'eCommerce', 'Canada', 2000000)
    >>> get_rel_deal_size(deal)
    0.5
    >>> deal = CompressedDeal('Spotify', 'Stage A', 1000000, datetime(2017, 5, 2), 'Internet', 'United States', 0)
    >>> get_rel_deal_size(deal)
    1.0
    """
    if deal.total_funding == 0:
        return 1.0
    else:
        return deal.deal_size / deal.total_funding
