# -*- coding: utf-8 -*
#2019/2/26 Xu_wenqiao transfer zone
#2017/08/06 LI Changsheng @nNanJing University
#2014-2015 Cai ShengYang @NanJing University
from yade import ymport,utils,pack, export, plot
import math,os
import numpy as np

def getBodies(ids,type):
	allIds = False
	if isinstance(ids,str) and ids.lower()=='all':
		ids=xrange(len(O.bodies))
		allIds = True
	bodies = []
	for i in ids:
		b = O.bodies[i]
		if not b: continue
		if not isinstance(b.shape,type):
			continue
		bodies.append(b)
	return bodies
def exportStress(ids='all',what=[],comment="comment",numLabel=None,useRef=False,name=str):
	CS1=[]
	CS2=[]
	CS3=[]
	SIGMA1=[]
	SIGMA2=[]
	SIGMA3=[]
	shear=[]
	SHEAR_STRESS=[]
	Volumetric_stress=[]
	TW=TesselationWrapper()
	TW.triangulate()	#compute regular Delaunay triangulation, don’t construct tesselation		
	TW.computeVolumes()	#will silently tesselate the packing, then compute volume of each Voronoi cell
	ten=bodyStressTensors()
	# get list of bodies to export
	bodies = getBodies(ids,Sphere)
	if not bodies: return
	nBodies = len(bodies)
	# output file
	print('asd')
	#fName = 'strain%d'%(O.iter)+'.vtk'
	outFile = open(name, 'a')

	# write radius
	outFile.write("SCALARS radius float 1\nLOOKUP_TABLE default\n")
	for b in bodies:
		#print(TW.volume(b.id))
		outFile.write("%.2f\n"%(b.shape.radius))
#	outFile.close()
	# writ#e additional data from 'what' param
	for name,command in what: # for each name...
		
		test = eval(command) # ... eval one example to see what type (float, Vector3, Matrix3) the result is ...
		#print(test)
		# ... and write appropriate header line and loop over all bodies and write appropriate vtk line(s)
		if isinstance(test,Matrix3):
			outFile.write("\nTENSORS %s double\n"%(name))
			for b in bodies:
				t = eval(command)
				outFile.write("%.2f %.2f %.2f\n%.2f %.2f %.2f\n%.2f %.2f %.2f\n\n"%(t[0,0],t[0,1],t[0,2],t[1,0],t[1,1],t[1,2],t[2,0],t[2,1],t[2,2]))
				#print(t)
				st=0.5*(t+np.transpose(t))
				I1=st[0,0]+st[1,1]+st[2,2]
				I2=st[0,0]*st[1,1]+st[0,0]*st[2,2]+st[1,1]*st[2,2]-st[0,1]**2-st[0,2]**2-st[1,2]**2
				I3=st[0,0]*st[1,1]*st[2,2]+2*st[0,1]*st[0,2]*st[1,2]-st[0,0]*(st[1,2]**2)-st[1,1]*(st[0,2]**2)-st[2,2]*(st[0,1]**2)
				shear_stress=np.sqrt(st[0,2]**2+st[0,1]**2+st[1,2]**2)
				print('shear_stress:'%s%shear_stress)
				Volumetric_stress.append(I1)
				SHEAR_STRESS.append(shear_stress)
				ast=st
				#print(J2)
				for i in range(3):
					ast[i,i]=ast[i,i]-I1/3.0 
				#print(ast)
				J1=0
				J2=((st[0,0]-st[1,1])**2+(st[2,2]-st[1,1])**2+(st[0,0]-st[2,2])**2+6*(st[0,1]**2+st[0,2]**2+st[1,2]**2))/6.0
				J3=np.linalg.det(ast)
				#print (I1,I2,I3,J1,J2,J3)
				if J2==0:
					b=0
				else:
					b=-sqrt(27)*J3/(2*(sqrt(J2))**3)
				#print repr(b)
				if b > 1:
					b=int(1)
				#print(J2)
				theta=math.acos(b)*1/3.0
				s1=2*sin(theta+2*math.pi/3.0)*sqrt(J2)/sqrt(3.0)
				s2=2.0*sqrt(J2)/sqrt(3.0)*sin(theta)
				s3=2*sqrt(J2)/sqrt(3.0)*sin(theta-2*math.pi/3.0)
				sigma1='%.2f'%(I1/3+s1)
				sigma2='%.2f'%(I1/3+s2)
				sigma3='%.2f'%(I1/3+s3)
				#print(theta,s1,s2,s3)
				CS1.append('%.2f'%s1)
				CS2.append('%.2f'%s2)
				CS3.append('%.2f'%s3)
				CS=zip(CS1,CS2,CS3)
				shear.append((s1-s3)/2.0)
				SIGMA1.append(sigma1)
				SIGMA2.append(sigma2)
				SIGMA3.append(sigma3)
				SIGMA=zip(SIGMA1,SIGMA2,SIGMA3)
			#outFile.write("\nVECTORS CONSTANT_S float\n")
			#for i in CS:
			#	k=' '.join([str(j) for j in i])
			#	outFile.write(k+"\n")
			outFile.write("\nVECTORS SIGMA float\n")
			for i in SIGMA:
				k=' '.join([str(j) for j in i])
				outFile.write(k+"\n")
			outFile.write("SCALARS Max_Shear float 1\nLOOKUP_TABLE default\n")
			for i in shear:
				outFile.write("%.2f\n"%(i))
			outFile.write("SCALARS Shear_Stress float 1\nLOOKUP_TABLE default\n")
			for i in SHEAR_STRESS:
				outFile.write("%.2f\n"%(i))
			outFile.write("SCALARS Volumetric_Stress float 1\nLOOKUP_TABLE default\n")
			for i in Volumetric_stress:
				outFile.write("%.2f\n"%(i))
	outFile.close()

O.run(800000,True)

