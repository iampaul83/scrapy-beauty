# 1. scrapy

```bash
git clone https://github.com/iampaul83/scrapy-beauty.git
cd scrapy-beauty

virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt

cd tutorial
scrapy crawl beauty2 -o out.json -L INFO
scrapy crawl beauty2 -o out.json -L INFO -a page_limit=100
```

# json -> html

```bash
cd ../html
npm install
cp ../tutorial/out.json beauty2.json
node index
open index.html
```
