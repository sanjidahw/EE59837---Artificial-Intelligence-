%{
|-------------------------------- EE 59837 ------------------------------|
| Project #2A - Public Transportation Bus Budget Planning                |
| I UNDERSTAND THAT COPYING PROGRAMS FROM OTHERS WILL BE DEALT           |
| WITH DISCIPLINARY RULES OF CCNY.                                       |
| -----------------------------------------------------------------------|
Group number          : Group 5
Student 1 Name        : Sanjidah Wahid
Student 1 CCNY Email  : swahid000
Student 1 Log In Name : EE59837_16
Student 2 Name        :
Student 2 CCNY Email  : 
Student 2 Log In Name : 
Student 3 Name        :
Student 3 CCNY Email  : 
Student 3 Log In Name :

The Gotham Transportation Authority is purchasing new buses to add to 
their current bus network. To honor a previous agreement with bus 
manufactorers, the GTA will buy one bus from each manufacturer. The GTA
would like to maximize the total number of passengers in the new buses
while staying below a given budget and fuel comsumption limit. 
%}
clc;
clear;

% set up money_to_spend and gasoline_consumption:
money_to_spend = 3600;
gas_consumption = 85;

% read input file into bus_table:
items_file = 'Bus_info.csv';
bus_table = readtable(items_file);

fprintf('******** READING ITEMS FROM %s ********\n',items_file);
fprintf('BUDGET IS SET TO %d\n',money_to_spend);
fprintf('FUEL COMSUMPTION LIMIT IS SET TO %d\n',gas_consumption);

% define chromosome length and fitness function:
chromosome_length = height(bus_table);
fit_func = @(chromosome) - (chromosome * bus_table.Passengers);

% define masks based on bus_table:
category_index_map = containers.Map();

for i = 1:height(bus_table)
    Company = bus_table.Companies{i};
    if isKey(category_index_map,Company)
        indices = category_index_map(Company);
        indices = horzcat(indices, i);
        category_index_map(Company) = indices;
    else
        category_index_map(Company) = [i];
    end 
end

noof_categories = size(category_index_map,1);

masks = zeros(noof_categories, height(bus_table));

keySet = keys(category_index_map);

for i = 1:noof_categories
    indices = category_index_map(keySet{i});
    for j = 1:length(indices)
        masks(i,indices(j)) = 1;
    end
end

%set A, b, Lb, Ub, int_indices:
A = vertcat(bus_table.Costs', bus_table.Gasoline', masks);
b = [money_to_spend, gas_consumption, ones(1,noof_categories)];
Lb = zeros(1,chromosome_length);
Ub = ones(1,chromosome_length);
int_indices = 1:chromosome_length;

% run ga:
  
disp('****GA STARTING*****');
options = optimoptions('ga','display','off');
selection = ga(fit_func,chromosome_length,A,b,...
                     [],[],Lb,Ub,[],int_indices);
disp('****GA FINISHED****');

% display results:
if isempty(selection)
    message = sprintf('*** GA CANNOT FIND VALID SELECTION ***');
    disp(message)
    return
end

message = sprintf('OPTIMAL SELECTION OF ITEMS: [');
for i = 1:chromosome_length
    if selection(i) == 1
        message = sprintf('%s %s-%s', message,...
            string(bus_table.Companies(i)), string(bus_table.Type(i)));
    end 
end

message = sprintf('%s ]', message);
disp(message);

message = sprintf('TOTAL MONEY SPENT: %d', selection*bus_table.Costs);
disp(message);

message = sprintf('TOTAL GAS CONSUMED: %d', selection*bus_table.Gasoline);
disp(message);

message = sprintf('TOTAL NUMBER OF PASSENGERS: %d', ...
    selection*bus_table.Passengers);
disp(message);

disp('*******************************************************************')









