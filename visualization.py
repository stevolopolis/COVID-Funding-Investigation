import matplotlib.pyplot as plt
import math
from typing import Optional


def vis_funding_per_interval(interval_deals: dict[str, int], title: str, label: str, ax: Optional[plt.Axes] = None) -> None:
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
    #plt.show()


def vis_category_line(funding_per_cat: dict[str, dict[str, int]], category: str, title: str) -> None:
    """Visualize multiple monthly deals based on selected category using line graphs.
    Outputs len(funding_per_cat) graphs in total."""
    n_cats = len(funding_per_cat)
    n_rows = math.ceil(n_cats / 3)
    fig, ax = plt.subplots(n_rows, 3)
    for i, cat in enumerate(funding_per_cat):
        intervals = funding_per_cat[cat].keys()
        funds = funding_per_cat[cat].values()

        subplot_row = i // 3
        subplot_col = i - (subplot_row * 3)
        ax[subplot_row, subplot_col].plot(intervals, funds)
        ax[subplot_row, subplot_col].set_title('%s -- %s' % (category, cat))
    
    plt.title(title)
    plt.show()


def vis_multi_category_line(funding_per_cat: dict[str, dict[str, int]], title: str) -> None:
    """Visualize multiple monthly deals based on selected category using line graphs.
    
    Outputs only one graph with len(funding_per_cat) number of lines."""
    for cat in funding_per_cat:
        intervals = funding_per_cat[cat].keys()
        funds = funding_per_cat[cat].values()

        plt.plot(intervals, funds)
        plt.title(title)
        plt.xticks(rotation='vertical')
        plt.xlabel('Dates')
        plt.ylabel('Funds')
    plt.show()


def vis_category_pie(funding_per_cat: dict[str, dict[str, int]], category: str) -> None:
    """Visualize multiply monthly deals based on selected category using a pie chart."""


def vis_covid_line(interval):
    if interval == 'month':
        plt.plot('20-Jan', color='r', linestyle='-', label='Start of COVID')
    elif interval == 'quarter':
        plt.axvline(x='20-Q1', color='r', linestyle='-', label='Start of COVID')
