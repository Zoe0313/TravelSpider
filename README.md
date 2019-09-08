# TravelSpider
======================

### 爬取数据思路
1. 通过请求 "https://piao.qunar.com/ticket/list.htm?keyword=北京"
获取北京地区热门景区信息。

2. 通过BeautifulSoup去分析提取出我们需要的信息。

3. 这里为了偷懒只爬取了前2页的景点信息，每页有15个景点。

4. 因为去哪儿并没有什么反爬措施，所以直接请求就可以了。

5. 这里只是随机选择了13个热门城市：
北京, 上海, 成都, 三亚, 广州, 重庆, 深圳, 西安, 杭州, 厦门, 武汉, 大连, 苏州。


### 生成xls文件
将数据导出到excel表中，以方便随时调取。
> 输出文件: towhere.xls


### 将爬取的数据排行绘制出来
> plt绘图
 * 柱状图: 去哪儿5月国内最受欢迎十大景区.png
<img src="https://raw.githubusercontent.com/Zoe0313/TravelSpider/master/去哪儿5月国内最受欢迎十大景区.png" width="80%">
 * 饼图: 去哪儿热点景区门票价格对比饼图.png
<img src="https://raw.githubusercontent.com/Zoe0313/TravelSpider/master/去哪儿热点景区门票价格对比饼图.png" width="80%">
