#!/usr/bin/env python3.8
# coding=utf-8
"""
This module implements funtions that create dataframe of data
and functions that creates graphs.
"""

from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import os

__author__ = "Martin Koči"
__email__ = "xkocim05@stud.fit.vutbr.cz"


def get_dataframe(filename: str, verbose: bool = False) -> pd.DataFrame:
    """Function creates dataframe from given filename and prepare it
    for analysis

    Args:
        filename (str): path where dataframe is stored
        verbose (bool, optional): If True returns old size of dataframe vs
        new size. Defaults to False.

    Returns:
        pd.DataFrame: prepared dataframe
    """

    df = pd.read_pickle(filename, compression='gzip')
    if verbose:
        original_size = df.memory_usage(index=False, deep=True).sum()
        print("orig_size={:.1f} MB".format(original_size / 1_048_576))

    df["p2a"] = df["p2a"].astype('datetime64')
    df.rename(columns={"p2a": "date"}, inplace=True)

    keys = ['p36', 'weekday(p2a)', 'h', 'j', 'p', 'q', 't',
            'i', 'k', 'l', 'n', 'o', 'r', 's']

    df[keys] = df[keys].astype('category')

    if verbose:
        new_size = df.memory_usage(index=False, deep=True).sum()
        print("new_size={:.1f} MB".format(new_size / 1_048_576))
    return df


def plot_conseq(df: pd.DataFrame, fig_location: str = None,
                show_figure: bool = False):
    """Creates graph from given dataframe

    Args:
        df (pd.DataFrame): Given dataframe
        fig_location (str, optional): Where to store graph. Defaults to None.
        show_figure (bool, optional): If True it will show graph.
                                      Defaults to False.
    """

    fig, axes = plt.subplots(4, 1, figsize=(8, 11))
    ax = axes.flatten()

    df_accidets = df.groupby(["region"]).agg(
        {
            "p13a": "sum",
            "p13b": "sum",
            "p13c": "sum",
            "p1": "count"
        }
    )
    df_accidets.rename(columns={"p1": "total_accidets"}, inplace=True)

    df_accidets = df_accidets.reset_index()

    sorted_df_tmp = df_accidets.sort_values('total_accidets',
                                            ascending=False)["region"]

    data = [
        ("Úmrtí", "#e34949", "p13a"),
        ("Ťažko zranených", "seagreen", "p13b"),
        ("Ľahko zranených", "#826633", "p13c"),
        ("Celkový počet nehôd", "#365bba", "total_accidets")
    ]

    for index, (title, color, column) in enumerate(data):
        palette = sns.dark_palette(color=color,
                                   n_colors=df_accidets["region"].count())

        sns.barplot(data=df_accidets, x="region", y=column, ax=ax[index],
                    color=color, zorder=2, order=sorted_df_tmp)

        ax[index].set(xlabel='Kraj', ylabel='Počet', title=title,
                      facecolor="#f0f2f5")

        ax[index].grid(axis="y", color="black", alpha=.2,
                       linewidth=.5, zorder=1)

    sns.despine()
    plt.subplots_adjust(hspace=0.65)
    plt.tight_layout()

    if fig_location is not None:
        directory = os.path.dirname(fig_location)
        if not os.path.isdir(directory if directory != '' else '.'):
            os.mkdir(directory)
        plt.savefig(fig_location)

    if show_figure:
        plt.show()


def plot_damage(df: pd.DataFrame, fig_location: str = None,
                show_figure: bool = False):
    """Creates graph from given dataframe

    Args:
        df (pd.DataFrame): Given dataframe
        fig_location (str, optional): Where to store graph. Defaults to None.
        show_figure (bool, optional): If True it will show graph.
                                      Defaults to False.
    """

    regions = ["PHA", "JHM", "STC", "JHC"]
    cause_labels = ["nezavinená vodičom",  "neprimeraná rýchlosť jazdy",
                    "nesprávne predbiehanie", "nedanie prednosti v jazde",
                    "nesprávny spôsob jazdy", "technická závada vozidla"]
    damage_labels = ["<50", "50 - 200", "201 - 500", "501 - 1000", "1000>"]
    cause_bins = [(100, 100), (201, 209), (301, 311),
                  (401, 414), (501, 516), (601, 615)]
    damage_bins = [-1, 49, 200, 500, 1000, float("inf")]

    df_regions = (
        df[["region", "p12", "p53"]].copy()
                                    .set_index("region")
                                    .loc[regions]
    )

    df_regions["p53"] = df_regions["p53"] / 10

    bins = pd.IntervalIndex.from_tuples(cause_bins, closed="both")
    cause_bins = pd.cut(df_regions["p12"].to_list(), bins=bins)
    cause_bins.categories = cause_labels
    df_regions["p12"] = cause_bins

    df_regions["p53_class"] = pd.cut(df_regions["p53"], damage_bins,
                                     labels=damage_labels)

    df_regions.rename(
        inplace=True,
        columns={
            'p12': 'Príčina nehody'
        }
    )

    df_regions = df_regions.groupby(["region", "p53_class", "Príčina nehody"])
    df_regions = df_regions.count().reset_index()

    plot = sns.catplot(data=df_regions, x="p53_class", col="region",
                       hue="Príčina nehody", col_wrap=2, y="p53", kind="bar",
                       height=4.2, aspect=1.1, zorder=2)

    plot.set_titles("{col_name}", size=14).tight_layout()

    for ax in plot.axes.flatten():
        ax.tick_params(labelbottom=True, labelleft=True)
        ax.set_xlabel("Škoda [tisíc Kč]", fontsize=11.5)
        ax.set_ylabel("Počet", fontsize=11.5)
        ax.set_yscale("log")
        ax.grid(axis="y", color="black", alpha=.2, linewidth=.5, zorder=1)
        ax.set_facecolor("#f0f2f5")

    plt.subplots_adjust(hspace=0.25, wspace=0.2)

    if fig_location is not None:
        directory = os.path.dirname(fig_location)
        if not os.path.isdir(directory if directory != '' else '.'):
            os.mkdir(directory)
        plt.savefig(fig_location)

    if show_figure:
        plt.show()


def plot_surface(df: pd.DataFrame, fig_location: str = None,
                 show_figure: bool = False):
    """Creates graph from given dataframe

    Args:
        df (pd.DataFrame): Given dataframe
        fig_location (str, optional): Where to store graph. Defaults to None.
        show_figure (bool, optional): If True it will show graph.
                                      Defaults to False.
    """

    regions = ["OLK", "JHM", "ULK", "MSK"]

    df_regions = (
        df[["region", "date", "p16"]].copy()
                                     .set_index("region")
                                     .loc[regions]
                                     .reset_index()
    )

    df_regions_crosstab = pd.crosstab(
        [df_regions["region"], df_regions["date"]],
        df_regions["p16"], rownames=["region", "date"], colnames=["p16"])

    df_regions_crosstab.rename(columns={
        0: 'iný stav',
        1: 'neznečistený suchý povrch',
        2: 'znečistený suchý povrch',
        3: 'mokrý povrch',
        4: 'blatistý',
        5: 'námraza, prejdený sneh - posypané',
        6: 'námraza, prejdený sneh - neposypané',
        7: 'rozliatý olej, nafta apod.',
        8: 'súvislá snehová vrstva, topiaci sneh',
        9: 'náhlá zmena stavu',
    }, inplace=True)

    df_regions_crosstab = df_regions_crosstab.reset_index().set_index("date")
    df_regions_crosstab = (
        (df_regions_crosstab.groupby(["region"])
                            .resample("M")
                            .sum()
                            .stack()
                            .reset_index()
                            .set_index("region"))
    )

    df_regions_crosstab.rename(
        inplace=True,
        columns={
            0: "počet nehod",
            "p16": "Stav vozovky"
        }
    )

    plot = sns.relplot(data=df_regions_crosstab, x="date", y="počet nehod",
                       hue="Stav vozovky", kind="line", col="region",
                       col_wrap=2,  ci=0, height=3.2, aspect=2, zorder=2)

    (plot.set_xlabels("Dátum vzniku nehody", size=11.5)
         .set_ylabels("Počet nehôd", size=11.5)
         .set_titles("{col_name}", size=14)
         .tight_layout())

    for ax in plot.axes.flatten():
        ax.grid(color="black", alpha=.2, linewidth=.5, zorder=1)
        ax.set_facecolor("#f0f2f5")

    if fig_location is not None:
        directory = os.path.dirname(fig_location)
        if not os.path.isdir(directory if directory != '' else '.'):
            os.mkdir(directory)
        plot.savefig(fig_location)

    if show_figure:
        plt.show()


if __name__ == "__main__":
    pass
    df = get_dataframe("accidents.pkl.gz", True)
    plot_conseq(df, fig_location="01_nasledky.png", show_figure=True)
    plot_damage(df, "02_priciny.png", True)
    plot_surface(df, "03_stav.png", True)
