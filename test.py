from maya import cmds

sel = cmds.ls(selection=True)

cmds.bakeResults(sel, simulation=False, time=(1,120), sparseAnimCurveBake=True)


