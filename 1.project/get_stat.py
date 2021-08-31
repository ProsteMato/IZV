"""
This class shows and/or saves figure that respresent accidents count
in Czech republic for specific regions and years.
"""
import os
import sys
import numpy as np
import argparse
import matplotlib.pyplot as plt
from download import DataDownloader


__author__ = "Martin Koči"
__email__ = "xkocim05@stud.fit.vutbr.cz"

def get_counts_for_year(data, year):
    """Calculates and returns accidents counts from data for specific year
    
    Arguments:
    data -- data that are processed
    year -- year that is filtered
    """
    
    accidents_counts = list(map(list, zip(*list((filter(lambda x: x[0] == year, data))))))[2]
    return accidents_counts


def parse_counts(data):
    """Makes and returns dict of years, regions and counts of accidents in data
    
    Arguments:
    data -- data that are processed
    """
    
    results = {}
    region_year = np.stack([data[0], data[4].astype('datetime64[Y]').astype(int) + 1970], axis=0)
    region_years, counts = np.unique(region_year, return_counts=True, axis=1)
    region_years_counts = list(zip(region_years[1], region_years[0], counts))
    results['years'] = np.unique(region_year[1])
    results['regions'] = np.unique(region_year[0])
    for year in results['years']:
        results[year] = np.array(get_counts_for_year(region_years_counts, year))
    return results


def plot_stat(data_source, fig_location = None, show_figure = False):
    """Plots a basic statistics from data_source about how much accidents
    specific regions in some period of time.
    
    Arguments:
    data_source -- dataset that is put into figure
    
    Keyword arguments:
    fig_location -- location consist of directory and filename where figure will be stored (default None)
    show_figure  -- show figure in window (default False)
    
    """
    
    accidents_counts = parse_counts(data_source[1])
    years = list(accidents_counts['years'])

    fig, axes = plt.subplots(ncols=1, nrows=len(years), sharey=True, constrained_layout=True, figsize=(7, 13))

    fig.suptitle("Počet nehôd v jednotlivých krajoch v Českej republike za určité obdobie\n")

    for ax in axes.flatten():
        year = years.pop(0)
        a = np.argsort(-accidents_counts[year])
        order = list(np.arange(accidents_counts['regions'].size))
        for num, index in enumerate(a):
            order[index] = num + 1
        ax.grid(axis="y", color="black", alpha=.3, linewidth=.5, zorder=1)
        rects = ax.bar(accidents_counts['regions'], accidents_counts[year], width=0.9, bottom=0,align='center', color='C3', zorder=3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_position('zero')
        ax.margins(0.05)
        ax.title.set_text(year)
        ax.set_ylabel('Počet nehôd')
        ax.set_xlabel('Skratka kraja')
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}.'.format(order.pop(0)),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, -1),
                        textcoords="offset points",
                        ha='center', va='top', fontsize=8, color='white')
    
    if fig_location is not None:
        directory = os.path.dirname(fig_location)
        if not os.path.isdir(directory if directory != '' else '.'):
            os.mkdir(directory)
        plt.savefig(fig_location, facecolor='white', edgecolor='white', transparent=False)
    
    if show_figure:
        plt.show()
        
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--fig_location', help="if set it will store figure in to that file")
    parser.add_argument('--show_figure', action='store_true', help="it wil plot figure into a window")
    
    args = parser.parse_args()
    plot_stat(DataDownloader().get_list(), fig_location=args.fig_location, show_figure=args.show_figure)
