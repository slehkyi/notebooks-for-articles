heights = [9,8,7,8,9,5,6]
# heights = [1,9,3,3,5,5,3,5,7,3]
ln = len(heights)
total_sum = 0
            
            
def find_hole(heights):
    first_max = 0
    ind_first_max = 0
    second_max = 0
    ind_second_max = 0
    # find borders
    for ind, h in enumerate(heights):
        if h > first_max:
            ind_first_max, first_max = ind_second_max, second_max
            ind_first_max, first_max = ind, h
        elif (h >= second_max and ind != ind_first_max):
            ind_second_max, second_max = ind, h

    # if borders create a hole, calculate the volume
    if abs(ind_first_max-ind_second_max) > 1:
        reverse = []
        for h in heights[ind_first_max:ind_second_max+1]:
            reverse.append(second_max-h)
        part_sum = sum([x for x in reverse if x>0])
    else:
        part_sum = 0
        
    return part_sum, ind_first_max, ind_second_max


start = 0
finish = ln
# go through the list looking for holes and calculating its volumes till the end
while finish - start > 1:    
    part_sum, ind_first_max, ind_second_max = find_hole(heights[start:finish])
    total_sum += part_sum
    start += max([ind_second_max,ind_first_max])
    
    
print("Total sum: "+str(total_sum))