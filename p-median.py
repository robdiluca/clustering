from scipy.io import arff
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
    numpy.save(nome_file, dist_matrix)
    return dist_matrix

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

def assignment(data, index_centroids, dist_matrix):

    data_cluster = numpy.zeros((len(dist_matrix), len(data[0])+1))
    for r in range(len(dist_matrix)):
        min = INF
        for c in index_centroids:
            elem = dist_matrix[r][c]
            if elem < min:
                min = elem
                centroid = c
        for j in range(len(data[0])):
            data_cluster[r][j] = data[r][j]
        data_cluster[r][len(data[0])] = centroid

    return data_cluster
    '''
    workbook = xlsxwriter.Workbook('arrays.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    for col, data in enumerate(data_cluster.T):
        worksheet.write_column(row, col, data)
    workbook.close()
    '''

def p_median(p, dist_matrix):

    # Indici dei centroidi iniziali
    median = random.sample(range(len(dist_matrix)), p)

    # Vettore media per test
    #median = [0, 1, 2]

    # Inizializzazione valore funzione obiettivo
    z = funzione_obiettivo(dist_matrix, median)

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
    while not(finito):

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
                    if(median[j] == old_best_i and i == old_best_j):
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
                if(max(s_ij_vector) < 0):
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
            log.info("     Best i, best j: " + str(best_i) + " " + str(best_j) + "\n" )
        else:
            finito = True

    return median, z


if __name__ == '__main__':
    ### Inizio impostazioni per la modalità verbosa ###
    parser = argparse.ArgumentParser()
    parser.add_argument('num_cluster', type=int, help='an integer for number of cluster')
    parser.add_argument('num_exec', type=int, help='an integer for number of starting points')
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    args = parser.parse_args()

    if args.verbose:
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
        log.info("Verbose mode.")
    else:
        log.basicConfig(format="%(levelname)s: %(message)s")
    ### Fine impostazioni modalità verbosa ###


    ### Lettura dei dati su cui effettuare il clustering ###
    # Lettura file .arff
    df = read_file('./datasets/2d-10c-toTest.arff')

    # Creazione della matrice delle distanze
    dist_matrix = distance_matrix(df, 'distance_matrix_toTest')

    # Trasformazione DataFrame (dal file .arff) in una matrice
    data = df.values

    # Matrice da utilizzare per fare i test
    #dist_matrix = [[0, 5, 7, 3, 4, 9], [5, 0, 10, 6, 8, 5], [7, 10, 0, 4, 7, 8], [3, 6, 4, 0, 2, 9], [4, 8, 7, 2, 0, 6], [9, 5, 8, 9, 6, 0]]
    ### Fine lettura dei dati su cui effettuare clustering

    # Impostazione del numero di cluster
    p = args.num_cluster
    if p <= 0:
        log.error("Il numero di cluster deve essere positivo")
        sys.exit()
    log.info("Numero di cluster inserito: " + str(p))

    best_f_ob = INF
    best_median = []
    for x in range(1, args.num_exec+1):
        ### Inizio calcolo degli indici centroidi ###
        # -> median: indici dei centroidi
        # -> best_f_ob: miglior valore della funzione obiettivo
        median, f_ob = p_median(p, dist_matrix)
        ### Fine calcolo centroidi ###
        print(f_ob)
        if f_ob < best_f_ob:
            best_f_ob = f_ob
            best_median = median.copy()

    ### Inizio stampa dei centroidi effettivi ###
    print("\n**** Centroidi: ****")
    for index in best_median:
        print(data[index])
    print("\nFunzione Obiettivo: " + str(best_f_ob))
    print("\n*******************")
    ### Fine stampa dei centroidi effettivi ###

    clustered_data = assignment(data, best_median, dist_matrix)


