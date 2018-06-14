import cantera as ct
import csv

cti_file='~/Dokumenty/nasa.cti'

mgp=0.002 #[kg] mass of gunpowder
area=0.05 #[m^2] frontal area of a piston
mpiston=2.0 #[kg] mass of the piston
tstep=0.001 #[s] time step of a simulation
lengthstart=0.2 #[m] initial length of a reactor
lengthstop=0.4 #[m] final length of a reactor

air = ct.Solution(cti_file,'gas')
air.TP= 300.0, 1.0*ct.one_atm

KNO3 = ct.Solution(cti_file,'ox')
KNO3.TP= 300.0, 1.0*ct.one_atm
q1=ct.Quantity(KNO3, mass=0.75*mgp)

S = ct.Solution(cti_file,'sulfur')
S.TP=300.0, 1.0*ct.one_atm
q2=ct.Quantity(S, mass=0.1*mgp)

C = ct.Solution(cti_file,'carbon')
C.TP=300.0, 1.0*ct.one_atm
q3=ct.Quantity(C, mass=0.15*mgp)

products = ct.Solution(cti_file,'products')
products.TP=300.0, 1.0*ct.one_atm
q4=ct.Quantity(products, mass=0)

K2S=ct.Solution(cti_file,'potsulf')
K2S.TP=300.0, 1.0*ct.one_atm
q5=ct.Quantity(K2S, mass=0)

inter = ct.Interface(cti_file,'surface',[q1,q2,q3,q4,q5])
inter.TP=500.0, 1.0*ct.one_atm

env=ct.Reservoir(air)

reactor=ct.Reactor(q1+q2+q3+q4+q5)
reactor.volume = lengthstart*area
ct.ReactorSurface(surface,reactor,A=(mgp/(1700))*(6/10^-3))

w=ct.Wall(reactor,env,A=area,K=tstep*area/mpiston)

sim=ct.ReactorNet([reactor,env])

print "Beginning simulation"

time=0.0
outfile=open('output.csv','w')
csvfile= csv.writer(outfile)
csvfile.writerow("time [s]","temperature [K]", "pressure [Pa]", "volume [m^3]", "velocity [m/s]")

print "Current simulation time:"

while time<120.0 and reactor.volume<area*lengthstop:
	csvfile.writerow(time,reactor.thermo.T,reactor.thermo.P,reactor.volume,w.velocity)
	print time+" s"
	time+=tstep
	sim.advance(time)

outfile.close()
print "Program has ended. The solution has been saved in output.csv"

                         
