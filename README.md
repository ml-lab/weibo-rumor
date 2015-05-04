# weibo-rumor

Details of the project report can be found [here](http://yixuan-li.com/2015/05/03/understanding-the-rumor-dispelling-behavior-in-microblogs-a-case-study-on-sina-weibo/).

The package contains data information about 20,000 pieces of rumor reports, crawled from the first 1,000 pages of Sina Weibo’s rumor showcase (http://service.account.weibo.com).

Requirements
------------
* Python >= 2.6 (but not 3.x)
* numpy
* matplotlib ([http://matplotlib.org/users/installing.html] (http://matplotlib.org/users/installing.html))
* BeautifulSoup ([http://www.crummy.com/software/BeautifulSoup/](http://www.crummy.com/software/BeautifulSoup/))
* seaborn ([http://stanford.edu/~mwaskom/software/seaborn/](http://stanford.edu/~mwaskom/software/seaborn/))

Usage
-----

- Fill in your own Sina Weibo username and password in the main function of “rumor_crawler.py” file and save.

```
    username = '...your username...'
    pwd = '...your password...'
```

- You can modify the starting crawling page and ending crawling page by adjusting the parameters when calling the function of ``iterate_pages(start,end)``. In our code, the default starting page is 1 and ending page is 100.

- Run the crawler: 

```
    $python rumor_crawler.py
```

- To visualize:

```
    $python visual.py 
```



