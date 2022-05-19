    '''
    train data April training
    '''
    train = pd. DataFrame()
    train4 = pd. DataFrame()
    for curHour in [8,15,18]:
        print("train4 curHour", curHour)
        trainTmp = feature_data.loc[(feature_data.time_interval_month == 4)&
               (feature_data.time_interval_begin_hour==curHour)
              # &(feature_data.time_interval_day<=15)
               ,:]
    
        for i in [58,48,38,28,18,0]:
            tmp = feature_data.loc[(feature_data.time_interval_month == 4)&
                    (feature_data.time_interval_begin_hour==curHour-1)
                                            &(feature_data.time_interval_minutes >= i),:]
            tmp = tmp.groupby(['link_ID', 'time_interval_day'])[
                    'travel_time'].agg([('mean_%d' % (i), np.mean), ('median_%d' % (i), np.median),
                                        ('mode_%d' % (i), mode_function)]). reset_index()
            #train = pd.merge(train,tmp,on=['link_ID','time_interval_day','time_interval_begin_hour'],how='left')
            trainTmp = pd.merge(trainTmp,tmp,on=['link_ID','time_interval_day'],how='left')
            
        train4 = pd.concat([train4,trainTmp], axis=0)
        print("     train4.shape", train4.shape)
    
    train4_history = feature_data.loc[(feature_data.time_interval_month == 3),: ]
    train4_history = train4_history.groupby(['link_ID', 'time_interval_minutes'])[
                'travel_time'].agg([('mean_m', np.mean), ('median_m', np.median),
                                    ('mode_m', mode_function)]). reset_index()
    
    train4 = pd.merge(train4,train4_history,on=['link_ID','time_interval_minutes'],how='left')
    
    train_history2 = feature_data.loc[(feature_data.time_interval_month == 3),: ]
    train_history2 = train_history2.groupby(['link_ID', 'time_interval_begin_hour'])[
                'travel_time'].agg([ ('median_h', np.median),
                                    ('mode_h', mode_function)]). reset_index()
                
    train4 = pd.merge(train4, train_history2,on=['link_ID','time_interval_begin_hour'],how='left')
    print("train4.shape", train4.shape)
    train = train4
    
    train_label = np.log1p(train.pop('travel_time'))
    train_time = train.pop('time_interval_begin')
    
    train.drop(['time_interval_month'],inplace=True,axis=1)
    train_link=train.pop('link_ID') #(253001, 35)
    print("train.shape", train.shape)
    
    '''
Test review for the whole month of June
    '''
    
    test = pd. DataFrame()
    for curHour in [8,15,18]:
        print("test curHour", curHour)
        testTmp = feature_data.loc[(feature_data.time_interval_month == 6)&
               (feature_data.time_interval_begin_hour==curHour)
               ,:]
    
        for i in [58,48,38,28,18,0]:
            tmp = feature_data.loc[(feature_data.time_interval_month == 6)&
                    (feature_data.time_interval_begin_hour==curHour-1)
                                            &(feature_data.time_interval_minutes >= i),:]
            tmp = tmp.groupby(['link_ID', 'time_interval_day'])[
                    'travel_time'].agg([('mean_%d' % (i), np.mean), ('median_%d' % (i), np.median),
                                        ('mode_%d' % (i), mode_function)]). reset_index()
            testTmp = pd.merge(testTmp,tmp,on=['link_ID','time_interval_day'],how='left')
        
        test = pd.concat([test,testTmp], axis=0)
        print("test.shape", test.shape)
    
    test_history = feature_data.loc[(feature_data.time_interval_month == 5),: ]
    test_history = test_history.groupby(['link_ID', 'time_interval_minutes'])[
                'travel_time'].agg([('mean_m', np.mean), ('median_m', np.median),
                                    ('mode_m', mode_function)]). reset_index()
    
    test = pd.merge(test,test_history,on=['link_ID','time_interval_minutes'],how='left')
    
    test_history2 = feature_data.loc[(feature_data.time_interval_month == 5),: ]
    test_history2 = test_history2.groupby(['link_ID', 'time_interval_begin_hour'])[
                'travel_time'].agg([ ('median_h', np.median),
                                    ('mode_h', mode_function)]). reset_index()
                
    test = pd.merge(test,test_history2,on=['link_ID','time_interval_begin_hour'],how='left')
    
    test_label = np.log1p(test.pop('travel_time'))
    test_time = test.pop('time_interval_begin')
    
    
    test.drop(['time_interval_month'],inplace=True,axis=1)
    
# Remove link_ID
    test_link=test.pop('link_ID')
