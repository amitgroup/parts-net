from __future__ import division, print_function, absolute_import
from .layer import Layer

from .intensity_threshold_layer import IntensityThresholdLayer
from .edge_layer import EdgeLayer
from .pooling_layer import PoolingLayer
from .spreading_layer import SpreadingLayer  # TODO Temporary
from .old_layers.parts_layer import PartsLayer
from .kmeans_parts_layer import KMeansPartsLayer
#from .gaussian_parts_layer import GaussianPartsLayer
from .oriented_parts_layer import OrientedPartsLayer
from .oriented_gaussian_parts_layer import OrientedGaussianPartsLayer
#from .hierarchical_parts_layer import HierarchicalPartsLayer
#from .binary_tree_parts_layer import BinaryTreePartsLayer
#from .random_forest_parts_layer import RandomForestPartsLayer
from .standardization_layer import StandardizationLayer
from .rectifier_layer import RectifierLayer
from .resize_layer import ResizeLayer
from .crop_layer import CropLayer
from .parts_net import PartsNet
from .feature_combiner_layer import FeatureCombinerLayer
from .mixture_classification_layer import MixtureClassificationLayer
from .gmm_classification_layer import GMMClassificationLayer
from .rotation_mixture_classification_layer import \
    RotationMixtureClassificationLayer
from .svm_classification_layer import SVMClassificationLayer
from . import rescalc
from . import plot
from . import covars

try:
    import mpi4py
    from . import parallel
except ImportError:
    from . import parallel_fallback as parallel
