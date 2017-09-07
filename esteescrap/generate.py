import pandas
segment=pandas.read_excel("Segment.xlsx",sheetname=0)
segment=segment.rename(columns = {'Strategy Category':'Name'})
segment=segment.drop("Fund",1)
orig_category=pandas.read_excel("New_tab_reports_updated.xls",sheetname=0)
orig_category
orig_group=pandas.read_excel("New_tab_reports_updated.xls",sheetname=2)
daily_data=pandas.DataFrame()
daily_data["Date"]=orig_category["Date"]
daily_data["Name"]=orig_category["Name"]
daily_data=pandas.merge(daily_data,segment,on="Name")
daily_data=daily_data.merge(orig_category[list(['Name','MTD BE PNL','Unnamed: 34','ConversionRate','FTD BE PNL'])])
daily_data["MTD BE PnL"]=(daily_data["MTD BE PNL"]-abs(daily_data["Unnamed: 34"]))*daily_data["ConversionRate"]
daily_data["FTD BE PnL"]=daily_data["FTD BE PNL"]*daily_data["ConversionRate"]
daily_data["MTD Stipend"]=daily_data["Unnamed: 34"]*daily_data["ConversionRate"]
daily_data=daily_data.rename(columns = {'Name':'Group Name'})
daily_data=daily_data[['Date','Segment','Group Name','MTD BE PnL','FTD BE PnL','MTD Stipend']]
daily_data['Date'] = daily_data['Date'].apply(lambda x:x.date().strftime('%m/%d/%y'))
mandate_margin=pandas.DataFrame()
mandate_margin["Date"]=orig_category["Date"]
mandate_margin["Name"]=orig_category["Name"]
mandate_margin=pandas.merge(mandate_margin,segment,on="Name")
mandate_margin=mandate_margin.merge(orig_category[list(['Name','MTD Money Deployed','FTD Turnover','Margin Mandate','ConversionRate'])])
mandate_margin["MTD Money Deployed (Million)"]=mandate_margin["MTD Money Deployed"]/1000000*mandate_margin["ConversionRate"]
mandate_margin["FTD Turnover (Million)"]=mandate_margin["FTD Turnover"]/1000000*mandate_margin["ConversionRate"]
mandate_margin["Mandate Total"]=mandate_margin["Margin Mandate"]/1000*mandate_margin["ConversionRate"]
mandate_margin=mandate_margin[['Date','Segment','Name','MTD Money Deployed (Million)','FTD Turnover (Million)','Mandate Total']]
mandate_margin['Date'] = mandate_margin['Date'].apply(lambda x:x.date().strftime('%m/%d/%y'))
es=pandas.DataFrame()
es["Date_Evaluation"]=orig_category["Date"]
es["Name"]=orig_category["Name"]
es=pandas.merge(es,segment,on="Name")
es=es.merge(orig_category[list(['Name','ConversionRate','ESMAX'])])
es["ES"]=es["ESMAX"]*es["ConversionRate"]
es=es.rename(columns = {'Name':'StrategyGroupName'})
es["ES"].fillna(0, inplace=True)
es=es[['Date_Evaluation','Segment','StrategyGroupName','ES']]
es['Date_Evaluation'] = es['Date_Evaluation'].apply(lambda x:x.date().strftime('%m/%d/%y'))
group_pnl=pandas.DataFrame()
group_pnl["Date"]=orig_group["Date"]
group_pnl["Name"]=orig_group["Name"]
group_pnl['Segment'] = group_pnl['Name'].astype(str).str[0:3]
group_pnl=pandas.merge(group_pnl,segment,on="Segment")
group_pnl=group_pnl.rename(columns = {'Name_y':'Strategy Category'})
group_pnl=group_pnl.rename(columns = {'Name_x':'Name'})
group_pnl=group_pnl.merge(orig_group[list(['Name','MTD Money Deployed','MTD BE PNL','FTD BE PNL','ConversionRate','Rebate'])])
group_pnl["Money Deployed"]=group_pnl["MTD Money Deployed"]*group_pnl["ConversionRate"]
group_pnl["MTD PnL"]=(group_pnl["MTD BE PNL"]-abs(group_pnl["Rebate"]))*group_pnl["ConversionRate"]
group_pnl["FTD PnL"]=group_pnl["FTD BE PNL"]*group_pnl["ConversionRate"]
group_pnl["MTD Stipends"]=(group_pnl["Rebate"])*group_pnl["ConversionRate"]
group_pnl=group_pnl.rename(columns = {'Name':'Strategy Group'})
group_pnl["FTD Stipends"]=0
group_pnl=group_pnl[['Date','Segment','Strategy Category','Strategy Group','Money Deployed','MTD PnL','FTD PnL','MTD Stipends','FTD Stipends']]
writer = pandas.ExcelWriter('output.xlsx')
daily_data.to_excel(writer,'Daily Data')
mandate_margin.to_excel(writer,'Mandate Margin')
es.to_excel(writer,'ES')
group_pnl.to_excel(writer,'Group Pnl Data')
writer.save()