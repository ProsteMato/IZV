#!/usr/bin/python3.8
# coding=utf-8
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import contextily as ctx
import sklearn.cluster
import numpy as np
# muzeze pridat vlastni knihovny


def make_geo(df: pd.DataFrame) -> geopandas.GeoDataFrame:
    """ Konvertovani dataframe do geopandas.GeoDataFrame se spravnym kodovani"""

    df.dropna(subset=['d', 'e'], inplace=True)

    df["p2a"] = df["p2a"].astype('datetime64')
    df.rename(columns={"p2a": "date"}, inplace=True)

    keys = ['p36', 'weekday(p2a)', 'h', 'j', 'p', 'q', 't',
            'i', 'k', 'l', 'n', 'o', 'r', 's']

    df[keys] = df[keys].astype('category')

    return geopandas.GeoDataFrame(
        df,
        geometry=geopandas.points_from_xy(df["d"], df["e"]),
        crs="EPSG:5514"
    )


def plot_geo(gdf: geopandas.GeoDataFrame, fig_location: str = None,
             show_figure: bool = False):
    """ Vykresleni grafu s dvemi podgrafy podle lokality nehody """
    gdf_region = gdf[gdf["region"] == "ZLK"]
    gdf_region = gdf_region.to_crs("epsg:3857")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 15))
    gdf_region[gdf_region["p5a"] == 1].plot(ax=ax1, markersize=4,
                                            color='tab:red')
    gdf_region[gdf_region["p5a"] == 2].plot(ax=ax2, markersize=4,
                                            color='tab:blue')

    ax1.set_title("Nehody v ZLK kraji: v obci", fontsize=15)
    ax2.set_title("Nehody v ZLK kraji: mimo obec", fontsize=15)

    for ax in [ax1, ax2]:
        ax.axis("off")
        ctx.add_basemap(ax, crs=gdf_region.crs.to_string(),
                        source=ctx.providers.Stamen.TonerLite)
    plt.subplots_adjust(wspace=0.05)
    plt.tight_layout()

    if fig_location is not None:
        plt.savefig(fig_location)
    if show_figure:
        plt.show()


def plot_cluster(gdf: geopandas.GeoDataFrame, fig_location: str = None,
                 show_figure: bool = False):
    """ Vykresleni grafu s lokalitou vsech nehod v kraji shlukovanych do clusteru """
    gdf_region = gdf[gdf["region"] == "ZLK"]
    gdf_region = gdf_region.to_crs("epsg:3857")

    coords = np.dstack([gdf_region.geometry.x,
                        gdf_region.geometry.y]).reshape(-1, 2)

    model = sklearn.cluster.MiniBatchKMeans(n_clusters=17).fit(coords)

    gdf_region_c = gdf_region.copy()
    gdf_region_c["cluster"] = model.labels_

    gdf_region_c = gdf_region_c.dissolve(by="cluster",
                                         aggfunc={"p1": "count"})

    gdf_region_c.rename(columns={"p1": "count"}, inplace=True)

    gdf_coords = geopandas.GeoDataFrame(
        geometry=geopandas.points_from_xy(model.cluster_centers_[:, 0],
                                          model.cluster_centers_[:, 1])
    )

    gdf_region_c = gdf_region_c.merge(gdf_coords,
                                      left_on="cluster",
                                      right_index=True).set_geometry("geometry_y")

    plt.figure(figsize=(20, 10))
    ax = plt.gca()
    

    gdf_region.plot(ax=ax, markersize=0.7, color='tab:grey')
    gdf_region_c.plot(ax=ax, markersize=gdf_region_c["count"],
                      column="count", legend=True, alpha=0.8,
                      cmap=plt.get_cmap("viridis"))

    ctx.add_basemap(ax, crs=gdf_region.crs.to_string(),
                    source=ctx.providers.Stamen.TonerLite)

    ax.set_title("Nehody v ZLK kraji", fontsize=15)
    plt.axis("off")
    plt.tight_layout()

    if fig_location is not None:
        plt.savefig(fig_location)
    if show_figure:
        plt.show()


if __name__ == "__main__":
    # zde muzete delat libovolne modifikace
    gdf = make_geo(pd.read_pickle("accidents.pkl.gz"))
    plot_geo(gdf, "geo1.png", True)
    plot_cluster(gdf, "geo2.png", True)
