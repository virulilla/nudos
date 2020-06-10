import arcpy, os

mdbRecibido = "C://CYII//nudos//data//recibido//RA_58270//Replica.mdb"

replicaRecibido = os.path.join("C://CYII//nudos//data//recibido//RA_58270", "replicaREC.gdb")
if arcpy.Exists(replicaRecibido):
    arcpy.Delete_management(replicaRecibido)
arcpy.CreateFileGDB_management("C://CYII//nudos//data//recibido//RA_58270", "replicaREC")

if os.path.exists("C://CYII//nudos//nudos.txt"):
    os.remove("C://CYII//nudos//nudos.txt")
f = open("C://CYII//nudos//nudos.txt",'w')

arcpy.env.workspace = os.path.join(mdbRecibido, "RedAbastecimiento")

arcpy.CopyFeatures_management("NudoDistribucion", os.path.join("C://CYII//nudos//data//recibido//RA_58270//replicaREC.gdb", "NudoDistribucion"))
arcpy.CopyFeatures_management("Tubo", os.path.join("C://CYII//nudos//data//recibido//RA_58270//replicaREC.gdb", "Tubo"))

arcpy.env.workspace = replicaRecibido

arcpy.MakeFeatureLayer_management("Tubo", "Tubo_view")
arcpy.MakeFeatureLayer_management("NudoDistribucion", "NudoDistribucion_view")

tipoNudoList = {"NudoT": 1, "NudoCambioSeccion": 2, "NudoCambioMaterial": 3, "NudoCambioAntiguedad": 4, "NudoTestero": 7}

with arcpy.da.SearchCursor("NudoDistribucion_view", '*') as cursor:
    for row in cursor:
        arcpy.MakeFeatureLayer_management("NudoDistribucion", "NudoDistribucionSelect_view", "OBJECTID = " + str(row[0]))
        arcpy.SelectLayerByLocation_management("Tubo_view", "INTERSECT", "NudoDistribucionSelect_view")
        # arcpy.MakeFeatureLayer_management(selectionTubos, "TubosSelect_view")
        if row[7] == tipoNudoList["NudoT"] and row[7] is not None:
            linea = []
            if int(arcpy.GetCount_management("Tubo_view").getOutput(0)) != 3:
                linea.append(str(row[0]) + "   " + str(row[12]) + "\n")
                f.writelines(linea)
        if row[7] == tipoNudoList["NudoCambioSeccion"] and row[7] is not None:
            linea = []
            if int(arcpy.GetCount_management("Tubo_view").getOutput(0)) == 2:
                with arcpy.da.SearchCursor("selectionTubos", '*') as cursorTubos:
                    dimList = []
                    for rowTubos in cursorTubos:
                        dimList.append(rowTubos[12])
                        if len(set(dimList)) != 2:
                            linea.append(str(row[0]) + "   " + str(row[12]) + "\n")
                            f.writelines(linea)
            elif int(arcpy.GetCount_management("Tubo_view").getOutput(0)) != 2:
                linea.append(str(row[0]) + "   " + str(row[12]) + "\n")
                f.writelines(linea)
        if row[7] == tipoNudoList["NudoCambioMaterial"] and row[7] is not None:
            linea = []
            if int(arcpy.GetCount_management("Tubo_view").getOutput(0)) == 2:
                with arcpy.da.SearchCursor("selectionTubos", '*') as cursorTubos:
                    matList = []
                    for rowTubos in cursorTubos:
                        matList.append(rowTubos[8])
                        if len(set(matList)) != 2:
                            linea.append(str(row[0]) + "   " + str(row[12]) + "\n")
                            f.writelines(linea)
            elif int(arcpy.GetCount_management("Tubo_view").getOutput(0)) != 2:
                linea.append(str(row[0]) + "   " + str(row[12]) + "\n")
                f.writelines(linea)
        if row[7] == tipoNudoList["NudoT"] and row[7] is not None:
            linea = []
            if int(arcpy.GetCount_management("Tubo_view").getOutput(0)) != 1:
                linea.append(str(row[0]) + "   " + str(row[12]) + "\n")
                f.writelines(linea)
        # arcpy.Delete_management("TubosSelect_view")
        arcpy.Delete_management("NudoDistribucionSelect_view")
f.close()
