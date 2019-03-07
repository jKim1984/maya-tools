import maya.cmds as cmds


def getSurroundingVerts(originVert):
    cmds.select(originVert)
    _surroundingEdges = cmds.polyListComponentConversion(te=True)
    cmds.select(_surroundingEdges)
    _surroundingVerts = cmds.polyListComponentConversion(tv=True)

    surroundingVertList = []
    for vert in _surroundingVerts:
        if vert != originVert:
            surroundingVertList.append(vert)

    return surroundingVertList


def checkEdges(originVert):
    cmds.select(originVert)
    edges = cmds.ls(cmds.polyListComponentConversion(te=True), flatten=True)
    cmds.select(edges)
    faces = cmds.ls(cmds.polyListComponentConversion(tf=True), flatten=True)

    if len(faces) < len(edges):
        return 1
    else:
        return 0


def distanceMerge(originVert, nextVert, reduction):

    shortestDist = 100
    shortestDistPoint = ''

    orgPos = cmds.xform(originVert, q=True, t=True, ws=True)
    sVertList = getSurroundingVerts(originVert)

    totalDist = []
    for vert in sVertList:
        vertPos = cmds.xform(vert, q=True, t=True, ws=True)
        newPos = (vertPos[0] - orgPos[0], vertPos[1] - orgPos[1], vertPos[2] - orgPos[2])

        diff = abs(newPos[0]) + abs(newPos[1]) + abs(newPos[2])
        totalDist.append(diff)

        if diff < shortestDist:
            shortestDist = diff
            shortestDistPoint = vert

    totalDist = sum(totalDist)
    if totalDist < reduction:
        cmds.select(shortestDistPoint)
        cmds.move(orgPos[0], orgPos[1], orgPos[2], shortestDistPoint)
        cmds.select(originVert, add=True)
        cmds.polyMergeVertex()
        cmds.select(clear=True)





class ReducePolyUI(object):
    def __init__(self):
        self.winName = 'ReducePolyUI'
        self.size = (200, 50)

        if cmds.window(self.winName, exists=True):
            cmds.deleteUI(self.winName)

    def mainWindowUI(self):
        self.mWin = cmds.window(self.winName, title='Reduce Polys', widthHeight=self.size, menuBar=True, sizeable=False)
        cmds.columnLayout(adjustableColumn=True)
        cmds.floatSliderGrp('reduceAmt', label='Reduction', field=True, min=.001, max=100)
        cmds.button(label='Reduce Poly', command=self.reducePoly)
        cmds.showWindow(self.winName)

    def reducePoly(self, *args):
        selObj = cmds.ls(sl=True)
        reduceAmt = cmds.floatSliderGrp('reduceAmt', q=True, value=True)
        numVerts = cmds.polyEvaluate(selObj, v=True)
        vertList = [selObj[0] + '.vtx[' + str(i) + ']' for i in range(numVerts)]
        for i in range(len(vertList)):
            edge = checkEdges(vertList[i])
            if edge != 1:
                distanceMerge(vertList[i], vertList[i + 1], reduceAmt)


