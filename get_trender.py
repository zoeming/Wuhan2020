# 请求库
import requests
# 解析库
from bs4 import BeautifulSoup
# 用于解决爬取的数据格式化
import io
import sys
import re
import time
import os

from pyecharts.charts import Line, Pie, Map, Page
from pyecharts import options as opts
from pyecharts import *
from colour import Color
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

# 获取对应新闻的所有url链接
def get_url():

	# 有重复标题新闻发布多次
	# 因此创建一个字典用于存储相关新闻信息
	UrlIfo = {}

	lst = ["http://wjw.xiaogan.gov.cn/xxgk/index.jhtml",
	"http://wjw.xiaogan.gov.cn/xxgk/index_2.jhtml",
	"http://wjw.xiaogan.gov.cn/xxgk/index_3.jhtml"]

	for url in lst:
		# 爬取的网页链接
		r= requests.get(url)
		# print(type(r))

		# 网页内容
		result = r.text
		# 再次封装，获取具体标签内的内容
		bs = BeautifulSoup(result,'lxml')

		# 通过查看网页发现数据都在a标签下
		# 获取已爬取内容中的a标签内容
		data=bs.find_all('a')

		
		
		for i in data:
			# 由于有其他干扰信息，故知获取孝感市新型冠状病毒感染的肺炎疫情情况相关信息
			if "孝感市新型冠状病毒感染的肺炎疫情情况" in i.text :
				# 键表示新闻标题，值表示对应url
				UrlIfo[i.text] = i.get('href')
				# print(i.get('href'),end='\n')

	# 得到相关肺炎人数报告相关新闻的url列表
	urlLst = UrlIfo.values()

	return urlLst

# 获取新闻中的信息，包括新增人数报告和整体人数报告
def get_info():
	# 获取相关新闻url列表
	urlLst = get_url()

	# 新增案例信息
	newInfo = []
	# 累积案例信息
	fullInfo = []

	for url in urlLst:
		# 爬取的网页链接
		r= requests.get(url)

		# 网页内容
		result = r.text
		# 再次封装，获取具体标签内的内容
		bs = BeautifulSoup(result,'html.parser')

		# 通过查看网页发现新闻都在span标签下
		# 获取已爬取内容中的span标签内容
		data=bs.find_all('p')	

		# 循环获取数据
		for i in data:
			# 将新增人数信息存储到newInfo中
			if "孝感市新增新型冠状病毒感染的肺炎确诊病例" in i.text:
				newInfo.append(i.text)
			# 将累积信息 存储到fullInfo中
			if "孝感市累计报告新型冠状病毒感染的肺炎确诊病例" in i.text:
				fullInfo.append(i.text)

	return newInfo, fullInfo
	
# 判断路径是否存在
def create_dir(root):
	if not os.path.exists(root):
		os.makedirs(root)

# 提取人数信息
def extract_info(illInfo,date,xiaoganIll,xiaonanIll,hanchuanIll,yingchengIll,yunmengIll,anluIll,dawuIll,xiaochangIll):
	# 因为有的地区有时候没有新增案例，所以当天新增先全部初始化为0
	xiaoganIll[date] = 0
	xiaonanIll[date] = 0
	hanchuanIll[date] = 0
	yingchengIll[date] = 0
	yunmengIll[date] = 0
	anluIll[date] = 0
	dawuIll[date] = 0
	xiaochangIll[date] = 0

	tmp = [0 for _ in range(8)]
	# 按照标点符号进行分割，便于后续处理
	illlist = re.split('。|，|：|、',illInfo)
	for i in illlist:
		if "孝感" in i:
			# 提取分割后数据中的整数，由于地区名称会重复出现，存储最大的
			if int(re.findall(r"\d+\.?\d*",i)[0]) > tmp[0]:
				xiaoganIll[date] = int(re.findall(r"\d+\.?\d*",i)[0])
				tmp[0] = xiaoganIll[date]
		if "孝南" in i:
			if int(re.findall(r"\d+\.?\d*",i)[0]) > tmp[1]:
				xiaonanIll[date] = int(re.findall(r"\d+\.?\d*",i)[0])
				tmp[1] = xiaonanIll[date]
		if "汉川" in i:
			if int(re.findall(r"\d+\.?\d*",i)[0]) > tmp[2]:
				hanchuanIll[date] = int(re.findall(r"\d+\.?\d*",i)[0])
				tmp[2] = hanchuanIll[date]
		if "应城" in i:
			if int(re.findall(r"\d+\.?\d*",i)[0]) > tmp[3]:
				yingchengIll[date] = int(re.findall(r"\d+\.?\d*",i)[0])
				tmp[3] = yingchengIll[date]
		if "云梦" in i:
			if int(re.findall(r"\d+\.?\d*",i)[0]) > tmp[4]:
				yunmengIll[date] = int(re.findall(r"\d+\.?\d*",i)[0])
				tmp[4] = yunmengIll[date]
		if "安陆" in i:
			if int(re.findall(r"\d+\.?\d*",i)[0]) > tmp[5]:
				anluIll[date] = int(re.findall(r"\d+\.?\d*",i)[0])
				tmp[5] = anluIll[date]
		if "大悟" in i:
			if int(re.findall(r"\d+\.?\d*",i)[0]) > tmp[6]:
				dawuIll[date] = int(re.findall(r"\d+\.?\d*",i)[0])
				tmp[6] = dawuIll[date]
		if "孝昌" in i:
			if int(re.findall(r"\d+\.?\d*",i)[0]) > tmp[7]:
				xiaochangIll[date] = int(re.findall(r"\d+\.?\d*",i)[0])
				tmp[7] = xiaochangIll[date]

	dates = list(reversed(list(xiaoganIll.keys())))
	xg = list(reversed(list((xiaoganIll.values()))))
	al = list(reversed(list((anluIll.values()))))
	xn = list(reversed(list((xiaonanIll.values()))))
	dw = list(reversed(list((dawuIll.values()))))
	hc = list(reversed(list((hanchuanIll.values()))))
	xc = list(reversed(list((xiaochangIll.values()))))
	ym = list(reversed(list((yunmengIll.values()))))
	yc = list(reversed(list((yingchengIll.values()))))

	return dates, xg, xn, hc, yc, ym, al, dw, xc
	
# 绘制曲线图
def line(dates, xg, xn, hc, yc, ym, al, dw, xc, max_num):
	c = (
		Line(init_opts=opts.InitOpts(width='800px', height='400px'))
			.add_xaxis(dates)
			.add_yaxis("孝感累积确诊病例", xg,
				is_smooth=True,
				linestyle_opts=opts.LineStyleOpts(width=4, color='#B44038'),
				itemstyle_opts=opts.ItemStyleOpts(
					color='#B44038', border_color="#B44038", border_width=5
					))
			.add_yaxis("孝南累积确诊病例", xn, is_smooth=True,
				linestyle_opts=opts.LineStyleOpts(width=2, color='#800080'),
				label_opts=opts.LabelOpts(position='bottom'),
				itemstyle_opts=opts.ItemStyleOpts(
					color='#800080', border_color="#800080", border_width=3
					))
			.add_yaxis("汉川累积病例", hc, is_smooth=True,
				linestyle_opts=opts.LineStyleOpts(width=2, color='#F1A846'),
				label_opts=opts.LabelOpts(position='bottom'),
				itemstyle_opts=opts.ItemStyleOpts(
					color='#F1A846', border_color="#F1A846", border_width=3
					))
			.add_yaxis("应城累积确诊病例", yc,
				is_smooth=True,
				linestyle_opts=opts.LineStyleOpts(width=4, color='#0000FF'),
				itemstyle_opts=opts.ItemStyleOpts(
					color='#0000FF', border_color="#0000FF", border_width=5
					))
			.add_yaxis("孝南累积确诊病例", xn, is_smooth=True,
				linestyle_opts=opts.LineStyleOpts(width=2, color='#A9A9A9'),
				label_opts=opts.LabelOpts(position='bottom'),
				itemstyle_opts=opts.ItemStyleOpts(
					color='#A9A9A9', border_color="#A9A9A9", border_width=3
					))
			.add_yaxis("云梦累积确诊病例", ym, is_smooth=True,
				linestyle_opts=opts.LineStyleOpts(width=2, color='#A9A9A9'),
				label_opts=opts.LabelOpts(position='bottom'),
				itemstyle_opts=opts.ItemStyleOpts(
					color='#A999A9', border_color="#A999A9", border_width=3
					))
			.add_yaxis("安陆累积病例", al, is_smooth=True,
				linestyle_opts=opts.LineStyleOpts(width=2, color='#FFC0CB'),
				label_opts=opts.LabelOpts(position='bottom'),
				itemstyle_opts=opts.ItemStyleOpts(
					color='#FFC0CB', border_color="#FFC0CB", border_width=3
					))
			.add_yaxis("大悟累积确诊病例", dw, is_smooth=True,
				linestyle_opts=opts.LineStyleOpts(width=2, color='#008000'),
				label_opts=opts.LabelOpts(position='bottom'),
				itemstyle_opts=opts.ItemStyleOpts(
					color='#008000', border_color="#008000", border_width=3
					))
			.add_yaxis("孝昌累积病例", xc, is_smooth=True,
				linestyle_opts=opts.LineStyleOpts(width=2, color='#F0E68C'),
				label_opts=opts.LabelOpts(position='bottom'),
				itemstyle_opts=opts.ItemStyleOpts(
					color='#F0E68C', border_color="#F0E68C", border_width=3
					))

			.set_global_opts(title_opts=opts.TitleOpts(title=""),
				yaxis_opts=opts.AxisOpts(
					max_=max_num,
					min_=0,
					name="",
					splitline_opts=opts.SplitLineOpts(is_show=True),
					is_scale=True,
					axisline_opts=opts.AxisLineOpts(is_show=False)
					))	    
	)

	return c

# 绘制饼图
def pie(xg, xn, hc, yc, ym, al, dw, xc):
	city = ["孝南","汉川","应城","云梦","安陆","大悟","孝昌"]
	num = [xn[-1],hc[-1],yc[-1],ym[-1],al[-1],dw[-1],xc[-1]]
	p = (
		Pie()
		.add(
			"",
			[list(z) for z in zip(city, num)],
			radius=["40%", "75%"],   # 圆环的粗细和大小
			)
		.set_global_opts(
			title_opts=opts.TitleOpts(title="孝感地区当日累积病例分布图"),
			legend_opts=opts.LegendOpts(
			orient="vertical", pos_top="5%", pos_left="2%"  # 左面比例尺
			),
			)
		.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
		)
	return p

# 累积人数
def cumulative_render(fullInfo):
	# 各地区信息都存入字典中，key是日期，Value是人数
	xiaoganIll = {}
	xiaonanIll = {}
	hanchuanIll = {}
	yingchengIll = {}
	yunmengIll = {}
	anluIll = {}
	dawuIll = {}
	xiaochangIll = {}

	for info in fullInfo:
		# 累积病例切割
		wordlist = re.split('。',info)
		# 获取日期
		date = re.split('24时',wordlist[0])[0]
		date = re.split('截至|截止',date)[-1]

		# 第一句话中有感染病例信息
		illInfo = wordlist[0]

		dates, xg, xn, hc, yc, ym, al, dw, xc = extract_info(illInfo,date,xiaoganIll,xiaonanIll,hanchuanIll,yingchengIll,yunmengIll,anluIll,dawuIll,xiaochangIll)

	page = Page()

	# 绘制曲线图
	c = line(dates, xg, xn, hc, yc, ym, al, dw, xc, 3000)
	page.add(c)

	# 绘制饼图
	p = pie(xg, xn, hc, yc, ym, al, dw, xc)
	page.add(p)

	root = 'html-charts/%s' % time.strftime("%Y-%m-%d",time.localtime(time.time()))
	create_dir(root)
	page.render('%s/累积病例趋势图.html' % root)

# 新增人数
def increase_render(newInfo):
	# 各地区信息都存入字典中，key是日期，Value是人数
	xiaoganIll = {}
	xiaonanIll = {}
	hanchuanIll = {}
	yingchengIll = {}
	yunmengIll = {}
	anluIll = {}
	dawuIll = {}
	xiaochangIll = {}

	for info in newInfo:				
		# 新增病例切割
		wordlist = re.split('。',info)
		# 获取日期，缩进都不一样，数据格式为“2020年1月29日0时—24时，孝感市新增新型冠状病毒感染的肺炎确诊病例125例，”
		# 只能用很蠢的方法。。先取0时之前的数据，然后取年之后的数据就得到了日期值
		date = re.split('0时',wordlist[0])[0]
		date = re.split('年',date)[1]

		# 第一句话中有感染病例信息
		illInfo = wordlist[0]
		
		dates, xg, xn, hc, yc, ym, al, dw, xc = extract_info(illInfo,date,xiaoganIll,xiaonanIll,hanchuanIll,yingchengIll,yunmengIll,anluIll,dawuIll,xiaochangIll)

	page = Page()
	
	# 绘制曲线图
	l = line(dates, xg, xn, hc, yc, ym, al, dw, xc, 500)
	page.add(l)

	# 绘制饼图
	p = pie(xg, xn, hc, yc, ym, al, dw, xc)
	page.add(p)

	root = 'html-charts/%s' % time.strftime("%Y-%m-%d",time.localtime(time.time()))
	create_dir(root)
	page.render('%s/新增病例趋势图.html' % root)

if __name__ == '__main__':
	newInfo, fullInfo = get_info()
	cumulative_render(fullInfo)
	increase_render(newInfo)
