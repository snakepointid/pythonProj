from __future__                 import division
import sys
sys.path.append('E:\project\pythonProj') 
from nltk.corpus                import brown
from NeuronLayers.BasicNeuron   import baseNeuronLayer
from NeuronLayers.CnnNeuron     import word2vecCovLayer
from NLP.statisticLanguageModel import statisLM
import numpy  as np
#-----------------------------------------------------------------------------------------------------------------------------------------------
corps = brown.sents(categories=None)
corps = list(corps)
slm = statisLM(corps,100)
#-----------------------------------------------------------------------------------------------------------------------------------------------
window = 5
wordDim = 100
outDim =100
outs =1
hiddenFunc = 'tanh'
outFunc = 'sigmoid'
cnnlayer = word2vecCovLayer(window,wordDim,outDim,actfunc=hiddenFunc)
outlayer = baseNeuronLayer(outDim,outs,actfunc = outFunc)
#-----------------------------------------------------------------------------------------------------------------------------------------------
'''if pickle from the save'''
#import cPickle
#dirs = "C:\\Users\\Administrator.NBJXUEJUN-LI\\Desktop\\project\\Python\\NLP\\savedObject\\CompCorpus\\"
#slm = cPickle.load(open(dirs+"slm.pkl","rb"))
#cnnlayerPara = cPickle.load(open(dirs+"cnnlayer.pkl","rb")) 
#outlayerPara = cPickle.load(open(dirs+"outlayer.pkl","rb")) 
#cnnlayer.W,cnnlayer.b = cnnlayerPara
#outlayer.W,outlayer.b = outlayerPara
#-----------------------------------------------------------------------------------------------------------------------------------------------      
'''
function
''' 
 
l2=0.0001                            
learning=0.05
def fit(context,y):        
     rawinput = np.zeros(shape=(window,context.shape[0],wordDim))
     for idx in range(context.shape[1]):
         rawinput[idx] = slm.wordvec[context.T[idx]]
     output            = cnnlayer.actNuerous(rawinput)
     output            = outlayer.actNuerous(output)
     outputError       = output - y  
     ers               = np.mean(np.abs(outputError))
     outputError       = outlayer.updateError(outputError,learning,l2)
     deltax            = cnnlayer.updataError(outputError,learning,l2)
     slm.updateWordVec(deltax,context,learning,l2)
     print (ers,learning )
#-----------------------------------------------------------------------------------------------------------------------------------------------      
'''
training
'''     
cot=0    
while 2>1:     
    for corp in slm.codeCorps:
        if len(corp)>=window:             
             fakecorp  = corp[::-1]                 
             for wordidx in range(0,len(corp)-window+1):
                 #if slm.subSampCode(corp[wordidx]):
                 addX  = np.array([corp[wordidx:wordidx+window],fakecorp[wordidx:wordidx+window]])
                 addY  = np.array([[1],[0]])
                 if cot==0:
                     X = addX
                     y = addY
                 else:
                     X = np.append(X,addX,axis=0)                     
                     y = np.append(y,addY,axis=0)
                 cot+=1
             if cot>2000:
                 fit(X,y)
                 cot = 0
#-----------------------------------------------------------------------------------------------------------------------------------------------      
'''
tesing
'''           
slm.getMostSimilarWord(word='one',types='cosSimilar')
#-----------------------------------------------------------------------------------------------------------------------------------------------      
'''save trained model and vec'''
#import cPickle
#cnnlayerPara = (cnnlayer.W,cnnlayer.b)
#outlayerPara = (outlayer.W,outlayer.b)
#dirs = "C:\\Users\\Administrator.NBJXUEJUN-LI\\Desktop\\project\\Python\\NLP\\savedObject\\CompCorpus\\"
#cPickle.dump(slm,open(dirs+"slm.pkl","wb")) 
#cPickle.dump(cnnlayerPara,open(dirs+"cnnlayer.pkl","wb")) 
#cPickle.dump(outlayerPara,open(dirs+"outlayer.pkl","wb")) 
