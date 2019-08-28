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
        self.tx=tc
        self.ty=tc*2
        self.rect=pygame.Rect(self.px,self.py,self.tx,self.ty)
        #movement
        self.vitx=0.
        self.vity=0.
        self.vitmax=rxx(5)
        self.acc=rxx(0.5)
        self.decc=rxx(0.1)
        self.grav=rxx(0.2)
        self.accjump=rxx(6)
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
    def bouger(self,aa):
        if aa=="Up" and time.time()-self.dkup>=self.t:
            self.dkup=time.time()
            self.vity-=self.grav
        elif aa=="Down" and time.time()-self.dkdown>=self.t:
            self.dkdown=time.time()
            self.vity+=self.acc
        elif aa=="Left" and time.time()-self.dkleft>=self.t:
            self.dkleft=time.time()
            self.vitx-=self.acc
        elif aa=="Right" and time.time()-self.dkright>=self.t:
            self.dkright=time.time()
            self.vitx+=self.acc
        elif aa=="Jump" and time.time()-self.dkjump>=self.tj and self.nbjump>0:
            self.dkjump=time.time()
            self.vity-=self.accjump
            self.nbjump-=1
    def update(self,mape):
        if time.time()-self.dbg>=self.t:
            self.dbg=time.time()
            #physique
            if self.vitx>self.vitmax: self.vitx=self.vitmax
            elif self.vitx<-self.vitmax: self.vitx=-self.vitmax
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
                                if self.py<my:
                                    self.py+=my-(self.py+self.ty)
                                    self.vity=0.
                                    self.nbjump=self.nbjump_tot
                                else:
                                    if self.px<=mx+mtx and self.px+self.tx>=mx+mtx:
                                        self.px+=(mx+mtx)-self.px
                                        self.vitx=0.
                                    elif self.px+self.tx>=mx and self.px <=mx:
                                        self.px-=(self.px+self.tx)-mx
                                        self.vitx=0.
                                self.rect=pygame.Rect(self.px,self.py,self.tx,self.ty)
            #camera
            self.cam=[-self.px+tex/2,-self.py+tey/2]
            #actions
            if self.isaction:
                if self.action=="creuser":
                    pos=pygame.mouse.get_pos()
                    xx=int((-self.cam[0]+pos[0])/mape.tc)
                    yy=int((-self.cam[1]+pos[1])/mape.tc)
                    if self.dcaseact!=[xx,yy]:
                        self.debaction=time.time()
                        self.dcaseact=[xx,yy]
                    elif time.time()-self.debaction>=emape[mape.mape[xx,yy]][5]:
                        mape.mape[xx,yy]=0
                        
                        
                        
                        
                
                    
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
        #de 102>130: herbe
        for y in range(28):
            for x in range(self.mtx): self.mape[x,y+101]=2
        #de 130>1000: pierre
        for y in range(1000-130):
            for x in range(self.mtx): self.mape[x,y+129]=3
        
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
    pygame.draw.rect( fenetre , (255,255,255) , (perso.cam[0]+perso.px,perso.cam[1]+perso.py,perso.tx,perso.ty) , 0)
    for x in range( int((-perso.cam[0])/mape.tc)-1 , int((-perso.cam[0]+tex)/mape.tc)+1 ):
        for y in range( int((-perso.cam[1])/mape.tc)-1 , int((-perso.cam[1]+tey)/mape.tc)+1 ):
            if x>=0 and x<mape.mtx and y>=0 and y<mape.mty:
                if emape[mape.mape[x,y]][2][emape[mape.mape[x,y]][4]]!=None:
                    fenetre.blit( emape[mape.mape[x,y]][2][emape[mape.mape[x,y]][4]] , [perso.cam[0]+x*mape.tc,perso.cam[1]+y*mape.tc])
    if perso.isaction and (time.time()-perso.debaction)<=emape[mape.mape[perso.dcaseact[0],perso.dcaseact[1]]][5]:
        nb=int((time.time()-perso.debaction)/emape[mape.mape[perso.dcaseact[0],perso.dcaseact[1]]][5]*5)
        fenetre.blit( imgsancreuser[nb] , [perso.cam[0]+perso.dcaseact[0]*mape.tc,perso.cam[1]+perso.dcaseact[1]*mape.tc])
    fenetre.blit( font.render("fps="+str(fps),True,(255,255,255)), [rx(15),ry(15)])
    fenetre.blit( font.render("x="+str(int(perso.px)),True,(255,255,255)), [rx(15),ry(35)])
    fenetre.blit( font.render("y="+str(int(perso.py)),True,(255,255,255)), [rx(15),ry(55)])
    fenetre.blit( font.render("vitx="+str(perso.vitx)[:5],True,(255,255,255)), [rx(15),ry(75)])
    fenetre.blit( font.render("vity="+str(perso.vity)[:5],True,(255,255,255)), [rx(15),ry(95)])
    pygame.display.update()


def main():
    mape=Mape()
    perso=Perso(1000,4200)
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
            elif event.type==MOUSEBUTTONDOWN:
                if event.button==1: perso.isaction=True
                if event.button==3: perso.isposer=True
            elif event.type==MOUSEBUTTONUP:
                if event.button==1:
                    perso.isaction=False
                    perso.dcaseact=[0,0]
                if event.button==3: perso.isposer=False
        tt=time.time()-t1
        if tt!=0: fps=int(1./tt)

main()
