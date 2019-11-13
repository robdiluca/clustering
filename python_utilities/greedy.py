from scipy.io import arff
from scipy.io import savemat
from scipy.spatial.distance import pdist, squareform
import argparse
import pandas as pd
import numpy
import random
import sys
import xlsxwriter
import logging as log

INF = float('inf')

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
    workbook = xlsxwriter.Workbook('dist.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    for col, data in enumerate(dist_matrix.T):
        worksheet.write_column(row, col, data)
    workbook.close()
    return dist_matrix


def funzione_obiettivo(dist_matrix, index_centroids):
    minimi = []
    for r in range(len(dist_matrix)):
        if not (r in index_centroids):
            distances = []
            for c in index_centroids:
                distances.append(dist_matrix[r][c])

            minimi.append(min(distances))

    somma = sum(minimi)

    return somma

def greedy(p, data, dist_matrix):

    median = []
    best_j = -1

    for i in range(p):

        print("Iterazione i = " + str(i))

        min_z = INF

        for j in range(len(dist_matrix)):
            print("Tentativo elemento di indice " + str(j))
            dirty_median = median.copy()
            if j not in median:
                dirty_median.append(j)
                print(dirty_median)
                z = funzione_obiettivo(dist_matrix, dirty_median)
                print(z)

                if z<min_z:
                    min_z = z
                    best_j = j

        median.append(best_j)
        print("Index centroids iterazione " + str(i) + ": " + str(median))

    return median, min_z

if __name__ == '__main__':
    ### Lettura dei dati su cui effettuare il clustering ###
    # Lettura file .arff
    df = read_file('./datasets/2d-10c-toTest.arff')

    # Creazione della matrice delle distanze
    dist_matrix = distance_matrix(df, 'distance_matrix_toTest')
    # dist_matrix = [[0, 5, 7, 3, 4, 9], [5, 0, 10, 6, 8, 5], [7, 10, 0, 4, 7, 8], [3, 6, 4, 0, 2, 9], [4, 8, 7, 2, 0, 6], [9, 5, 8, 9, 6, 0]]

    print(len(dist_matrix))

    # Trasformazione DataFrame (dal file .arff) in una matrice
    data = df.values

    p = 4

    median, z = greedy(p, data, dist_matrix)
    print("Indici dei centroidi: " + str(median))
    print("Funzione obiettivo: " + str(z))