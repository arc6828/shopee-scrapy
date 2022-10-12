# shopee-scrapy
 try to do scrapy with shopee

 pip install Scrapy

 scrapy startproject tutorial
 cd tutorial
 scrapy shell "https://quotes.toscrape.com"
 scrapy crawl quotes
 scrapy crawl quotes -O quotes.json
 scrapy crawl author -O authors.json

 papermill Test.ipynb Testoutput.ipynb
 papermill local/input.ipynb s3://bkt/output.ipynb -p alpha 0.6 -p l1_ratio 0.1