import collections

# Day 3
def FindMostCommonBitForPosition(input = [], pos = 0):
    bits = []
    for line in input:
        bits.append(line[pos])
    
    c = collections.Counter(bits)
    # print(c)
    if c['1'] >= c['0']:
        return '1'
    else:
        return '0'

def FilterList(bit, input = [], pos = 0):
    out = []
    for line in input:
        if line[pos] == bit:
            out.append(line)

    return out

# Day 5
def GetStraightLines(x1, x2, y1, y2):
    points = []
        
    if x1 == x2:
        if y1 < y2:
            endpoints = list(range(y1, y2)) + [y2]
        else:
            endpoints  = list(range(y1, y2, -1)) + [y2]

        for i in endpoints:
            points.append((x1, i))
    if y1 == y2:
        if x1 < x2:
            endpoints = list(range(x1, x2)) + [x2]
        else:
            endpoints = list(range(x1, x2, -1)) + [x2]
            
        for i in endpoints:
            points.append((i, y1))
    return points

def GetDiagonalLines(x1, x2, y1, y2):
    points = []
    if x1 == x2 or y1 == y2:
        return points
    
    stepX = 1
    stepY = 1
    if x1 > x2:
        stepX = -1
    if y1 > y2:
        stepY = -1
    
    y = y1
    for x in range(x1, x2, stepX):
        points.append((x, y))
        y += stepY
    points.append((x2, y2))
    return points
    
# Day 6
def SimulateFish(input, numDays, defaultTime, newTime):

    fish = {}
    for i in range(newTime):
        fish[i] = 0
    
    for x in input:
        fish[x] += 1
        
    for i in range(numDays):
        oldFish = fish.copy()
        for j in range(newTime - 1):
            fish[j] = oldFish[j+1]
        fish[newTime - 1] = oldFish[0]
        fish[defaultTime - 1] += oldFish[0]
        # print(fish)
    sum = 0
    for f in fish:
        sum += fish[f]

    return sum

# Day 8
def SolveDigitMapping(patterns = []):
    mapping = {}
    
    patterns.sort(key = len)
    
    mapping[1] = patterns[0]
    mapping[4] =  patterns[2]
    mapping[7] = patterns[1]
    mapping[8] = patterns[9]

    candidates069 = [patterns[6], patterns[7], patterns[8]]
    
    for c in candidates069:
        if all(x in c for x in mapping[4]):
            mapping[9] = c
            candidates069.remove(c)
            break
    if all(x in candidates069[0] for x in mapping[1]):
        mapping[0] = candidates069[0]
        mapping[6] = candidates069[1]
    else:
        mapping[0] = candidates069[1]
        mapping[6] = candidates069[0]

    candidates235 = [patterns[3], patterns[4], patterns[5]]
    for c in candidates235:
        if all(x in c for x in mapping[7]):
            mapping[3] = c
            candidates235.remove(c)
            break
    if all(x in mapping[6] for x in candidates235[0]):
        mapping[5] = candidates235[0]
        mapping[2] = candidates235[1]
    else:
        mapping[5] = candidates235[1]
        mapping[2] = candidates235[0]

    out = {}
    
    for m in mapping:
        out[mapping[m]] = m

    return out

def DecodeDigits(digits = [], mapping = {}):

    # print(digits)
    # print(mapping)
    num = ""
    for d in digits:
        for m in mapping:
            if all(c in m for c in d) and all(c in d for c in m):
                num += str(mapping[m])
                # print(digits, d, m)
                break
    # print(num)

    return int(num)

# Day 9
def CalculateRiskLevel(heightmap = [], x = 0, y = 0):
    height = heightmap[y][x]
    # print(height)
    if y >= 1:
        if heightmap[y-1][x] <= height:
            return 0
    if x >= 1:
        if heightmap[y][x-1] <= height:
            return 0
    if x + 1 < len(heightmap[0]):
        if heightmap[y][x+1] <= height:
            return 0
    if y + 1 < len(heightmap):
        if heightmap[y+1][x] <= height:
            return 0

    # print("detected low point at: ", x, y)
    return height + 1

def RecursiveGetBasinSize(heightmap = [], x = 0, y = 0, checked = []):
    height = heightmap[y][x]
    if height == 9:
        return 0

    if((x, y) in checked):
        return 0
    else:
        checked.append((x, y))

    size = 1
    if y >= 1:
        if heightmap[y-1][x] > height:
            size += RecursiveGetBasinSize(heightmap, x, y-1, checked)
    if x >= 1:
        if heightmap[y][x-1] > height:
            size += RecursiveGetBasinSize(heightmap, x-1, y, checked)
    if x + 1 < len(heightmap[0]):
        if heightmap[y][x+1] > height:
            size += RecursiveGetBasinSize(heightmap, x+1, y, checked)
    if y + 1 < len(heightmap):
        if heightmap[y+1][x] > height:
            size += RecursiveGetBasinSize(heightmap, x, y+1, checked)

    # print("basinsize for ", x, y, "is", size)
    return size

# Day 10
def FindFirstIllegalCharacter(line):
    chunkstack = []
    length = 0
    for c in line:
        # print(chunkstack)
        if c == '(':
            chunkstack.append(0)
            length += 1
        if c == '[':
            chunkstack.append(1)
            length += 1
        if c == '{':
            chunkstack.append(2)
            length += 1
        if c == '<':
            chunkstack.append(3)
            length += 1
        if c == ')':
            if length == 0 or chunkstack[length-1] != 0:
                return ')'
            else:
                chunkstack.pop()
                length -= 1
        if c == ']':
            if length == 0 or chunkstack[length-1] != 1:
                return ']'
            else:
                chunkstack.pop()
                length -= 1        
        if c == '}':
            if length == 0 or chunkstack[length-1] != 2:
                return '}'
            else:
                chunkstack.pop()
                length -= 1
        if c == '>':
            if length == 0 or chunkstack[length-1] != 3:
                return '>'
            else:
                chunkstack.pop()
                length -= 1
    return chunkstack

def GetAutocompleteScore(stack = []):
    score = 0
    while stack:
        score *= 5
        score += stack.pop() + 1
        
    return score

# Day 11
def SimulateStep(OctopusGrid = []):
    flashed = []
    flashNeighbours = []
    width = len(OctopusGrid[0])
    height = len(OctopusGrid)

    for y in range(height):
        for x in range(width):
            value = OctopusGrid[y][x] + 1
            OctopusGrid[y][x] = value
            if value > 9:
                flashed.append((x, y))
                flashNeighbours += GetNeighbours(x, y, width, height)

    flashNeighbours.sort()
    for n in flashNeighbours:
        x = n[0]
        y = n[1]
        OctopusGrid[y][x] += 1
        if n in flashed:
            continue
        elif OctopusGrid[y][x] > 9:
            flashed.append((x, y))
            flashNeighbours += GetNeighbours(x, y, width, height)

    for f in flashed:
        OctopusGrid[f[1]][f[0]] = 0

    return len(flashed)

def GetNeighbours(x, y, width, height, bDiagonal = True):
    neighbours = []
    topEdge = y == 0
    bottomEdge = y == height - 1
    leftEdge = x == 0
    rightEdge = x == width - 1

    if not topEdge:
        neighbours.append((x, y-1))
        if not leftEdge and bDiagonal:
            neighbours.append((x-1, y-1))
        if not rightEdge and bDiagonal:
            neighbours.append((x+1, y-1))
    if not leftEdge:
        neighbours.append((x-1, y))
    if not rightEdge:
        neighbours.append((x+1, y))
    if not bottomEdge:
        neighbours.append((x, y+1))
        if not leftEdge and bDiagonal:
            neighbours.append((x-1, y+1))
        if not rightEdge and bDiagonal:
            neighbours.append((x+1, y+1))
    
    return neighbours

# Day 12
def MapGraph(connections = []):
    graph = {}
    for c in connections:
        left = c.split('-')[0]
        right = c.split('-')[1]
        if left in graph:
            graph[left].append(right)
        else:
            graph[left] = [right]
        if right in graph:
            graph[right].append(left)
        else:
            graph[right] = [left]
    
    return graph

def RecFindPaths(graph, current, visited = [], smallCaveEnteredTwice = True):
    paths = 0

    if current == "end":
        return 1

    visited.append(current)
    
    for neighbour in graph[current]:
        if neighbour not in visited or neighbour.isupper():
            paths += RecFindPaths(graph, neighbour, visited.copy(), smallCaveEnteredTwice)
        elif not smallCaveEnteredTwice and neighbour != "start" and neighbour != "end":
            paths += RecFindPaths(graph, neighbour, visited.copy(), True)

    return paths

# Day 13
def FoldPaper(dots, foldInstruction):
    newDots = []
    bVertical = foldInstruction.startswith("y")
    foldLine = foldInstruction.split('=')[1]
    foldLine = int(foldLine)
    
    for d in dots:
        x = d[0]
        y = d[1]
        if bVertical:
            if y < foldLine:
                newDots.append(d)
            else:
                newDots.append((x, foldLine*2-y))
        else:
            if x < foldLine:
                newDots.append(d)
            else:
                newDots.append((foldLine*2-x, y))

    return list(dict.fromkeys(newDots))

# Day 14
def Polymerize(template = "", rules = {}):
    polymer = template[0]

    for i in range(1, len(template)):
        pair = template[i-1] + template[i]
        if pair in rules:
            polymer += rules[pair]
        polymer += template[i]

    return polymer

def PolymerizeEfficient(template = "", rules = {}, numSteps = 0):
    emptyDict = {r:0 for r in rules}
    counts = emptyDict.copy()

    for i in range(1, len(template)):
        pair = template[i-1]+template[i]
        counts[pair] += 1
    
    for i in range(numSteps):
        newCounts = emptyDict.copy()
        for pair in counts:
            for r in rules[pair]:
                newCounts[r] += counts[pair]
        counts = newCounts
        
    return counts

# Day 15
def GetShortestPath(risklevels):
    totalrisks = {}
    length = len(risklevels)
    x = 0
    y = 0
    totalrisks[(0, 0)] = 0

    openNeighbours = []

    while(True):
        currentRisk = totalrisks[(x, y)]
        for n in GetNeighbours(x, y, length, length, False):
            if n not in totalrisks or totalrisks[n] > currentRisk + risklevels[n[1]][n[0]]:
                totalrisks[n] = currentRisk + risklevels[n[1]][n[0]]
                openNeighbours.append(n)
        
        if len(openNeighbours) > 0:
            new = openNeighbours.pop(0)
            x = new[0]
            y = new[1]
        else:
            return totalrisks[(length-1, length-1)]

# Day 16
def HexToBits(input):
    out = ""
    for c in input:
        out += format(int(c, base=16), '04b')
    return out

def ResolvePacket(packet):
    v = packet[0:3]
    t = packet[3:6]

    versionSum = int(v, base=2)
    
    if t == "100":
        # literal value
        value = ""
        prefixPos = 6
        while packet[prefixPos] != "0":
            value += packet[prefixPos+1:prefixPos+5]
            prefixPos += 5        
        value += packet[prefixPos+1:prefixPos+5]
        
        return [versionSum, prefixPos+5, int(value, base=2)]
    else:
        lengthID = packet[6]
        if lengthID == "0":
            totalLength = int(packet[7:22], base=2)
            #split subpackets
            subpackets = packet[22:22+totalLength]
            values = []
            while len(subpackets) > 0:
                sub = ResolvePacket(subpackets)
                versionSum += sub[0]
                values.append(sub[2])
                subpackets = subpackets[sub[1]:]
                
            return [versionSum, totalLength+22, ResolveOperatorPacketValue(t, values)]
        else:
            numPackets = int(packet[7:18], base=2)
            # split packets
            subpacketlengths = 0
            values =  []
            for i in range(numPackets):
                sub = ResolvePacket(packet[18+subpacketlengths:])
                versionSum += sub[0]
                values.append(sub[2])
                subpacketlengths += sub[1]

            return [versionSum, subpacketlengths+18, ResolveOperatorPacketValue(t,values)]

def ResolveOperatorPacketValue(type = "", values = []):
    out = 0
    if type == "000":
        #0: sum
        out = sum(values)

    if type == "001":
        #1: product
        out = 1
        for v in values:
            out *= v

    if type == "010":
        #2: minimum
        out = min(values)

    if type == "011":
        #3: maximum
        out = max(values)

    if type == "101":
        #5: greater than
        if values[0] > values[1]:
            out = 1
        else:
            out = 0

    if type == "110":
        #6: less than
        if values[0] < values[1]:
            out = 1
        else:
            out = 0

    if type == "111":
        #7: equal
        if values[0] == values[1]:
            out = 1
        else:
            out = 0

    # print(type, values, "-->", out)
    return out

# Day 17
def FindMinVelocityX(targetX = ()):
    for i in range(targetX[1]):
        # print("testing x velocity of", i)
        currentVel = i
        currentPos = 0
        while currentVel > 0:
            currentPos += currentVel
            currentVel -= 1
            # print("step complete", currentPos, currentVel)
        if currentPos >= targetX[0] and currentPos <= targetX[1]:
            return i

def FindMaxVelocityY(targetY = ()):
    validVelocities = []
    for i in range(1000):
        currentVel = i
        currentPos = 0
        while currentPos >= targetY[0]:
            if currentPos <= targetY[1]:
                validVelocities.append(i)
            currentPos += currentVel
            currentVel -= 1

    return validVelocities[-1]

def TestVelocity(vel = (), targetX = (), targetY = ()):
    currentPos = (0, 0)
    currentVel = vel

    step = 0
    maxHeight = 0
    bValid = False
    while currentPos[0] <= targetX[1] and currentPos[1] >= targetY[0]:
        # print(currentPos)
        if currentPos[0] >= targetX[0] and currentPos[0] <= targetX[1] and currentPos[1] >= targetY[0] and currentPos[1] <= targetY[1]:
            bValid = True
        step += 1
        currentPos = (currentPos[0]+currentVel[0], currentPos[1]+currentVel[1])
        maxHeight = max(maxHeight, currentPos[1])
        currentVel = (max(0, currentVel[0]-1), currentVel[1]-1)

    return bValid, maxHeight

# Day 18
from ast import literal_eval as make_tuple
def DecodeSnailfishNumber(line = ""):    
    n = make_tuple(line)    
    return n

# Day 19
def FindAndMergeScanners(scanners):
    out = scanners.copy()
    for s1 in scanners:
        for s2 in scanners:
            if s1 == s2:
                continue
            if s1.TryMerge(s2):                
                # ind1 = scanners.index(s1)
                # ind2 = scanners.index(s2)
                # print(f"merged scanners at index {ind1} and {ind2}")
                out.remove(s2)
                return out

# Day 20
def EnhanceImage(image = {}, alg = "", bTreatAnknownAsLit = False):
    out =  {}
    candidates = set()
    neighbourOffsets = [(x, y) for y in range(-1, 2) for x in range(-1, 2)]
    
    for i in image:
        for n in neighbourOffsets:
            candidates.add((i[0]+n[0], i[1]+n[1]))

    for c in candidates:
        binString = ""
        for n in neighbourOffsets:
            p = (n[0]+c[0], n[1]+c[1])
            if p in image:
                binString += str(image[p])
            else:
                if bTreatAnknownAsLit:
                    binString += "1"
                else:
                    binString += "0"
        # print(c, binString)
        index = int(binString, 2)
        if alg[index] == "#":
            out[c] = "1"
        else:
            out[c] = "0"        

    return out

def PrintImage(image = [], width = (-5, 10), height = (-5, 10)):    
    for y in range(height[0], height[1]):
        outline = ""
        for x in range(width[0], width[1]):
            if (x, y) in image:
                # outline += image[(x, y)]
                if image[(x, y)] == "1":
                    outline += "#"
                else:
                    outline += "."
            else:
                outline += "-"
        print(outline)

# Day 21:
def GenerateOutcomes(pos, score):
    outcomes = {}
    outcomeNumbers = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}

    for i in range(3, 10):
        newPos = (pos + i) % 10
        newScore = score + newPos + 1
        outcomes[(newPos, newScore)] = outcomeNumbers[i]

    return outcomes

def GenerateNewUniverses(universes, player):
    newUniverses = {}
    numWins = 0

    for u in universes:
        if player == 1:
            outcomes = GenerateOutcomes(u[0], u[1])
        else:
            outcomes = GenerateOutcomes(u[2], u[3])
        currentNum = universes[u]

        for o in outcomes:
            if o[1] >= 21:
                numWins += outcomes[o] * currentNum
            else:
                if player == 1:
                    newKey = (o[0], o[1], u[2], u[3])
                else:
                    newKey = (u[0], u[1], o[0], o[1])

                if newKey not in newUniverses:
                    newUniverses[newKey] = outcomes[o] * currentNum
                else:
                    newUniverses[newKey] += outcomes[o] * currentNum

    return newUniverses, numWins

# Day 22:
def GenerateCuboidCoordinates(coordinates, minValue, maxValue):
    sanitizedCoords = [max(min(x, maxValue), minValue) for x in coordinates]
    for i in range(len(coordinates)):
        c = coordinates[i]
        if i % 2 == 0:
            if c > maxValue:
                return []
        else:
            if c < minValue:
                return []
    
    # print("sanitized:", sanitizedCoords)
    out = [(x, y, z) for x in range(sanitizedCoords[0], sanitizedCoords[1]+1) for y in range(sanitizedCoords[2], sanitizedCoords[3]+1) for z in range(sanitizedCoords[4], sanitizedCoords[5]+1)]
    return out

# Day 24:
def FindBestPair(compareAdd, stackAdd, testRange):
    for i in testRange:
        stackValue = i + stackAdd
        for j in testRange:
            if j == stackValue + compareAdd:
                return i, j

# Day 25:
def CalculateStep(east, south, width, height):
    newEast = set()
    newSouth = set()
    numMoves = 0

    for x, y in east:
        newPos = ((x + 1) % width, y)
        if newPos in east or newPos in south:
            newEast.add((x, y))
        else:
            newEast.add(newPos)
            numMoves += 1
    for x, y in south:
        newPos = (x, (y+1) % height)
        if newPos in newEast or newPos in south:
            newSouth.add((x, y))
        else:
            newSouth.add(newPos)
            numMoves += 1

    return numMoves, newEast, newSouth

def PrintSeaCucumbers(east, south, width, height):
    for y in range(height):
        line = ""
        for x in range(width):
            if (x, y) in east:
                line += ">"
            elif (x, y) in south:
                line += "v"
            else:
                line += "."
        print(line)
    

