import numpy as np
from numpy.ma.core import arctan
import pygame
from scipy.integrate import odeint
from tkinter import *
# ///////////////////////////////// tkinter part ////////////////////
# ///////////////// For inputing values from GUI window

K=[]
window=Tk()
window.title("Projectile Motion")
window.geometry("275x115+650+300")
# ////////////////////// Label

Ux=Label(window,text="X velocity")
Uy=Label(window,text="Y velocity")
Gravity=Label(window,text="Gravity(g)")

def getVals():
    K.append([float(Ux.get()),float(Uy.get()),float(Gravity.get())])
    window.destroy()

# /////////////////////// Pack

Ux.grid(row=1,column=2)
Uy.grid(row=2,column=2)
Gravity.grid(row=3,column=2)


# ///////////////////////

Ux=IntVar()
Uy=IntVar()
Gravity=IntVar()
# //////////////////////
Ux=Entry(window,textvariable="Ux")
Uy=Entry(window,textvariable="Uy")
Gravity=Entry(window,textvariable="Gravity")
# ////////////////////


Ux.grid(row=1,column=4)
Uy.grid(row=2,column=4)
Gravity.grid(row=3,column=4)

submit=Button(window,text="START",fg='blue',command=getVals).grid(row=5,column=3)

window.mainloop()
# print(K)
# ///////////////////////////////////////////////////// Tinker over

# //////////////////////////////////////////// ode int part ////////////////////////////////
# ///////////// Constants //////////////////
# theta=np.pi*K[0][0]/180                                  # Angle in degree
Ux=K[0][0]                                               # initial velocity in x direction
Uy=K[0][1]                                               # initial velocity in x direction
g=K[0][2]                                                # Gravity on earth
U=(Ux**2+Uy**2)**0.5                                     # Resultant velocity

# //////////////////////////// Lagrangian equation ////////////////////////////////////

        #  dx/dt = Ucos(theta),dy/dt=Usin(theta)-gt

# //////////////////////////// Defining function for solving differential equation 
# ////////////////////////////////
            #  ODEint method working
            # we have our eqn x" = 0 and y" = -g
            # so we now reduce this order by defining it in terms of Ux and Uy where Ux and Uy are velocities in x and y direction.
            # so we have x' = Ux and y' = Uy
            # also Ux' = x" = 0  and Uy' = y" = -g
            # so we have successfully reduced this equation now we will solve them using odeint by taking them into vector notation
            # In Vector Notation we seprate all d/dt terms on LHS and other terms on RHS

#                   [ x'  ]  = [ Ux ]          as x'=Ux (Derived above)
#                   [ Ux' ]  = [ 0  ]          as Ux'=0 (Derived above)

#                   [ y'  ]  = [ Uy  ]          as y'=Uy (Derived above)
#                   [ Uy' ]  = [ -g  ]          as Uy'=-g (Derived above)

#  Now odeint command uses the following arguments for its working    odeint(Fun,initial,args)   
#  "Fun" here Fun should be function which takes in the initial condition(all the d/dt terms weather in vector notation or as simple notation )
#  ,time or whatever is the independant variable in array form and arguments as input and return the RHS of our reduced ode int problem.
# 
#  In General if we have to solve dy/dx = x+a+b   we will make a fun which will take initial condition of y and it should return x+a+b as output here "a"
#  ,"b" are extra argument for our function so these should be specified in command as odeint(Fun,initial,args=(a,b))

# ////////////////////////////////


def Funx(initialx,t):
    x,Ux=initialx
    dxdt=[Ux,0]
    return(dxdt)

def Funy(initialy,t,g):
    y,Uy=initialy
    dydt=[Uy,-g]
    return dydt


initialx=[0,Ux]                      # here initialx = [initial x coordinate , initial x velocity]
initialy=[0,Uy]                      # here initialy = [initial y coordinate , initial y velocity]

# //////////////////////////// Precalculation for scale////////////////////
#  For adjusting Scale of animation Range and Height is pre calculated to set x and y axis ??????????????

theta=arctan(Uy/Ux)
Range=U**2*np.sin(2*theta)/g
Height=(U*np.sin(theta))**2/(2*g)

# ////////////////////////////  Pygamepart ///////////////////////////////

White=(255,255,255)                       # Defining Colour for further use
Black=(0,0,0)                             # Defining Colour for further use
width,height=1200,850                     #Defining Width and height of pygame window

# //////////////////////////// Checking if range is negative i.e theta>90 and setting range in accordance to it

if Range<-1:
    xlim=[int(Range)-2,1]                                   # For tweaking the grid in negative axis number 20 can be tweaked 
    ylim=[-1,int(Height)+3]

else:
    xlim=[-1,int(Range)+2]
    ylim=[-1,int(Height)+3]
# //////////////////////////// Rescaling Pygame window for making grid on it 

scalex=width/(xlim[1]-xlim[0])
scaley=height/(ylim[1]-ylim[0])

# //////////////////////////////////////// time and time array to use in while loop
time=0
tarray=[0]
# ////////////////////////////////////// Pygame display setup   

gameDisplay=pygame.display.set_mode((width,height))     # Defining New Display 
pygame.display.set_caption("Projectile motion")         # Setting window title
pygame.font.init()                                      # initialising font for further use
font=pygame.font.Font('freesansbold.ttf',15)

# Rescaler Function : Takes a tuple in grid coordinate system and converts it transform it in Pygames pixel coordinate system

def T(x,y):
	return(float(scalex*(x-xlim[0])),float(height-scaley*(y-ylim[0])))

# //////////////////////////////// For Tracing Path of the Projectile

Point=[]
def drawpoint(k):
    Point.append(k)
    for i in range(len(Point)):
        pygame.draw.circle(gameDisplay,Black,((int(Point[i][0]),int(Point[i][1]))),1)

# ///////////////////////////// This function stops the animation once the projectile hits the ground

def end():
    while end:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.update()
        pygame.time.Clock().tick(0)

maxheight=0      # Stores maximum height value in it

while True:

# /////////////////////////////////////////////////// Display Grid Setup ////////////////////////////
    
    gameDisplay.fill(White)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            
    pygame.draw.line(gameDisplay,Black,(scalex*(-xlim[0]),0),(scalex*(-xlim[0]),height),2)
    pygame.draw.line(gameDisplay,Black,(0,height-scaley*(-ylim[0])),(width,height-scaley*(-ylim[0])),2)

    for i in range(int(width/scalex)):
    	pygame.draw.line(gameDisplay,Black,(i*scalex,0),(i*scalex,height),1)

    for i in range(int(height/scaley)):
    	pygame.draw.line(gameDisplay,Black,(0,i*scaley),(width,i*scaley),1)

#///////////////////////////////////////////////////////// Simultaneously calculating derivative and drawing path and circle according to it

    time+=0.002                                                       # For speed of animation this time can be tweaked
    tarray.append(time)    
    G=odeint(Funx,initialx,tarray)
    H=odeint(Funy,initialy,tarray,args=(g,))
    initialx=G[-1]
    initialy=H[-1]
    # print(initialx,time)
    G,H=G[:,0],H[:,0]
    drawpoint(T(G[-1],H[-1]))
    pygame.draw.circle(gameDisplay,Black,T(G[-1],H[-1]),20)
    # print(tarray)
# //////////////////////////////////////////// For Text on display //////////////////////////////
 
    # /////////////////////////////////////////////// Display Part////////////////
    text=font.render("X="+str(round(float(G[-1]),3))+", Y="+str(round(float(H[-1]),3)),True,Black,White)
    textrect=text.get_rect()
    textrect.center=(T(G[-1],H[-1])[0]-75,T(G[-1],H[-1])[1]-40)
    gameDisplay.blit(text,textrect)
    # ///////////////////////////////////////////////
    Data=font.render("MaxHeight="+str(round(float(maxheight),3))+" m , Range="+str(round(float(G[-1]),3))+" m ,Time Period = "
    +str(round(time,3))+"sec",True,Black,White)
    Datarect=Data.get_rect()
    Datarect.center=(width-400,30)
    gameDisplay.blit(Data,Datarect)
    # /////////////////////////////////////////////
    Data1=font.render("Theta ="+str(round(180*theta/np.pi,3))+",Gravity ="+str(round(g,3))+" m/sec^2, U ="+str(round(U,3)) +" m/sec",True,Black,White)
    Datarect1=Data1.get_rect()
    Datarect1.center=(width-400,50)
    gameDisplay.blit(Data1,Datarect1)
    
    # ///////////////////////////////////////////////////////////////////////////
    tarray.pop(0)

# ///////////////storing maximum height//////////////////

    if H[-1]>maxheight:
        maxheight=H[-1]

# ////////////////////// Checking if projectile hits the ground and stopping the game window

    if H[-1]<=-0.0000001:
        end()
    pygame.display.update()

#Created by Harsh Maurya with 💖 ............ :)