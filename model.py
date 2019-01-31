import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier

from sklearn import svm
from sklearn import cross_validation,metrics
from sklearn.metrics import precision_score,recall_score,f1_score

import matplotlib.pyplot as plt


data_train=pd.read_csv('df.csv')
array=data_train.values
response= array[:,0]
predictors=array[:,1:4]

data_test=pd.read_csv('df_test.csv')
array2=data_test.values
response_test=array2[:,0]
pred_test=array2[:,1:4]



def main():
    # print '\nstarting GBM'
    # seed=7
    # kfold=model_selection.KFold(n_split=10,random_state=seed)
    # model=GradientBoostingClassifier(n_estimators=100,random_state=seed)
    # results=model_selection.cross_val_score(model,predictors,response,cv=kfold,scoring='roc-auc')
    # print '\nError Variance Mean'
    # print(results.mean())
    # print '\nVariance of Error'
    # print(results.std())





    print '\nstarting svm'
    svr=svm.SVC(class_weight='balanced',C=100,kernel='rbf',decision_function_shape='ovr')
    res=svr.fit(predictors,response)
    predicted_class_label=res.predict(predictors)
    predicted_class_label = list(predicted_class_label)

    print 'Evaluation using Precision, Recall and F-measure'
    pr=precision_score(response, predicted_class_label, average='micro')
    print '\n Precision:'+str(pr)
    re=recall_score(response, predicted_class_label, average='micro')
    print '\n Recall:'+str(re)
    fm=f1_score(response, predicted_class_label, average='micro')
    print '\n F-measure:'+str(fm)

    print 'Classification of the test samples'
    predicted_class_label = res.predict(response_test)
    predicted_class_label = list(predicted_class_label)

    print 'Evaluation using Precision, Recall and F-measure'
    pr=precision_score(response_test, predicted_class_label, average='micro')
    print '\n Precision:'+str(pr)
    re=recall_score(response_test, predicted_class_label, average='micro')
    print '\n Recall:'+str(re)
    fm=f1_score(response_test, predicted_class_label, average='micro')
    print '\n F-measure:'+str(fm)



if __name__=='__main__':
    main()
