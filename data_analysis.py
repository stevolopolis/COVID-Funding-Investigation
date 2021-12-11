from typing import Optional
from datetime import datetime
from data_loader import CompressedDeal
import statistics
import math

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def funding_per_interval(deals: list[CompressedDeal], category: str, metric: Optional[str] = 'sum', interval: Optional[str] = 'month', rel: Optional[bool] = False) -> dict[str, dict[str, int]]:
    """Return a dictionary mapping each category to a dictionary returned by funding_per_month().
    
    Used for generating monthly funding line graphs for each selected category.
    
    Sample Usage:
    
    >>> from data_loader import read_csv
    >>> deals = read_csv('scraped_deal_data_15.csv', compressed=True)
    >>> funding_per_category(deals, metric='sum')
    {'USA': {'Jan': 0, 'Feb: 0, ...}, 'China': {'Jan': 0, 'Feb: 0, ...}}
    """
    categorized_deals_dict = categorize_deals(deals, category)
    funding_per_cat = {}
    for cat in categorized_deals_dict:
        if interval == 'month':
            funding_per_cat[cat] = funding_per_month(categorized_deals_dict[cat], metric=metric, rel=rel)
        elif interval == 'quarter':
            funding_per_cat[cat] = funding_per_quarter(categorized_deals_dict[cat], metric=metric, rel=rel)

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


def funding_per_country(deals: list[CompressedDeal], year: str) -> dict[str, int]:
    """Return a dictionary mapping countries to their total funding amounts during covid.
    
    The covid period is defined to start from 20-Jan to 20-Dec. 
    (Optional: create slider to control the definition of 'covid period'.)
    
    Sample Usage:
    >>> from data_loader import read_csv
    >>> deals = read_csv('scraped_deal_data_15.csv, compressed=True)
    >>> funding_per_country(deals)
    {'United States': ..., 'China': ..., ...}
    """
    country_deals_dict = categorize_deals(deals, 'country')
    country_year_deals = {country: 0 for country in country_deals_dict}
    for country in country_deals_dict:
        for deal in country_deals_dict[country]:
            deal_year = datetime_to_year(deal.deal_date)
            if deal_year == year:
                country_year_deals[country] += deal.deal_size
    
    return country_year_deals


def funding_per_company(deals: list[CompressedDeal], year:str) -> dict[str, int]:
    """Return a dictionary mapping companies to their total funding amounts during covid.
    
    The covid period is defined to start from 20-Jan to 20-Dec. 
    (Optional: create slider to control the definition of 'covid period'.)
    
    Sample Usage:
    >>> from data_loader import read_csv
    >>> deals = read_csv('scraped_deal_data_15.csv, compressed=True)
    >>> funding_per_company(deals)
    {'Spotify': ..., 'Slack': ..., ...}
    """
    company_deals_dict = categorize_deals(deals, 'company')
    country_year_deals = {company: 0 for company in company_deals_dict}
    for company in company_deals_dict:
        for deal in company_deals_dict[company]:
            deal_year = datetime_to_year(deal.deal_date)
            if deal_year == year:
                country_year_deals[company] += deal.deal_size

    return country_year_deals


def funding_per_company_type(deals: list[CompressedDeal], rel: Optional[bool] = False) -> dict[str, int]:
    return None


def funding_per_quarter(deals: list[CompressedDeal], metric: Optional[str] = 'sum', rel: Optional[bool] = False) -> dict[str, int]:
    """Return dictionary mapping quarters to funding amount based on a selected metric.
    
    Takes in a list of CompressedDeal generated from data_loader.py to created the corresponding dictionary.

    Metrics include: sum, mean, median, max, min
    
    Sample Usage:
    
    >>> from data_loader import read_csv
    >>> deals = read_csv('scraped_deal_data_15.csv', compressed=True)
    >>> funding_per_month(deals, metric='sum)
    {'Q1': ..., 'Q2': ..., ...}
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

def funding_per_month(deals: list[CompressedDeal], metric: Optional[str] = 'sum', rel: Optional[bool] = False) -> dict[str, int]:
    """Return dictionary mapping month to funding amount based on a selected metric.
    
    Takes in a list of CompressedDeal generated from data_loader.py to created the corresponding dictionary.

    Metrics include: sum, mean, median, max, min
    
    Sample Usage:
    
    >>> from data_loader import read_csv
    >>> deals = read_csv('scraped_deal_data_15.csv', compressed=True)
    >>> funding_per_month(deals, metric='sum)
    {'Jan': ...}
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
    month_int = int(date.strftime('%m'))
    return MONTHS[month_int - 1]


def datetime_to_year(date: datetime) -> str:
    year_int = int(date.strftime('%y'))
    return str(year_int)


def get_mean(data_ls: list[int]) -> int:
    if len(data_ls) == 0:
        return 0
    else:
        return statistics.mean(data_ls)


def get_median(data_ls: list[int]) -> int:
    if len(data_ls) == 0:
        return 0
    else:
        return statistics.median(data_ls)


def get_rel_deal_size(deal: CompressedDeal):
    if deal.total_funding == 0:
        return 0 # Subjected to change 
    else:
        return deal.deal_size / deal.total_funding
