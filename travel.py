"""
爬取数据思路:
1. 通过请求 https://piao.qunar.com/ticket/list.htm?keyword=北京
获取北京地区热门景区信息
2. 通过BeautifulSoup去分析提取出我们需要的信息。
3. 这里为了偷懒只爬取了前2页的景点信息，每页有15个景点。

4. 因为去哪儿并没有什么反爬措施，所以直接请求就可以了。
5. 这里只是随机选择了13个热门城市：
北京, 上海, 成都, 三亚, 广州, 重庆, 深圳, 西安, 杭州, 厦门, 武汉, 大连, 苏州。

将数据导出到excel表中，以方便随时调取.
输出文件:towhere.xls

利用plt绘制柱状图和饼图。
柱状图: 去哪儿5月国内最受欢迎十大景区
饼图: 去哪儿热点景区门票价格对比饼图
"""

import requests
from bs4 import BeautifulSoup
import xlwt
#from pymongo import MongoClient
from pylab import *

mpl.rcParams['font.sans-serif'] = ['SimHei']


class QuNaEr():
    def __init__(self, keyword):
        self.keyword = keyword

    def qne_spider(self,page):
        url = 'https://piao.qunar.com/ticket/list.htm?keyword=%s&region=&from=mpl_search_suggest&page=%s' % (
        self.keyword, page)
        response = requests.get(url)
        response.encoding = 'utf-8'
        text = response.text
        bs_obj = BeautifulSoup(text, 'html.parser')

        arr = bs_obj.find('div', {'class': 'result_list'}).contents

        info_list = []
        for i in arr:
            info = i.attrs
            # 景区名称
            name = info.get('data-sight-name')
            # 地址
            address = info.get('data-address')
            # 近期售票数
            count = info.get('data-sale-count')
            # 经纬度
            point = info.get('data-point')

            # 起始价格
            price = i.find('span', {'class': 'sight_item_price'})
            price = price.find_all('em')
            price = price[0].text

            information = []
            information.append(self.keyword)
            information.append(name)
            information.append(int(count))
            information.append(float(price))
            information.append(address)
            info_list.append(information)

        return info_list
            # print(name,address,count,point,price)
            # conn = MongoClient('localhost', port=27017)
            # db = conn.QuNaEr  # 库
            # table = db.qunaer_51  # 表
            #
            # table.insert_one({
            #     'name': name,
            #     'address': address,
            #     'count': int(count),
            #     'point': point,
            #     'price': float(price),
            #     'city': self.keyword
            # })

    def draw_rank(self, rank_list):
        # x,y轴数据
        x_arr = []  # 景区名称
        y_arr = []  # 销量
        for i in rank_list:
            x_arr.append(i[1])
            y_arr.append(i[2])

        plt.bar(x_arr, y_arr, color='rgb')  # 指定color，不然所有的柱体都会是一个颜色
        plt.gcf().autofmt_xdate()  # 旋转x轴，避免重叠
        plt.xlabel(u'景点')  # x轴描述信息
        plt.ylabel(u'销量')  # y轴描述信息
        plt.title(u'去哪儿5月国内最受欢迎十大景区')  # 指定图表描述信息
        plt.ylim(0, 30000)  # 指定Y轴的高度
        plt.savefig('去哪儿5月国内最受欢迎十大景区')  # 保存为图片
        plt.show()

    def draw_pie(self, data_list):
        arr = [[0, 50], [50, 100], [100, 200], [200, 300], [300, 500], [500, 1000]]
        name_arr = []
        total_arr = []
        for i in arr:
            result = [x for x in filter(lambda x:i[0]<=x[3]<=i[1], data_list)]
            name = '%d-%d元 ' % (i[0], i[1])# 价格区间
            name_arr.append(name)
            total_arr.append(len(result))# 在该价格区间中的数量

        color = 'red', 'orange', 'green', 'blue', 'gray', 'goldenrod'  # 各类别颜色
        explode = (0.2, 0, 0, 0, 0, 0)  # 各类别的偏移半径

        # 绘制饼状图
        pie = plt.pie(total_arr, colors=color, explode=explode, labels=name_arr, shadow=True, autopct='%1.1f%%')

        plt.axis('equal')
        plt.title(u'去哪儿热点景区门票价格对比饼图')#, fontsize=12)

        plt.legend(loc=0, bbox_to_anchor=(0.82, 1))  # 图例
        # 设置legend的字体大小
        leg = plt.gca().get_legend()
        ltext = leg.get_texts()
        plt.setp(ltext, fontsize=8)
        plt.savefig('去哪儿热点景区门票价格对比饼图')  # 保存为图片
        plt.show()

if __name__ == '__main__':

    info_result = []
    title = ['城市','景点','销量','票价','地址']
    info_result.append(title)

    citys = ['北京', '上海', '成都', '三亚', '广州', '重庆', '深圳', '西安', '杭州', '厦门', '武汉', '大连', '苏州']
    for city in citys:
        qne = QuNaEr(city)
        for page in range(1, 2):
            info = qne.qne_spider(page)
            info_result = info_result + info

    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('travel', True)
    for i, row in enumerate(info_result):
        for j,col in enumerate(row):
            worksheet.write(i,j,col)
    workbook.save('towhere.xls')

    # 最受欢迎的10个景区
    L = info_result[1:]
    L.sort(key=lambda data:data[2],reverse=True)
    #print([x[2] for x in L[:10]])

    qne = QuNaEr('')
    qne.draw_rank(L[:10])

    L.sort(key=lambda data:data[3],reverse=False)
    qne.draw_pie(L)

