from maya import cmds

class AnimationRecorder(object):
    def __init__(self,sel=[],locators=[], locatorsSelection=[], ctrls=[]):
        self.sel = cmds.ls(selection = True)
        self.locators = locators
        self.locatorsSelection = locatorsSelection
        self.ctrls = ctrls
        self.minTime = cmds.playbackOptions(minTime=True, query=True)
        self.maxTime = cmds.playbackOptions(maxTime=True, query=True)

    def recordAnimOnLocators(self, *args):
        suffix = '_LOC'
        
        if (self.ctrls == None):
            cmds.warning('You must select something!')
        else:
            #creates locators and parent constrain it to the selected controls
            for i in range(len(self.ctrls)):
                locName = self.ctrls[i] + suffix 
                loc = cmds.spaceLocator(name= locName)
                if loc not in self.locators:
                    self.locators.append(loc)
                tempConst = cmds.parentConstraint(self.ctrls[i], loc, mo=False)
    
            #select all the created locators
            cmds.select(clear=True)
            for locator in self.locators:
                cmds.select(locator, add=True)
            self.locatorsSelection = cmds.ls(selection=True)

            #bakes all the selected locators
            cmds.bakeResults(self.locatorsSelection, simulation=False, smart=True, sparseAnimCurveBake=True, time=(self.minTime, self.maxTime))
            #deletes selected locators' temp constraints
            cmds.delete(constraints=True)


    def transferAnimFromLocators(self, *args):
        if(len(self.ctrls)>0):
            #parent constraint controls to locators
            for i in range(len(self.locators)):
                if((cmds.getAttr((self.ctrls[i]+".rotateX"), lock=True))==False and (cmds.getAttr((self.ctrls[i]+".translateX"), lock=True))==False ):
                    cmds.parentConstraint(self.locators[i], self.ctrls[i], mo=False)
                elif((cmds.getAttr((self.ctrls[i]+".translateX"), lock=True))):
                    cmds.parentConstraint(self.locators[i], self.ctrls[i], mo=False, skipTranslate=["x","y","z"])
                elif((cmds.getAttr((self.ctrls[i]+".rotateX"), lock=True))):
                    cmds.parentConstraint(self.locators[i], self.ctrls[i], mo=False, skipRotate = ["x","y","z"])
            
            #bakes animation into controls and deletes constraints
            cmds.bakeResults(self.ctrls, simulation=False, smart=True, sparseAnimCurveBake=True, time=(self.minTime, self.maxTime))
            #deletes locators and temp constraints
            cmds.delete(self.locatorsSelection)

            #applying Euler filter to all the controls
            cmds.select(clear=True)
            for control in self.ctrls:
                cmds.select(control, add=True)
            controlsSelection = cmds.ls(selection=True)
            cmds.filterCurve(controlsSelection, filter='euler')
            cmds.select(clear=True)
        else:
            cmds.warning('Nothing to Transfer!')

    def addControls(self, *args):
        self.sel = cmds.ls(selection=True)
        self.ctrls = cmds.textScrollList('controlsOnWindow', query=True, allItems=True)
        if(len(self.sel)>0):
            for x in range(len(self.sel)):
                if ((self.ctrls==None) or (self.sel[x] not in self.ctrls)):
                    cmds.textScrollList('controlsOnWindow', edit=True, append=self.sel[x])
        #query again the scroll list to update self.ctrls
        self.ctrls = cmds.textScrollList('controlsOnWindow', query=True, allItems=True)

    def deleteControls(self, *args):
        cmds.textScrollList('controlsOnWindow', edit=True, removeAll=True)
        del self.locators[:]
        print self.locators
        self.ctrls = cmds.textScrollList('controlsOnWindow', query=True, allItems=True)
    
    def showUI(self):
        if(cmds.window("animRecorderWindow", exists=True)):
            cmds.deleteUI("animRecorderWindow")
        
        animRecorderWindow = cmds.window('animRecorderWindow', title="Animation Recorder", iconName='AnimRecorder', widthHeight=(300, 200), sizeable=False )
        cmds.columnLayout()
        cmds.setParent('..')
        cmds.rowLayout(numberOfColumns=3, columnWidth3 =(230,35,35))
        cmds.text('  Selected Controls:', align='left', font='boldLabelFont', height=30)
        cmds.button(label=' - ', width=25, command=self.deleteControls)
        cmds.button(label=' + ', width=25, command=self.addControls)
        cmds.setParent('..')
        cmds.columnLayout( adjustableColumn=True )
        cmds.textScrollList('controlsOnWindow',numberOfRows=15)
        cmds.rowLayout(numberOfColumns=4, columnWidth4=(110,40,80,70), height=30, columnAttach4=('right','left','right', 'left'))
        cmds.text('Bake Animation:')
        cmds.checkBox(label='')
        cmds.text('Euler Filter:')
        cmds.checkBox(label='', value=True)
        cmds.setParent('..')
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(150,150),columnAttach2=('right','right'))
        cmds.button( label='Record Animation', command=self.recordAnimOnLocators, height=50,width=150 )
        cmds.button( label='Trasfer Animation', command=self.transferAnimFromLocators,height=50, width=150)
        cmds.setParent('..')
        cmds.columnLayout()
        cmds.button( label='Close',width=302, height=50, command=('cmds.deleteUI(\"' + animRecorderWindow + '\", window=True)') )
        cmds.showWindow( animRecorderWindow )

animRec = AnimationRecorder()
animRec.showUI()
