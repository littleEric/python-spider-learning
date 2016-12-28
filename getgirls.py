from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re,os

def get_linkas(url):
    ##储存主页链接
    href_list = list()
    try:
        html = urlopen(url)
        bsObj = BeautifulSoup(html,"lxml")
    except HTTPError as e:
        print(".............failed to open url on function get_linka..........")
    try:
        ##找到存链接的div
        div_all = bsObj.find("div", {"class": "all"})
        ##找到存链接的ul
        ul_archives = div_all.find_all("ul", {"class": "archives"})
        for ul_archive in ul_archives:
            ##获取所有a标签
            a_tags = ul_archive.find_all("a", {"href": re.compile("http:\/\/www\.mzitu\.com\/\d+")})
            for a_tag in a_tags:
                href_list.append(a_tag["href"])
        return (href_list)
    except AttributeError as e:
        print(".............AttributeError on function get_linka..........")
    ##储存主页链接

#####从每页中获取图片最大页数
def get_linkbs(url):
    try:
        html = urlopen(url)
        bsObj = BeautifulSoup(html,"lxml")
    except HTTPError as e:
        print(".............failed to open url on function get_linkb..........")
        return None
    try:
        div_pagenavi = bsObj.find("div", {"class": "pagenavi"})
        if div_pagenavi == None:
            print("=================failed to get div_pagenavi on function get_linkbs==============")
            return None
        else:
            #a_tags = div_pagenavi.find_all("a", {"href": re.compile("http:\/\/www\.mzitu\.com\/\d+\/\d+")})
            span_dots = div_pagenavi.find("span",{"class":"dots"})
            max_a_tag_val = int(span_dots.next_sibling.span.string)
            #return range(2,max_a_tag_val+1)
            ##找出本页标题
            title = bsObj.find("div",{"class":"content"}).find("h2").string
            return {"title":title,"max_value":max_a_tag_val}
    except AttributeError as e:
        print(".............AttributeError on function get_linkb..........")
        return None
##从每页挖出图片
def get_img_link(url):
    try:
        html = urlopen(url)
        bsObj = BeautifulSoup(html,"lxml")
    except HTTPError as e:
        print("=============could not found picture link in the page==================")
        return None
    try:
        div_main_img = bsObj.find("div",{"class":"main-image"})
        img_src = div_main_img.p.a.img['src']
    except AttributeError as e:
        print(".............AttributeError on function get_linkb..........")
        return None
    return img_src
##新建文件夹
def mkdir(path):
    ##去掉path中的空格
    path = path.strip()
    if not os.path.exists(path):
        ##如果不存在则创建目录
        os.mkdir(path)
    else:
        return path
##读取图片
def read_pic(url):
    return urlopen(url).read()
##写二进制流
def write_pic(filepath,binary_data):
    if os.path.exists(filepath):
        return 0
    else:
        file = open(filepath,"wb")
        file.write(binary_data)
        file.flush()
        file.close()
        return 1
##主程序
def get_all_girls(entranceurl):
    linkas = get_linkas(entranceurl)
    for linka in linkas:
        if linka == None:
            print("===============linka is None================")
        else:
            linkbs = get_linkbs(linka)
            if linkbs == None:
                print("===============could not open linka on function get_all_girls===============")
            else:
                ##检测文件夹是否存在
                currentpath = "/Volumes/100G(HDD)/mzitu/"+linkbs['title']
                if os.path.exists(currentpath):
                    print("==============" + currentpath + " existed==================")
                    continue
                    ##linkbs不为空，创建文件夹
                mkdir(currentpath)
                for linkb in range(1,linkbs['max_value']+1):
                    #print(linka+'/'+str(linkb))
                    img_page_url = linka+'/'+str(linkb)
                    #print(get_img_link(img_page_url))
                    filepath = currentpath+'/'+ str(linkb) + '.jpg'
                    if write_pic(filepath,read_pic(get_img_link(img_page_url))):
                        print(filepath)
                    else:
                        print("============"+filepath+" has existed============")
##运行主程序
get_all_girls("http://www.mzitu.com/all")

##程序debug
#print(get_linkbs("http://www.mzitu.com/82490"))
#mkdir("/Volumes/100G(HDD)/mzitu/1")
#write_pic("/Volumes/100G(HDD)/mzitu/1/1.jpg",read_pic("http://i.meizitu.net/2016/12/26a11.jpg"))