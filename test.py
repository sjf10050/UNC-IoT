# -*- coding:utf-8 -*-

'''
从百度把前10页的搜索到的url爬取保存
'''
import baidu as baidu
import dbAPI as dbAPI
import xlwt
def writrToExcel():
    # _id = request.GET.get('id', 0)
    # list_obj = Song.objects.filter(is_delete__exact=False)  # django orm   
    # if list_obj:   # 创建工作薄 
    book = xlwt.Workbook(encoding='utf-8',style_compression=0)
    sheet = book.add_sheet('SearchRecords',cell_overwrite_ok=True)
    sheet.write(0,0, u"title")
    sheet.write(0,1, u"link")
    book.save('results/a.xls')
    

if __name__ == '__main__':
    #writrToExcel()
    #a="aaa"
    #s="this is %s ?"%a
    #print(s)
    dbAPI.DelResult("abcd")
    #print(baidu.getresultcount('apple'))
    #dbAPI.exportToFile("china Unicom1540973897.505704")
    #baidu.getresultcount('apple')
