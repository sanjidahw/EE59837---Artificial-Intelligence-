% Insect swarm
% an insect swarm emerging from a flower wants to spread out while keeping
% in contact with each other via their antennas. Use the genetic algorithm
% to help them decide on their next movements.
% Sanjidah Wahid
% ee59837_16
clc 
clear

%% User inputs and initalizations

% user inputs:
swarm_population = 10;
speed = 1;
communication_dist = 10; 
num_moves = 2; 
positions = zeros(swarm_population, 3, num_moves); 

% assign the insects to random locations (ensure that the z is at least
% radius above 0 to avoid collision with ground):
positions(:,3,1) = positions(:,3,1)+communication_dist;

% define chromosome length:
chromosome_length = 5;
    
% define lower bounds and upper bounds of the chromosomes:
Lb = zeros(1,chromosome_length);
Ub = ones(1,chromosome_length);
int_indices = 1:chromosome_length;

% declare the displacement vectors:
displacement_vectors = [[0, 1]; [1/sqrt(2), 1/sqrt(2)];...
            [1, 0]; [1/sqrt(2), -1/sqrt(2)];...
			[0, -1]; [-1/sqrt(2), -1/sqrt(2)];...
			[-1, 0]; [-1/sqrt(2), 1/sqrt(2)]];
displacement_vectors = speed .* displacement_vectors;

options = optimoptions('ga','display','off'); 

for t = 1:num_moves-1
    fprintf("\n\n***** TIME IS NOW: %d*****\n", t)
    
    for plane_count = 1:swarm_population
        fprintf("***** BEGINNING GA FOR INSECT #%d *****\n", plane_count)
         
        % get all neighbors and the position of the current insect:
        neighbors = positions(:,:,t);
        neighbors(plane_count,:) = [];
        current_position = positions(plane_count, :, t);
    
        % the fitness function - complete the fitness function definition
        % at the end of the script (second to last function):
        fit_func = @(chromosome) fitness_function(chromosome, ...
                   current_position, speed, neighbors, communication_dist, displacement_vectors);

        % invoke matlab genetic algorithm for the current insect:
        selection = ga(fit_func, chromosome_length, [], [], ...
            [], [], Lb, Ub, [], int_indices, options);
        
        % get the next position and assign it to the next time step:
        displacement = displacement_vectors(bi2de(selection(3:end),...
            'left-msb')+1,:);
        next_position = get_next_position(selection, current_position, ...
            speed, displacement_vectors);
        
        positions(plane_count,:,t+1) = next_position;
        fprintf("\tselection fitness = %f\n", fit_func(selection))
        fprintf("***** FINISHED GA FOR UAV #%d AT TIME %d *****\n", ...
            plane_count, t)
        
    end
end

%% Visualize the Insects

visualize3D(positions, num_moves, swarm_population, communication_dist);
open_anim = true;
while open_anim == true
    fprintf("Replay the animation?\n\t(1) yes\n\t(2) no\n");
    user_choice = input('');
    if user_choice == 2
        open_anim = false;
        fprintf('Thank you. Have a nice day!\n');
        break;
    else
        close all
        visualize3D(positions, num_moves, swarm_population, communication_dist);
    end
end

% Write the fitness function:
function fitness_score = fitness_function(chromosome, position, speed, ...
                            neighbors, communication_dist, displacement_vectors)
    fitness_score = 0;
    neighbor_count = 0;
    
    candidate_pos = get_next_position(chromosome, position, speed, ...
        displacement_vectors);
    
    for i = 1:length(neighbors)
        distance = norm(candidate_pos - neighbors(i,:));
        if distance <= communication_dist  
            neighbor_count = neighbor_count + 1;
            fitness_score = fitness_score + (communication_dist - distance);
        end
    end
    
    if neighbor_count < 1 || candidate_pos(3) <= communication_dist
        fitness_score = abs(intmax);
    end

end

function next_pos = get_next_position(chromosome, position, speed, ...
                                        displacement_vectors)
    if bi2de(chromosome(1:2)) == 0 
         
        next_pos = position;
    elseif bi2de(chromosome(1:2), 'left-msb') == 1 
        
        displacement = displacement_vectors(bi2de(chromosome(3:end), 'left-msb')+1,:);
        next_pos(1:2)= position(1:2) + displacement;
        next_pos(3) = position(3) + speed; 
    elseif bi2de(chromosome(1:2), 'left-msb') == 2
        
        displacement = displacement_vectors(bi2de(chromosome(3:end), 'left-msb')+1,:);
        next_pos(1:2)= position(1:2) + displacement;
        next_pos(3) = position(3) - speed; 
    elseif bi2de(chromosome(1:2), 'left-msb') == 3 
        
        next_pos = position;
        displacement = displacement_vectors(bi2de(chromosome(3:end), 'left-msb')+1,:);
        next_pos(1:2)= position(1:2) + displacement;
    else
    end
end
