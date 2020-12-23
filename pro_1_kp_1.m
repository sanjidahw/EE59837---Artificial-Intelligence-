%{
-------------------------------- EE 59837 --------------------------------
| Project #1A - Public Transportation Train Budget Planning              |
|------------------------------------------------------------------------|
| The Gotham Transportation Authority is purchasing new trains for its   |
| elevated train lines. The GTA wants to maximize the total number of    |
| daily passengers while putting a constraint on the weight of the train.|
| Due to regulations, GTA cannot purchase more than one car from a given |
| manufacturer.                                                          |
--------------------------------------------------------------------------

Instructor            : Prof. Uyar
Completion Date       : 2020 September 7
Group number          : sample_pro_1_kp_1a.m
Student 1 Name        : James Bond
Student 1 CCNY email  : jbond007
Student 1 Log In Name : ee6530_10
Student 2 Name        : Clement McClean, Jr.
Student 2 CCNY email  : 
Student 2 Log In Name : 
Student 3 Name        :	Kelvin Ma
Student 3 CCNY email  :
Student 3 Log In Name :
--------------------------------------------------------------------------
| I UNDERSTAND THAT COPYING PROGRAMS FROM OTHERS WILL BE DEALT           |
| WITH DISCIPLINARY RULES OF CCNY.                                       |
--------------------------------------------------------------------------
%}
clc;
clear;

% set weight_limit, read input file into variable trains_table:


fprintf('******** READING ITEMS FROM %s ********\n',input_file);
fprintf('WEIGHT LIMIT IS SET TO %d\n',weight_limit);

% define chromosome length and fitness function:


% define A, b, Lb, Ub, int_indices:







% run ga:
disp('****GA STARTING*****');
options = optimoptions('ga','display','off');
[selection, selection_fitness] = ga(fit_func,chromosome_length,A,b,...
                                    [],[],Lb,Ub,[],int_indices);
fprintf('Best fitness for this run = %d\n', abs(selection_fitness));
disp('****GA Finished****');

%display results:
if selection == zeros(chromosome_length, 1)
    message = sprintf('GA CANNOT FIND VALID SELECTION WITH GIVEN CONSTRAINTS');
    disp(message)
else
    message = sprintf('OPTIMAL SELECTION OF ITEMS: [');
    for i = 1:chromosome_length
        if selection(i) == 1
            message = sprintf('%s \n\t- %s', message, string(trains_table.Manufacturer(i)));    
        end
    end

    fprintf('%s\n ]\n', message);
    fprintf('TOTAL weight OF RAILCARS: %d Tons\n', selection * trains_table.weight);
    fprintf('TOTAL DAILY PASSENGERS: %d\n', selection * trains_table.daily_passengers);
end
disp('*********************************************')
