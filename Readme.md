# Scrapy test for scraping data from Immoscout

# Setup

## create environment
```shell
python3 -m venv .env
```

# switch to the environment
```shell
source .env/bin/activate
```

## create scrapy project

```shell
scrapy startproject tutorial
```

# run

```shell
scrapy crawl quotes -o output.csv
```

# run scraper against raiffeissen casa
```shell
cd tutorial/tutorial
scrapy crawl raiffeisen_casa -o output2.csv
```

# references

https://docs.scrapy.org/en/latest/intro/tutorial.html
