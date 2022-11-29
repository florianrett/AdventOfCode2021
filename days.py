import HelperFunctions as hf
import HelperClasses as hc
import collections
import copy

def day1a(input):
    numIncreases = 0
    prev = 999999999
    for value in input:
        depth = int(value)
        if depth > prev:
            numIncreases += 1
        prev = depth
    return numIncreases

def day1b(input):
    windows = []
    for i in range(0, len(input) - 2):
        depth1 = int(input[i])
        depth2 = int(input[i+1])
        depth3 = int(input[i+2])
        windows.append(depth1+depth2+depth3)

    return day1a(windows)

def day2a(input):
    x = 0
    y = 0

    for line in input:
        s = line.split(" ")
        move = s[0]
        value = int(s[1])
        if move == "forward":
            x += value
        if move == "up":
            y -= value
        if move == "down":
            y += value

    return x * y

def day2b(input):
    x = 0
    y = 0
    aim = 0

    for line in input:
        s = line.split(" ")
        move = s[0]
        value = int(s[1])
        if move == "forward":
            x += value
            y += aim * value
        if move == "up":
            aim -= value
        if move == "down":
            aim += value
    return x * y

def day3a(input):
    numBits = len(input[0])

    mostCommonBits = ""
    leastCommonBits = ""
    for i in range(0, numBits):
        if hf.FindMostCommonBitForPosition(input, i) == '1':
            mostCommonBits += "1"
            leastCommonBits += "0"
        else:
            mostCommonBits += "0"
            leastCommonBits += "1"

    gammarate = int(mostCommonBits, 2)
    epsilonrate = int(leastCommonBits, 2)

    return gammarate * epsilonrate

def day3b(input):
    numBits = len(input[0])
    oxRatings = input
    co2Ratings = input

    for i in range(0, numBits):
        oxRatings = hf.FilterList(hf.FindMostCommonBitForPosition(oxRatings, i), oxRatings, i)

        if len(co2Ratings) > 1:
            if hf.FindMostCommonBitForPosition(co2Ratings, i) == '1':
                co2Ratings = hf.FilterList('0', co2Ratings, i)
            else:
                co2Ratings = hf.FilterList('1', co2Ratings, i)

    oxygen = int(oxRatings[0], 2)
    co2scrubber = int(co2Ratings[0], 2)

    return oxygen * co2scrubber

def day4a(input):
    numbers = []
    boards = []
    for n in input[0].split(','):
        numbers.append(int(n))

    for i in range(0, int(len(input) / 6)):
        start = i*6+2
        boardstring = input[start] + " " + input[start+1] + " " + input[start+2] + " " + input[start+3] + " " + input[start+4]
        newBoard = hc.BingoBoard(boardstring)
        boards.append(newBoard)

    for number in numbers:
        print("Drawing number", number)
        for b in boards:
            if b.MarkNumber(number):
                return b.GetWinningScore(number)
    return -1

def day4b(input):
    numbers = []
    boards = []
    winningboards = []
    for n in input[0].split(','):
        numbers.append(int(n))

    for i in range(0, int(len(input) / 6)):
        start = i*6+2
        boardstring = input[start] + " " + input[start+1] + " " + input[start+2] + " " + input[start+3] + " " + input[start+4]
        newBoard = hc.BingoBoard(boardstring)
        boards.append(newBoard)

    for number in numbers:
        print("Drawing number", number)
        for b in boards:
            if b in winningboards:
                continue
            else:
                if b.MarkNumber(number):
                    winningboards.append(b)
                    if len(winningboards) == len(boards):
                        return b.GetWinningScore(number)
    return -1

def day5a(input):
    coveredPoints = []
    for line in input:
        split = line.split(" -> ")
        x1 = int(split[0].split(",")[0])
        y1 = int(split[0].split(",")[1])
        x2 = int(split[1].split(",")[0])
        y2 = int(split[1].split(",")[1])
        # print(x1, y1, x2, y2)

        for p in hf.GetStraightLines(x1, x2, y1, y2):
            coveredPoints.append(p)

    result = 0
    c = collections.Counter(coveredPoints)
    for p in c:
        if c[p] >= 2:
            result += 1

    return result

def day5b(input):
    coveredPoints = []
    for line in input:
        split = line.split(" -> ")
        x1 = int(split[0].split(",")[0])
        y1 = int(split[0].split(",")[1])
        x2 = int(split[1].split(",")[0])
        y2 = int(split[1].split(",")[1])
        # print(x1, y1, x2, y2)

        for p in hf.GetStraightLines(x1, x2, y1, y2):
            coveredPoints.append(p)
        for p in hf.GetDiagonalLines(x1, x2, y1, y2):
            coveredPoints.append(p)

    result = 0
    c = collections.Counter(coveredPoints)
    for p in c:
        if c[p] >= 2:
            result += 1

    return result

def day6a(input):
    startlist = []
    for x in input[0].split(','):
        startlist.append(int(x))

    return hf.SimulateFish(startlist, 80, 7, 9)

def day6b(input):
    startlist = []
    for x in input[0].split(','):
        startlist.append(int(x))

    return hf.SimulateFish(startlist, 256, 7, 9)

def day7a(input):
    crabs = []
    for i in input[0].split(','):
        crabs.append(int(i))

    crabs.sort()
    pos = 0
    fuel = sum(crabs)
    for i in range(max(crabs)):
        test = sum(abs(i-c) for c in crabs)
        if test < fuel:
            fuel = test

    return fuel

def day7b(input):
    crabs = []
    for i in input[0].split(','):
        crabs.append(int(i))

    crabs.sort()
    pos = 0
    fuel = -1
    for i in range(max(crabs)):
        test = int(sum( (distance + 1) * distance / 2 for distance in [abs(c-i) for c in crabs]))
        if test < fuel or fuel < 0:
            fuel = test

    return fuel

def day8a(input):
    sum = 0
    for line in input:
        digits = line.split(' | ')[1].split(' ')

        for l in [len(digit) for digit in digits]:
            if l == 2 or l == 3 or l == 4 or l == 7:
                sum  += 1
    return sum

def day8b(input):
    sum = 0

    for line in input:
        split = line.split(' | ')
        mapping = hf.SolveDigitMapping(split[0].split(' '))
        sum += hf.DecodeDigits(split[1].split(' '), mapping)

    return sum

def day9a(input):
    heightmap = []
    for line in input:
        heightmap.append([int(x) for x in line])

    risklevels = 0
    for i in range(len(heightmap)):
        for j in range(len(heightmap[0])):
            risklevels += hf.CalculateRiskLevel(heightmap, j, i)

    return risklevels

def day9b(input):
    heightmap = []
    for line in input:
        heightmap.append([int(x) for x in line])

    basinSizes = []
    for i in range(len(heightmap)):
        for j in range(len(heightmap[0])):
            if hf.CalculateRiskLevel(heightmap, j, i) > 0:
                basinSizes.append(hf.RecursiveGetBasinSize(heightmap, j, i))

    basinSizes.sort()
    basinSizes.reverse()
    return basinSizes[0] * basinSizes[1] * basinSizes[2]

def day10a(input):
    score = 0
    # hf.FindFirstIllegalCharacter(input[2])
    for line in input:
        result = hf.FindFirstIllegalCharacter(line)
        # print(result)
        # break
        if result == ')':
            score += 3
        if result == ']':
            score += 57
        if result == '}':
            score += 1197
        if result == '>':
            score += 25137
    return score

def day10b(input):
    scores = []
    for line in input:
        result = hf.FindFirstIllegalCharacter(line)
        # print(result)
        # break
        if result != ')' and result != ']' and result != '}' and result != '>':
            scores.append(hf.GetAutocompleteScore(result))
    scores.sort()
    return scores[int(len(scores)/2)]

def day11a(input):
    grid = []
    for line in input:
        newList = []
        for c in line:
            newList.append(int(c))
        grid.append(newList)

    sum = 0
    for i in range(100):
        sum += hf.SimulateStep(grid)
    # print(grid)
    return sum

def day11b(input):
    grid = []
    for line in input:
        newList = []
        for c in line:
            newList.append(int(c))
        grid.append(newList)

    currentStep = 0
    numOctopuses = len(grid) * len(grid[0])
    while True:
        currentStep += 1
        if hf.SimulateStep(grid) == numOctopuses:
            break
    return currentStep

def day12a(input):
    graph = hf.MapGraph(input)

    num = hf.RecFindPaths(graph, "start")
    return num

def day12b(input):
    graph = hf.MapGraph(input)

    num = hf.RecFindPaths(graph, "start", smallCaveEnteredTwice=False)
    return num

def day13a(input):
    dots = []
    for line in input:
        coords = line.split(',')
        if len(coords) > 1:
            dots.append((int(coords[0]), int(coords[1])))
        else:
            fold = line.split(' ')
            if len(fold) == 3:
                instruction = fold[2]
                return len(hf.FoldPaper(dots, instruction))

    return -1

def day13b(input):
    dots = []
    for line in input:
        coords = line.split(',')
        if len(coords) > 1:
            dots.append(((int(coords[0])), int(coords[1])))
        else:
            fold = line.split(' ')
            if len(fold) == 3:
                instruction = fold[2]
                dots = hf.FoldPaper(dots, instruction)
                print(dots)
    for y in range(6):
        line = ""
        for x in range(40):
            if (x, y) in dots:
                line += "#"
            else:
                line += "."
        print(line)

        
    return -1

def day14a(input):
    polymer = input[0]
    rules = {}
    for i in range(2, len(input)):
        rule = input[i].split(" -> ")
        rules[rule[0]] = rule[1]

    for i in range(10):
        polymer = hf.Polymerize(polymer, rules)
        # print(polymer)

    counts = collections.Counter(c for c in polymer)
    most = counts.most_common()[0][1]
    least = counts.most_common().pop()[1]
    return int(most) - int(least)

def day14b(input):
    polymer = input[0]
    rules = {}
    for i in range(2, len(input)):
        rule = input[i].split(" -> ")
        newPolymers = [rule[0][0]+rule[1], rule[1]+rule[0][1]]
        rules[rule[0]] = newPolymers

    polymerCounts = hf.PolymerizeEfficient(polymer, rules, 40)
    counts = {}
    for p in polymerCounts:
        e = p[1] # only count last element of each pair
        if e not in counts:
            counts[e] = 0
        counts[e] += polymerCounts[p]
    counts[polymer[0]] += 1
    counter = collections.Counter(counts)
    
    return counter.most_common()[0][1] - counter.most_common().pop()[1]

def day15a(input):
    risk = []
    for line in input:
        row = []
        for c in line:
            row.append(int(c))
        risk.append(row)

    return hf.GetShortestPath(risk)

def day15b(input):
    risk = []
    for i in range(5):
        for line in input:
            row = []
            for j in range(5):
                for c in line:
                    value = int(c) + i + j
                    value = (value - 1) % 9 + 1
                    row.append(value)
            risk.append(row)

    return hf.GetShortestPath(risk)

def day16a(input):
    bits = hf.HexToBits(input[0])#.rstrip('0')
    
    versionSum = hf.ResolvePacket(bits)[0]
    return versionSum

def day16b(input):
    bits = hf.HexToBits(input[0])#.rstrip('0')

    value = hf.ResolvePacket(bits)[2]
    return value

def day17a(input):
    split = input[0].split("=")
    rangeX = split[1].split(',')[0]
    tx = rangeX.split("..")
    tx = (int(tx[0]), int(tx[1]))
    ty = split[2].split("..")
    ty = (int(ty[0]), int(ty[1]))
    
    x = hf.FindMinVelocityX(tx)
    y = hf.FindMaxVelocityY(ty)

    return hf.TestVelocity((x, y), tx, ty)[1]

def day17b(input):
    split = input[0].split("=")
    rangeX = split[1].split(',')[0]
    tx = rangeX.split("..")
    tx = (int(tx[0]), int(tx[1]))
    ty = split[2].split("..")
    ty = (int(ty[0]), int(ty[1]))

    num = 0
    maxY = hf.FindMaxVelocityY(ty)
    for x in range(tx[1]+1):
        for y in range(ty[0], maxY+1):
            probe = hf.TestVelocity((x, y), tx, ty)
            if probe[0]:
                num += 1
    return num

def day18a(input):

    current = hc.SnailFishNumber(hf.DecodeSnailfishNumber(input[0]))
    current.Reduce()

    for i in range(1, len(input)):
        current = hc.SnailFishNumber(leftChild= current, rightChild= hc.SnailFishNumber(hf.DecodeSnailfishNumber(input[i])))
        current.Reduce()
    
    # print(current)
    return current.GetMagnitude()

def day18b(input):
    numbers = []
    for line in input:
        numbers.append(hc.SnailFishNumber(hf.DecodeSnailfishNumber(line)))
    
    magnitudes = []
    # for n in numbers:
    #     for n2 in numbers:
    #         if n == n2:
    #             continue
    #         n3 = hc.SnailFishNumber(leftChild=copy.deepcopy(n), rightChild=copy.deepcopy(n2))
    #         n3.Reduce()
    #         magnitudes.append(n3.GetMagnitude())
    # print(magnitudes)
    magnitudes = [x.GetMagnitude() for x in [hc.SnailFishNumber(leftChild=copy.deepcopy(n1), rightChild=copy.deepcopy(n2)).Reduce() for n1 in numbers for n2 in numbers if n1 != n2]]
    # print(magnitudes)

    return max(magnitudes)

def day19a(input):
    inputdata = []
    test = ""
    for line in input:
        if "scanner" in line:
            current = []
        elif len(line) > 0:
            current.append(tuple([int(x) for x in line.split(",")]))
        else:
            inputdata.append(current)
    inputdata.append(current) # last scanner

    scanners = []
    for s in inputdata:
        scanners.append(hc.Scanner(s))
    
    # scan = hc.Scanner([])
    # print(scan.ResolveRotation((-4, -132, -21), (-132, 4, -21)))
    while len(scanners) > 1:
        print("Remaining Scanners", len(scanners))
        scanners = hf.FindAndMergeScanners(scanners)

    return len(scanners[0].beacons)

def day19b(input):
    return -1

def day20a(input):
    alg = input[0]
    image = {}

    for y in range(2, len(input)):
        for x in range(len(input[y])):
            if input[y][x] == "#":
                image[(x, y-2)] = 1
            else:
                image[(x, y-2)] = 0

    image = hf.EnhanceImage(image, alg)
    # hf.PrintImage(image, (-3, 20), (-3, 20))
    image = hf.EnhanceImage(image, alg, True)
    # hf.PrintImage(image, (-3, 20), (-3, 20))


    return len([i for i in image if image[i] == "1"])

def day20b(input):
    alg = input[0]
    image = {}

    for y in range(2, len(input)):
        for x in range(len(input[y])):
            if input[y][x] == "#":
                image[(x, y-2)] = 1
            else:
                image[(x, y-2)] = 0

    for i in range(25):
        image = hf.EnhanceImage(image, alg)
        # hf.PrintImage(image, (-3, 20), (-3, 20))
        image = hf.EnhanceImage(image, alg, True)
        # hf.PrintImage(image, (-3, 20), (-3, 20))


    return len([i for i in image if image[i] == "1"])

def day21a(input):
    p1pos = int(input[0][-1]) - 1
    p2pos = int(input[1][-1]) - 1
    p1score = 0
    p2score = 0

    nextDieNumber = 1
    numDieRolls = 0
    while True:
        for i in range(3):
            p1pos = (p1pos + nextDieNumber) % 10
            nextDieNumber += 1
            numDieRolls += 1
            if nextDieNumber == 101:
                nextDieNumber = 1
        p1score += p1pos + 1
        if p1score >= 1000:
            break

        for i in range(3):
            p2pos = (p2pos + nextDieNumber) % 10
            nextDieNumber += 1
            numDieRolls += 1
            if nextDieNumber == 101:
                nextDieNumber = 1
        p2score += p2pos + 1
        if p2score >= 1000:
            break

        # print(p1pos + 1, p1score, p2pos + 1, p2score)

    losingScore = min(p1score, p2score)

    return losingScore * numDieRolls

def day21b(input):
    p1pos = int(input[0][-1]) - 1
    p2pos = int(input[1][-1]) - 1
    p1wins = 0
    p2wins = 0

    universes = {}
    universes[(p1pos, 0, p2pos, 0)] = 1
    
    currentTurn = 1
    while len(universes) > 0:
        result = hf.GenerateNewUniverses(universes, currentTurn)
        universes = result[0]
        if currentTurn == 1:
            p1wins += result[1]
            currentTurn = 2
        else:
            p2wins += result[1]
            currentTurn = 1
        
        # print(universes)

    return max(p1wins, p2wins)

def day22a(input):
    instructions = []
    for line in input:
        split = line.split(" ")
        bState = split[0] == "on"
        coordinates = []
        for c in split[1].replace("x", "").replace("y", "").replace("z", "").replace("=", "").split(","):
            r = c.split("..")
            coordinates += [int(x) for x in r]
        instructions.append((bState, coordinates))

    initCuboid = hc.Cuboid(-50, 50, -50, 50, -50, 50)
    activeCuboids = []
    for ins in instructions:
        c = ins[1]
        newCuboid = hc.Cuboid(c[0], c[1], c[2], c[3], c[4], c[5])

        if not newCuboid.Overlaps(initCuboid):
            continue

        # print("executing:", ins)
        newActiveCuboids = []
        for cuboid in activeCuboids:
            if cuboid.Overlaps(newCuboid):
                cuts = cuboid.Cut(newCuboid)
                newActiveCuboids += cuts
            else:
                newActiveCuboids.append(cuboid)
                continue

        if ins[0]:
            newActiveCuboids.append(newCuboid)
        
        activeCuboids = newActiveCuboids.copy()

        # print("resulting volume:", sum([x.GetVolume() for x in activeCuboids]))
    
    return sum([x.GetVolume() for x in activeCuboids])

def day22b(input):    
    instructions = []
    for line in input:
        split = line.split(" ")
        bState = split[0] == "on"
        coordinates = []
        for c in split[1].replace("x", "").replace("y", "").replace("z", "").replace("=", "").split(","):
            r = c.split("..")
            coordinates += [int(x) for x in r]
        instructions.append((bState, coordinates))

    activeCuboids = []
    for ins in instructions:
        c = ins[1]
        newCuboid = hc.Cuboid(c[0], c[1], c[2], c[3], c[4], c[5])

        # print("executing:", ins)
        newActiveCuboids = []
        for cuboid in activeCuboids:
            if cuboid.Overlaps(newCuboid):
                cuts = cuboid.Cut(newCuboid)
                newActiveCuboids += cuts
            else:
                newActiveCuboids.append(cuboid)
                continue

        if ins[0]:
            newActiveCuboids.append(newCuboid)
        
        activeCuboids = newActiveCuboids.copy()
        # print("resulting volume:", sum([x.GetVolume() for x in activeCuboids]))    

    return sum([x.GetVolume() for x in activeCuboids])

def day23a(input):
    roomA = [input[3][3], input[2][3]]
    roomB = [input[3][5], input[2][5]]
    roomC = [input[3][7], input[2][7]]
    roomD = [input[3][9], input[2][9]]

    state = hc.GameState([roomA, roomB, roomC, roomD], {}, 0, 2)    

    # Debug    
    # roomA = ["A"]
    # roomB = ["B", "B"]
    # roomC = ["C", "C"]
    # roomD = ["A"]
    # hallway = {5:"D", 7:"D"}

    # state = hc.GameState([roomA, roomB, roomC, roomD], hallway, 0, 2)
    print(state)
    # print("------------------------>")
    # for s in state.GeneratePossibleNextStates():
    #     print(s)
    #     print(s.GetStringRepresentation())


    openStates = [state]
    knownStates = {}
    shortestSolution = -1
    numSteps = 0
    while len(openStates) != 0:
        # print(len(openStates))
        numSteps += 1
        s = openStates.pop(0)
        if shortestSolution > 0 and s.totalCost > shortestSolution:
            continue
        if s.IsCompleted():
            shortestSolution = s.totalCost
            # print("found new shortest solution", shortestSolution)
            # print(s)
            continue
        if s.GetStringRepresentation() in knownStates:
            if s.totalCost > knownStates[s.GetStringRepresentation()]:
                continue


        # print("----------------------------------------------")
        # print("origin state:\n", s)
        # print("--------------------")
        for newState in s.GeneratePossibleNextStates():
            # print(newState, newState.totalCost)
            rep = newState.GetStringRepresentation()
            if rep in knownStates:
                if newState.totalCost >= knownStates[rep]:
                    continue
            knownStates[rep] = newState.totalCost
            openStates.append(newState)

    return shortestSolution

def day23b(input):
    roomA = [input[3][3], "D", "D", input[2][3]]
    roomB = [input[3][5], "B", "C", input[2][5]]
    roomC = [input[3][7], "A", "B", input[2][7]]
    roomD = [input[3][9], "C", "A", input[2][9]]

    state = hc.GameState([roomA, roomB, roomC, roomD], {}, 0, 4)
    
    
    openStates = [state]
    knownStates = {}
    shortestSolution = -1
    numSteps = 0
    while len(openStates) != 0:
        # print(len(openStates))
        numSteps += 1
        s = openStates.pop(0)
        if shortestSolution > 0 and s.totalCost > shortestSolution:
            continue
        if s.IsCompleted():
            shortestSolution = s.totalCost
            # print("found new shortest solution", shortestSolution)
            # print(s)
            continue
        if s.GetStringRepresentation() in knownStates:
            if s.totalCost > knownStates[s.GetStringRepresentation()]:
                continue


        # print("----------------------------------------------")
        # print("origin state:\n", s)
        # print("--------------------")
        for newState in s.GeneratePossibleNextStates():
            # print(newState, newState.totalCost)
            rep = newState.GetStringRepresentation()
            if rep in knownStates:
                if newState.totalCost >= knownStates[rep]:
                    continue
            knownStates[rep] = newState.totalCost
            openStates.append(newState)
            
    return shortestSolution

def day24a(input):
    # variable data from input
    div = []
    compareAdd = []
    stackAdd = []
    for i in range(14):
        div.append(int(input[i*18+4].split(" ")[2]))
        compareAdd.append(int(input[i*18+5].split(" ")[2]))
        stackAdd.append(int(input[i*18+15].split(" ")[2]))

    # print(div)
    # print(compareAdd)
    # print(stackAdd)

    matchingIndices = {}
    indexStack = []
    for i in range(len(div)):
        if div[i] == 1:
            indexStack.append(i)
        else:
            matchingIndices[indexStack.pop()] = i
    # print(matchingIndices)

    bestValidDigits = {}

    for push, pop in matchingIndices.items():
        pair =  hf.FindBestPair(compareAdd[pop], stackAdd[push], range(9, 1, -1))
        bestValidDigits[push] = pair[0]
        bestValidDigits[pop] = pair[1]

    best = ""
    for i in range(14):
        best += str(bestValidDigits[i])
    
    return best

def day24b(input):
    # variable data from input
    div = []
    compareAdd = []
    stackAdd = []
    for i in range(14):
        div.append(int(input[i*18+4].split(" ")[2]))
        compareAdd.append(int(input[i*18+5].split(" ")[2]))
        stackAdd.append(int(input[i*18+15].split(" ")[2]))

    matchingIndices = {}
    indexStack = []
    for i in range(len(div)):
        if div[i] == 1:
            indexStack.append(i)
        else:
            matchingIndices[indexStack.pop()] = i

    bestValidDigits = {}

    for push, pop in matchingIndices.items():
        pair =  hf.FindBestPair(compareAdd[pop], stackAdd[push], range(1, 9))
        bestValidDigits[push] = pair[0]
        bestValidDigits[pop] = pair[1]

    best = ""
    for i in range(14):
        best += str(bestValidDigits[i])
    
    return best

def day25a(input):
    east = set()
    south = set()
    height = len(input)
    width = len(input[0])
    for y in range(height):
        for x in range(width):
            c = input[y][x]
            if c == "v":
                south.add((x, y))
            elif c == ">":
                east.add((x, y))
    
    numSteps = 0
    while True:
        numSteps += 1
        # hf.PrintSeaCucumbers(east, south, width, height)
        result = hf.CalculateStep(east, south, width, height)
        # hf.PrintSeaCucumbers(result[1], result[2], width, height)

        east = result[1]
        south = result[2]
        if result[0] == 0:
            break

    return numSteps

def day25b(input):
    return "Merry Christmas!"