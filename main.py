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
        if row[8] == tipoNudoList["NudoT"]:
            linea = []
            if int(arcpy.GetCount_management("Tubo_view").getOutput(0)) != 3:
                linea.append(str(row[0]) + "   " + str(row[1]) + "<> 3 tubos conectados" + "\n")
                f.writelines(linea)
        if row[8] == tipoNudoList["NudoCambioSeccion"]:
            linea = []
            if int(arcpy.GetCount_management("Tubo_view").getOutput(0)) == 2:
                with arcpy.da.SearchCursor("Tubo_view", '*') as cursorTubos:
                    dimList = []
                    for rowTubos in cursorTubos:
                        dimList.append(rowTubos[14])
                    if len(set(dimList)) != 2:
                        linea.append(str(row[0]) + "   " + str(row[1]) + "No hay cambio diametro" + "\n")
                        f.writelines(linea)
            elif int(arcpy.GetCount_management("Tubo_view").getOutput(0)) != 2:
                linea.append(str(row[0]) + "   " + str(row[1]) + "> 2 tubos conectados" + "\n")
                f.writelines(linea)
        if row[8] == tipoNudoList["NudoCambioMaterial"]:
            linea = []
            if int(arcpy.GetCount_management("Tubo_view").getOutput(0)) == 2:
                with arcpy.da.SearchCursor("Tubo_view", '*') as cursorTubos:
                    matList = []
                    for rowTubos in cursorTubos:
                        matList.append(rowTubos[9])
                    if len(set(matList)) != 2:
                        linea.append(str(row[0]) + "   " + str(row[1]) + "No hay cambio material" + "\n")
                        f.writelines(linea)
            elif int(arcpy.GetCount_management("Tubo_view").getOutput(0)) != 2:
                linea.append(str(row[0]) + "   " + str(row[1]) + "> 2 tubos conectados" + "\n")
                f.writelines(linea)
        if row[8] == tipoNudoList["NudoTestero"]:
            linea = []
            if int(arcpy.GetCount_management("Tubo_view").getOutput(0)) != 1:
                linea.append(str(row[0]) + "   " + str(row[1]) + "> 1 tubo conectado" + "\n")
                f.writelines(linea)
        arcpy.Delete_management("NudoDistribucionSelect_view")
f.close()
