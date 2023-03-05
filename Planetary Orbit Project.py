"""
Object-oriented Python program to simulate the orbit of the inner planets (Mercury, Venus, Earth, Mars) around the 
sun and the launch of a satellite to Mars.
Note: Sun is yellow, Mercury is orange, Venus is brown, Earth is blue, Mars is red and Satellite is black
Planetary data obtained from https://nssdc.gsfc.nasa.gov/planetary/factsheet/
"""


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

G=6.67408e-11 #Global variable for gravitational constant

class Body (object): # Build objects
    def __init__(self, name, color, size, mass, r, v):
        self.name = name
        self.color = color[:-1] #Remove ("/n") for patch to be generated properly.
        self.size =size #Relative sizes used for animation (NOT TO SCALE)
        self.mass = mass
        self.r = np.array([r,0])#Y- Position is set to 0 for all bodies.
        self.v = np.array(list(v.split(",")), dtype="float") #Split the X-Y components of velocity

        #Additional Values
        self.previous_y=0 # the previous_y value of position will be used to determine the periods
        self.repeat= True #Statement to print orbital period once

    
    def update_vel(self,dt,n): #Beeman algorithm for velocity of the nth body
        n.v += 1/6*(2*n.a_next+5*n.a-n.apast)*dt
     
    def update_position(self,dt,n):#Beeman algorithm for position of the nth body
        n.r += n.v*dt+1/6*((4*n.a-n.apast))*(dt**2)
    
    def calculate_Ke(self,n): #Calulate the kinteic energy
        Ke= 0.5*n.mass*(np.linalg.norm((n.v)))**2 #np.linalg.norm is used to calc modulus
        self.Ke_total += Ke #add to total Ke of the system.
        
    def check_period(self,n): #Print oribatal periods
        if n.r[1]>0 and n.previous_y<0 and n.repeat==True: #Conditions necesary to print orbital period (NOTE LINE 56, SATELLITE PRINT IS SET TO FALSE)
                    orbit_period=((self.t)/(60*60*24)) #convert time into years
                    print(n.name[:-1] + "'s orbital period is: " + str(orbit_period) + " days") #print orbital period [:-1] removes ("/n")
                    n.repeat = False #Print periods only once
        else:
            pass
        

class Simulation:
    
    def __init__(self):
        self.bodies=[] #create the list of object bodies
        self.t=0 #initial time is zero
        self.num_iterations=4000 #Number of iterations for simulation & for the printing of the energy graph.
        
        #Read input data
        planets=['Sun.txt', 'Mercury.txt', 'Venus.txt', 'Earth.txt', 'Mars.txt', 'satelite.txt'] #CHANGE WHEN ADDING NEW BODY
        for i in range (0,len(planets)):
            filein=open(planets[i],'r') #Reads the file of the data of a specefic body
            rfile= filein.readlines()
            planet=Body(rfile[2],rfile[3],float(rfile[4]),float(rfile[5]),float(rfile[6]),(rfile[7])) #Create object
            self.bodies.append(planet) #Appeneded object to bodies list
        self.bodies[5].repeat=False #Skip printing satelite's period.
        
        #Graphing data
        self.time_list=[] #List of time, used for energy and satellite distance to mars graph.
        self.energy_list=[] #List of total energy of system.
        self.satelite_distance=[] #List of distance of satellite to mars.
        
    def acceleration(self,n,m,G): #Beeman algorithm for acceleration, the nth body is beeing updated for the effect of the mth body
        a= (-(n.r-m.r)*(G*n.mass*m.mass/(np.linalg.norm(n.r - m.r))**3))/(n.mass)      
        return a 
    
    def initialize(self): #Start the simulation
        for n in self.bodies: #iterates over all bodies
            n.a=0 #defines the current acceleration parameter
            for m in self.bodies: #with respect to all other bodies
                if n==m: #Skip interaction with self.
                    pass
                else:
                    a = self.acceleration(n, m,G) #contribution of the mth body to the nth body's acceleration
                    n.a+= a
            n.apast = n.a #for the first timestep the previous acceleration is approximated to be the same as the current one.
            
            
    def run_simulation(self,i): #updates the program
    
        #Resets the energies to zero
        self.Pe_total=0
        self.Ke_total=0
        
        #Tracking time
        dt=60*60*24 #1 day intervals
        self.t+=dt #Total time since the simulation started
        time=(i*dt) #Current Time
        self.time_list.append(time) #Create list of times after each frame of animation

        #__update positions___
        for n in self.bodies: 
            Body.update_position(self,dt, n)
            Body.check_period(self,n) #checks if any planet has completed a full period on this timestep
     
        #___update accelerations & Potential Energy___
        for n in self.bodies: 
            n.a_next=0 #creates the future acceleration parameter
            for m in self.bodies:
                if n==m: #a body doesn't interact with itself.
                    pass
                else:
                    self.calculate_Pe(n,m,G) #calculates the contribution of the mth body to the potential energy of the nth body and adds it to the total Pe
                    a_next = self.acceleration(n,m,G) #caclulate the future acceleration
                    n.a_next+= a_next
                    
        #___update velocity & Kinetic Energy__
        for n in self.bodies:
            Body.update_vel(self,dt, n)
            Body.calculate_Ke(self,n) #calculates the kinetic energy of the nth body.
            
        #__set parameters for new timestep__   
        for n in self.bodies: 
            n.apast=n.a
            n.a=n.a_next
            n.previous_y=n.r[1]
        
        
        #Energy Plot
        Simulation.energy_plot(self, time)
        
        #Distance Mars-Satelite
        Simulation.distance_mars_plot(self, time)
            
         
    def animate(self, i): #Animation function
        
        self.run_simulation(i) #update bodies
        for n in self.bodies:
            n.center = n.r  #centres the patches      
        return self.patches
        
    def createpatches(self): #created the patches and animates them
        fig = plt.figure()
        ax = plt.axes()
        self.patches=[] #created the patches list
        for n in self.bodies: #appends one patch for each body, the features of the patch are defined in the text files.
            self.patches.append(ax.add_patch(plt.Circle(n.r ,n.size , color = n.color, animated = True)))
        #set the figure parameters
        ax.axis('scaled')
        ax.set_xlim(-3e11,3e11)
        ax.set_ylim(-3e11, 3e11)
        ax.set_title("Animation")
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')  
        self.anim = FuncAnimation(fig, self.animate , frames = self.num_iterations, repeat = False, interval = 5, blit = True) #Animation function (Change interval to change speed of animation)
        
    def calculate_Pe(self,n,m,G): #calculates the contribution of the mth body to the potential energy of the nth body
        Pe= -G*n.mass*m.mass/np.linalg.norm((n.r - m.r))
        self.Pe_total += Pe/2 #adds he contribution to the total Pe, diving by two to avoid double counting pairs of planets.


    def calc_tot_energy(self): #calulate the total energy
        E=self.Ke_total+self.Pe_total #adds the energies
        return E

    
    def energy_plot(self, time):#Plot energy
        total_energy=Simulation.calc_tot_energy(self)
        #ENERGY ADD
        f = open("Energy.txt", "a")
        f.write(str(total_energy))
        f.write("\n")
        f.close()
        self.energy_list.append(total_energy)
        
        #ENERGY PLOT
        if time/(60*60*24)==(self.num_iterations-1): #PLOT ENERGY AFTER X DAYS (-1 as counter starts from 0)
            fig=plt.figure()
            ax = plt.axes()
            ax.set_title("Total energy of system [J] vs time [s] (24 hours timestep)")
            ax.set_xlabel('Time [s]')  
            ax.set_ylabel('Energy [J]') 
            plt.plot(self.time_list,self.energy_list)      
            plt.show()
    

 
    def distance_mars_plot(self, time): #Calculate & Plot distance Mars-Satelite
        distance_satelite_mars=self.bodies[4].r-self.bodies[5].r #X,Y Distance between mars object [4] & satellite object [5]
        self.satelite_distance.append(np.linalg.norm(distance_satelite_mars)) #Append magnitude distance
        

        if time/(60*60*24)==500: #PLOT DISTANCE AFTER 500 DAYS
            #Print minimum distance with corresponding time
            print("Minimum distance to Mars: " + str((min(self.satelite_distance))/10**6) +" million meters")
            index=(self.satelite_distance.index(min(self.satelite_distance)))
            print("Time to closest approach: " + str((self.time_list[index])/(60*60*24)) + " days")
            
            #Plot of distance Mars-Satelite vs time
            fig2=plt.figure()
            ax = plt.axes()
            ax.set_title("Distance of satellite to Mars [m] vs time[s]")
            ax.set_xlabel('Time [s]')  
            ax.set_ylabel('Distance [m]') 
            plt.plot(self.time_list,self.satelite_distance)
            plt.show()

        
def main():
    #Clear Energy file
    f = open("Energy.txt", "a")
    f.truncate(0)
    f.close()
    #Run program
    F= Simulation()
    F.initialize()
    F.createpatches()
main()
