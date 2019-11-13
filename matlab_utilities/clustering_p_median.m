% Il seguente script legge i file:
% 1. array_x.xlsx, contenente le x associazioni punti - cluster
% 2. centroids_x.xlsx, contenente i centrodi scelti nel caso di x punti

x = 50; % Numero di istanze del dataset

while x<=1000
    data = xlsread(strcat('./1_tentativo/array/array_',int2str(x),'.xlsx'));
    assignment = data(:,3);
    data = data(:,1:2);
    
    centroids = xlsread(strcat('./1_tentativo/centroids/centroids_',int2str(x),'.xlsx'));
    
    PlotClusters(data,assignment,centroids,x);
    save_to_dat(x)
    x = x + 50;
end