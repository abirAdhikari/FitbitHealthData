library(car)
#install.packages("mice")
library(mice)#required for finding missing data patteren



data=read.csv("data.csv",header = T)#reading CSV
data=data[,-c(1,2)]#delete timestamp column
head(data)

#Trying to find Missing data patteren for imputation
#Finding Missing Patteren
pMiss <- function(x){sum(is.na(x))/length(x)*100}
miss_colwise_1=apply(data,2,pMiss)#columnwise missing data

barplot(miss_colwise_1,col = "red",main = "Percentage of Missing Data for whole dataset")#percentage of Missing Data

#too many missing data imputation not possible, replacing missng with 0

data[is.na(data)]=0#replacing NA with 0



#EDA
cor(data$left_pedal_smoothness,data$accumulated_power)

cor(data$left_torque_effectiveness,data$accumulated_power)
cor(data)

plot(data$left_pedal_smoothness,data$accumulated_power)
plot(data$left_torque_effectiveness,data$accumulated_power)
#Testing for multiolinearity and Heteroskedasticity
#modeling heart rate

model_test=lm(heart_rate~stance_time_percent+total_timer_time+temperature+altitude,data = data)

summary(model_test)

#install.packages("gvlma")
library(gvlma)
gvlma(model_test)#global test
ncvTest(model_test)#in car package #test for heteroskedasticity
vif(model_test)#test for multicolinearity
acf(model_test$residuals)#test for autocorrelation
#all these variables has rejected H_0 for all the test with level of significance p<0.05

#PCA for choosing important variables

samp=sample(1:nrow(data),size=0.4*nrow(data))
pca.train= data[samp,]
pca.test=data[-samp,]
response=pca.train[,12]
#PCA
pca.t= prcomp(pca.train[,-12],scale. = T)
names(pca.t)
pca.t$center
pca.t$scale
pca.t$rotation
dim(pca.t$x)
biplot(pca.t,scale = 0)

stdv= pca.t$sdev
pr= stdv^2
pr[1:18]

prop_var= pr/sum(pr)
prop_var
plot(prop_var,xlab = "Principal Comp",ylab = "proportion of variance explained",type = "b")
plot(cumsum(prop_var),xlab = "Principal Comp",ylab = "Cumulative proportion of Variance",type = "b")

#creating new train data
train.dat= data.frame(response,pca.t$x)
train.dat=train.dat[,1:4]
write.csv(train.dat,"df.csv")

#creating Test data
response2=pca.test[,12]
pca.tes=prcomp(pca.test[,-12],scale. =T)
test.dat=data.frame(response2,pca.tes$x)
test.dat=test.dat[,1:4]
write.csv(test.dat,"df_test.csv")


#####Decision Tree
#install.packages("rpart")
library(rpart)
rpart.mod= rpart(response~.,data = train.dat,method = "anova")
summary(rpart.mod)

test.data=predict(pca.t,newdata = pca.test)
test.data=as.data.frame(test.data)
test.data=test.data[,1:4]

rp.pred=predict(rpart.mod,test.data)

mean(rp.pred-pca.test$training_type_name)#PREDICTION ERROR MEAN
var(rp.pred-pca.test$training_type_name)#PREDICTION ERROR VARIENCE
