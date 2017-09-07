import pandas
fund=int(input("Enter the Fund Number "))
startt=input("Enter the Starting Time: ")
endt=input("Enter the Ending Time: ")
data=pandas.read_excel("ES-july16.xlsx",sheetname=1)
data['Just_Date'] = data['Date'].apply(lambda x:x.date().strftime('%m/%d/%y'))
data=data.set_index(["Date"])
data=data.loc[data['Fund'] == fund]
data=data.between_time(startt,endt)
newmax=data.groupby(['Just_Date'], sort=False)['Mandate'].max()
newmin=data.groupby(['Just_Date'], sort=False)['Mandate'].min()
newdf=pandas.DataFrame()
newdf["MandateMax"]=newmax
newdf["MandateMin"]=newmin
newmax=data.groupby(['Just_Date'], sort=False)['ES'].max()
newmin=data.groupby(['Just_Date'], sort=False)['ES'].min()
newdf["ESMax"]=newmax
newdf["ES"]=newmin
newdf.reset_index(level=0, inplace=True)
newdf = pandas.merge(newdf,data,left_index = True, on=['ES','Just_Date'])
newdf["ESMin"]=newdf["ES"]
newdf=newdf[['Fund','MandateMax','MandateMin','ESMax','ESMin','Just_Date']]
newdf=newdf.drop_duplicates(subset=['Just_Date'],keep='first')
newdf=newdf[['ESMin','ESMax','MandateMin','MandateMax']]
writer = pandas.ExcelWriter('Fund '+str(fund)+'from'+startt[0]+'.xlsx')
newdf.to_excel(writer,'Max&Min')
writer.save()