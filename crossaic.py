import pandas as pd
import numpy as np
import math
import sys
from itertools import chain

class Aic:
    
    def __init__(self,x,y,method):
        self.x = x
        self.y = y
        self.method = method
        
    def _ncolselect(self):
        ncol = []
        x = self.x.copy()
        for col in x.select_dtypes(include=['number']).columns:
            if len(x[col].value_counts(dropna=False).index)>10:
                ncol.append(col)
        return (ncol)
    
    def _ccolselect(self):
        x = self.x.copy()
        ccol = set(x.columns)-set(self._ncolselect())
        return (list(ccol))     
    
    def _cutpoint(self,var):
        len1=len(var.index)
        len2=math.floor(math.log10(len1))+2
        pnum=np.array(range(0,int(len2)+1))
        return pnum*(len1/len2)
        
    #2ランキングを振る
    def _order(self,var):
        temp=var
        temp1=pd.concat([temp,temp.rank(method='min')],axis=1)
        return temp1
    #category 切る
    
    def _category(self,var):
        #list=[]
        #for i in range(len(cutpoint(titanic[var]))-1):
        temp=pd.concat([var,pd.cut(self._order(var).iloc[:,1],self._cutpoint(var))],axis=1)
        temp.columns=["temp1","temp2"]
        group=temp.groupby("temp2")
        group.min()["temp1"].values.tolist()
        names=[str(i)+"<=" for i in group.min()["temp1"].values.tolist()]
        temp2 = pd.cut(self._order(var).iloc[:,1],self._cutpoint(var),labels=names)
        #temp2 = temp2.astype('O')
        return (temp2.cat.add_categories("99:missing").fillna("99:missing").astype('O'))
    
    def _remakeframe(self):
        ncols = self._ncolselect()
        ccols = self._ccolselect()
        x = self.x.copy()
        for col in ncols:
            #from IPython.core.debugger import Pdb; Pdb().set_trace()
            x[col] = self._category(x[col])
        
        return (x)
    
    def _chky(self):
        y = self.y.copy()
        if len(y.unique())>=10:
            return (True)
        else:
            return (False)
        
    def _calc_aic(self,var,target):
        #数値前提
        #従属
        #print var
        crossed = pd.crosstab(var,target,margins=True)
        len1=len(crossed.index)
        len2=len(crossed.columns)
        crossed1 = np.log(crossed)*crossed
        crossed1 = crossed1.fillna(0)
        MLLd=crossed1.iloc[0:len1-1,0:len2-1].sum().sum()-crossed1.iloc[len1-1,len2-1]
        leny = len(target.unique())
        aic0=-2*MLLd+2*((len1-1)*leny-1)
                #独立
        MLPi=crossed1.iloc[len1-1,:].sum()+crossed1.iloc[:,len2-1].sum()-4*crossed1.iloc[len1-1,len2-1]
        aic1=-2*MLPi+2*(len1-1+leny-1)
        return (crossed.index.name + ':{:.5f}'.format(aic0-aic1),crossed)
        
    def fit(self):     
        l_n = []
        l_c = []
        if self._chky():
            print ('unique value is too many to solve')
            sys.exit()
            
        x = self._remakeframe()
        for col in x.columns:
            aic,crossed = self._calc_aic(x[col],self.y)
            l_n.append(aic)
            l_c.append(crossed)
            
        print (len(l_n),len(l_c))
        return (pd.concat(l_c,keys=l_n))
            
            
        
