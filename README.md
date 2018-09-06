[![licence](http://img.shields.io/badge/licence-MIT-blue.svg?style=flat)](https://github.com/amueller/word_cloud/blob/master/LICENSE)

![Logo](logo.png)

Arabic words cloud
================

This python simple script generates word cloud from arabic texts. Read more about word [word_cloud](https://github.com/amueller/word_cloud).
To avoid reverted text issue, I used [python-arabic-reshaper](https://github.com//mpcabd/python-arabic-reshaper)

## Required packages

Use pip to install :

* numpy
* pandas
* matplotlib
* pillow
* python-bidi
* wordcloud

## Tested fonts
Install the KacstOne fonts :
```
apt install fonts-kacst
```

## Usage examples

* A sample output for [One Thousand and One Nights](https://en.wikipedia.org/wiki/One_Thousand_and_One_Nights) "ألف ليلة وليلة" text (Part I):

![1001_nights](Outputs/1001_nights.png)

* A sample output for [Hayy ibn Yaqdhan](https://en.wikipedia.org/wiki/Hayy_ibn_Yaqdhan) "حي بن يقضان" novel :

![Ibn-yakdhan](Outputs/Ibn-yakdhan.png)

* A sample output for [Al-Atlal](https://en.wikipedia.org/wiki/Al-Atlal) "الأصلال" a famous classical poem singed by Oum Kalthoum :

![Al-Atlal](Outputs/Al-Atlal.png)

* A sample output for [Geber](https://en.wikipedia.org/wiki/Jabir_ibn_Hayyan) Alchemical text :

![Jaber](Outputs/Jaber.png)


## Known issues

* No support for texts with diacritical marks (i.e. العَربيةُ لُغةٌ رائِعةٌ).
* The common redundant words such as كان في ثم ... (prepositions, coordination etc.) must be cleaned manually.  
