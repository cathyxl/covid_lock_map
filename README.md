
![image](https://github.com/xulin66999/covid_lock_map/blob/master/map.png)
This project predicts lock down condition of China by refering to the crawled weibo texts.

### Function documentation
* Show the lock condtion of each province in China from 2020/2/15-2020/7/20. 
* Each time there is a month span of lock condition display. After clicking on timeline, a new month span will appear with the clicked one as the center date.
* Click on each province, the corresponding city lock condition will also appear.
* By click on timelines under the China lock map, there are also some related mblog news displayed on the left column.


#### Files
* web：flask projects. <br>
    * app.py: Start of flask projects. <br>
    * deal_with_crawled_data.py: Deal with raw crawled data by weibo_search. Predict lock condition from original crawled data. <br>
    * logistics.py: Background logistic of webpage demonstration, get map data. <br><br>


* weibo_search: scrapy based weibo search spider.  <br>
    * account_build, simulate account login <br>
    * spiders
        * search.py, search weibo  <br>
        * search_each_day.py, search weibo by a specified day interval  <br>
    * utils, some extra functions deal with weibo data.
    * items.py, weibo data structure
    * middlewares.py,
    * pipelines.py, pipelines to be done during crawling.
    * run.py, interface to run weibo crawler.
    * settings.py, configurations for crawler.

#### Requirements
pip install scrapy pypinyin flask

#### How to use
* web, python app.py
* weibo_search, python run.py

The corresponding display web page can be accessed through http://175.24.68.244:5002/. 
