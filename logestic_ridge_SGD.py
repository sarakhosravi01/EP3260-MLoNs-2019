#Group 2
import numpy as np

def SGD(x,y, w, alpha, num_iters, lambda_, epsilon):
    Z = np.matmul(x,np.diagflat(y))
    N = Z.shape[1]
    for i in range(num_iters):
        col = int(np.random.random(1) * N)
        A = np.matmul(-1 * w.T, Z[:,col])
        A = A.reshape(A.shape[0],1)
        #print(A.shape)
        column = Z[:,col].reshape(Z[:,col].shape[0],1)
        g = np.matmul(column,(1/(1+np.exp(A))-1))+ 2 * lambda_ * w
        print(g.shape)
        w = w - alpha * g
        # if (np.linalg.norm(g) <= epsilon):
        #     break
    return w

def cost(x,y,w,lambda_):
    N = x.shape[1]
    value = 0
    for i in range(N):
        y_ = y[i].reshape(y[i].shape[0],1)
        x_ = x[:,i].reshape(x[:,i].shape[0],1)
        value += np.log(1+np.exp(-1*np.matmul(np.matmul(y_,w.T),x_)))
    return value/N + lambda_ * (np.linalg.norm(w) ** 2)

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import time
# from sklearn.linear_model import RidgeClassifier

np.random.seed(0)

data = pd.read_csv("household_power_consumption.txt",";")

print(data.shape)
print(data.head(3))
print(data.tail(3))

X = pd.DataFrame(data.iloc[:,2:6], columns=["Global_active_power","Global_reactive_power","Voltage","Global_intensity"])
Y = pd.DataFrame(data.iloc[:,7], columns=["Sub_metering_2"])

print(X.head())

X = X.replace({'?':0})
Y = Y.replace({'?':0})

###########!!!!!We need to set the timestamp as the index of data set and use it in next steps.
###########!!!!!We can also use index to sort data set before training.

X_features = X.columns
Y_features = Y.columns
XY = pd.concat([X[X_features], Y[Y_features]], axis=1)

# Split XY into training set and test set of equal size
train, test = train_test_split(XY, test_size = 0.005)
# Sort the train and test sets after index (which became unsorted through sampling)
train = train.sort_index(axis=0)
test = test.sort_index(axis=0)

# Extract X,Y components from test and train sets
X_train = train[X_features].astype(float); X_test = test[X_features].astype(float)
Y_train = train[Y_features].astype(float); Y_test = test[Y_features].astype(float)

print(X_train.shape,X_test.shape, Y_train.shape,Y_test.shape)

w = np.zeros((X_train.shape[1],1))
alpha = 0.1
num_iters = 1000
lambda_ = 0.1
epsilon = 0.001
y = np.array(Y_train.iloc[0:6000])
x = np.array(X_train.iloc[0:6000,:])
sgde = SGD(x.T,y,w, alpha, num_iters, lambda_, epsilon)
print(sgde)

err = cost(x.T,y,sgde,0.1)
print(err)


