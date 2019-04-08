# crawler
> A web crawler to download the recipes from Yummly(https://www.yummly.com/recipes) as many as possible.

## Prerequisites
- Python 3.7+ with `pip`

## Install

```
pip install beautifulsoup4
pip install lxml
```
## Basic Strategy
- By using the filter tools and endpoints of https://www.yummly.com/recipes, I search the conbinations of cuisines and techniques one by one. The final goal is obtaining nearly all the recipes.

## Begin to use
> run crawler.py

## Multi Thread Running
- You can use multi thread to accelerate the speed of crawler. Comment the code in line 234 and uncomment the code in line 235.
- The efficiency of multi thread crawler may depend on the network condition.
