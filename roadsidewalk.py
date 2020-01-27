import csv
import matplotlib.pyplot as plt
import numpy as np

'''
Frames are selected based on a number of factors, such as environmental clutter,
distance from camera, etc. Explained in detail below.

Descriptors are carefully reviewed and inputted into frame_descriptors.csv
Each image frame has a descriptor for:
a. frame number
b. type (0 = Road, 1 = Sidewalk, 2 = Both, 3 = None)
c. intent (Pedestrian intent to cross (0/1))
d. distance (Distance from closest pedestrian (0-3: 0 is closest, 3 is furthest))
e. blend (Pedestrian blending into the environment (0/1))
f. clutter (number of pedestrians, objects in environment (0/1))
g. edge (If pedestrian is on edge of screen (0/1))
h. expectation (expect to get type correct = 0 or wrong = 1)
'''

# this method parses predefined descriptors of images from a given csv file.
# Returns those descriptors in a list. Additionally, will tally up the distances
# to be used for further analysis. For the purpose of this experiment, the
# descriptor file is frame_descriptors.csv
def parse_descriptors(file, distances):
    file = open(file, 'r')
    reader = csv.reader(file)
    next(reader)
    
    place, intent, distance, blend, clutter, edge, expect = ([] for i in range(7))

    for row in reader:

        #tally up the distance chart
        if row[3] == '0':
            distances[0] += 1
        elif row[3] == '1':
            distances[1] += 1
        elif row[3] == '2':
            distances[2] += 1
        else:
            distances[3] += 1

        #append relevant information
        place.append(row[1])
        intent.append(row[2])
        distance.append(row[3])
        blend.append(row[4])
        clutter.append(row[5])
        edge.append(row[6])
        expect.append(row[7]) # expectation if place matches or not

    file.close()
    return [place, intent, distance, blend, clutter, edge, expect]

# compares matching elements between two lists (1 & 2) and appends
# the non matching indices as a list to non_match
def index_non_match(list1, list2, non_match):   
    for x in range(0, len(list1)):
        if list1[x] != list2[x]:
            non_match.append(x)

# for indices that were incorrect (non_match), compare the binary values
# from list1 and return the accuracy of positive cases as a percentage.
# Returns the percent of matches over total incorrect answers.
def get_accuracy(non_match, list1):
    count = 0
    
    for x in non_match:
        if list1[x] == '1':
            count += 1

    return count/len(non_match)

# retrieves the ratio of incorrect matches based on distance.
# Takes in a list of incorrect answers, list of all distances (list1),
# and list that records the count for each distance.
def get_distance_accuracy(non_match, list1, distances):
    count0 = 0.0 #closest
    count1 = 0.0 #close
    count2 = 0.0 #mid
    count3 = 0.0 #far

    # adds up the count for all distances that subject answered incorrectly
    for x in non_match:
        if list1[x] == '0':
            count0 += 1
        elif list1[x] == '1':
            count1 += 1
        elif list1[x] == '2':
            count2 += 1
        else:
            count3 += 1

    return count0/distances[0], count1/distances[1], count2/distances[2], count3/distances[3]


            
if __name__ == '__main__':
    ### parses results from experiment ### 
    file = open('experiment.csv', 'r')
    reader = csv.reader(file)
    next(reader) #skips the header

    response = []
    
    for row in reader:
        response.append(row[2])

    file.close()

    # record all the distances. Each row (trial) has exactly one distance
    distance_count = [0, 0, 0, 0] # 1st element corresponds to closest, last corresponds to furthest

    
    ### analyze results ###

    # pie chart for total percent correct/incorrect
    place, intent, distance, blend, clutter, edge, expect = parse_descriptors('frame_descriptors.csv', distance_count)
    non_match = []  # int list that records indices that were incorrect
    index_non_match(response, place, non_match)
    
    p_wrong = round(len(non_match)/len(place)*100) # percentage of incorrect answers
    
    labels = ('Correct', 'Incorrect')
    sizes = (100-p_wrong, p_wrong)
    explode = (0.12, 0)  # pop-out effect of pie chart
    color = ['#19C61F','#F5380F']

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes,explode,labels,shadow=True, autopct='%0.0f%%',colors=color)
    ax1.axis('equal')

    # bar chart for accuracy of binary factors for all incorrect answers
    plt.figure(2)
    p_blend = get_accuracy(non_match, blend)
    p_clutter = get_accuracy(non_match, clutter)
    p_edge = get_accuracy(non_match, edge)
    p_blend *= 100
    p_clutter *= 100
    p_edge *= 100
    p_total = p_blend + p_clutter + p_edge
    percentages = [p_blend, p_clutter, p_edge, p_total]
    percentages = np.rint(percentages)
    
    objects = ("Blend", "Clutter", "Edge", "Total")
    y_pos = np.arange(len(objects))
    plt.bar(y_pos, percentages, align='center', color=['black','black','black','cyan'])
    plt.xticks(y_pos, objects)
    plt.yticks(np.arange(0,101, step=25))
    plt.ylabel('Percent (%)')
    plt.title('Percent of cases causing incorrect answers')
    
    for i, v in enumerate(percentages):  # plot text values onto graph above bars
        plt.text(i-0.125, v + 0.25, str(v))
    
    # bar chart for accuracy based on distance
    plt.figure(3)
    p_closest, p_close, p_med, p_far = get_distance_accuracy(non_match, distance, distance_count)
    percentages = [p_closest*100, p_close*100, p_med*100, p_far*100]
    percentages = np.rint(percentages)
    
    objects = ("Closest", "Close", "Medium", "Far")
    y_pos = np.arange(len(objects))
    plt.bar(y_pos, percentages, align='center')
    plt.xticks(y_pos, objects)
    plt.yticks(np.arange(0,101, step=25))
    plt.ylabel('Percent (%)')
    plt.title('Percent of incorrect answers based on distance')

    for i, v in enumerate(percentages):
        plt.text(i-0.125, v + 0.25, str(v))
        
    plt.show()
    
    
                    
