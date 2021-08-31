Hodnoceni projektu 1: xkocim05
================================================================================
+2 delky vsech datovych sloupcu jsou stejne (az 2 bodu) <br/>
+0 pocet sloupcu je stejny jako pocet hlavicek (az 2 bodu) <br/>
+2 stahlo se 81_501 zaznamu (az 2 bodu) <br/>
+1 uspesne se stahl Plzensky kraj (s chybou) (az 1 bodu) <br/>
+1 podarilo se vytvorit pandas.DataFrame (az 1 bodu) <br/>
+1 rozumne rozlozeni datovych typu (az 1 bodu) <br/>
+0 souradnice jsou spravne jako floaty i s desetinnymi misty (az 1 bodu) <br/>
+0 neni mozne hodnotit cas 1.42 s, jelikoz t1, t4 a t5 neprosly (az 2 bodu) <br/>
+3.00 kvalita kodu downloader.py (az 3 bodu) <br/>
+3.00 kvalita kodu get_stat.py (az 3 bodu) <br/>
+2.00 graf z get_stat.py (az 2 bodu) <br/>
CELKEM: 15.0 bodu <br/>

Komentar k hodnoceni
================================================================================
Kompaktni reseni <br/>

Vystup testu
================================================================================
##t1s1:ok delky vsech datovych sloupcu jsou stejne <br/>
##t1s2:fail pocet sloupcu neni stejny jako pocet hlavicek 65 66 <br/>
##t1s3:ok stahlo se 81_501 zaznamu <br/>
##t2:ok podarilo se stahnout i plzensky kraj a maji dost polozek <br/>
##t3:ok podarilo se vytvorit pandas dataframe <br/>
##t4:ok datove typy byly voleny rozumne <br/>
##t5:fail sloupec d zrejme nema zadne desetinna mista:  [0. 0. 0. ... 0. 0. 0.] <br/>
##t6:fail  8       E128 continuation line under-indented for visual indent <br/>
##t6:fail  1       E203 whitespace before ':' <br/>
##t6:fail  17      E231 missing whitespace after ':' <br/>
##t6:fail  2       E251 unexpected spaces around keyword / parameter equals <br/>
##t6:fail  1       E302 expected 2 blank lines, found 1 <br/>
##t6:fail  2       E303 too many blank lines (2) <br/>
##t7:ok  [1.420617837982718, 1.4102773040067405, 1.4260029080323875, 1.426256288017612, 1.4273072910145856] <br/>

Velikost dat 44 MB <br/>

Chybovy vystup test
================================================================================


PEP8 get_stat.py
================================================================================
1       E231 missing whitespace after ',' <br/>
4       E251 unexpected spaces around keyword / parameter equals <br/>
1       E302 expected 2 blank lines, found 1 <br/>
13      W293 blank line contains whitespace <br/>


Vystup stderr z get_stat.py
================================================================================
N/A <br/>
