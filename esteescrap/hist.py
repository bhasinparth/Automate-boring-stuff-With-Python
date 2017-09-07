import pandas 
import html5lib
st=input("Enter the start date ")
lt=input("Enter the end date ")
val=input("Enter the index ")
if val=='Nifty 50':
    term=207437
else:
    term=10460783
url='https://www.google.com/finance/historical?cid='+str(term)+'&startdate='+st[3:6]+'+'+st[0:2]+'%2C+'+st[7:11]+'&enddate='+lt[3:6]+'+'+lt[0:2]+'%2C+'+st[7:11]+'&num=3000.html'
table=pandas.read_html(url)
table=table[2]
writer = pandas.ExcelWriter(val+" "+st+"-"+lt+'.xlsx')
table.to_excel(writer,'Sheet 0')
writer.save()
