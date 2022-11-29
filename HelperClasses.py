from collections import Counter
from math import floor
from math import ceil
from typing import Sequence
# Day 4
class BingoBoard:
    board = []
    markedTiles = []
    winningCombinations = [
        [0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19], [20, 21, 22, 23, 24], 
        [0, 5, 10, 15, 20], [1, 6, 11, 16, 21], [2, 7, 12, 17, 22], [3, 8, 13, 18, 23], [4, 9, 14, 19, 24]
    ]

    def __init__(self, input = ""):
        self.board = []
        self.markedTiles = []
        split = input.replace("  ", " ").lstrip().split(" ")
        for i in split:
            self.board.append(int(i))

    def MarkNumber(self, num = 0):
        if num in self.board:
            self.markedTiles.append(self.board.index(num))

        if self.CheckBoard():
            return True

        return False

    def CheckBoard(self):
        for w in self.winningCombinations:
            if all(elem in self.markedTiles for elem in w):
                return True
        return False

    def GetWinningScore(self, winningNumber = 0):
        sum = 0
        for i in range(0, len(self.board)):
            if i not in self.markedTiles:
                sum += self.board[i]

        return winningNumber * sum

# Day 18
class SnailFishNumber:

    parent = None
    bIsRealNumber = False
    leftChild = None
    rightChild = None
    value = 0

    def __init__(self, NumAsTuple = (), Parent = None, leftChild = None, rightChild = None):
        self.parent = Parent
        
        if leftChild != None and rightChild != None:
            self.leftChild = leftChild
            leftChild.parent = self
            self.rightChild = rightChild
            rightChild.parent = self
            self.bIsRealNumber = False
        else:
            self.parent = Parent
            self.bIsRealNumber = type(NumAsTuple) != list
            # print(NumAsTuple, self.bIsRealNumber)
            if self.bIsRealNumber:
                self.value = NumAsTuple
            else:
                self.leftChild = SnailFishNumber(NumAsTuple[0], self)
                self.rightChild = SnailFishNumber(NumAsTuple[1], self)

    def GetMagnitude(self):
        if self.bIsRealNumber:
            return self.value
        else:
            return self.leftChild.GetMagnitude() * 3 + self.rightChild.GetMagnitude() * 2

    def Reduce(self):
        # print("reduce", self)
        while True:
            if self.FindExplodingPair(0):
                continue
            elif self.FindSplit():
                continue
            else:
                # No more reduction -> finished
                return self

    def FindSplit(self):
        if self.bIsRealNumber:
            if self.value >= 10:
                self.bIsRealNumber = False
                self.leftChild = SnailFishNumber(floor(self.value / 2), self)
                self.rightChild = SnailFishNumber(ceil(self.value / 2), self)
                return True
            else:
                return False
        else:
            if self.leftChild.FindSplit():
                return True
            else:
                return self.rightChild.FindSplit()

    def FindExplodingPair(self, Depth = 0):
        if self.bIsRealNumber:
            return False
        else:
            if Depth == 4 and not self.bIsRealNumber:
                # actual exploding
                self.parent.AddToLeftSideUpwards(self, self.leftChild.value)
                self.parent.AddToRightSideUpwards(self, self.rightChild.value)
                self.bIsRealNumber = True
                self.leftChild = None
                self.rightChild = None
                self.value = 0
                return True

            if self.leftChild.FindExplodingPair(Depth + 1):
                return True
            else:
                return self.rightChild.FindExplodingPair(Depth + 1)
        pass

    def AddToLeftSideUpwards(self, callingChild, value):
        if callingChild == self.rightChild:
            self.leftChild.AddToLeftSideDownwards(value)
        else:
            if self.parent != None:
                self.parent.AddToLeftSideUpwards(self, value)

    def AddToLeftSideDownwards(self, value):
        if self.bIsRealNumber:
            self.value += value
        else:
            self.rightChild.AddToLeftSideDownwards(value)

    def AddToRightSideUpwards(self, callingCHild, value):
        if callingCHild == self.leftChild:
            self.rightChild.AddToRightSideDownwards(value)
        else:
            if self.parent != None:
                self.parent.AddToRightSideUpwards(self, value)

    def AddToRightSideDownwards(self, value):
        if self.bIsRealNumber:
            self.value += value
        else:
            self.leftChild.AddToRightSideDownwards(value)

    def __str__(self) -> str:
        if self.bIsRealNumber:
            return str(self.value)
        else:
            return "[" + str(self.leftChild) + ", " + str(self.rightChild) + "]"

# Day 19
class Scanner:

    beacons = []
    eulerDistances = {} # indices mapped to squared distance

    def __init__(self, beacons = []) -> None:
        self.beacons = []
        self.eulerDistances = {}
        for b in beacons:
            self.AddBeacon(b)
            
        pass
    

    def AddBeacon(self, beacon):
        for i in range(len(self.beacons)):
            self.eulerDistances[(i, len(self.beacons))] = self.SqEuler(self.beacons[i], beacon)
        self.beacons.append(beacon)


    def SqEuler(self, a, b):
        return pow(b[0]-a[0], 2) + pow(b[1]-a[1], 2) + pow(b[2]-a[2], 2)

    def TryMerge(self, other):        
        matchingBeacons = {}
        matchingDistances = []

        # TODO: rewrite matching more efficiently. create distance sets -> union -> search for specific distances only (maybe reverse distance map)
        for d in self.eulerDistances:
            for d2 in other.eulerDistances:
                if self.eulerDistances[d] == other.eulerDistances[d2]:
                    matchingDistances.append(d)
                    for i in d:
                        if i in matchingBeacons:
                            matchingBeacons[i] += d2
                            # print(d, d2)
                        else:
                            matchingBeacons[i] = list(d2)
                            # print(d, d2)

        matchingBeacons = {k:max(set(matchingBeacons[k]), key=matchingBeacons[k].count) for k in matchingBeacons}
        if len(matchingBeacons) < 12:
            # no explicit match, can't merge
            return False
        else:
            print(matchingBeacons)

        # print(matchingBeacons)
        # print(matchingDistances)

        for i in range(len(matchingDistances)):            
            start = matchingDistances[i][0]
            end = matchingDistances[i][1]
            startSelf = self.beacons[start]
            endSelf = self.beacons[end]
            vectorSelf = (endSelf[0] - startSelf[0], endSelf[1] - startSelf[1], endSelf[2] - startSelf[2])
            startOther = other.beacons[matchingBeacons[start]]
            endOther = other.beacons[matchingBeacons[end]]
            vectorOther = (endOther[0] - startOther[0], endOther[1] - startOther[1], endOther[2] - startOther[2])

            if self.ValidateAlignmentVector(vectorSelf) and self.ValidateAlignmentVector(vectorOther): # TODO: check why there are duplicate mappings
                break
        
        

        # print(startSelf, endSelf, startOther, endOther, vectorSelf, vectorOther)
        rotationSolver = self.ResolveRotation(vectorSelf, vectorOther)
        translationVector = self.GetTranslationVector(startSelf, rotationSolver(startOther))
        # print("translationVector:", translationVector)
        # print(rotationSolver((1, 2, 4)))

        # Add all non-matching beacons from other to this scanners known beacons
        for unkownBeacon in [other.beacons[x] for x in range(len(other.beacons)) if x not in matchingBeacons.values()]:
            rotated = rotationSolver(unkownBeacon)
            self.AddBeacon(self.AddVector(rotationSolver(unkownBeacon), translationVector))
        
        return True

    def ValidateAlignmentVector(self, vector):
        # also invalidate e.g. (-1, 0, 1)
        return len(set(vector)) == 3

    # resolves rotation between two vectors so applying rotation to origin vector will result in target vector
    def ResolveRotation(self, target, origin):
        print("resolving rotation for vectors", target, origin)
        solvers = [
            lambda o : (o[0], o[1], o[2]),
            lambda o : (o[0], o[2] * -1, o[1]),
            lambda o : (o[0], o[1] * -1, o[2] * -1),
            lambda o : (o[0], o[2], o[1] * -1),
            lambda o : (o[0] * -1, o[1] * -1, o[2]),
            lambda o : (o[0] * -1, o[2], o[1]),
            lambda o : (o[0] * -1, o[1], o[2] * -1),
            lambda o : (o[0] * -1, o[2] * -1, o[1] * -1),
            lambda o : (o[1], o[0], o[2] * -1),
            lambda o : (o[2] * -1, o[0], o[1] * -1),
            lambda o : (o[1] * -1, o[0], o[2]),
            lambda o : (o[2], o[0], o[1]),
            lambda o : (o[1], o[0] * -1, o[2]),
            lambda o : (o[2], o[0] * -1, o[1] * -1),
            lambda o : (o[1] * -1, o[0] * -1, o[2] * -1),
            lambda o : (o[2] * -1, o[0] * -1, o[1]),
            lambda o : (o[1], o[2], o[0]),
            lambda o : (o[2] * -1, o[1], o[0]),
            lambda o : (o[1] * -1, o[2] * -1, o[0]),
            lambda o : (o[2], o[1] * -1, o[0]),
            lambda o : (o[1] * -1, o[2], o[0] * -1),
            lambda o : (o[2] * -1, o[1] * -1, o[0] * -1),
            lambda o : (o[1], o[2] * -1, o[0] * -1),
            lambda o : (o[2], o[1], o[0] * -1)
        ]
        # possible alternative: use 3 lambdas for 90 deg rotations around x, y, z

        workingSolvers = []
        for s in solvers:
            if s(origin) == target:
                workingSolvers.append(s)
        
        if len(workingSolvers) > 1:
            print("Number of working solvers:", len(workingSolvers), "for", origin, "->", target)
                
        return workingSolvers[0]
        
    def GetTranslationVector(self, target, origin):
        return (target[0] - origin[0], target[1] - origin[1], target[2] - origin[2])

    def AddVector(self, target, offset):
        return (target[0] + offset[0], target[1] + offset[1], target[2] + offset[2])

    def PermutateOffsets(self, x, y, z):
        out = []
        out.add((x, y, z))
        out.add((x, z, -y))
        out.add((x, -y, -z))
        out.add((x, -z, y))
        
        print(out)

    def Print(self):
        pass

# Day 22
class Cuboid:

    
    def __init__(self, minX, maxX, minY, maxY, minZ, maxZ) -> None:
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY
        self.minZ = minZ
        self.maxZ = maxZ

        pass

    def Overlaps(self, other) -> bool:
        if self.maxX < other.minX or self.minX > other.maxX:
            return False
        if self.maxY < other.minY or self.minY > other.maxY:
            return False
        if self.maxZ < other.minZ or self.minZ > other.maxZ:
            return False
        return True

    def GetVolume(self) -> int:
        # print(self.minX, self.maxX, self.minY, self.maxY, self.minZ, self.maxZ)
        return (self.maxX - self.minX + 1) * (self.maxY - self.minY + 1) * (self.maxZ - self.minZ + 1)

    def Cut(self, other):
        cuts = []
        # +X
        if self.maxX > other.maxX:
            cuts.append(Cuboid(other.maxX + 1, self.maxX, self.minY, self.maxY, self.minZ, self.maxZ))
        # -X
        if self.minX < other.minX:
            cuts.append(Cuboid(self.minX, other.minX - 1, self.minY, self.maxY, self.minZ, self.maxZ))
        # +Y
        if self.maxY > other.maxY:
            cuts.append(Cuboid(max(self.minX, other.minX), min(self.maxX, other.maxX), other.maxY + 1, self.maxY, self.minZ, self.maxZ))
        # -Y
        if self.minY < other.minY:
            cuts.append(Cuboid(max(self.minX, other.minX), min(self.maxX, other.maxX), self.minY, other.minY - 1, self.minZ, self.maxZ))
        # +Z
        if self.maxZ > other.maxZ:
            cuts.append(Cuboid(max(self.minX, other.minX), min(self.maxX, other.maxX), max(self.minY, other.minY), min(self.maxY, other.maxY), other.maxZ + 1, self.maxZ))
        # -Z
        if self.minZ < other.minZ:
            cuts.append(Cuboid(max(self.minX, other.minX), min(self.maxX, other.maxX), max(self.minY, other.minY), min(self.maxY, other.maxY), self.minZ, other.minZ - 1))

        # print("cuts:")
        # for c in cuts:
        #     print(c)
        return cuts

    def __str__(self) -> str:
        return f'X: {self.minX} -> {self.maxX} Y: {self.minY} -> {self.maxY} Z: {self.minZ} -> {self.maxZ}'

# Day 23
class GameState:
    roomA = []
    roomB = []
    roomC = []
    roomD = []
    hallway = {}
    totalCost = 0
    roomDepth = 4
    hallwayPositions = [0, 1, 3, 5, 7, 9, 10]

    def __init__(self, rooms, hallway, totalMoveCost = 0, roomDepth = 4) -> None:
        self.roomA = rooms[0]
        self.roomB = rooms[1]
        self.roomC = rooms[2]
        self.roomD = rooms[3]
        self.hallway = hallway
        self.totalCost =  totalMoveCost
        self.roomDepth = roomDepth
        pass

    def GeneratePossibleNextStates(self):
        nextStates = []

        # possible moves: 
        # - move into room if room is "clean"
        # - move last entry from any room to hallway

        # move from hallway into room
        for pos, id in self.hallway.items():
            if self.CanMoveToRoom(id):
                room = self.GetRoomForId(id)
                if self.CanMoveThroughHallway(pos, id):
                    stepCost = self.GetHallwaySteps(pos, id) + self.GetStepsInRoom(room, True)
                    stepCost *= self.GetStepCostForId(id)
                    newRooms = [self.roomA.copy(), self.roomB.copy(), self.roomC.copy(), self.roomD.copy()]
                    for r in newRooms:
                        if r == room:
                            r.append(id)
                    newHallway = self.hallway.copy()
                    newHallway.pop(pos)

                    nextStates.append(GameState(newRooms, newHallway, self.totalCost + stepCost, self.roomDepth))
        for pos in self.hallwayPositions:
            if pos in self.hallway:
                continue
            if self.CanMoveFromRoom("A"):
                if self.CanMoveThroughHallway(pos, "A"):
                    id = self.roomA[-1]
                    stepCost = self.GetHallwaySteps(pos, "A") + self.GetStepsInRoom(self.roomA, False)
                    stepCost *= self.GetStepCostForId(id)
                    newRooms = [self.roomA.copy(), self.roomB.copy(), self.roomC.copy(), self.roomD.copy()]
                    newRooms[0].pop()
                    newHallway = self.hallway.copy()
                    newHallway[pos] = id

                    nextStates.append(GameState(newRooms, newHallway, self.totalCost + stepCost, self.roomDepth))
            if self.CanMoveFromRoom("B"):
                if self.CanMoveThroughHallway(pos, "B"):
                    id = self.roomB[-1]
                    stepCost = self.GetHallwaySteps(pos, "B") + self.GetStepsInRoom(self.roomB, False)
                    stepCost *= self.GetStepCostForId(id)
                    newRooms = [self.roomA.copy(), self.roomB.copy(), self.roomC.copy(), self.roomD.copy()]
                    newRooms[1].pop()
                    newHallway = self.hallway.copy()
                    newHallway[pos] = id

                    nextStates.append(GameState(newRooms, newHallway, self.totalCost + stepCost, self.roomDepth))
            if self.CanMoveFromRoom("C"):
                if self.CanMoveThroughHallway(pos, "C"):
                    id = self.roomC[-1]
                    stepCost = self.GetHallwaySteps(pos, "C") + self.GetStepsInRoom(self.roomC, False)
                    stepCost *= self.GetStepCostForId(id)
                    newRooms = [self.roomA.copy(), self.roomB.copy(), self.roomC.copy(), self.roomD.copy()]
                    newRooms[2].pop()
                    newHallway = self.hallway.copy()
                    newHallway[pos] = id

                    nextStates.append(GameState(newRooms, newHallway, self.totalCost + stepCost, self.roomDepth))
            if self.CanMoveFromRoom("D"):
                if self.CanMoveThroughHallway(pos, "D"):
                    id = self.roomD[-1]
                    stepCost = self.GetHallwaySteps(pos, "D") + self.GetStepsInRoom(self.roomD, False)
                    stepCost *= self.GetStepCostForId(id)
                    newRooms = [self.roomA.copy(), self.roomB.copy(), self.roomC.copy(), self.roomD.copy()]
                    newRooms[3].pop()
                    newHallway = self.hallway.copy()
                    newHallway[pos] = id

                    nextStates.append(GameState(newRooms, newHallway, self.totalCost + stepCost, self.roomDepth))

        return nextStates

    def CanMoveFromRoom(self, id):
        room = self.GetRoomForId(id)
        if len(room) == 0:
            return False
        for x in room:
            if x != id:
                break
        else:
            # loop completed normally -> no wrong id in room -> nobody should need to leave this room
            return False
        return True
    
    def CanMoveToRoom(self, id):
        for x in self.GetRoomForId(id):
            if x != id:
                return False
        return True

    def GetRoomForId(self, id):
        if id == "A":
            return self.roomA
        if id == "B":
            return self.roomB
        if id == "C":
            return self.roomC
        if id == "D":
            return self.roomD
        print("Error, invalid id:", id)
    
    # def GetIdForRoom(self, room):
    #     if room == self.roomA:
    #         return "A"
    #     if room == self.roomB:
    #         return "B"
    #     if room == self.roomC:
    #         return "C"
    #     if room == self.roomD:
    #         return "D"
    #     print("Error, invalid room", room)

    def GetStepCostForId(self, id):
        if id == "A":
            return 1
        if id == "B":
            return 10
        if id == "C":
            return 100
        if id == "D":
            return 1000
        print("Error, invalid id:", id)

    def CanMoveThroughHallway(self, hallwayPos, room):
        startPos = self.GetHallwayPosForRoom(room)
        if startPos < hallwayPos:
            stops = range(startPos, hallwayPos)
        else:
            stops = range(startPos, hallwayPos, -1)

        for s in stops:
            if s in self.hallway:
                return False
        return True

    def GetHallwaySteps(self, hallwayPos, room):
        roomPos = self.GetHallwayPosForRoom(room)
        return abs(roomPos - hallwayPos)
    
    def GetHallwayPosForRoom(self, room):
        if room == "A":
            return 2
        if room == "B":
            return 4
        if room == "C":
            return 6
        if room == "D":
            return 8
    
    def GetStepsInRoom(self, room, bMovingIn):
        if bMovingIn:
            return self.roomDepth - len(room)
        else:
            return self.roomDepth - len(room) + 1

    def IsCompleted(self):
        if len(self.roomA) != self.roomDepth:
            return False
        if len(self.roomB) != self.roomDepth:
            return False
        if len(self.roomC) != self.roomDepth:
            return False
        if len(self.roomD) != self.roomDepth:
            return False
        for x in self.roomA:
            if x != "A":
                return False
        for x in self.roomB:
            if x != "B":
                return False
        for x in self.roomC:
            if x != "C":
                return False
        for x in self.roomD:
            if x != "D":
                return False
        return True

    def __str__(self) -> str:
        out = ""
        out += "#############\n"
        out += "#{0}{1}.{2}.{3}.{4}.{5}{6}#\n".format(self.GetHallwayChar(0), self.GetHallwayChar(1), self.GetHallwayChar(3), self.GetHallwayChar(5), self.GetHallwayChar(7), self.GetHallwayChar(9), self.GetHallwayChar(10))
        out += "  " + self.GetRoomRow(3) + "\n"
        out += "  " + self.GetRoomRow(2) + "\n"
        out += "  " + self.GetRoomRow(1) + "\n"
        out += "  " + self.GetRoomRow(0) + "\n"
        out += "  #########"
        return out

    def GetStringRepresentation(self):
        out = "{0}{1}.{2}.{3}.{4}.{5}{6}".format(self.GetHallwayChar(0), self.GetHallwayChar(1), self.GetHallwayChar(3), self.GetHallwayChar(5), self.GetHallwayChar(7), self.GetHallwayChar(9), self.GetHallwayChar(10))
        a, b, c, d = "", "", "", ""
        for x in self.roomA:
            a += x
        for x in self.roomB:
            b += x
        for x in self.roomC:
            c += x
        for x in self.roomD:
            d += x
        out += f'_{a}_{b}_{c}_{d}'
        return out

    def GetHallwayChar(self, index):
        if index in self.hallway:
            return self.hallway[index]
        else:
            return "."

    def GetRoomRow(self, row):
        out = "#"
        if len(self.roomA) > row:
            out += self.roomA[row] + "#"
        else:
            out += ".#"
        if len(self.roomB) > row:
            out += self.roomB[row] + "#"
        else:
            out += ".#"
        if len(self.roomC) > row:
            out += self.roomC[row] + "#"
        else:
            out += ".#"
        if len(self.roomD) > row:
            out += self.roomD[row] + "#"
        else:
            out += ".#"

        return out