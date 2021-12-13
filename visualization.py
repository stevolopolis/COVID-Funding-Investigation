"""Data visualization

This file contains functions that visualize the scraped data in 
different ways. The functions are varied in terms of the interval of
each data point, the category of data visualizing, or the type of 
graph used to visualize the data. 

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of interested personel
for investigating the funding data over the COVID-19 period. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2021 Steven T. S., Luo.
"""

import math
from typing import Optional
import matplotlib.pyplot as plt

COLORS = ['gold', 'lightcoral', 'yellowgreen', 'turquoise', 'cornflowerblue',
          'mediumpurple', 'orange', 'palegreen', 'slategray', 'peru']


def vis_funding_per_interval(interval_deals: dict[str, int],
                             title: str,
                             label: str,
                             ax: Optional[plt.Axes] = None) -> None:
    """Visualizes the deals with given intervals using a line graph."""

    intervals = interval_deals.keys()
    funds = interval_deals.values()

    if ax is None:
        plt.plot(intervals, funds, label=label)
        plt.title(title)
        plt.xlabel('Dates')
        plt.ylabel('Funds')
    else:
        ax.plot(intervals, funds, label=label)
        ax.set_title(title)
        ax.set_xlabel('Dates')
        ax.set_ylabel('Funds')

    plt.xticks(rotation='vertical')


def vis_category_line(funding_per_cat: dict[str, dict[str, int]],
                      category: str,
                      title: str) -> None:
    """Visualize monthly deals of a selected category using line graphs.

    Outputs len(funding_per_cat) graphs in total."""
    n_cats = len(funding_per_cat)
    n_rows = math.ceil(n_cats / 3)
    _, ax = plt.subplots(n_rows, 3)
    for i, cat in enumerate(funding_per_cat):
        intervals = funding_per_cat[cat].keys()
        funds = funding_per_cat[cat].values()

        subplot_row = i // 3
        subplot_col = i - (subplot_row * 3)
        ax[subplot_row, subplot_col].plot(intervals, funds)
        ax[subplot_row, subplot_col].set_title('%s -- %s' % (category, cat))

    plt.title(title)


def vis_multi_category_line(funding_per_cat: dict[str, dict[str, int]], title: str) -> None:
    """Visualize monthly deals of a selected category using line graphs.
    
    Outputs only one graph with len(funding_per_cat) number of lines."""
    for cat in funding_per_cat:
        intervals = funding_per_cat[cat].keys()
        funds = funding_per_cat[cat].values()

        plt.plot(intervals, funds)
        plt.title(title)
        plt.xticks(rotation='vertical')
        plt.xlabel('Dates')
        plt.ylabel('Funds')


def vis_category_pie(funding_per_cat: dict[str, int],
                     title: str,
                     top_n: Optional[int] = 4,
                     ax: Optional[plt.Axes] = None) -> None:
    """Visualize top funding amounts during COVID period of
    a selected category using a pie chart."""
    ranked_categories = sort_dict(funding_per_cat)
    top_n_ranked_categories = choose_top_n(ranked_categories, top_n)
    labels = list(top_n_ranked_categories.keys())
    sizes = list(top_n_ranked_categories.values())
    sizes_millions = [round(num / 1000000, 2) for num in sizes]

    custom_colors = COLORS[: top_n + 1]

    if ax:
        ax.pie(sizes_millions, labels=labels, colors=custom_colors, autopct='%.1fM', startangle=90)
        ax.set_title(title)
    else:
        plt.pie(sizes_millions, labels=labels, colors=custom_colors, autopct='%.1fM', startangle=90)
        plt.title(title)


def vis_covid_line(interval: str) -> None:
    """Plot red vertical line at the time of start of COVID-19
    
    COVID-19 assumed to start in 2020 January / 2020 Q1."""
    if interval == 'month':
        plt.plot('20-Jan', color='r', linestyle='-', label='Start of COVID')
    elif interval == 'quarter':
        plt.axvline(x='20-Q1', color='r', linestyle='-', label='Start of COVID')


def sort_dict(unsorted_dict: dict[str, int]) -> dict[str, int]:
    """Return sorted dictionary mapping category names to funding amounts based on
    the funding amount. Sorts by highest funding amount to lowest.
    
    Sample Usage:
    >>> sample_dict = {'b': 10, 'a': 100, 'd': 1, 'c': 5}
    >>> sort_dict(sample_dict)
    {'a': 100, 'b': 10, 'c': 5, 'd': 1}
    """
    sorted_list = sorted([(value, key) for key, value in unsorted_dict.items()], reverse=True)
    return {key: value for value, key in sorted_list}


def choose_top_n(sorted_dict: dict[str, int], top_n: int) -> list[tuple[str, int]]:
    """Return first n key-value pairs of a sorted dictionary.
    
    Sample Usage:
    >>> sorted_dict = {'a': 100, 'b': 10, 'c': 5, 'd': 1}
    >>> choose_to_n(sorted_dict, 3)
    {'a': 100, 'b': 10, 'c': 5}
    """
    top_n_dict = {}
    others_sum = 0
    for i, key in enumerate(sorted_dict):
        if i >= top_n:
            others_sum += sorted_dict[key]
        else:
            top_n_dict[key] = sorted_dict[key]
    top_n_dict['others'] = others_sum

    return top_n_dict
