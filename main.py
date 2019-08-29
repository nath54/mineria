#coding:utf-8
import random,pygame,os,time,numpy
from pygame.locals import *
from data import *

pygame.init()

btex,btey=1280,1024
io=pygame.display.Info()
tex,tey=io.current_w,io.current_h

def rx(x): return int(x/btex*tex)
def ry(y): return int(y/btey*tey)
def rxx(x): return float(x/btex*tex)
def ryy(y): return float(y/btey*tey)

fenetre=pygame.display.set_mode([tex,tey],pygame.FULLSCREEN)
pygame.display.set_caption("Mineria v2")
font=pygame.font.SysFont("Arial",rx(20))

tc=rx(50)

x=0
y=0
for m in emape:
    y=0
    for i in m[2]:
        if i!=None:
            emape[x][2][y]=pygame.transform.scale( pygame.image.load(dimgm+i), [tc,tc])
        y+=1
    x+=1

imgsancreuser=["anim_c1.png","anim_c2.png","anim_c3.png","anim_c4.png","anim_c5.png"]
for x in range(len(imgsancreuser)): imgsancreuser[x]=pygame.transform.scale( pygame.image.load(dimg+imgsancreuser[x]) , [tc,tc])

class Perso:
    def __init__(self,x,y):
        #location
        self.px=x
        self.py=y
        self.tx=tc*1
        self.ty=tc*1.5
        self.rect=pygame.Rect(self.px,self.py,self.tx,self.ty)
        #movement
        self.vitx=0.
        self.vity=0.
        self.vitmax=rxx(5)
        self.acc=rxx(0.5)
        self.decc=rxx(0.1)
        self.grav=rxx(0.2)
        self.accjump=rxx(7)
        self.nbjump_tot=1
        self.nbjump=self.nbjump_tot
        #keys
        self.kup=K_UP
        self.kdown=K_DOWN
        self.kleft=K_LEFT
        self.kright=K_RIGHT
        self.kjump=K_SPACE
        #time
        self.t=0.01
        self.tj=1
        self.dbg=time.time()
        self.dkup=time.time()
        self.dkdown=time.time()
        self.dkleft=time.time()
        self.dkright=time.time()
        self.dkjump=time.time()
        #camera
        self.cam=[-self.px+tex/2,-self.py+tey/2]
        #actions
        self.action="creuser"
        self.isaction=False
        self.isposer=False
        self.debaction=0
        self.dcaseact=[0,0]
        #inventaire
        self.inventaire=[] # pour chaque élément : 0=l'id de l'élément , 1=le nombre de bloc de cet élément possédé
        self.esb=0
        #vie_endurance
        self.vie_tot=500
        self.vie=self.vie_tot
        self.energie_tot=500
        self.energie=self.energie_tot
        self.issprint=False
        self.dsprint=time.time()
        self.tsprint=1.5
        self.drempener=time.time()
        self.trempener=0.03
        self.dutilener=time.time()
        self.tutilener=0.01
    def bouger(self,aa):
        vitmax=self.vitmax
        if self.issprint: vitmax=self.vitmax*2
        if aa=="Up" and time.time()-self.dkup>=self.t:
            self.dkup=time.time()
        elif aa=="Down" and time.time()-self.dkdown>=self.t:
            self.dkdown=time.time()
            self.vity+=self.acc
        elif aa=="Left" and time.time()-self.dkleft>=self.t:
            self.dkleft=time.time()
            if self.vitx>-vitmax: self.vitx-=self.acc
        elif aa=="Right" and time.time()-self.dkright>=self.t:
            self.dkright=time.time()
            if self.vitx<vitmax: self.vitx+=self.acc
        elif aa=="Jump" and time.time()-self.dkjump>=self.tj and self.nbjump>0:
            self.dkjump=time.time()
            self.vity-=self.accjump
            self.nbjump-=1
    def update(self,mape):
        if time.time()-self.dbg>=self.t:
            self.dbg=time.time()
            #energie
            if not self.issprint:
                if time.time()-self.dsprint>=self.tsprint:
                    if time.time()-self.drempener>=self.trempener:
                        self.drempener=time.time()
                        if self.energie<self.energie_tot: self.energie+=1
            else:
                if time.time()-self.dutilener>=self.tutilener:
                    self.dutilener=time.time()
                    self.energie-=1
                    if self.energie<=0:
                        self.energie=0
                        self.issprint=False
            #physique
            vitmax=self.vitmax
            if self.issprint: vitmax=self.vitmax*2
            dd=rx(0.5)
            if self.vitx>=vitmax+dd: self.vitx-=dd
            elif self.vitx>vitmax: self.vitx=vitmax
            elif self.vitx<-vitmax-dd:  self.vitx+=dd
            elif self.vitx<-vitmax: self.vitx=-vitmax
            if self.vitx>0 and self.vitx>self.decc: self.vitx-=self.decc
            elif self.vitx>0: self.vitx=0.
            elif self.vitx<0 and self.vitx<-self.decc: self.vitx+=self.decc
            elif self.vitx<0: self.vitx=0.
            self.vity+=self.grav
            #mouvement
            self.px+=self.vitx
            self.py+=self.vity
            self.rect=pygame.Rect(self.px,self.py,self.tx,self.ty)
            #collisions
            for x in range( int(self.px/mape.tc) - 3 , int(self.px/mape.tc) + 3 ):
                for y in range( int(self.py/mape.tc) - 3 , int(self.py/mape.tc) + 3 ):
                    if x>=0 and x<mape.mtx and y>=0 and y<mape.mty:
                        m=mape.mape[x,y]
                        if emape[m][1]==0: 
                            mx=x*mape.tc
                            my=y*mape.tc
                            mtx,mty=mape.tc,mape.tc
                            if self.rect.colliderect( (mx,my,mtx,mty) ):
                                if self.py+self.ty/1.5<my and self.py<my:
                                    self.py+=my-(self.py+self.ty)
                                    self.vity=0.
                                    self.nbjump=self.nbjump_tot
                                    self.rect=pygame.Rect(self.px,self.py,self.tx,self.ty)
                                elif self.py<my+mty and self.py+self.ty>my+mty:
                                    self.py+=(my+mty)-self.py
                                    self.vity=0
                                    self.rect=pygame.Rect(self.px,self.py,self.tx,self.ty)
                                if self.px<mx+mtx and self.px+self.tx>mx+mtx:
                                    self.px+=(mx+mtx)-self.px
                                    self.vitx=0.
                                    self.rect=pygame.Rect(self.px,self.py,self.tx,self.ty)
                                elif self.px+self.tx>mx and self.px <mx:
                                    self.px-=(self.px+self.tx)-mx
                                    self.vitx=0.
                                    self.rect=pygame.Rect(self.px,self.py,self.tx,self.ty)
                                self.rect=pygame.Rect(self.px,self.py,self.tx,self.ty)
            if self.px<0: self.px=0
            elif self.px>mape.mtx*mape.tc: self.px>mape.mtx*mape.tc
            if self.py<0: self.py=0
            elif self.py>mape.mty*mape.tc: self.py>mape.mty*mape.tc
            #camera
            self.cam=[-self.px+tex/2,-self.py+tey/2]
            #actions
            pos=pygame.mouse.get_pos()
            xx=int((-self.cam[0]+pos[0])/mape.tc)
            yy=int((-self.cam[1]+pos[1])/mape.tc)
            if self.isaction:
                if self.action=="creuser" and emape[ mape.mape[xx,yy] ][7]:
                    if self.dcaseact!=[xx,yy]:
                        self.debaction=time.time()
                        self.dcaseact=[xx,yy]
                    elif time.time()-self.debaction>=emape[mape.mape[xx,yy]][5]:
                        ci=None
                        for i in self.inventaire:
                            if i[0]==mape.mape[xx,yy]: ci=self.inventaire.index(i)
                        if ci==None: self.inventaire.append( [mape.mape[xx,yy],1] )
                        else: self.inventaire[ci][1]+=1
                        mape.mape[xx,yy]=0
            if self.isposer:
                if len(self.inventaire)>self.esb:
                    if emape[mape.mape[xx,yy]][1]==2:
                        mape.mape[xx,yy]=self.inventaire[self.esb][0]
                        self.inventaire[self.esb][1]-=1
                        if self.inventaire[self.esb][1]<=0:
                            del(self.inventaire[self.esb])
                        
                        
                        
                        
                
                    
class Mape:
    def __init__(self):
        #mape
        self.mtx=1000
        self.mty=1000
        self.tc=tc
        self.mape=numpy.zeros([self.mtx,self.mty],dtype=int)
        #generation de la mape:
        
        #de 0>100: air
        for y in range(100):
            for x in range(self.mtx): self.mape[x,y+0]=0
        #de 101>101: herbe
        for y in range(1):
            for x in range(self.mtx): self.mape[x,y+100]=1
        #de 102>110: herbe
        for y in range(8):
            for x in range(self.mtx): self.mape[x,y+101]=2
        #de 130>1000: pierre
        for y in range(1000-110):
            for x in range(self.mtx): self.mape[x,y+109]=3
        
        #ciel
        self.clciel=(0,100,150)
        
def verif_keys(perso):
    keys=pygame.key.get_pressed()
    if keys[perso.kup]: perso.bouger("Up")
    if keys[perso.kdown]: perso.bouger("Down")
    if keys[perso.kleft]: perso.bouger("Left")
    if keys[perso.kright]: perso.bouger("Right")
    if keys[perso.kjump]: perso.bouger("Jump")
    return perso

def aff(perso,mape,fps):
    fenetre.fill( mape.clciel )
    #personnage
    pygame.draw.rect( fenetre , (255,255,255) , (perso.cam[0]+perso.px,perso.cam[1]+perso.py,perso.tx,perso.ty) , 0)
    #mape
    for x in range( int((-perso.cam[0])/mape.tc)-1 , int((-perso.cam[0]+tex)/mape.tc)+1 ):
        for y in range( int((-perso.cam[1])/mape.tc)-1 , int((-perso.cam[1]+tey)/mape.tc)+1 ):
            if x>=0 and x<mape.mtx and y>=0 and y<mape.mty:
                if emape[mape.mape[x,y]][2][emape[mape.mape[x,y]][4]]!=None:
                    fenetre.blit( emape[mape.mape[x,y]][2][emape[mape.mape[x,y]][4]] , [perso.cam[0]+x*mape.tc,perso.cam[1]+y*mape.tc])
    #animation de destruction d'un bloc
    if perso.isaction and (time.time()-perso.debaction)<=emape[mape.mape[perso.dcaseact[0],perso.dcaseact[1]]][5]:
        nb=int((time.time()-perso.debaction)/emape[mape.mape[perso.dcaseact[0],perso.dcaseact[1]]][5]*5)
        fenetre.blit( imgsancreuser[nb] , [perso.cam[0]+perso.dcaseact[0]*mape.tc,perso.cam[1]+perso.dcaseact[1]*mape.tc])
    #première colonne de l'inventaire affiché à l'écran , 1 colonne = 10 cases
    xx,yy=rx(250),ry(900)
    tcx,tcy=rx(60),ry(60)
    for x in range(10):
        cl,t=(0,0,0),rx(2)
        if x==perso.esb: cl,t=(150,150,150),t
        if len(perso.inventaire)>x and emape[perso.inventaire[x][0]][2][0]!=None:
            fenetre.blit( pygame.transform.scale( emape[perso.inventaire[x][0]][2][0] , [tcx-t*2,tcy-t*2] ) , [xx+t,yy+t])
        pygame.draw.rect(fenetre,cl,(xx,yy,tcx,tcy),t)
        xx+=tcx+t
    #barres  vie et énergie
    pygame.draw.rect( fenetre , (255,0,0) , (rx(250),ry(870),int(perso.vie/perso.vie_tot*rx(600)),ry(15) ) , 0)
    pygame.draw.rect( fenetre , (0,0,0) , (rx(250),ry(870),rx(600),ry(15) ) , rx(1))
    pygame.draw.rect( fenetre , (255,200,0) , (rx(250),ry(853),int(perso.energie/perso.energie_tot*rx(600)),ry(15) ) , 0)
    pygame.draw.rect( fenetre , (0,0,0) , (rx(250),ry(853),rx(600),ry(15) ) , rx(1))
    #textes affiché à l'écran ( sert surtout à débugger )
    fenetre.blit( font.render("fps="+str(fps),True,(255,255,255)), [rx(15),ry(15)])
    fenetre.blit( font.render("x="+str(int(perso.px)),True,(255,255,255)), [rx(15),ry(35)])
    fenetre.blit( font.render("y="+str(int(perso.py)),True,(255,255,255)), [rx(15),ry(55)])
    fenetre.blit( font.render("vitx="+str(perso.vitx)[:5],True,(255,255,255)), [rx(15),ry(75)])
    fenetre.blit( font.render("vity="+str(perso.vity)[:5],True,(255,255,255)), [rx(15),ry(95)])
    pygame.display.update()


def main():
    mape=Mape()
    perso=Perso(1000,4600)
    fps=0
    encour=True
    while encour:
        t1=time.time()
        #aff
        aff(perso,mape,fps)
        perso=verif_keys(perso)
        perso.update(mape)
        #events
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN:
                if event.key==K_ESCAPE: encour=False
                if event.key == K_RSHIFT:
                    if perso.energie>0: perso.issprint=True
                    perso.dsprint=time.time()
            elif event.type==KEYUP:
                if event.key == K_RSHIFT:
                    perso.issprint=False
                    perso.dsprint=time.time()
            elif event.type==MOUSEBUTTONDOWN:
                if event.button==1: perso.isaction=True
                if event.button==3: perso.isposer=True
                if event.button==5:
                    perso.esb-=1
                    if perso.esb==-1: perso.esb=10
                if event.button==4:
                    perso.esb+=1
                    if perso.esb==11: perso.esb=0
            elif event.type==MOUSEBUTTONUP:
                if event.button==1:
                    perso.isaction=False
                    perso.dcaseact=[0,0]
                if event.button==3: perso.isposer=False
        tt=time.time()-t1
        if tt!=0: fps=int(1./tt)

rb0=pygame.Rect(rx(500),ry(400),rx(300),ry(50))
def affmenu(fps,pos,men):
    bts=[]
    for x in range(10): bts.append(None)
    fenetre.fill((0,0,0))
    if men==0:
        cl=(200,200,20)
        if rb0.collidepoint(pos): cl=(150,150,20)
        bts[0]=pygame.draw.rect( fenetre,cl , rb0 , 0)
        fenetre.blit( font.render("Play",True,(0,0,0)) , [rx(550),ry(410)])
    pygame.display.update()
    return bts

def menu():
    men=0
    encourm=True
    fps=0
    while encourm:
        t1=time.time()
        pos=pygame.mouse.get_pos()
        bts=affmenu(fps,pos,men)
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN:
                if event.key==K_ESCAPE: encourm=False
            elif event.type==MOUSEBUTTONUP:
                for b in bts:
                    if b!=None and b.collidepoint(pos):
                        di=bts.index(b)
                        if di==0: main()
        tt=time.time()-t1
        if tt!=0: fps=int(1./tt)

menu()
