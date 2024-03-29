import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression as _lr
from sklearn.metrics import mean_squared_error
from scipy.stats.stats import pearsonr
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler


class LinearRegression:
    random.seed(12)
    def __init__(self,data_x,data_y):
       self.dataset_x =np.array(data_x)
       self.expected=np.array(data_y).reshape(-1,1)
       self.thetas=[]
       self.bias=random.uniform(0,1)
       self.hypothesis_matrix=[]
       #print(self.dataset_x[:,0])#all elements of first columns
       #print(self.dataset_x.shape[1])#number of columns

    def initial_coefficient(self):
        print("initial_coefficient")
        print(self.dataset_x.shape[1])
        self.thetas=np.array([random.uniform(0,1) for i in range((self.dataset_x.shape[1]))]).reshape(-1,1)
        print(self.thetas)

    def gradient_descent(self,alpha):
        old_thetas=self.thetas
        self.thetas=old_thetas-(alpha)*(np.matmul(self.dataset_x.T , (self.hypothesis_matrix-self.expected))/self.dataset_x.shape[0])
        return self.thetas,old_thetas

    def fit_linearregression(self,alpha,max_itreration):

        for i in range(max_itreration):
           self.hypothesis_matrix=np.array(np.matmul(self.dataset_x, self.thetas))
           error_cost_matrix=(self.hypothesis_matrix-self.expected)
           updated_theta,old_thetas=self.gradient_descent(alpha)
           convergence=True
           if np.isclose(updated_theta,old_thetas,rtol=0,atol=0).all():
               break
           else:
               convergence=False

        return self.thetas,self.hypothesis_matrix

    def predit(self,test_data_x,modelcoefficient):
        predited_y = np.array(np.matmul(np.array(test_data_x), modelcoefficient))
        return predited_y


class performance_metrics:

    def Mean_Squared_error(self,expected,predicted):
        #print(np.subtract(np.array(expected),np.array(predicted)))
        mean_squared_error=np.square(np.subtract(np.array(expected),np.array(predicted))).mean()

        return mean_squared_error

    def pearson_corelation_coefficient(self,expected,predicted):
        cov_XY=np.sum(np.subtract(np.array(expected),np.array(expected).mean())*np.subtract(np.array(predicted),np.array(predicted).mean()))
        std_X= np.sqrt(np.sum(np.square(np.subtract(np.array(expected),np.array(expected).mean()))))
        std_Y=np.sqrt(np.sum(np.square(np.subtract(np.array(predicted),np.array(predicted).mean()))))

        return cov_XY/(std_X*std_Y)

    def Rsquared_valued(self,expected,predicted):
        '''
        r(Y,{\hat {Y}})^{2}={\frac {SS_{\text{reg}}}{SS_{\text{tot}}}}
        where
        {\displaystyle SS_{\text{reg}}}SS_{\text{reg}} is the regression sum of squares, also called the explained sum of squares
        {\displaystyle SS_{\text{tot}}}SS_{\text{tot}} is the total sum of squares (proportional to the variance of the data)
        {\displaystyle SS_{\text{reg}}=\sum _{i}({\hat {Y}}_{i}-{\bar {Y}})^{2}}SS_{\text{reg}}=\sum _{i}({\hat {Y}}_{i}-{\bar {Y}})^{2}
        {\displaystyle SS_{\text{tot}}=\sum _{i}(Y_{i}-{\bar {Y}})^{2}}SS_{\text{tot}}=\sum _{i}(Y_{i}-{\bar {Y}})^{2}
        '''
        
        SS_residual = np.sum(np.square(np.subtract(np.array(expected), np.array(predicted))))
        SS_total=np.sum(np.square(np.subtract(np.array(expected),np.array(expected).mean())))

        return 1-(SS_residual/SS_total)


if __name__ == "__main__":

    data_path="BSOM_DataSet_for_HW2.csv"
    data=pd.read_csv(data_path)
    data=data.drop(['LEVEL'],axis=1)
    #data=data[['all_mcqs_avg_n20','STEP_1','all_NBME_avg_n4']]
    data = (data - data.mean()) / data.std()
    #data=pd.DataFrame(StandardScaler().fit(data).transform(data),columns=['all_mcqs_avg_n20','STEP_1','all_NBME_avg_n4'])
    'Replacing missign values with mean for STEP_1'
    mean=data['STEP_1'].mean()
    #print(data['STEP_1'])
    'split data into training set and test set'
    data_copy = data.copy()
    train_set = data_copy.sample(frac=0.80, random_state=12)
    test_set = data_copy.drop(train_set.index)
    #print(train_set.shape)
    #print(test_set.shape)
    'training data'
    #train_data=train_set.drop(['LEVEL'],axis=1)
    train_set.insert(0, 'x0', 1)
    train_data_x=train_set[['x0','all_mcqs_avg_n20']]
    train_data_y=train_set['STEP_1']
    train_data_y=np.array(train_data_y.fillna(mean)).reshape(-1,1)
    'test data'
    #test_data = test_set.drop(['LEVEL'], axis=1)
    #test_data = (test_set - test_set.mean()) / test_set.std()
    test_set.insert(0, 'x0', 1)
    test_data_x = test_set[['x0', 'all_mcqs_avg_n20']]
    test_data_y = test_set['STEP_1']
    test_data_y = np.array(test_data_y.fillna(mean)).reshape(-1, 1)

    'Linear regression function model optimization for training data'
    Linear_obj=LinearRegression(train_data_x,train_data_y)
    Linear_obj.initial_coefficient()
    coeff,hyp = Linear_obj.fit_linearregression(0.1,1000)

    'plot the regression model line'
    plt.scatter(train_data_x["all_mcqs_avg_n20"], train_data_y)
    train_pred_y=np.array(train_data_x["all_mcqs_avg_n20"]*coeff[1] + coeff[0]).reshape(-1,1)

    'from sklearn library'
    lr = _lr().fit(train_data_x, train_data_y)
    # print(lr.intercept_)
    print("sklearn coefficients", lr.coef_[0][1], lr.intercept_)
    plt.plot(train_data_x["all_mcqs_avg_n20"], train_data_x["all_mcqs_avg_n20"] * lr.coef_[0][1] + lr.intercept_,marker='*' ,label="Sklearn Linear Regression Line")


    print("algorithm coefficients",coeff[1],coeff[0])
    plt.plot(train_data_x["all_mcqs_avg_n20"], train_data_x["all_mcqs_avg_n20"]*coeff[1] + coeff[0],label='Linear Regression Line')
    plt.xlabel("X-all_mcqs_avg_n20")
    plt.ylabel("Y-Predicted")



    plt.title("Linear Regression Model for X=all_mcqs_avg_n20 Y=STEP_1")
    plt.legend()
    plt.show()

    'Residual plot'
    plt.scatter(train_data_y,train_data_y-train_pred_y)
    plt.axhline(y=0,color='r',linestyle='--')
    plt.xlabel("predicted/fit values")
    plt.ylabel("residual ( observed - predicted)")
    plt.title("Residual vs fit plot")
    plt.show()

    'prediction on test data'
    #print(coeff)
    pred_y = Linear_obj.predit(test_data_x,coeff)
    pred_y_tool=lr.predict(test_data_x)
    #print(pred_y,pred_y_tool)


    '''metrics'''
    metrics=performance_metrics()
    mean_squared_error_algo=metrics.Mean_Squared_error(test_data_y,pred_y)
    print("meanerror_algorithm",mean_squared_error_algo)
    mean=mean_squared_error(test_data_y,pred_y_tool)
    print("sklearn",mean)
    'pearson coefficient'
    r=metrics.pearson_corelation_coefficient(test_data_y,pred_y)
    print("r pearson coefficient_algorithm:",r)
    #print(np.array(data_y),np.array(pred_y))
    print("scipy pearson coefficient      :",pearsonr(test_data_y, pred_y_tool)[0])
    'R-squared value'
    R_squared=metrics.Rsquared_valued(test_data_y,pred_y)
    print("R-sqared algorithm :",R_squared)
    print("R-squared sklearn :",r2_score(test_data_y,pred_y_tool))

    

 
