#!/usr/bin/python3.8
# coding=utf-8
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


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

    df = pd.read_pickle(filename)
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


def plot_top_accidents(df: pd.DataFrame, fig_location: str = None,
                        show_figure: bool = False):
    """function plots top 10 accidents occurents"""
    
    df_p12 = df[["p12"]].copy()
    df_p12 = df_p12.value_counts().reset_index().rename(columns={0:"Počet nehod"})
    df_p12 = df_p12.sort_values("Počet nehod", ascending=False)
    df_p12 = df_p12.head(10)

    df_p12["p12"] = df_p12["p12"].replace(
        {
            508: "nevenovanie sa jazde",
            100: "nezavinená vodičom",
            504: "nesprávne otáčanie alebo cúvanie",
            516: "iný druh nesprávneho riadenia vozidla",
            503: "nedodržiavanie bezpečnej vzdialenosti",
            204: "neprisposobená rýchlosť stavu vozovky",
            511: "nezvládnutie riadenia vozidla",
            205: "neprispôsobená rýchlosť technickému stavu vozovky",
            502: "vyhýbanie bez dostatočnej vôle",
            403: "nedanie prednosti v jazde (značka daj prednost)"
        })
    sns.set_style("whitegrid")
    
    plt.figure(figsize=(18, 5))
    ax = plt.gca()
    
    g = sns.catplot(kind="bar", y="p12", x="Počet nehod", data=df_p12, order=df_p12["p12"], orient="h", height=4, aspect=3)

    g.set(ylabel="", title="Top 10 najčastejších príčin nehody v Českej republike", facecolor="#f0f2f5")
    sns.despine()
    plt.subplots_adjust(hspace = 0.8, top=0.9, bottom=0.2)
    
    print('================================================================')
    print("Počet nehôd pri nevenovaní sa jazde: ", df_p12.iloc[0]["Počet nehod"])
    print('================================================================')
    print("Počet nehôd ktoré nezavinil vodič: ", df_p12.iloc[1]["Počet nehod"])
    print('================================================================')
    
    if fig_location is not None:
        plt.savefig(fig_location)
    if show_figure:
        plt.show()

        
def plot_couse(df: pd.DataFrame, fig_location: str = None,
                show_figure: bool = False):
    """function plots couse of accidents"""
    
    df_p10 = df[["p10"]].copy()
    df_p10 = df_p10.value_counts().reset_index().rename(columns={0:"Počet nehod"})

    df_p10["p10"] = df_p10["p10"].replace(
        {
            1: "vodičom motorového vozidla",
            2: "vodičom nemotorového vozidla",
            3: "chodcom",
            4: "lesnou zverou, domácim zvieraťom",
            5: "iným účastníkom",
            6: "závadou komunikácie",
            7: "technickou závadou vozidla",
            0: "iné zavinenie"
        })
    sns.set_style("whitegrid")
    
    plt.figure(figsize=(18, 5))
    ax = plt.gca()
    
    g = sns.catplot(kind="bar", y="p10", x="Počet nehod", data=df_p10, orient="h", height=4, aspect=3)

    g.set(ylabel="", title="Zavinenie nehody v ČR", facecolor="#f0f2f5", xscale="log")
    sns.despine()
    plt.subplots_adjust(hspace = 0.8, top=0.9, bottom=0.2)
    
    if fig_location is not None:
        plt.savefig(fig_location)
    if show_figure:
        plt.show()


def plot_animal_accidents(df: pd.DataFrame, fig_location: str = None,
                            show_figure: bool = False):
    """function plots accidents couse by animals"""
    
    df_zver = df[(df["p10"] == 4)][["p19", "date"]].copy()
    df_zver = df_zver.drop(df_zver[df_zver.p19 < 0].index)
    df_zver.loc[(df_zver["p19"] >= 0) & (df_zver["p19"] <= 3), "Čas"] = "deň"
    df_zver.loc[(df_zver["p19"] >= 4) & (df_zver["p19"] <= 7), "Čas"] = "noc"

    df_zver_c = df_zver.set_index("date").groupby(["Čas"]).resample("Y").count().drop("Čas", 1).reset_index()
    df_zver_c['date'] = df_zver_c['date'].dt.strftime('%Y')
    
    plt.figure(figsize=(7, 4))
    ax = plt.gca()
    
    g = sns.barplot(ax=ax,data=df_zver_c, x="date", y="p19", hue="Čas")
    g.set(xlabel="Rok", ylabel="Počet nehôd",
            title="Počet nehôd so zverou od 2016 do Sep 2020",
            facecolor="#f0f2f5")
    
    df_zver_c = df_zver_c.rename(columns={"p19": "Počet nehôd", "date": "Rok"})
    print(df_zver_c.set_index("Rok").to_latex())
    
    df_zver = df_zver.set_index("date").resample("Y").count().drop("Čas", 1).reset_index()
    df_zver['date'] = df_zver['date'].dt.strftime('%Y')
    print('================================================================')
    print("Počet nehôd ktoré zavinili zvieratá z roku 2018 na rok 2019 vzrástol o: {} %".format(
        df_zver.iloc[3]["p19"] / df_zver.iloc[2]["p19"] * 100 - 100)
        )
         
    print('================================================================')
    
    plt.tight_layout()
    if fig_location is not None:
        plt.savefig(fig_location)
    if show_figure:
        plt.show()


if __name__ == "__main__":
    # zde muzete delat libovolne modifikace
    df = get_dataframe("accidents.pkl.gz")
    plot_top_accidents(df, "fig1.pdf")
    plot_couse(df, "fig2.pdf")
    plot_animal_accidents(df, "fig3.pdf")
    