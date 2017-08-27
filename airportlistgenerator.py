import pandas
import numpy
import html5lib
url="https://en.wikipedia.org/wiki/List_of_international_airports_by_country"
table=pandas.read_html(url)
maindf=pandas.DataFrame()
for x in range(62):
    newdf=pandas.DataFrame()
    newdf["Place"]=table[x][0]
    newdf["Airport"]=table[x][1]
    newdf["Code"]=table[x][2]
    maindf=maindf.append(newdf)

maindf=maindf.dropna(how='any')
to_drop=['Location']
maindf=maindf[~maindf['Place'].isin(to_drop)]
maindf=maindf.reset_index(drop=True)
writer = pandas.ExcelWriter('AirportList.xlsx')
maindf.to_excel(writer,'List')
writer.save()
