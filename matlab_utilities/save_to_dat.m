% save_to_dat     A function that allows to read data from xlsx file and write into a dat file
% save_to_dat(num_of_inst) reads num_of_inst instances from a xlsx file and
% write it into a dat file in order to perform other processing activities.
function save_to_dat(num_of_inst)
    A = xlsread(strcat('./1_tentativo/distances/distance_matrix_',int2str(num_of_inst),'.xlsx'));
    nome_dat = strcat('./1_tentativo/distances_dat/distance_matrix_dat_',int2str(num_of_inst),'.dat');
    save(nome_dat,'A','-ascii')
end

