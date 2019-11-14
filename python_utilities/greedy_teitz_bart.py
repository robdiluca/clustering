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
import time

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

    # Salvataggio su file della matrice delle distanze
    workbook = xlsxwriter.Workbook('distances/' + nome_file + ".xlsx")
    worksheet = workbook.add_worksheet()
    row = 0
    for col, data in enumerate(dist_matrix.T):
        worksheet.write_column(row, col, data)
    workbook.close()

    return dist_matrix


# Calcolo della funzione obiettivo sulla base della matrice delle distanze
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


# Calcolo delle associazioni punti - cluster
def assignment(data, index_centroids, dist_matrix, nome_file):
    data_cluster = numpy.zeros((len(dist_matrix), len(data[0]) + 1))

    for r in range(len(dist_matrix)):
        min = INF

        # Identificazione cluster
        for c in index_centroids:
            elem = dist_matrix[r][c]
            if elem < min:
                min = elem
                centroid = c
        for j in range(len(data[0])):
            data_cluster[r][j] = data[r][j]
        data_cluster[r][len(data[0])] = centroid

        # Trasformazione id cluster (per utilizzarlo con le funzioni matlab per il plot dei cluster)
        for c in range(len(index_centroids)):
            if data_cluster[r][len(data[0])] == index_centroids[c]:
                data_cluster[r][len(data[0])] = c + 1

    # Salvataggio su file xlsx delle assegnazioni punti - cluster
    workbook = xlsxwriter.Workbook('array/' + nome_file + '.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    for col, data in enumerate(data_cluster.T):
        worksheet.write_column(row, col, data)
    workbook.close()

    return data_cluster

def greedy(p, dist_matrix):

    median = []
    best_j = -1

    for i in range(p):

        #print("Iterazione i = " + str(i))

        min_z = INF

        for j in range(len(dist_matrix)):
            #print("Tentativo elemento di indice " + str(j))
            dirty_median = median.copy()
            if j not in median:
                dirty_median.append(j)
                #print(dirty_median)
                z = funzione_obiettivo(dist_matrix, dirty_median)
                #print(z)

                if z<min_z:
                    min_z = z
                    best_j = j

        median.append(best_j)
        #print("Index centroids iterazione " + str(i) + ": " + str(median))

    return median, min_z


# Algoritmo Euristico Teitz-Bart per il problema di localizzazione P-Mediana applicata al caso del Clustering
# TO-DO: inserire nel main il codice le variabili di input per abilitare la possibilità di esecuzione verbosa
#        in modo da vedere passo per passo l'esecuzione dell'algoritmo di Teitz-Bart.
def p_median(p, dist_matrix):
    # Indici dei centroidi iniziali e funzione obiettivo iniziale
    median, z = greedy(p, dist_matrix)

    # Inizializzazione variabile per criterio d'arresto
    finito = False

    # Variabili di utilità per non eseguire controlli inutili
    old_best_j = -1
    old_best_i = -1

    # Variabile per il numero di passo
    k = 1

    # Vettore indici da non valutare nelle iterazioni (al variare di i)
    bad_i = []

    # Iterazioni
    while not (finito):

        log.info("**** PASSO " + str(k) + ": ")

        k += 1
        best_saving = 0
        best_j = 0
        best_i = 0
        best_f_ob = 0

        log.info("     Centroidi in posizione: " + str(median) + "\n")

        # Iterazione su tutti gli indici del dataset
        for i in range(len(dist_matrix)):

            # La valutazione di i deve essere effettuata se l'indice non è già quello di un centroide e non
            # è uno degli indici che nelle iterazioni precedenti non hanno generato alcun saving positivo
            if (i not in median) and (i not in bad_i):

                # Inizializzo il vettore dei saving associati alla i
                s_ij_vector = []

                # Iterazione su tutti gli indici correntemente selezionati come centroidi
                for j in range(len(median)):

                    # Permette di evitare la valutazione degli indici che sono stati appena invertiti
                    if (median[j] == old_best_i and i == old_best_j):
                        old_best_i = -1
                    else:
                        dirty_median = median.copy()
                        dirty_median[j] = i
                        log.info("     " + str(median) + " -> " + str(dirty_median))

                        # Valutazione funzione obiettivo con un nuovo set di centroidi
                        f_ob = funzione_obiettivo(dist_matrix, dirty_median)

                        # Valutazione del saving
                        s_ij = z - f_ob

                        # Inserimento del saving all'interno del vettore dei saving
                        s_ij_vector.append(s_ij)

                        # Aggiornamento del best_saving
                        if s_ij > best_saving:
                            best_saving = s_ij
                            best_i = i
                            best_j = j
                            best_f_ob = f_ob

                log.info("     Risultati del tentativo: ")
                log.info("     Vettore dei saving relativo a " + str(i) + " : " + str(s_ij_vector))

                # se max(s_ij_vector) < 0 allora la i non ha portato alcun saving positivo
                if (max(s_ij_vector) < 0):
                    log.info("         -> Nessun saving relativo a " + str(i) + "\n")
                    bad_i.append(i)
                else:
                    log.info("         -> Saving migliore associato a " + str(i) + " : " + str(max(s_ij_vector)) + "\n")

        if best_saving > 0:
            old_best_j = median[best_j]
            old_best_i = best_i
            median[best_j] = best_i
            z = best_f_ob
            log.info("     Confronto tra i tentativi: ")
            log.info("     Best f-ob: " + str(best_f_ob))
            log.info("     Best i, best j: " + str(best_i) + " " + str(best_j) + "\n")
        else:
            finito = True

    return median, z


if __name__ == '__main__':

    p = 4  # Numero di cluster

    x = 100  # Dimensione del dataset

    # Ciclo while per analizzare i dataset di diverse dimensioni
    while x <= 300:

        ### Lettura dei dati su cui effettuare il clustering ###
        # Lettura file .arff
        df = read_file('archivio/s-set2_' + str(x) + '.arff')

        # Creazione della matrice delle distanze
        dist_matrix = distance_matrix(df, 'distance_matrix_' + str(x))

        print(len(dist_matrix))
        # Trasformazione DataFrame (dal file .arff) in una matrice
        data = df.values

        ### Inizio calcolo degli indici centroidi ###
        # -> median: indici dei centroidi
        # -> best_f_ob: miglior valore della funzione obiettivo
        start_time = time.time()
        median, f_ob = p_median(p, dist_matrix)
        ### Fine calcolo centroidi ###
        print("**** EXECUTION TIME: %s seconds" % (time.time() - start_time))
        print(f_ob)

        ### Inizio stampa dei centroidi effettivi ###
        print("\n**** Centroidi con " + str(x) + " istanze: ****")

        # Matrice dei centroidi effettivi
        centroids_matrix = numpy.zeros((p, len(data[0])))

        j = 0
        for index in median:
            print(data[index])
            centroids_matrix[j] = data[index]
            j += 1

        print("\nFunzione Obiettivo: " + str(f_ob))

        print("\n*******************\n\n")
        ### Fine stampa dei centroidi effettivi ###

        # Salvataggio matrice dei centroidi
        workbook = xlsxwriter.Workbook('centroids/centroids_' + str(x) + '.xlsx')
        worksheet = workbook.add_worksheet()
        row = 0
        for col, dat in enumerate(centroids_matrix.T):
            worksheet.write_column(row, col, dat)
        workbook.close()

        # Calcolo delle assegnazioni punti - cluster
        clustered_data = assignment(data, median, dist_matrix, 'array_' + str(x))
        x += 100