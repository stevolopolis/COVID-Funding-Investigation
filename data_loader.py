import csv
import datetime
from dataclasses import dataclass


@dataclass
class Deal:
    """A funding deal made to a company.
    
    Rounds include: seed, A-E, IPO.

    This dataclass will be used to store data from the csv files in a more orderly manner.

    Instance Attributes:
        - company: the name of the funded company
        - stage: funding stage
        - deal_size: size of the deal in USD
        - deal_date: date of the funding deal
        - r_investors: list of investors in the current funding round
        - description: basic description of the company
        - industry: industry of the company (e.g. technology, software)
        - country: country of the company
        - total_funding: total amount of funding in USD received by the company
        - a_investors: list of all investors that has invested into the company
    """
    company: str
    stage: str
    deal_size: int
    deal_date: datetime.datetime
    r_investors: list[str]
    description: str
    industry: str
    country: str
    total_funding: int
    a_investors: list[str]


@dataclass
class CompressedDeal: 
    """A funding deal made to a company.
    
    Rounds include: seed, A-E, IPO.

    This dataclass is a compressed version of Deal which could save memory space during inference.
    It will be used exclusively for analyzing any patterns in raw funding amounts.

    Instance Attributes:
        - company: the name of the funded company
        - stage: funding stage
        - deal_size: size of the deal in USD
        - deal_date: date of the funding deal
        - industry: industry of the company (e.g. technology, software)
        - country: country of the company
        - total_funding: total amount of funding in USD received by the company
    """
    company: str
    stage: str
    deal_size: int
    deal_date: datetime.datetime
    industry: str
    country: str
    total_funding: int


def read_csv(csv_path: str, compressed: bool) -> list[CompressedDeal]:
    """Return a list of CompressedDeal/Deal based on the data in a csv filepath. 

    If compressed is True, a list of CompressedDeal would be returned. Using a list of CompressedDeal
    will be more memory efficient than using a list of Deal as the descriptions and investor details
    are omitted. This is appropriate when we are only analysing the patterns in funding amounts
    rather than the identities of the companies or the investors.

    The data in csv files have 10 columns, each corresponding to a category of data as shown in the
    order of the instance attributes in Deal. All data are stored as strings, hence corresponding 
    data type conversion will also be handled in this function."""
    deal_ls = []
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)  # skip the header

        for deal_row in reader:
            if compressed:
                deal = CompressedDeal(deal_row[0],
                                      deal_row[1],
                                      str_funding_to_int(deal_row[2]),
                                      str_deal_date_to_datetime(deal_row[3]),
                                      deal_row[6],
                                      deal_row[7],
                                      str_funding_to_int(deal_row[8]))
            else:
                deal = Deal(deal_row[0],
                            deal_row[1],
                            str_funding_to_int(deal_row[2]),
                            str_deal_date_to_datetime(deal_row[3]),
                            str_investors_to_list(deal_row[4]),
                            deal_row[5],
                            deal_row[6],
                            deal_row[7],
                            str_funding_to_int(deal_row[8]),
                            str_investors_to_list(deal_row[9]))

            deal_ls.append(deal)

    return deal_ls


def str_funding_to_int(funding_str: str) -> int:
    """Convert funding strings into integer values.
    
    Funding strings in CSV files are in the following format: '$1,000.00M'.
    For rows/deals that do not have funding amount data, they will be saved
    as empty strings or 'N/A'. These will be treated as 0.
    
    Sample Usage:

    >>> str_funding_to_int('$1,000.00M')
    1000000
    >>> str_funding_to_int('$0.02M')
    20000
    >>> str_funding_to_int('N/A')
    0
    """
    if funding_str == '' or funding_str == 'N/A':
        return 0
    else:
        funding_str = funding_str[1:-1].replace(',', '') # remove '$', 'M', and ',' from string
        funding_int = float(funding_str) * 1000000
        return funding_int


def str_deal_date_to_datetime(deal_date_str: str) -> datetime.datetime:
    """Convert deal date strings into datetime objects.
    
    Deal date strings in CSV files are in the following format: '10/19/2017'
    
    Sample Usage:
    
    >>> str_deal_date_to_datetime('10/19/2017')
    datetime.datetime(2017, 19, 10)
    """
    day = int(deal_date_str.split('/')[1])
    month = int(deal_date_str.split('/')[0])
    year = int(deal_date_str.split('/')[2])
    return datetime.datetime(year, month, day)


def str_investors_to_list(investors_str: str) -> list[str]:
    """Convert investors strings into list of investor strings.
    
    Sample Usage:
    
    >>> str_investors_to_list('YC, Andreesson Horowitz, Tiger Global')
    ['YC', 'Andreessen Horowitz', 'Tiger Global']
    """
    return investors_str.split(', ')
