#coding:utf-8

dimg="images/"
dimgm=dimg+"mape/"

#       0       1         2
etats=["dur","liquide","vide"]

emape=[]

#                 0=nom      1=etat  2=images           3=soumis grav   4=animation 5=tcreuser  6=is posable    7=is prenable
#                 0          1       2                  3               4           5           6               7
emape.append(["air"         ,2      ,[None]             ,False          ,0          ,0.01       ,True           ,False   ])
emape.append(["herbe"       ,2      ,["herbe.png"]      ,True           ,0          ,0.3        ,True           ,True    ])
emape.append(["terre"       ,0      ,["terre.png"]      ,True           ,0          ,0.6        ,True           ,True    ])
emape.append(["pierre"      ,0      ,["pierre.png"]     ,False          ,0          ,1.5        ,True           ,True    ])
emape.append(["tronc"       ,0      ,["tronc1.png"]     ,True           ,0          ,1          ,True           ,True    ])
emape.append(["feuilles"    ,0      ,["feuilles.png"]   ,False          ,0          ,0.2        ,True           ,True    ])
















