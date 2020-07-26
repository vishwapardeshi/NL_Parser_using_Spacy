# Natural Language Recipe Ingredient Parser using SpaCy

![Build Status](https://travis-ci.com/vishwapardeshi/Custom_NER_Recipe_Ingredient_Parser.svg?branch=master)

Recipes on almost all food-blogging or recipe curating website never separate the name of the ingredient from the measurement, quantity and additional description. Thus, to simply scrape the ingredient name from a recipe's webpage is not possible without some text processing. This project is an **end-to-end NLP project which scrapes webpages for recipes and extracts ingredient name from recipes using Custom Named Entity Recognition (spaCy).**

I used Test-Driven Development methodology.

## Outline

This natural language recipe ingredient parser can be used by food blogging website or apps likewise to improve management of opaque ingredients by converting into easy to manipulate & exploit strings stored in tabular format. Thus, it can be used for 
1. Building Shopping Lists 

2. Making recipes easily searchable

3. Curating recipes from ingredients entered by users

4. Creating an ingredient database

## Methodology

As this is an end-to-end NLP project, it covers everything from acquiring data, building ELT pipelines and custom Named Entity Recognition model using Test-Driven Development Methodoly. **The unit tests can be found in the test folder which uses pyTest.** 

1. Scrape Recipes from webpages using BeautifulSoup

2. Clean the scraped data 

3. Build ELT pipeline to generate training data formatted for feeding spaCy model

4. Train the model using the generated annonated data

5. Extract ingredients from web-scraped recipes. 

In addition to this, I also explored dependency parsing to extract ingredients from recipes which can be found in the jupyternotebook.


## Tools 
```
> 1. Web scraping: Python, BeautifulSoup, Requests, re(regular expression), pandas
> 2. ELT Pipeline: Python, Pandas, BeautifulSoup
> 3. Unit Testing: pyTest, TravisCI
> 4. Named Entity Recongition: spaCy
> 5. Exploration: JupyterNotebooks
```
