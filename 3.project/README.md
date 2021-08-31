Hodnoceni treti casti projektu: xkocim05
================================================================================
Geograficka data
--------------------------------------------------------------------------------
+1.00 spravne CRS (5514, 3857) (az 1 b) <br/>
+2.00 spravne rozsah (viz FAQ) (az 2 b) <br/>
+2.00 pocet radku 485591 > 485e3 (az 2 b) <br/>
+2.00 bez NaN v souradnicich (az 2 b) <br/>
+3.00 plot_geo: prehlednost, vzhled (az 3 b) <br/>
+2.00 plot_geo: zobrazeni ve WebMercator (a ne v S-JTSK) (az 2 b) <br/>
+1.00 plot_cluster: prehlednost, vzhled (az 2 b) <br/>
+3.00 plot_cluster: clustering (az 3 b) <br/>
+1.00 funkce make_geo ma spravne docstring (PEP257) (az 1 b) <br/>
+0.50 funkce plot_geo ma spravne docstring (PEP257) (az 0.5 b) <br/>
+0.50 funkce plot_cluster ma spravne docstring (PEP257) (az 0.5 b) <br/>
+1.00 kvalita kodu dle PEP8 (0 kritickych, 0 E2.., 0 E7..)) (az 1 b) <br/>

Overeni hypotezy
--------------------------------------------------------------------------------
+1.00 filtrace (az 2 b) <br/>
+2.00 kontingencni tabulka (az 2 b) <br/>
+2.00 vypocet chi2 testu (az 2 b) <br/>
+1.00 komentare (az 1 b) <br/>
+3.00 zaver: dochazi k silnemu ovlivneni (az 3 b) <br/>

Vlastni analyza
--------------------------------------------------------------------------------
+3.00 tabulka: prehlednost, vzhled (az 5 b) <br/>
+4.00 graf: popis, vzhled (az 4 b) <br/>
+4.00 graf: vhodna velikost, citelnost (az 4 b) <br/>
+2.00 graf: pouziti vektoroveho formatu (az 2 b) <br/>
+3.00 textovy popis (az 3 b) <br/>
+4.00 statisticka smysluplnost analyzy (az 4 b) <br/>
+3.00 dalsi ciselne hodnoty v textu (az 3 b) <br/>
+3.00 generovani hodnot skriptem (az 3 b) <br/>
+2.00 kvalita kodu dle PEP8 (0 kritickych, 7 E2.., 0 E7..)) (az 2 b) <br/>

CELKEM: 56.0 bodu <br/>

Komentar k hodnoceni (zejmena k vizualizacim)
================================================================================
cluster: nepopsany colorbar <br/>

stat: slozitejsi filtrace <br/>

doc: pekne jen tabulka neni uplne tabulkou - cekal bych den / noc jko sloupec, Rok posunuty na uroven ostatnich hlavicek ... <br/>

Vystup skriptu geografickych dat (stdout)
================================================================================
#gdf_crs  EPSG:5514 <br/>
#gdf_nan 0 <br/>
#gdf_range_x_min -901630.1875 <br/>
#gdf_range_x_max -432869.21875 <br/>
#gdf_range_y_min -1219810.375 <br/>
#gdf_range_y_max -938489.5 <br/>
#gdf_count  485591 <br/>
#make_geo_docstring  ok <br/>
#plot_geo_docstring  ok <br/>
#plot_cluster_docstring  ok <br/>
#plot_geo_done 3470.78 ms <br/>
#plot_cluster_done 2386.19 ms <br/>


Vystup skriptu geografickych dat (stderr)
================================================================================


Vystup PEP8 testu souboru geo.py
================================================================================
1       E303 too many blank lines (2) <br/>
1       W293 blank line contains whitespace <br/>


Vystup skriptu dokumentace (stdout)
================================================================================


Počet nehôd pri nevenovaní sa jazde:  82695
================================================================

Počet nehôd ktoré nezavinil vodič:  72277
================================================================
```latex
\begin{tabular}{llr} \\
\toprule \\
{} &  Čas &  Počet nehôd \\
Rok  &      &              \\
\midrule
2016 &  deň &         4707 \\
2017 &  deň &         5084 \\
2018 &  deň &         5459 \\
2019 &  deň &         6621 \\
2020 &  deň &         5347 \\
2016 &  noc &         6210 \\
2017 &  noc &         7410 \\
2018 &  noc &         7378 \\
2019 &  noc &         9307 \\
2020 &  noc &         5502 \\
\bottomrule
\end{tabular}
```

Počet nehôd ktoré zavinili zvieratá z roku 2018 na rok 2019 vzrástol o: 24.07883461868036 %
================================================================


Vystup skriptu dokumentace (stderr)
================================================================================
failed to get the current screen resources <br/>


Vystup PEP8 testu souboru doc.py
================================================================================
1       E123 closing bracket does not match indentation of opening bracket's line <br/>
5       E127 continuation line over-indented for visual indent <br/>
3       E231 missing whitespace after ':' <br/>
4       E251 unexpected spaces around keyword / parameter equals <br/>
18      W293 blank line contains whitespace <br/>
1       W391 blank line at end of file <br/>
