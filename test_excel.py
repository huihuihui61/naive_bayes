#-*- coding:utf-8
import xlrd
import xlwt
import random
import urllib
import urllib2
import json
JSON_PREFIX = "http://c.m.163.com/nc/video/detail/"

def randomGetNum(nrows,table):
    resultList = random.sample(range(0, nrows), 1000)
    return resultList

def parseExcelRandom():
    data = xlrd.open_workbook('base_20171013.xlsx')
    table = data.sheets()[0]
    nrows = table.nrows
    randIndex = randomGetNum(nrows,table)
    for i in range(len(randIndex)):
        if randIndex[i] == 0:
            continue
        if len(table.row_values(randIndex[i])) == 8:
            docid =  table.row_values(randIndex[i])[0].encode('utf-8')
            title = table.row_values(randIndex[i])[2].encode('utf-8')
            sansu_score = table.row_values(randIndex[i])[6]
            seqing_score = table.row_values(randIndex[i])[7]
            if sansu_score != '' and seqing_score != '':
                img_url = getJSONweb(docid)
                if img_url != None:
                    print "================================================================================"
                    print docid
                    print title
                    print img_url
                    print "sansu_score:" + str(sansu_score) + "           " + "seqing_score:" + str(seqing_score)
                    print "==============================================================================="

def parseExcel():
    data = xlrd.open_workbook('base_20171013.xlsx')
    table = data.sheets()[0]
    nrows = table.nrows
    n = 0
    from xlwt import Workbook
    w = Workbook(encoding='utf-8')
    ws = w.add_sheet("Sheet1",cell_overwrite_ok=True)
    for i in range(nrows):
        docid = table.row_values(i)[0].encode('utf-8')
        title = table.row_values(i)[2].encode('utf-8')
        sansu_score = table.row_values(i)[6]
        seqing_score = table.row_values(i)[7]
        if sansu_score != '' and seqing_score != '':
            img_url = getJSONweb(docid)
            if img_url != None:
                n += 1
                if n <= 2500:
                    print "================================================================================"
                    print docid
                    print title
                    print img_url
                    print "sansu_score:" + str(sansu_score) + "           " + "seqing_score:" + str(seqing_score)
                    print "==============================================================================="
                    writeExcel(docid,title,img_url,sansu_score,seqing_score,n,ws)
    w.save("res.xls")

def writeExcel(docid,title,img_url,sansu_score,seqing_score,index,ws):
    ws.write(index,0,docid)
    ws.write(index,1,title)
    ws.write(index,2,img_url)
    ws.write(index,3,sansu_score)
    ws.write(index,4,seqing_score)

def getJSONweb(docid):
    try:
        url = JSON_PREFIX + docid + ".html"
        #print url
        request = urllib2.Request(url)
        request.add_header('User-Agent','MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0')
        page = urllib2.urlopen(request)
        hjson = json.loads(page.read())
        if 'cover' in hjson:
            img_url = hjson['cover']
            return img_url
    except Exception,e:
        print "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww"
        print docid
        print e

if __name__ == "__main__":
    parseExcel()