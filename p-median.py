from scipy.io import arff
from scipy.spatial.distance import pdist, squareform
import pandas as pd
import numpy

# Lettura dati dal file arff
def read_file(arff_file):
    data = arff.loadarff(arff_file)
    df = pd.DataFrame(data[0])
    df.head()
    return df

# Calcolo delle distanze
def distance_matrix(df, nome_file):
    distances = pdist(df.values, metric='euclidean')
    dist_matrix = squareform(distances)

    # Salvataggio su file
    numpy.save(nome_file, dist_matrix)
    return dist_matrix

def funzione_obiettivo(row, dist_matrix, index_centroids):

    minimi = []
    for r in range(0,len(dist_matrix)+1):
        if not(r in index_centroids):
            distances = []
            for c in index_centroids:
                distances.append(dist_matrix[r,c])
                #print(dist_matrix[r,c])
            minimi.append(min(distances))
            #print(minimi)

    somma = sum(minimi)
    #print(somma)
    return somma

def p_median(p, df, dist_matrix):
    row = df.sample(n=p)
    dirty_row = row
    index_centroids = list(numpy.array(row['a0'].index))
    temp_row = pd.concat([row, df]).drop_duplicates(keep=False)

    print(row)
    for index, r in temp_row.iterrows():
        print(row.drop(index))

    #z_iniziale = funzione_obiettivo(row, dist_matrix, index_centroids)
    return 0

df = read_file('./datasets/2d-10c.arff')
dist_matrix = distance_matrix(df, 'distance_matrix')
p = 5
p_median(p, df, dist_matrix)



