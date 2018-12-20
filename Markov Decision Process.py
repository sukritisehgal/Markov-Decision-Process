import numpy as np
import copy

def MDP(check,reward, utility, destinationCoordinates):
    delta = -1
    if(check==0):
        utilityUpdated = copy.deepcopy(reward)
        check+=1
    else:
        utilityUpdated=copy.deepcopy(utility)

    for i in range(0,len(utilityUpdated)):
        for j in range(0,len(utilityUpdated[i])):
            if (j == int(destinationCoordinates[0]) and i == int(destinationCoordinates[1])):
                utilityUpdated[i][j]=99
                continue

            if (j == 0):
                columnStart = 0
            else:
                columnStart = j - 1

            if (j == len(utility) - 1):
                columnEnd = len(utility) - 1
            else:
                columnEnd = j + 1

            if (i == 0):
                rowStart = 0
            else:
                rowStart = i - 1

            if (i == len(utility) - 1):
                rowEnd = len(utility) - 1
            else:
                rowEnd = i + 1

            down = np.float64(0.7 * utility[rowEnd][j] + 0.1 * (
                        utility[rowStart][j] + utility[i][columnStart] + utility[i][columnEnd]))
            left = np.float64(0.7 * utility[i][columnStart] + 0.1 * (
                        utility[rowStart][j] + utility[rowEnd][j] + utility[i][columnEnd]))
            up = np.float64(0.7 * utility[rowStart][j] + 0.1 * (
                        utility[rowEnd][j] + utility[i][columnStart] + utility[i][columnEnd]))
            right = np.float64(0.7 * utility[i][columnEnd] + 0.1 * (
                        utility[rowStart][j] + utility[i][columnStart] + utility[rowEnd][j]))

            utilityUpdated[i][j] = reward[i][j]+0.9*(max(right,down,up,left))

            difference = abs(utilityUpdated[i][j] - utility[i][j])
            if (difference > delta):
                delta = difference

    return [check,delta,utilityUpdated]


def turn_right(direction):
    if(direction=="s"):
        return "w"
    if (direction == "w"):
        return "n"
    if (direction == "e"):
        return "s"
    if (direction == "n"):
        return "e"


def turn_left(direction):
    if(direction=="s"):
        return "e"
    if (direction == "w"):
        return "s"
    if (direction == "e"):
        return "n"
    if (direction == "n"):
        return "w"

def Run_MDP(reward,carIndex,destination):

    destinationCoordinates = destination[carIndex]
    check=0

    utility=copy.deepcopy(reward)
    delta = 100000
    Policy=[]

    while (delta > 0.111111111):
        [check,delta,utility] = MDP(check,reward, utility, destinationCoordinates)

    for i in range(0,len(utility)):
        row=[]
        for j in range(0,len(utility[i])):
            if (j == int(destinationCoordinates[0]) and i == int(destinationCoordinates[1])):
                row.append("#")
                continue

            if (j == 0):
                columnStart = 0
            else:
                columnStart = j - 1

            if (j == len(utility) - 1):
                columnEnd = len(utility) - 1
            else:
                columnEnd = j + 1

            if (i == 0):
                rowStart = 0
            else:
                rowStart = i - 1

            if (i == len(utility) - 1):
                rowEnd = len(utility) - 1
            else:
                rowEnd = i + 1

            up=utility[rowStart][j]
            down=utility[rowEnd][j]
            right=utility[i][columnEnd]
            left=utility[i][columnStart]

            maximum=up
            direction="n"
            if(down>maximum):
                maximum=down
                direction="s"
            if(right>maximum):
                maximum=right
                direction="e"
            if(left>maximum):
                maximum=left
                direction="w"

            row.append(direction)
        Policy.append(row)

    return Policy

outputfile = open("output.txt", "w")
with open('input.txt') as inputfile:
    inputs = inputfile.readlines()
    inputs = [y.strip() for y in inputs]

    matrixLength = int(inputs[0])
    carsLocation = []
    obstacleCordinates = []
    destinationLocation = []

    cars = int(inputs[1])
    numberOfObstacles = int(inputs[2])
    for i in range(3, numberOfObstacles + 3):
        k = inputs[i].split(',')
        obstacleCordinates.append(k)

    indexOfCar = numberOfObstacles + 3

    for i in range(indexOfCar, indexOfCar + cars):
        t = inputs[i].split(',')
        carsLocation.append(t)

    nextIndex = indexOfCar + cars
    for i in range(nextIndex, nextIndex + cars):
        t = inputs[i].split(',')
        destinationLocation.append(t)


    for i in range(len(carsLocation)):
        destinationCoordinates = destinationLocation[i]
        reward = [[-1 for row in range(matrixLength)] for col in range(matrixLength)]
        reward[int(destinationCoordinates[1])][int(destinationCoordinates[0])] += 100
        for u in obstacleCordinates:
            reward[int(u[1])][int(u[0])] -= 100

        Policy = Run_MDP(reward, i, destinationLocation)

        rewards=[]
        for j in range(10):
            current=0
            np.random.seed(j)
            swerve= np.random.random_sample(1000000)
            k=0
            destCord = destinationLocation[i]
            pos = carsLocation[i][:]
            temporary = pos[0]
            pos[0] = pos[1]
            pos[1] = temporary
            move = Policy[int(pos[0])][int(pos[1])]
            while((pos[0],pos[1])!= (destCord[1],destCord[0])):
                current=current+reward[int(pos[0])][int(pos[1])]
                if(swerve[k]>0.7):
                    if(swerve[k]>0.8):
                        if(swerve[k]>0.9):
                            move = turn_right(move)
                            move = turn_right(move)
                        else:
                            move = turn_right(move)
                    else:
                        move = turn_left(move)
                    if (move == "w"):
                        if (int(pos[1]) > 0):
                            pos[1] = str(int(pos[1]) - 1)
                        move = Policy[int(pos[0])][int(pos[1])]
                    elif (move == "n"):
                        if (int(pos[0]) > 0):
                            pos[0] = str(int(pos[0]) - 1)
                        move = Policy[int(pos[0])][int(pos[1])]
                    elif (move == "s"):
                        if (int(pos[0]) < matrixLength - 1):
                            pos[0] = str(int(pos[0]) + 1)
                        move = Policy[int(pos[0])][int(pos[1])]
                    elif (move == "e"):
                        if (int(pos[1]) < matrixLength - 1):
                            pos[1] = str(int(pos[1]) + 1)
                        move = Policy[int(pos[0])][int(pos[1])]
                else:
                    if(move=="w"):
                        if(int(pos[1])>0):
                            pos[1]=str(int(pos[1])-1)
                        move = Policy[int(pos[0])][int(pos[1])]
                    elif(move=="n"):
                        if(int(pos[0])>0):
                            pos[0] = str(int(pos[0]) - 1)
                        move = Policy[int(pos[0])][int(pos[1])]
                    elif(move=="s"):
                        if(int(pos[0])<matrixLength-1):
                            pos[0] = str(int(pos[0]) + 1)
                        move = Policy[int(pos[0])][int(pos[1])]
                    elif (move == "e"):
                        if (int(pos[1]) < matrixLength - 1):
                            pos[1] = str(int(pos[1]) + 1)
                        move = Policy[int(pos[0])][int(pos[1])]
                k += 1
            current+=100
            rewards.append(current)

        avg = int(np.floor(np.sum(rewards)/len(rewards)))
        print avg
        if(i==len(carsLocation)-1):
            outputfile.write(str(avg))
        else:
            outputfile.write(str(avg))
            outputfile.write("\n")
    inputfile.close()
    outputfile.close()





