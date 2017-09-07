import pandas
legal=pandas.read_excel("AccountInformation1.xlsx",sheetname=0)
balance=pandas.read_excel("AccountInformation1.xlsx",sheetname=1)
new=balance.groupby(["Date","Legal Entity"],as_index=False)["Money Deployed"].sum()
result = pandas.merge(legal, new, on=['Date', 'Legal Entity'])
new=balance.groupby(["Date","Legal Entity"],as_index=False)["MTD sqOff Loss"].sum()
result = pandas.merge(result, new, on=['Date', 'Legal Entity'])
new=balance.groupby(["Date","Legal Entity"],as_index=False)["Delta LR"].sum()
result = pandas.merge(result, new, on=['Date', 'Legal Entity'])
new=balance.groupby(["Date","Legal Entity"],as_index=False)["Balance"].sum()
result = pandas.merge(result, new, on=['Date', 'Legal Entity'])
new=balance.groupby(["Date","Legal Entity"],as_index=False)["Allocated Capital"].sum()
result = pandas.merge(result, new, on=['Date', 'Legal Entity'])
result.loc[result["MTD sqOff Loss"]<0,"MTD sqOff Loss"]=0
result["Utilization"]=result["MTD_MoneyDeployed"]+result["MTD sqOff Loss"]+result["Delta LR_x"]
result["Utilization"]=result["Utilization"]/result["Balance"]
result.loc[result["Utilization"]<0,"Utilization"]=0
result["LR/Mandate"]=result["LiquidityRiskMax"]/result["Mandate"]
result.loc[result["LR/Mandate"]<0,"LR/Mandate"]=0
result["LR/Allocated"]=result["LiquidityRiskMax"]/result["Allocated Capital"]
result.loc[result["LR/Allocated"]<0,"LR/Allocated"]=0
result=result[['Date','Legal Entity','Utilization','LR/Mandate']]
result=result[result['Date']>'2016-05-31']
result=result.set_index('Date')
eadvisors=result.loc[result['Legal Entity']=='Estee Advisors']
eif=result.loc[result['Legal Entity']=='Estee India Fund']
ecapital=result.loc[result['Legal Entity']=='Estee Capital LLC']
ecommodities=result.loc[result['Legal Entity']=='Estee Commodities']
ialpha=result.loc[result['Legal Entity']=='I-Alpha']
client=result.loc[result['Legal Entity']=='Client Accounts']
eml=result.loc[result['Legal Entity']=='Estee Management Limited']
ujay=result.loc[result['Legal Entity']=='UJAY']
import matplotlib
import matplotlib.pyplot as plt
k=eadvisors.plot.area(stacked=False)
vals = k.get_yticks()
k.set_yticklabels(['{:3.2f}%'.format(x*100) for x in vals])
k=k.plot(('1990-01-01', '2080-12-12'), (0.95, 0.95), 'r-')
plt.savefig('Estee Advisors.png')

k=eif.plot.area(stacked=False)
vals = k.get_yticks()
k.set_yticklabels(['{:3.2f}%'.format(x*100) for x in vals])
k=k.plot(('1990-01-01', '2080-12-12'), (0.95, 0.95), 'r-')
plt.savefig('Estee India Fund.png')

k=ecapital.plot.area(stacked=False)
vals = k.get_yticks()
k.set_yticklabels(['{:3.2f}%'.format(x*100) for x in vals])
k=k.plot(('1990-01-01', '2080-12-12'), (0.95, 0.95), 'r-')
plt.savefig('Estee Capital LLC.png')

k=ecommodities.plot.area(stacked=False)
vals = k.get_yticks()
k.set_yticklabels(['{:3.2f}%'.format(x*100) for x in vals])
k=k.plot(('1990-01-01', '2080-12-12'), (0.95, 0.95), 'r-')
plt.savefig('Estee Commodities.png')

k=ialpha.plot.area(stacked=False)
vals = k.get_yticks()
k.set_yticklabels(['{:3.2f}%'.format(x*100) for x in vals])
k=k.plot(('1990-01-01', '2080-12-12'), (0.95, 0.95), 'r-')
plt.savefig('I-Alpha.png')

k=client.plot.area(stacked=False)
vals = k.get_yticks()
k.set_yticklabels(['{:3.2f}%'.format(x*100) for x in vals])
k=k.plot(('1990-01-01', '2080-12-12'), (0.95, 0.95), 'r-')
plt.savefig('Client Accounts.png')

k=eml.plot.area(stacked=False)
vals = k.get_yticks()
k.set_yticklabels(['{:3.2f}%'.format(x*100) for x in vals])
k=k.plot(('1990-01-01', '2080-12-12'), (0.95, 0.95), 'r-')
plt.savefig('Estee Management Limited.png')

k=ujay.plot.area(stacked=False)
vals = k.get_yticks()
k.set_yticklabels(['{:3.2f}%'.format(x*100) for x in vals])
k=k.plot(('1990-01-01', '2080-12-12'), (0.95, 0.95), 'r-')
plt.savefig('UJAY.png')

writer = pandas.ExcelWriter('Values.xlsx')
eadvisors.to_excel(writer,'Estee Advisors')
eif.to_excel(writer,'Estee India Fund')
ecapital.to_excel(writer,'Estee Capital LLC')
ecommodities.to_excel(writer,'Estee Commodities')
ialpha.to_excel(writer,'I-Alpha')
client.to_excel(writer,'Client Accounts')
eml.to_excel(writer,'Estee Management Limited')
ujay.to_excel(writer,'UJAY')
writer.save()