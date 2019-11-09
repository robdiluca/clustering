from scipy.io import arff
from scipy.spatial.distance import pdist, squareform
import pandas as pd
import numpy
import random

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
    #numpy.save(nome_file, dist_matrix)
    return dist_matrix

def p_median(p, df, dist_matrix):
    return 0

def funzione_obiettivo(dist_matrix, index_centroids):

    minimi = []
    for r in range(len(dist_matrix)):
        if not(r in index_centroids):
            distances = []
            for c in index_centroids:
                distances.append(dist_matrix[r][c])
                
            minimi.append(min(distances))

    somma = sum(minimi)

    return somma

def p_median(p, dist_matrix):
    # indici dei centroidi iniziali
    #median = random.sample(range(len(dist_matrix)), p)
    median = [0, 1, 2]

    z = funzione_obiettivo(dist_matrix, median)
    finito = False
    old_best_j = -1
    old_best_i = -1

    while not(finito):

        print("Inizio iterazione")
        best_saving = 0
        best_j = 0
        best_i = 0
        best_f_ob = 0
        s_ij = 0

        print(median)
        for i in range(len(dist_matrix)):
            if i not in median:
                for j in range(len(median)):
                    #if(i != old_best_j and median[j] != old_best_i):
                    dirty_median = median.copy()
                    print(str(i) + " " + str(j))
                    print("Valutazione sostituzione " + str(i) + " " + str(median[j]))
                    dirty_median[j] = i
                    f_ob = funzione_obiettivo(dist_matrix, dirty_median)
                    s_ij = z - f_ob

                    if s_ij > best_saving:
                        best_saving = s_ij
                        best_i = i
                        best_j = j
                        best_f_ob = f_ob

        if best_saving > 0:
            #old_best_j = median[best_j]
            #old_best_i = best_i
            median[best_j] = best_i
            z = best_f_ob
            print("Best f-ob: " + str(best_f_ob))
            print("Best i, best j: " + str(best_i) + " " + str(best_j))
        else:
            finito = True

    return 0

if __name__ == "__main__":
    #df = read_file('./datasets/2d-10c.arff')
    #dist_matrix = distance_matrix(df, 'distance_matrix')
    #data = df.values
    p = 3
    dist_matrix = [[0, 5, 7, 3, 4, 9], [5, 0, 10, 6, 8, 5], [7, 10, 0, 4, 7, 8], [3, 6, 4, 0, 2, 9], [4, 8, 7, 2, 0, 6], [9, 5, 8, 9, 6, 0]]
    p_median(p, dist_matrix)
