#coding:utf-8

dimg="images/"
dimgm=dimg+"mape/"

#       0       1         2
etats=["dur","liquide","vide"]

emape=[]

#                 0=nom              1=etat  2=images               3=soumis grav   4=animation 5=tcreuser  6=is posable    7=is prenable
#                 0                  1       2                      3               4           5           6               7
emape.append(["air"                 ,2      ,[None]                 ,False          ,0          ,0.01       ,True           ,False   ]) #0
emape.append(["herbe"               ,2      ,["herbe1.png"]         ,True           ,0          ,0.3        ,True           ,True    ]) #1
emape.append(["terre"               ,0      ,["terre.png"]          ,True           ,0          ,0.6        ,True           ,True    ]) #2
emape.append(["pierre"              ,0      ,["pierre.png"]         ,False          ,0          ,1.5        ,True           ,True    ]) #3
emape.append(["tronc"               ,0      ,["tronc1.png"]         ,False          ,0          ,1          ,True           ,True    ]) #4
emape.append(["feuilles"            ,0      ,["feuilles.png"]       ,False          ,0          ,0.2        ,True           ,True    ]) #5
emape.append(["eau"                 ,1      ,["eau.png"]            ,True           ,0          ,1          ,True           ,True    ]) #6
emape.append(["boue"                ,0      ,["boue.png"]           ,True           ,0          ,0.8        ,True           ,True    ]) #7
emape.append(["sable"               ,0      ,["sable.png"]          ,True           ,0          ,0.4        ,True           ,True    ]) #8
emape.append(["verre"               ,0      ,["verre.png"]          ,False          ,0          ,0.3        ,True           ,True    ]) #9
emape.append(["fleur rouge"         ,2      ,["fleur_rouge.png"]    ,True           ,0          ,0.2        ,True           ,True    ]) #10
emape.append(["fleur bleu"          ,2      ,["fleur_bleu.png"]     ,True           ,0          ,0.2        ,True           ,True    ]) #11
emape.append(["fleur vert"          ,2      ,["fleur_vert.png"]     ,True           ,0          ,0.2        ,True           ,True    ]) #12
emape.append(["colorant rouge"      ,0      ,["colorant_rouge.png"] ,False          ,0          ,0          ,False          ,True    ]) #13
emape.append(["colorant bleu"       ,0      ,["colorant_bleu.png"]  ,False          ,0          ,0          ,False          ,True    ]) #14
emape.append(["colorant vert"       ,0      ,["colorant_vert.png"]  ,False          ,0          ,0          ,False          ,True    ]) #15
emape.append(["colorant jaune"      ,0      ,["colorant_jaune.png"] ,False          ,0          ,0          ,False          ,True    ]) #16
emape.append(["colorant violet"     ,0      ,["colorant_violet.png"],False          ,0          ,0          ,False          ,True    ]) #17
emape.append(["bois"                ,0      ,["bois.png"]           ,False          ,0          ,0.9        ,True           ,True    ]) #18
emape.append(["planche de bois"     ,0      ,["planche_bois.png"]   ,False          ,0          ,0.9        ,True           ,True    ]) #19
emape.append(["rondin de bois"      ,0      ,["rondin_bois.png"]    ,False          ,0          ,0.9        ,False          ,True    ]) #20
emape.append(["planche de pierre"   ,0      ,["planche_pierre.png"] ,False          ,0          ,0.9        ,True           ,True    ]) #21
emape.append(["rondin de pierre"    ,0      ,["rondin_pierre.png"]  ,False          ,0          ,0.9        ,False          ,True    ]) #22
emape.append(["sang"                ,1      ,["sang.png"]           ,True           ,0          ,1          ,True           ,True    ]) #23
emape.append(["lave"                ,1      ,["lave.png"]           ,True           ,0          ,1          ,True           ,True    ]) #24
emape.append(["eau regenerante"     ,1      ,["eau_regenerante.png"],True           ,0          ,1          ,True           ,True    ]) #25













