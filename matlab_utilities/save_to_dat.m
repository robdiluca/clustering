% save_to_dat     A function that allows to read data from xlsx file and write into a dat file
% save_to_dat(num_of_inst) reads num_of_inst instances from a xlsx file and
% write it into a dat file in order to perform other processing activities.
function save_to_dat(num_of_inst)
    A = xlsread(strcat('./5_tentativi/distances/distance_matrix_',int2str(num_of_inst),'.xlsx'));
    nome_dat = strcat('./5_tentativi/distances_dat/distance_matrix_dat_',int2str(num_of_inst),'.dat');
    
    fileID = fopen(nome_dat,'w');
    fprintf(fileID,'%s\n\n%s\n','P: [4]','COSTI_I_J:','[ ');
    fclose(fileID);
    save(nome_dat,'A','-ascii','-append')
    fileID = fopen(nome_dat,'a');
    fprintf(fileID,'\n%s',']');
    fclose(fileID);
end

