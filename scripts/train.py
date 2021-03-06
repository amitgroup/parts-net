from __future__ import division, print_function, absolute_import 

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('model', metavar='<parts net file>', type=argparse.FileType('wb'), help='Filename of model file')
parser.add_argument('--log', action='store_true')

args = parser.parse_args()

if args.log:
    from pnet.vzlog import default as vz
import numpy as np
import amitgroup as ag
import sys
ag.set_verbose(True)

from pnet.bernoulli_mm import BernoulliMM
import pnet
from sklearn.svm import LinearSVC 


layers = [
    #pnet.IntensityThresholdLayer(),
    pnet.EdgeLayer(k=5, radius=1, spread='orthogonal', minimum_contrast=0.05),
    #pnet.IntensityThresholdLayer(),
    pnet.PartsLayer(100, (5, 5), settings=dict(outer_frame=1, 
                                               em_seed=1,
                                               threshold=8, 
                                               samples_per_image=40, 
                                               max_samples=10000, 
                                               min_prob=0.0005)),
    pnet.PoolingLayer(shape=(6, 6), strides=(4, 4)),
] #+ 

if 1:
    layers = [
        #pnet.IntensityThresholdLayer(),
        pnet.EdgeLayer(k=5, radius=1, spread='orthogonal', minimum_contrast=0.05),

        pnet.HierarchicalPartsLayer(2, 10, (5, 5), settings=dict(outer_frame=1, 
                                                  em_seed=seed + 2,
                                                  threshold=2, 
                                                  samples_per_image=40, 
                                                  max_samples=100000, 
                                                  min_prob=0.0005)),
        pnet.PoolingLayer(shape=(4, 4), strides=(4, 4)),
    ]

elif 1:
    layers = [
        pnet.IntensityThresholdLayer(),
        #pnet.EdgeLayer(k=5, radius=1, spread='orthogonal', minimum_contrast=0.05),
        #pnet.IntensityThresholdLayer(),
        pnet.PartsNet([
            pnet.PartsLayer(100*8, (5, 5), settings=dict(outer_frame=1, 
                                                      em_seed=1,
                                                      threshold=4, 
                                                      samples_per_image=40, 
                                                      max_samples=100000, 
                                                      min_prob=0.0005)),
            pnet.PoolingLayer(shape=(4, 4), strides=(4, 4)),
        ]),
        pnet.MixtureClassificationLayer(n_components=1),
    ]

else:
    layers = [
        #pnet.IntensityThresholdLayer(),
        pnet.EdgeLayer(k=5, radius=1, spread='orthogonal', minimum_contrast=0.05),
        #pnet.IntensityThresholdLayer(),
        pnet.PartsLayer(50, (2, 2), settings=dict(outer_frame=0, 
                                                  #em_seed=2,
                                                  threshold=5, 
                                                  samples_per_image=100, 
                                                  max_samples=5000, 
                                                  min_prob=0.01,
                                                  standardize=1,
                                                  min_percentile=25,
                                                  n_coded=4,
                                                  )),
        pnet.PoolingLayer(shape=(2, 2), strides=(1, 1)),
    ] + [
        pnet.PartsLayer(70, (5, 5), settings=dict(outer_frame=0,
                                                  threshold=4,
                                                  samples_per_image=100,
                                                  max_samples=50000,
                                                  min_prob=0.001,
                                                  standardize=1,
                                                  min_percentile=0,
                                                  n_coded=2,
                                                  support_mask=np.array([
                                                                         [1, 0, 1, 0, 1],
                                                                         [0, 0, 0, 0, 0],
                                                                         [1, 0, 1, 0, 1],
                                                                         [0, 0, 0, 0, 0],
                                                                         [1, 0, 1, 0, 1],
                                                                         ], dtype=np.bool),
                                                  )),
        pnet.PoolingLayer(shape=(3, 3), strides=(3, 3)),
        pnet.MixtureClassificationLayer(n_components=1),
    ]

net = pnet.PartsNet(layers)

digits = range(10)
ims = ag.io.load_mnist('training', selection=slice(10000), return_labels=False)

#print(net.sizes(X[[0]]))

net.train(ims)

sup_ims = []
sup_labels = []
# Load supervised training data
for d in digits:
    ims0 = ag.io.load_mnist('training', [d], selection=slice(100), return_labels=False)
    sup_ims.append(ims0)
    sup_labels.append(d * np.ones(len(ims0), dtype=np.int64))

sup_ims = np.concatenate(sup_ims, axis=0)
sup_labels = np.concatenate(sup_labels, axis=0)

net.train(sup_ims, sup_labels)


net.save(args.model)

if args.log:
    net.infoplot(vz)
    vz.flush()
