def mape_ln(y,d):
    c=d.get_label()
    result= -np.sum(np.abs(np.expm1(y)-np.abs(np.expm1(c)))/np.abs(np.expm1(c)))/len(c)
    return "mape",result
# where y is the predicted value and d is the true value
