# xgboost training, verification and prediction source code:
import xgboost as xgb
xlf = xgb. XGBRegressor(max_depth=8,
                       learning_rate=0.01,
                       n_estimators=1000,
                       silent=True,
                       objective=mape_object,
                       #objective='reg:linear',
                       nthread=-1,
                       gamma=0,
                       min_child_weight=6,
                       max_delta_step=0,
                       subsample=0.9,
                       colsample_bytree=0.8,
                       colsample_bylevel=1,
                       reg_alpha=1e0,
                       reg_lambda=0,
                       scale_pos_weight=1,
                       seed=9,
                       missing=None)

xlf.fit(train.values, train_label.values, eval_metric=mape_ln, 
        verbose=True, eval_set=[(test.values, test_label.values)],
        early_stopping_rounds=10)


'''
Predict sub, and save the results next May
'''
sub = pd. DataFrame()
for curHour in [8,15,18]:
    print("sub curHour", curHour)
    subTmp = feature_data.loc[(feature_data.time_interval_month == 5)&
           (feature_data.time_interval_begin_hour==curHour)
           #&(feature_data.time_interval_day>15)
           ,:]

    for i in [58,48,38,28,18,0]:
        tmp = feature_data.loc[(feature_data.time_interval_month == 5)&
                (feature_data.time_interval_begin_hour==curHour-1)
                                        &(feature_data.time_interval_minutes >= i),:]
        tmp = tmp.groupby(['link_ID', 'time_interval_day'])[
                'travel_time'].agg([('mean_%d' % (i), np.mean), ('median_%d' % (i), np.median),
                                    ('mode_%d' % (i), mode_function)]). reset_index()
        subTmp = pd.merge(subTmp,tmp,on=['link_ID','time_interval_day'],how='left')
    
    sub = pd.concat([sub,subTmp], axis=0)
    print("sub.shape", sub.shape)

sub_history = feature_data.loc[(feature_data.time_interval_month == 4),: ]
sub_history = sub_history.groupby(['link_ID', 'time_interval_minutes'])[
            'travel_time'].agg([('mean_m', np.mean), ('median_m', np.median),
                                ('mode_m', mode_function)]). reset_index()

sub = pd.merge(sub,sub_history,on=['link_ID','time_interval_minutes'],how='left')

sub_history2 = feature_data.loc[(feature_data.time_interval_month == 4),: ]
sub_history2 = sub_history2.groupby(['link_ID', 'time_interval_begin_hour'])[
            'travel_time'].agg([('median_h', np.median),
                                ('mode_h', mode_function)]). reset_index()
            
sub = pd.merge(sub,sub_history2,on=['link_ID','time_interval_begin_hour'],how='left')
sub_label = np.log1p(sub.pop('travel_time'))
sub_time = sub.pop('time_interval_begin')

sub.drop(['time_interval_month'],inplace=True,axis=1)
# Remove link_ID
sub_link = sub.pop('link_ID')

# Forecast
sub_pred = xlf.predict(sub.values, ntree_limit=xlf.best_iteration)
mape_ln1(sub_pred, sub_label) #('mape', -0.27325180044232567)

sub_out = pd.concat([sub_link, sub], axis=1)
sub_out = pd.concat([sub_out,np.expm1(sub_label)],axis=1)
sub_out['xgb_pred'] = np.expm1(sub_pred)
sub_out.to_csv('./predict_result/xgb_pred_m5.csv', index=False)

'''
Predict sub and save the results for the whole month of June
'''
sub = pd. DataFrame()
for curHour in [8,15,18]:
    print("sub curHour", curHour)
    subTmp = feature_data.loc[(feature_data.time_interval_month == 6)&
           (feature_data.time_interval_begin_hour==curHour)
           ,:]

    for i in [58,48,38,28,18,0]:
        tmp = feature_data.loc[(feature_data.time_interval_month == 6)&
                (feature_data.time_interval_begin_hour==curHour-1)
                                        &(feature_data.time_interval_minutes >= i),:]
        tmp = tmp.groupby(['link_ID', 'time_interval_day'])[
                'travel_time'].agg([('mean_%d' % (i), np.mean), ('median_%d' % (i), np.median),
                                    ('mode_%d' % (i), mode_function)]). reset_index()
        subTmp = pd.merge(subTmp,tmp,on=['link_ID','time_interval_day'],how='left')
    
    sub = pd.concat([sub,subTmp], axis=0)
    print("sub.shape", sub.shape)

sub_history = feature_data.loc[(feature_data.time_interval_month == 5),: ]
sub_history = sub_history.groupby(['link_ID', 'time_interval_minutes'])[
            'travel_time'].agg([('mean_m', np.mean), ('median_m', np.median),
                                ('mode_m', mode_function)]). reset_index()

sub = pd.merge(sub,sub_history,on=['link_ID','time_interval_minutes'],how='left')

sub_history2 = feature_data.loc[(feature_data.time_interval_month == 5),: ]
sub_history2 = sub_history2.groupby(['link_ID', 'time_interval_begin_hour'])[
            'travel_time'].agg([('median_h', np.median),
                                ('mode_h', mode_function)]). reset_index()
            
sub = pd.merge(sub,sub_history2,on=['link_ID','time_interval_begin_hour'],how='left')
sub_label = np.log1p(sub.pop('travel_time'))
sub_time = sub.pop('time_interval_begin')

sub.drop(['time_interval_month'],inplace=True,axis=1)
# Remove link_ID
sub_link = sub.pop('link_ID')

# Forecast
sub_pred = xlf.predict(sub.values, ntree_limit=xlf.best_iteration)
mape_ln1(sub_pred, sub_label)

sub_out = pd.concat([sub_link, sub], axis=1)
sub_out = pd.concat([sub_out,np.expm1(sub_label)],axis=1)
sub_out['xgb_pred'] = np.expm1(sub_pred)
sub_out.to_csv('./predict_result/xgb_pred_m6.csv', index=False)

'''
Predict sub, and save the results on July
'''
sub = pd. DataFrame()
for curHour in [8,15,18]:
    print("sub curHour", curHour)
    subTmp = feature_data.loc[(feature_data.time_interval_month == 7)&
           (feature_data.time_interval_begin_hour==curHour)
          # &(feature_data.time_interval_day<=15)
           ,:]

    for i in [58,48,38,28,18,0]:
        tmp = feature_data.loc[(feature_data.time_interval_month == 7)&
                (feature_data.time_interval_begin_hour==curHour-1)
                                        &(feature_data.time_interval_minutes >= i),:]
        tmp = tmp.groupby(['link_ID', 'time_interval_day'])[
                'travel_time'].agg([('mean_%d' % (i), np.mean), ('median_%d' % (i), np.median),
                                    ('mode_%d' % (i), mode_function)]). reset_index()
        subTmp = pd.merge(subTmp,tmp,on=['link_ID','time_interval_day'],how='left')
    
    sub = pd.concat([sub,subTmp], axis=0)
    print("sub.shape", sub.shape)

sub_history = feature_data.loc[(feature_data.time_interval_month == 5),: ]
sub_history = sub_history.groupby(['link_ID', 'time_interval_minutes'])[
            'travel_time'].agg([('mean_m', np.mean), ('median_m', np.median),
                                ('mode_m', mode_function)]). reset_index()

sub = pd.merge(sub,sub_history,on=['link_ID','time_interval_minutes'],how='left')

sub_history2 = feature_data.loc[(feature_data.time_interval_month == 5),: ]
sub_history2 = sub_history2.groupby(['link_ID', 'time_interval_begin_hour'])[
            'travel_time'].agg([('median_h', np.median),
                                ('mode_h', mode_function)]). reset_index()
            
sub = pd.merge(sub,sub_history2,on=['link_ID','time_interval_begin_hour'],how='left')
sub_label = np.log1p(sub.pop('travel_time'))
sub_time = sub.pop('time_interval_begin')

sub.drop(['time_interval_month'],inplace=True,axis=1)
# Remove link_ID
sub_link = sub.pop('link_ID')

# Forecast
sub_pred = xlf.predict(sub.values, ntree_limit=xlf.best_iteration)
mape_ln1(sub_pred, sub_label)

sub_out = pd.concat([sub_link, sub], axis=1)
sub_out = pd.concat([sub_out,np.expm1(sub_label)],axis=1)
sub_out['xgb_pred'] = np.expm1(sub_pred)
sub_out.to_csv('./predict_result/xgb_pred_m7.csv', index=False)
