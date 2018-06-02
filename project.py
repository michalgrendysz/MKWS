import cantera as ct
import csv

cti_file='nasa.cti'

m=0.002 #kg
area=0.05 #m^2
mpiston=2.0 #kg
tstep=0.001 #s
lengthstart=0.2 #m
lengthstop=0.4 #m

air = ct.Solution(cti_file,'air')
air.TP= 300.0, 1.0*ct.one_atm

KNO3 = ct.Solution(cti_file,'KNO3')
KNO3.TP= 300.0, 1.0*ct.one_atm
q1=ct.Quantity(KNO3, mass=0.75*m)

S = ct.Solution(cti_file,'S')
S.TP=300.0, 1.0*ct.one_atm
q2=ct.Quantity(S, mass=0.1*m)

C = ct.Solution(cti_file,'C')
C.TP=300.0, 1.0*ct.one_atm
q3=ct.Quantity(C, mass=0.15*m)

products = ct.Solution(cti_file,'products')
products.TP=300.0, 1.0*ct.one_atm
q4=ct.Quantity(products, mass=0)

K2S=ct.Solution(cti_file,'K2S')
K2S.TP=300.0, 1.0*ct.one_atm
q5=ct.Quantity(K2S, mass=0)

inter = ct.Interface(cti_file,'surface',[q1,q2,q3,q4,q5])
inter.TP=300.0, 1.0*ct.one_atm

env=ct.Reservoir(air)

reactor=ct.Reactor(q1+q2+q3+q4+q5)
reactor.volume = lengthstart*area
ct.ReactorSurface(inter,reactor,A=100.0)

w=ct.Wall(reactor,env,A=area,K=tstep*area/mpiston)

sim=ct.ReactorNet([reactor,env])

print "Beginning simulation"

time=0.0
outfile=open('output.csv','w')
csvfile= csv.writer(outfile)
csvfile.writerow("time [s]","temperature [K]", "pressure [Pa]", "volume [m^3]", "velocity [m/s]")

print "Current simulation time:"

while time<120.0 and reactor.volume<area*lengthstop:
	if time==1.0:
		inter.TP=500.0,1.0*ct.one_atm
	csvfile.writerow(time,reactor.thermo.T,reactor.thermo.P,reactor.volume,w.velocity)
	print time+" s"
	time+=tstep
	sim.advance(time)

outfile.close()
print "Program has ended. The solution has been saved in output.csv"

                         
