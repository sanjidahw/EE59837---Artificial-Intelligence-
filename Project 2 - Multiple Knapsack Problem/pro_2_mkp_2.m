%{
-------------------------------- EE 59837 --------------------------------
| Project #2B -  Class Schedule Optimization                             |
--------------------------------------------------------------------------
Given a list of classes at City College of Gotham, Stanley has to pick 
as many classes as he can as long as it meets his financial requirements.  
For example, he can select from several categories: EE, ELECTIVE,ENGR,LIBERAL.
He can take multiple classes from each category.
For example, classLimits = [2, 2, 1, 1]; means he can take up to 2 EE, 
2 ELECTIVE, 1 ENGR and 1 LIBERAL classes. 

Instructor            : Prof. Uyar
Completion Date       : 2020 September 23
Group number          : Group 5
Student 1 Name        : Sanjidah Wahid
Student 1 CCNY email  : swahid000
Student 1 Log In Name : ee59837_16
Student 2 Name        : 
Student 2 CCNY email  :
Student 2 Log In Name : 
Student 3 Name        :	
Student 2 CCNY email  :
Student 3 Log In Name :
--------------------------------------------------------------------------
| I UNDERSTAND THAT COPYING PROGRAMS FROM OTHERS WILL BE DEALT           |
| WITH DISCIPLINARY RULES OF CCNY.                                       |
--------------------------------------------------------------------------
%}
clc;
clear;

% set budget, and read input file into class_table:
budget = 4500;

%items_file = fullfile(pwd,'CSV_Files','Class_Pick.csv');
items_file = 'Class_info.csv';
class_table =  readtable(items_file);
class_table = sortrows(class_table,'ClassType');

fprintf('******** READING ITEMS FROM %s ********\n',items_file);
fprintf('BUDGET IS SET TO %d\n',budget);

% Define limits for each class type:
classTypes = {'EE','ELECTIVE','ENGR','LIBERAL'};
classLimits = [2, 2, 2, 2]; % number of each classType allowed (i.e., max)
classTypes = sortrows(classTypes);
classMap = containers.Map(classTypes,classLimits);

% define chromosome and fitness function:
chromosome_length = height(class_table);
fit_func = @(chromosome) - (chromosome * class_table.Credits);

% defined masks based on class_table:
category_index_map = containers.Map();

for i = 1:height(class_table)
    ClassType = class_table.ClassType{i};
    if isKey(category_index_map,ClassType)
        indices = category_index_map(ClassType);
        indices = horzcat(indices, i);
        category_index_map(ClassType) = indices;
    else
        category_index_map(ClassType) = [i];
    end 
end

noof_categories = size(category_index_map,1);

masks = zeros(noof_categories, height(class_table));

keySet = keys(category_index_map);

for i = 1:noof_categories
    indices = category_index_map(keySet{i});
    for j = 1:length(indices)
        masks(i,indices(j)) = 1;
    end
end

% define A, b, Lb, Ub, and int_indices:
A = vertcat(class_table.Cost', masks);
b = [budget, classLimits];
Lb = zeros(1,chromosome_length);
Ub = ones(1,chromosome_length);
int_indices = 1:chromosome_length;

% run ga:
disp('****GA STARTING*****');
options = optimoptions('ga','display','off');
selection = ga(fit_func,chromosome_length,A,b,...
[],[],Lb,Ub,[],int_indices);
disp('****GA Finished****');

% display results:
message = sprintf('OPTIMAL SELECTION OF ITEMS: [');
for i = 1:chromosome_length
    if selection(i) == 1
        message = sprintf('%s \n\t%s - %s', message, string(class_table.Class(i)), ...
            string(class_table.Class_Name(i)));    
    end
end

fprintf('%s \n]\n', message);
fprintf('TOTAL CREDITS TO TAKE THIS SEMESTER: %d\n', selection * class_table.Credits);
fprintf('TOTAL TUITION FOR THIS SEMESTER: $%d\n', selection * class_table.Cost);
disp('*********************************************')
