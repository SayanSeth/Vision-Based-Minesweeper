path='C:\Users\Dell\Documents\DIY\';
list = dir(path); 
[p , ~] = size(list) ;
file = list(p-1);
imageName = file.name;
im = imread(strcat(path,imageName));
R=im(:,:,1);
G=im(:,:,2);
B=im(:,:,3);

[r,c,~]=size(G);

binGreen=zeros(r,c);
for i=1:r
    for j=1:c
        if R(i,j)<=50 && G(i,j)>=200&&B(i,j)<=50
            binGreen(i,j)=255;
        end
    end
end
target=binGreen;
 target_labeled=bwlabel(target);
stats_target=regionprops((target_labeled),'centroid');
binRed=zeros(r,c);
binBlue=zeros(r,c);

for a=1:10  
while(1)
    list = dir(path); 
[q , ~] = size(list) ;


file = list(q -1);
imageName = file.name;
disp(imageName);
im = imread(strcat(path,imageName));
     R=im(:,:,1);
     G=im(:,:,2);
     B=im(:,:,3);
% imshow(R);
[r,c,~]=size(R);


%%
for i=1:r               
    for j=1:c
        if ((R(i,j)>=200) &&(G(i,j)<=100 )&& (B(i,j)<=100))
            binRed(i,j)=1;
        else 
            binRed(i,j)=0;
        end
    end
end

%% Blue Binarize
for i=1:r
    for j=1:c
        if (R(i,j)<=50) && (G(i,j)<=50) && (B(i,j)>=200)
            binBlue(i,j)=1;
        else
            binBlue(i,j)=0;
        end
    end
end
% imshow(binBlue);



%%
bot_body=binBlue;        
bot_head=binRed;
[bot_head_labeled,n1]=bwlabel(bot_head);
[bot_body_labeled,n2]=bwlabel(bot_body);
if n1==0||n2==0
    continue;
end

stats_body=regionprops(bot_body_labeled,'centroid');
    bot_body_position=stats_body.Centroid;
stats_head=regionprops(bot_head_labeled,'centroid')
    bot_head_position=stats_head.Centroid;        
stats_bota=regionprops(bot_body_labeled, 'area');
    bot_area=stats_bota.Area;
bot_radius=sqrt(bot_area/pi);
target_position=stats_target(a).Centroid;
  
bot_angle = -atan2(bot_head_position(2)-bot_body_position(2),bot_head_position(1)-bot_body_position(1));
target_angle = -atan2(target_position(2)-bot_body_position(2),target_position(1)-bot_body_position(1));
bot_target_angle = bot_angle - target_angle;


stats_tarea=regionprops(target_labeled,'area');
     target_area=stats_tarea.Area;
target_radius=(target_area/pi);  
    bot_target_distance=sqrt((bot_body_position(2)-target_position(2))^2 + (bot_body_position(1)-target_position(1))^2);
if(bot_target_distance<=150)
           character_for_arduino='s';
end;
if(bot_target_angle>0)
    characters_for_arduino='r';
elseif(bot_target_angle<0)
    characters_for_arduino='l';
else
    characters_for_arduino='f';
end

    
    fprintf(arduino,'%c',character_for_arduino);
    
    if(character_for_arduino=='s')
        break;
    end
    
   pause(.5);
end
pause(.5);
end
bazar='x';
fprintf(arduino,'%c',bazar);