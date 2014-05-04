#!/usr/bin/python
import sys
import scipy.sparse
# append the path to xgboost
sys.path.append('../')
import xgboost as xgb

### simple example
# load file from text file, also binary buffer generated by xgboost
dtrain = xgb.DMatrix('agaricus.txt.train')
dtest = xgb.DMatrix('agaricus.txt.test')

# specify parameters via map, definition are same as c++ version
param = {'bst:max_depth':4, 'bst:eta':1, 'silent':1, 'loss_type':2 }

# specify validations set to watch performance
evallist  = [(dtest,'eval'), (dtrain,'train')]
num_round = 2
bst = xgb.train( param, dtrain, num_round, evallist )

# this is prediction
preds = bst.predict( dtest )
labels = dtest.get_label()
print 'error=%f' % (  sum(1 for i in xrange(len(preds)) if int(preds[i]>0.5)!=labels[i]) /float(len(preds)))
bst.save_model('0001.model')


###
# build dmatrix in python iteratively
#
print 'start running example of build DMatrix in python'
dtrain = xgb.DMatrix()
labels = []
for l in open('agaricus.txt.train'):
    arr = l.split()
    labels.append( int(arr[0]))
    feats = []
    for it in arr[1:]:
        k,v = it.split(':')
        feats.append( (int(k), float(v)) )
    dtrain.add_row( feats )
dtrain.set_label( labels )
evallist  = [(dtest,'eval'), (dtrain,'train')]

bst = xgb.train( param, dtrain, num_round, evallist )

###
# build dmatrix from scipy.sparse
print 'start running example of build DMatrix from scipy.sparse'
labels = []
row = []; col = []; dat = []
i = 0
for l in open('agaricus.txt.train'):
    arr = l.split()
    labels.append( int(arr[0]))
    for it in arr[1:]:
        k,v = it.split(':')
        row.append(i); col.append(int(k)); dat.append(float(v))
    i += 1

csr = scipy.sparse.csr_matrix( (dat, (row,col)) )
dtrain = xgb.DMatrix( csr )
dtrain.set_label(labels)
evallist  = [(dtest,'eval'), (dtrain,'train')]
bst = xgb.train( param, dtrain, num_round, evallist )

print 'start running example of build DMatrix from numpy array'
# NOTE: npymat is numpy array, we will convert it into scipy.sparse.csr_matrix in internal implementation,then convert to DMatrix
npymat = csr.todense()
dtrain = xgb.DMatrix( npymat )
dtrain.set_label(labels)
evallist  = [(dtest,'eval'), (dtrain,'train')]
bst = xgb.train( param, dtrain, num_round, evallist )

