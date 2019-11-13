from scipy.io import arff
from scipy.spatial.distance import pdist, squareform
import pandas as pd
import numpy
import random


if __name__ == '__main__':
    # Lettura dati dal file arff
    data = arff.loadarff('./datasets/sizes1.arff')
    df = pd.DataFrame(data[0])
    df.head()

    # trasformazione in matrice
    data = df.values

    p = 50

    while p <= 1000:
        # Indici dei dati
        index_data = random.sample(range(len(data)), p)

        new_data = []

        for index in index_data:
            new_data.append(data[index])

        with open('sizes1_'+str(p)+'.arff', "w") as fp:
                fp.write('''@RELATION sizes1_nuovo.arff \n\n@ATTRIBUTE a0 real\n@ATTRIBUTE a1 real\n\n@DATA\n''')
                for elem in new_data:
                    fp.write( str(elem[0]) + "," + str(elem[1])+"\n")

        print("Indici: " + str(index_data))
        print(len(new_data))
        print(new_data)

        p = p+50

    '''
        while p <= 1000:
            # Indici dei dati
            index_data = random.sample(range(len(data)), p)
            
            new_data = []
    
            for index in index_data:
                new_data.append(data[index])
    
            p = p + 50
    
            print("Indici: " + str(index_data))
            print(len(new_data))
            print(new_data)
    '''




