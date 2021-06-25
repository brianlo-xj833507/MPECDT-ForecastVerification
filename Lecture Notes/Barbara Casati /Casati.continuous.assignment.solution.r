#------ initializing arrays with monthly values

samplemm=c(31,28,31,30,31,30,31,31,30,31,30,31)

meanXmm=c(15,17,19,21,23,25,27,25,23,21,19,17)
meanYmm=c(20,21,22,23,24,25,26,25,24,23,22,21)

stdevXmm=c(1,1,1.5,1.5,1.5,2,2,2,1.5,1.5,1.5,1)
stdevYmm=c(1,1,2,2,2,3,3,3,2,2,2,1)

corrXYmm=c(0.8,0.8,0.7,0.7,0.7,0.6,0.6,0.6,0.7,0.7,0.7,0.8)

#------- evaluate the aggregated annual bias

weightmm=samplemm/sum(samplemm)

meanXaggr=sum(meanXmm*weightmm)         # 21.02192
meanYaggr=sum(meanYmm*weightmm)	        # 23.01096

biasYXaggr=meanYaggr-meanXaggr		# 1.989041

#------- evaluate the aggregated annual stdev

# key equation: var(X)=mean(X^2)-[mean(X)]^2

meanX2mm=(stdevXmm)^2+(meanXmm)^2
meanY2mm=(stdevYmm)^2+(meanYmm)^2

meanX2aggr=sum(meanX2mm*weightmm)         # 457.0158
meanY2aggr=sum(meanY2mm*weightmm)	  # 537.2027

varXaggr=meanX2aggr-(meanXaggr)^2	# 15.09473
varYaggr=meanY2aggr-(meanYaggr)^2	# 7.69851

stdevXaggr=sqrt(varXaggr)		# 3.885193
stdevYaggr=sqrt(varYaggr)		# 2.774619

#------- evaluate the aggregated annual correlation

# key equations: 
# cov(X,Y)=corr(X,Y)*stdev(X)*stdev(Y)
# cov(X,Y)=mean(X*Y)-mean(X)*mean(y)

covXYmm=corrXYmm*stdevXmm*stdevYmm

meanXYmm=covXYmm+meanXmm*meanYmm
meanXYaggr=sum(meanXYmm*weightmm)		# 492.2479

covXYaggr=meanXYaggr-meanXaggr*meanYaggr	# 8.513458
corXYaggr=covXYaggr/(stdevXaggr*stdevYaggr)	# 0.7897508

#------- evaluate the aggregated MSE

MSEaggr=(biasYXaggr)^2+varXaggr+varYaggr-2*covXYaggr  # 9.722603

#------- buddy check!

MSEmm=(meanYmm-meanXmm)^2+(stdevXmm)^2+(stdevYmm)^2-2*covXYmm
controlMSEaggr=sum(MSEmm*weightmm)		# 9.722603

#------- the end -------

distrX=matrix(0,nrow=100,ncol=12)
distrY=matrix(0,nrow=100,ncol=12)
for(mm in seq(1,12)){
distrX[,mm]=rnorm(100,meanXmm[mm],stdevXmm[mm])
distrY[,mm]=rnorm(100,meanYmm[mm],stdevYmm[mm])
}


png(file="assignment.png",width=800,height=400)
plot(seq(1,12),rep(20,12),ylim=c(10,35),type="n",xlab="month",ylab="temperature")
boxplot(distrX,add=TRUE,vertical=TRUE,col=4,boxwex=0.8,range=0)
boxplot(distrY,add=TRUE,vertical=TRUE,col=2,boxwex=0.3,range=0)
axis(3,at=seq(1,12),labels=corrXYmm)
mtext("monthly correlation",side=3,line=3)
legend(x=1,y=35,fill=c(4,2),legend=c("obs X","fcst Y"))
dev.off()

