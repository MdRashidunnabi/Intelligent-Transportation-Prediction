def AddBaseTimeFeature(df):
    df['time_interval_begin']=pd.to_datetime(df['time_interval'].map(lambdax:x[1:20]))
    df=df.drop(['date','time_interval'],axis=1)
    df['time_interval_month']=df['time_interval_begin'].map(lambdax:x.strftime('%m'))
    df['time_interval_day']=df['time_interval_begin'].map(lambdax:x.day)
    df['time_interval_begin_hour']=df['time_interval_begin'].map(lambdax:x.strftime('%H'))
    df['time_interval_minutes']=df['time_interval_begin'].map(lambdax:x.strftime('%M'))
    #Monday=1,Sunday=7
    df['time_interval_week']=df['time_interval_begin'].map(lambdax:x.weekday()+1)
    df['time_interval_point_num']=df['time_interval_minutes'].map(lambdax:str((int(x)+2)/2))
return df

link_info=pd.read_table(data_path+'/new_data'+'/gy_contest_link_info.txt',sep='; ',dtype={'link_ID':'str'})
link_info=link_info.sort_values('link_ID')
training_data=pd.read_table(data_path+'/new_data'+'/gy_contest_traveltime_training_data_second.txt',sep='; ',dtype={'link_ID':'str'})
feature_data=pd.merge(training_data,link_info,on='link_ID')
feature_data=feature_data.sort_values(['link_ID','time_interval'])
print ('Generating final feature matrix').
feature_data_date=AddBaseTimeFeature(feature_data)
print ('Writing final feature matrix').
feature_data_date.to_csv(data_path+'/new_data'+'/feature_data_2017.csv',index=False)

print('Reading feature matrix').
feature_data=pd.read_csv(data_path+'/data'+'/feature_data_without_missdata.csv', dtype={"link_ID":str})##Specify linkID as str( Object), convenient for oneHot
week=pd.get_dummies(feature_data['time_interval_week'],prefix='week')
delfeature_data['time_interval_week']
print ('feature matrix joins week-oneHot').
feature_data=pd.concat([feature_data,week],axis=1)

## Add category information for each point that is the first few points
print ('feature matrix and point_num stitching').
point_num=pd.get_dummies(feature_data['time_interval_point_num'],prefix='point_num')
delfeature_data['time_interval_point_num']
feature_data=pd.concat([feature_data,point_num],axis=1)
