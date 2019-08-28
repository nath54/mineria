#coding:utf-8

dimg="images/"
dimgm=dimg+"mape/"

#       0       1         2
etats=["dur","liquide","vide"]

emape=[]

#0=nom 1=etat 2=images 3=est soumis a la gravité 4=animation 5=tcreuser
emape.append(["air",2,[None],False,0,0.01])
emape.append(["herbe",2,["herbe.png"],True,0,0.3])
emape.append(["terre",0,["terre.png"],True,0,0.6])
emape.append(["pierre",0,["pierre.png"],False,0,1.5])

















