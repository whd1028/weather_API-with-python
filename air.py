import urllib
import urllib.request as ureq
from bs4 import BeautifulSoup


def Collect(locale,pno=1,nor=10):
   site_url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty"
   serviceKey=""
   stationName = urllib.parse.quote(locale)
   dataTerm ="DAILY"   
   qeury_str = str.format("{0}?serviceKey={1}&stationName={2}&dataTerm={3}&numOfRows={4}&pageNo={5}",
                          site_url,serviceKey,stationName,dataTerm,nor,pno)
   
   request = ureq.Request(qeury_str)
   response = ureq.urlopen(request)
   if response.getcode()!=200:
       return None   
   html = BeautifulSoup(response,'html.parser')
   return html

def GetTotalCount(locale):
   html = Collect(locale)
   if html == None:
       return 0
   tc = int(html.totalcount.text)
   return tc

def CollectDustInfo(locale):
   tc = GetTotalCount(locale)
   ccount = 0
   pno=1
   titems=[]
   while ccount<tc:
       html = Collect(locale,pno,10)
       ccount += 10
       pno+=1
       items = html.find_all('item')
       titems.extend(items)
   return titems

# items = CollectDustInfo("종로구")
# for item in items:
#     print("측정일수:",item.datatime.text)
#     print("아황산가스 지수:",int(item.so2grade.text))
print(Collect("종로구"))