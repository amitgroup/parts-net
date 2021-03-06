from __future__ import division, print_function, absolute_import 

import amitgroup as ag
import numpy as np
from pnet.layer import Layer

@Layer.register('intensity-threshold-layer')
class IntensityThresholdLayer(Layer):
    def __init__(self, threshold=0.5):
        self._threshold = threshold

    def _extract(self, phi, data):
        X = phi(data)
        return (X > 0.5).astype(np.uint8)[...,np.newaxis] 

    def save_to_dict(self):
        return dict(threshold=self._threshold) 

    @classmethod
    def load_from_dict(cls, d):
        return cls(threshold=d['threshold']) 

