import maya.cmds as cmds
import random as rand



#######################################################################################
#
# Main Code Class
#
#######################################################################################

class TerrainGenerator(object):

    def __init__(self):
        pass

    # main code that raises the vertexes to the heights and creates the terrain
    # will take color info and raise the vertexes to the appropriate height
    def raiseTerrain(self, amplify, noiseValue):

        self.obj = cmds.ls(sl=True)
        mesh = self.obj
        cmds.rename(mesh, 'mainTerrain_')

        numVert = cmds.polyEvaluate(mesh, vertex=True)

        if cmds.polyColorSet(mesh, q=True, allColorSets=True) is None:
            self.addDefaultColors(mesh)

        vert = cmds.ls(mesh[0] + '.vtx[:]', flatten=True)

        mainHeight = amplify
        for i in range(len(vert)):
            value = cmds.polyColorPerVertex(vert, q=True, r=True)
            cmds.select(mesh[0] + '.vtx[' + str(i) + ']')
            cmds.move(0, value[i] * mainHeight, 0, r=True)
            cmds.select(clear=True)

        cmds.select(mesh)
        noise = noiseValue
        self.noiseValue(noise)
        cmds.select(clear=True)


    def addDivisions(self, mesh):
        cmds.polySubdivideFacet(mesh, dv=1, m=False)

    def selectByColor(self, mesh):

        vertNum = cmds.ls(mesh[0] + '.vtx[:]', flatten=True)

        colorList = [cmds.polyColorPerVertex(i, q=True, r=True) for i in vertNum]
        for i in vertNum:
            vertColor = cmds.polyColorPerVertex(i, q=True, r=True)
            colorList.append(vertColor)

        print vertNum
        print colorList

        for v in range(len(vertNum)):
            verts = mesh[0] + '.vtx[' + str(v) + ']'
            if round((cmds.polyColorPerVertex(verts, q=True, r=True)[0]), 2) == round((colorList[v][0]), 2):
                cmds.select(verts, add=True)
            if round((cmds.polyColorPerVertex(verts, q=True, r=True)[0]), 2) == 1.0:
                cmds.select(verts, deselect=True)

    def noiseValue(self, amt):

        selObj = cmds.ls(sl=True)
        verts = cmds.ls(selObj[0] + '.vtx[:]', flatten=True)

        randAmt = [0, 0, 0]
        for i in verts:
            for j in range(len(randAmt)):
                randAmt[j] = rand.random() * (amt * 2) - amt
            cmds.select(i, replace=True)
            cmds.move(randAmt[0], randAmt[1], randAmt[2], relative=True)

    # default colors when user has not added colors to the object
    # add a random color value to random vertices
    def addDefaultColors(self, mesh):

        cmds.select(mesh[0] + '.vtx[:]')
        vertexes = cmds.ls(sl=True, flatten=True)
        print vertexes
        for i in vertexes:
            colorRange = rand.uniform(0.000, 1.000)
            cmds.polyColorPerVertex(i, cdo=True, rgb=[colorRange, colorRange, colorRange])
        cmds.select(clear=True)
        cmds.select(mesh)

#######################################################################################
#
# Prop Code
#
#######################################################################################

    # Items will be listed in the UI in a window
    # selected items will be added to the points
    def addProps(self, terrain, mesh):

        randVertList = self.randomSelectVertex(terrain[0])
        cmds.select(clear=True)

        prop = mesh
        for j in randVertList:
            vertPos = cmds.xform(j, t=True, q=True, ws=True)
            cmds.duplicate(prop, rr=True)
            cmds.move(vertPos[0], vertPos[1], vertPos[2], prop)

        cmds.group(n='Prop_Grp_')

    def delProps(self):
        cmds.select()


    # select random verts for various props
    # scene will be populated to the random points when random is selected
    # this just gets the random verts. User will also be allowed to add to selected vertices
    def randomSelectVertex(self, mesh, percentage=.3):

        cmds.select(mesh)

        vertices = []

        vertNum = range(cmds.polyEvaluate(mesh, v=True))
        rand.shuffle(vertNum)
        verts = vertNum[:int(percentage * len(vertNum))]
        for i in range(len(verts)):
            verts[i] = mesh + '.vtx[' + str(verts[i]) + ']'
        vertices.extend(verts)
        cmds.select(vertices, r=True)

        return vertices


#######################################################################################
#
# Reduction
#
#######################################################################################


def polyVertAdjacent(self,vertex):

    cmds.select(vert)

    edge = cmds.polyListComponentConversion(te=True)
    cmds.select(edge)
    vertList = cmds.polyListComponentConversion(tv=True)
    cmds.select(vertList)

    cmds.ls(sl=True, flatten=True)

    verts = []
    for vert in vertList:
        if vert != vertex:
            verts.append(vert)

    return verts

def getPosition(self, origin):
    originXForm = cmds.xform(origin, q=True, t=True, ws=True)

def getVertexes(self, origin):
    # get origin average distance from the surrounding verts
    vertList = polyVertAdjacent(origin)
    lowestDiff = 181.0
    totalPos = [0, 0, 0]
    originPosition = cmds.xform(origin, q=True, t=True, ws=True)

    positionList = []
    for vert in vertList:
        vertPos = findPos()
        vertPosCheck = [(vertPos[0] - originPosition[0]), (vertPos[1] - originPosition[1]),
                        (vertPos[1] - originPosition[1])]

        totalPos[0] += vertPosCheck[0]
        totalPos[1] += vertPosCheck[1]
        totalPos[2] += vertPosCheck[2]
        difference = (abs(vertPosCheck[0]) + abs(vertPosCheck[1]) + abs(vertPosCheck[2]))

        if difference < lowestDiff:
            lowestDiff = difference
            lowestDiffPoint = vert

    totalDiff = abs(totalPos[0]) + abs(totalPos[1]) + abs(totalPos[2])

    if totalDiff < reduction:
        cmds.select(lowestDiffPoint)
        movePoint = cmds.xform(q=True, t=True, ws=True)
        cmds.move(movePoint[0], movePoint[1], movePoint[2], origin)
        cmds.select(origin, add=True)
        cmds.polyMergeVertex(d=.0001)
        cmds.select(cl=True)

def edgeChecker(self, origin):
    """
    determines if the passed vert is on an edge (contour)

    : param origin : the tested vert
    : type origin : string

    : return : 1 if on an edge, 0 otherwise
    """
    cmds.select(origin)
    edges = cmds.polyListComponentConversion(te=True)
    faces = cmds.polyListComponentConversion(tf=True)
    cmds.select(edges)
    edges = cmds.ls(sl=True, fl=True)
    cmds.select(faces)
    faces = cmds.ls(sl=True, fl=True)
    if len(edges) > len(faces):
        return 1
    else:
        return 0


def terrainReduction(self):
    """
    collector function
    """
    terrain = cmds.ls(sl=True, fl=True)
    testPoint = cmds.polyListComponentConversion(tv=True)
    cmds.select(testPoint)
    testPoint = cmds.ls(sl=True, fl=True)
    print testPoint
    cmds.progressWindow(t="Working", progress=0, isInterruptable=True)
    for i in range(len(testPoint)):
        edge = terrainWindow.edgeChecker(testPoint[i])
        if edge != 1:
            terrainWindow.vertChecker(testPoint[i], testPoint[i + 1])
    cmds.progressWindow(endProgress=True)


#######################################################################################
#
# UI Class
#
#######################################################################################

class TerrainGeneratorUI(object):
    def __init__(self):
        self.winName = 'TerrainGenerator'
        self.winSize = (500, 1000)
        self.terrainGen = TerrainGenerator()


        if cmds.window('TerrainGenerator', exists=True):
            cmds.deleteUI('TerrainGenerator')

    def mainWindow(self):
        self.rWindow = cmds.window(self.winName, title='Reference Generator', widthHeight=self.winSize, sizeable=False,
                              retain=False, menuBar=True)

        self.editMenu = cmds.menu('editMenu', label='Edit')
        cmds.menuItem(label="Save Settings", parent=self.editMenu)
        cmds.menuItem(label="Reset Settings", parent=self.editMenu)

        self.helpMenu = cmds.menu('helpMenu', label='Help')
        cmds.menuItem(label="Help on Tool", parent=self.helpMenu)

        self.mainForm = cmds.formLayout('mainForm')
        self.backFrame = cmds.scrollLayout('mainScroll', hst=16, vst=16, borderVisible=True)

        cmds.formLayout(self.mainForm, edit=True, attachForm=[(self.backFrame, 'left', 0),
                                                              (self.backFrame, 'top', 0),
                                                              (self.backFrame, 'right', 0),
                                                              (self.backFrame, 'bottom', 30)])

        self.frameForm = cmds.formLayout('secondForm', parent=self.backFrame)

        self.terrainFrame = cmds.frameLayout('Terrain', width=490, collapsable=True, parent=self.frameForm)
        self.amplitude = cmds.floatSliderGrp(label='amplitude', field=True, minValue=0.0, maxValue=10.0,
                                             fieldMinValue=0.0, fieldMaxValue=10.0, step=.5, parent=self.terrainFrame)
        self.noise = cmds.floatSliderGrp(label='Noise', field=True, minValue=0.00, maxValue=.4, step=.01, parent=self.terrainFrame)
        self.minHeight = cmds.intSliderGrp(label='Min Height', field=True, parent=self.terrainFrame)
        self.create = cmds.button('Create', parent=self.terrainFrame, command=self.createTerrain)
        self.addDivisions = cmds.button('Add Divisions', parent=self.terrainFrame, command=self.addDivision)
        self.reduce = cmds.button('Reduce Terrain', parent=self.terrainFrame)

        self.frameForm2 = cmds.formLayout('thirdForm', parent=self.backFrame)
        self.props = cmds.frameLayout('Props', width=490, collapsable=True, parent=self.frameForm2)
        self.propList = cmds.textScrollList('Prop List', parent=self.props)
        self.addBtn = cmds.button('Add', parent=self.props)
        self.removeBtn = cmds.button('Remove', parent=self.props)
        self.populateBtn = cmds.button('Populate Scene', parent=self.props, command=self.populateScene)
        cmds.formLayout('secondForm', e=True, attachForm=())

        cmds.button(self.addBtn, edit=True, command=self.addItemToList)
        cmds.button(self.removeBtn, edit=True, command=self.removeItemFromList)

        cmds.showWindow(self.rWindow)


    def getObjFromList(self):
        if (cmds.textScrollList(self.propList, q=True, selectItem=True)) is None:
            cmds.error('Nothing is Selected')
            return
        else:
            selProp = cmds.textScrollList(self.propList, q=True, selectItem=True)[0]
            return selProp

    def createTerrain(self, *args):
        noiseValue = cmds.floatSliderGrp(self.noise, q=True, value=True)
        ampFloat = cmds.floatSliderGrp(self.amplitude, q=True, value=True)
        self.terrainGen.raiseTerrain(ampFloat, noiseValue)

    def addDivision(self, *args):
        mesh = cmds.ls(sl=True)
        self.terrainGen.addDivisions(mesh[0])

    ###################
    # Scroll List Attrs
    ###################
    def getItemFromList(self, *args):
        if (cmds.textScrollList(self.propList, q=True, selectItem=True)) is None:
            cmds.error('Nothing is Selected')
            return
        else:
            selProp = cmds.textScrollList(self.propList, q=True, selectItem=True)[0]
            return selProp

    def addItemToList(self, *args):
        mesh = cmds.ls(sl=True)
        addProp = cmds.textScrollList(self.propList, e=True, append=mesh)

    def removeItemFromList(self, *args):
        mesh = self.getItemFromList()
        cmds.textScrollList(self.propList, e=True, removeItem=mesh)


    def populateScene(self, *args):
        mesh = self.getItemFromList()
        terrain = cmds.ls('mainTerrain_*')
        print terrain
        self.terrainGen.addProps(terrain, mesh)


    def delProps(self, *args):
        mesh = cmds.ls(sl=True)

