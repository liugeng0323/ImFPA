from scipy.special import gamma
from sklearn.metrics import f1_score
class FlowerPollination():
    X_train=pd.DataFrame()
    Y_train=pd.DataFrame()
    def __init__(self,x,y):
        self.X_train = x
        self.Y_train = y
    def Fun(self,threshold):
    #     z=gmean(Y_train,pd.DataFrame(pipeline.predict_proba(X_train)[:,0]<=threshold).replace({True:1}).replace({False:0}))
        bb=pd.DataFrame(columns=['number'],index=self.X_train.index,data=pipeline.predict_proba(X_train)[:,0]<=threshold).replace({True:1}).replace({False:0})
        bb['exit']=self.Y_train['class']
        z=f1_score(bb['exit'], bb['number'])
        return z

    def Levy(self,d):
        beta=3/2
        sigma=np.power((gamma(1+beta)*np.sin(np.pi*beta/2))/(gamma((1+beta)/2)*beta*np.power(2,(beta-1)/2)),1/beta)
        u=np.random.randn(1,d)*sigma
        v=np.random.randn(1,d)
        step=u/np.power(np.fabs(v),(1/beta))
        L=0.01*step
        return L
    def simplebounds(self,s,Lb,Ub):
        ns_tmp=s
        I=ns_tmp<Lb
        ns_tmp[I]=Lb[I]
        J=ns_tmp>Ub
        ns_tmp[J]=Ub[J]
        s=ns_tmp
        return s
    def main(self):
        para=np.array([20,0.8])
        n=para[0] 
        p=para[1]
        N_iter=2000
        d=1
        Lb=0*np.ones([1,d], dtype = int)+0.25
        Ub=1*np.ones([1,d], dtype = int)
        Sol=np.zeros((int(n),d))
        Fitness=np.zeros((int(n),1))
        for i in range(0,int(n)):
            Sol[i,:]=Lb+(Ub-Lb)*np.random.rand(1, d)
            Fitness[i,:]=self.Fun(Sol[i,:])
        a=Fitness.reshape(int(n))
        fmin=np.max(Fitness)
        try:
                I=int(np.argwhere(a==np.max(a)))
        except:
                I=int(np.argwhere(a==np.max(a))[0])
        best=Sol[I,:]
        S=Sol
        for t in range(0,int(N_iter)):
            for i in range(0,int(n)):
                if np.random.rand()>p:
                    L=self.Levy(d)
                    ds=L*(Sol[i,:]-best)
                    S[i,:]=Sol[i,:]+ds
                    S[i,:]=self.simplebounds(S[i,:].reshape(1,d),Lb,Ub)
                else:
                    epsilon=np.random.rand()
                    JK=np.random.choice(int(n),int(n),replace=False)
                    S[i,:]=S[i,:]+epsilon*(Sol[JK[0],:]-Sol[JK[1],:])
                    S[i,:]=self.simplebounds(S[i,:].reshape(1,d),Lb,Ub)
                S[i,:]=self.simplebounds(S[i,:].reshape(1,d),Lb,Ub)
                Fnew=self.Fun(S[i,:])

                if Fnew>=Fitness[i]:
                    Sol[i,:]=S[i,:]
                    Fitness[i]=Fnew
                if Fnew>=fmin:
    #                 print('change')
    #                 print('change S[i,:]',S[i,:])
    #                 print('change Fnew',Fnew)
                    best=S[i,:][0]
                    print(best)
        #             thre_best=S[i,:]
                    fmin=Fnew
        # print('best',best)
        # print('thre_best',thre_best)
        print(fmin)
        print(best)  
        #     if np.round(t/100)==t/100:
        #         print('best',best)
        #         print(fmin)
        threshold=best
        return threshold
mm=FlowerPollination(X_train,Y_train)
threshold=mm.main()