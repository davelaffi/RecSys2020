import time
import numpy as np
import scipy.sparse as sp
from tqdm import tqdm
from SlimBPR.SlimBPR import SlimBPR
from Base.BaseRecommender import BaseRecommender
from Base.Similarity.Compute_Similarity_Python import Compute_Similarity_Python


class SlimBPRRec(BaseRecommender):

    RECOMMENDER_NAME = "SlimBPRRecommender"
    
    def __init__(self,URM):
        #super(SlimBPRRec, self).__init__(URM)
        self.URM_train = URM
        self.similarity = None

    def fit(self,learning_rate, nnz):

        self.learning_rate = learning_rate
        self.epochs = 20
        self.positive_item_regularization = 1.0
        self.negative_item_regularization = 1.0
        self.nnz = nnz
        
        # Compute similarity matrix
        self.similarity = SlimBPR(self.URM_train,
                                    self.learning_rate,
                                    self.epochs,
                                    self.positive_item_regularization,
                                    self.negative_item_regularization,
                                    self.nnz).get_S_SLIM_BPR()
            
    def getSimilarity(self, knn) :
        self.knn = knn
        self.W_sparse = SlimBPR.getBestKnn(self, knn, self.similarity)
        self.RECS = self.URM_train.dot(self.W_sparse)
