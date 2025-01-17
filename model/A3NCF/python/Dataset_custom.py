# -*- coding: utf-8 -*-
"""Dataset.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1my1pklE4WTwm7nwIhOTysBUBiRMH-ca_
"""

import scipy.sparse as sp
import numpy as np

class Dataset(object):
    '''
    classdocs
    '''

    def __init__(self, path, k):
        '''
        Constructor
        '''
        self.trainMatrix = self.load_rating_file_as_matrix(path + ".train.dat")
        self.user_review_fea = self.load_review_feature(path + "." + str(k) + ".user.theta")
        self.item_review_fea = self.load_review_feature(path + "." + str(k) + ".item.theta")
        self.testRatings = self.load_rating_file_as_matrix(path + ".test.dat")
        #self.testNegatives = self.load_negative_file(path + ".test.negative")
        #assert len(self.testRatings) == len(self.testNegatives)
        
        self.num_users, self.num_items = self.trainMatrix.shape
        
    def load_rating_file_as_list(self, filename):
        ratingList = []
        with open(filename, "r") as f:
            line = f.readline()
            while line != None and line != "":
                arr = line.split("\t")
                user, item, rating= int(arr[0]), int(arr[1]), float(arr[2])
                ratingList.append([user, item, rating])
                line = f.readline()
        return ratingList
    
    
    def load_review_feature(self, filename):
        dict = {}
        with open(filename, "r") as f:
            line = f.readline()
            while line != None and line != "":
                fea = line.split(',')
                index = int(fea[0])
                if index not in dict:
                    fea = fea[1:]
                    fea[-1] = fea[-1].replace('\n','')
                    dict[index] = fea
                line = f.readline()
        return dict

    
    def load_negative_file(self, filename):
        negativeList = []
        with open(filename, "r") as f:
            line = f.readline()
            while line != None and line != "":
                arr = line.split("\t")
                negatives = []
                for x in arr[1: ]:
                    negatives.append(int(x))
                negativeList.append(negatives)
                line = f.readline()
        return negativeList
    
    def load_rating_file_as_matrix(self, filename):
        '''
        Read .rating file and Return dok matrix.
        The first line of .rating file is: num_users\t num_items
        '''
        # Get number of users and items
        num_users, num_items = 0, 0
        with open(filename, "r") as f:
            line = f.readline()
            while line != None and line != "":
              # 0,1,2,3이 진짜로 0번이 1번에게 2점주고 3이라고 쓴 건 아닌거같아서
                if line == '0,1,2,3\n':
                  line = f.readline()
                arr = line.split(",")
                ## \t를 ,로 변경
                u, i = int(arr[0]), int(arr[1])
                num_users = max(num_users, u)
                num_items = max(num_items, i)
                line = f.readline()
        # Construct matrix
        mat = sp.dok_matrix((num_users+1, num_items+1), dtype=np.float32)
        with open(filename, "r") as f:
            line = f.readline()
            while line != None and line != "":
              # 0,1,2,3이 진짜로 0번이 1번에게 2점주고 3이라고 쓴 건 아닌거같아서
                if line == '0,1,2,3\n':
                  line = f.readline()
                arr = line.split(",")
                ## \t를 ,로 변경
                user = int(arr[0])
                item = int(arr[1])
                ratings = float(arr[2])
                
                #print user, item , rating
                if ratings > 0:
                  mat[user, item] = ratings
                line = f.readline()
        return mat