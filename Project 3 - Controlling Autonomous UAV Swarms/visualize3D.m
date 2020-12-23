
%% Visualizing the results
function visualize3D(position, movement, swarm, radius_dist)
    figure;
    img_name = 'flower_bg';
    copter_pad = imread(img_name, 'jpg');
    [unit_sph_x, unit_sph_y, unit_sph_z] = sphere; 
    
    min_x = min(min(position(:,1,:))) - radius_dist;
    max_x = max(max(position(:,1,:))) + radius_dist;
    min_y = min(min(position(:,2,:))) - radius_dist;
    max_y = max(max(position(:,2,:))) + radius_dist;
    min_z = 0;
    max_z = max(max(position(:,3,:))) + radius_dist;
    x_span = (max_x - min_x);
    y_span = (max_y - min_y);
    x_axis_min = (round(min_x/radius_dist)-1)*radius_dist;
    x_axis_max = (round(max_x/radius_dist)+1)*radius_dist;
    y_axis_min = (round(min_y/radius_dist)-1)*radius_dist;
    y_axis_max = (round(max_y/radius_dist)+1)*radius_dist;
    z_axis_min = min_z;
    z_axis_max = (round(max_z/radius_dist)+1)*radius_dist;
    iconsize = [x_span/30 y_span/30]; 
 
    for t = 1:movement
       pause(0.25); 
       hold off
       
       for plane_count = 1:swarm
           
            x_pos = position(plane_count,1,t);
            y_pos = position(plane_count,2,t);
            z_pos = position(plane_count,3,t);

            sph_x = (radius_dist*unit_sph_x + x_pos);
            sph_y = (radius_dist*unit_sph_y + y_pos);
            sph_z = (radius_dist*unit_sph_z + z_pos);
            surf(sph_x, sph_y, sph_z,'FaceColor', 'blue', ...
                 'LineStyle', '-', 'EdgeColor', 'blue', ... 
                 'FaceAlpha', 0.05, 'EdgeAlpha', 0.1);
            xlim([x_axis_min x_axis_max])
            ylim([y_axis_min y_axis_max])
            zlim([z_axis_min z_axis_max])
            hold on
            
            scatter3(x_pos, y_pos, z_pos, 'filled');
       end
       plot_title = sprintf('Insect Positions at t = %d', t);
       xlim([x_axis_min x_axis_max]);
       ylim([y_axis_min y_axis_max]);
       imagesc([x_axis_min x_axis_max],[y_axis_min y_axis_max],copter_pad);
       hold on
       title(plot_title);
    end
end