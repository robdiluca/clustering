from scipy.io import arff
from scipy.spatial.distance import pdist, squareform
import pandas as pd
import numpy

# Lettura dati dal file arff
data = arff.loadarff('./datasets/2d-10c.arff')
df = pd.DataFrame(data[0])
df.head()

# Calcolo delle distanze
distances = pdist(df.values, metric='euclidean')
dist_matrix = squareform(distances)

# Salvataggio su file
numpy.save('distance_matrix', dist_matrix)

