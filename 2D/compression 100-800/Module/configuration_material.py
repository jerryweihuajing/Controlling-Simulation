# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 21:33:04 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Configuration-Material
"""

import math

#setting frict materials -----
fyoung = 8e9
fpoisson = 0.25
frictAng = 0 #0
fden = 2500

#setting rock materials -----
ryoung = 2e7 #csy: 2e7 fyj: 2e8
rpoisson = 0.25
rfrictAng = math.atan(0.6) #csy: 0.6 fyj: 0.3
rreps = 0.06
rden = 2500 #2500

#setting detachment materials ----- 
dyoung = 2e7 #csy: 2e7 fyj: 2e8
dpoisson = 0
dfrictAng = math.atan(0) 
dreps = 0.001
dden = 2100 #csy: 2100 fyj:2300

m_wall = O.materials.append(FrictMat(young = fyoung,
                                     poisson = fpoisson,
                                     frictionAngle = frictAng,
                                     density = fden))
                                                                       
m_rock = O.materials.append(CpmMat(young = ryoung,
                                   poisson = rpoisson,
                                   frictionAngle = rfrictAng,
                                   epsCrackOnset = rreps,
                                   density = rden,
                                   relDuctility = 0))

m_detachment = O.materials.append(CpmMat(young = dyoung,
                                         poisson = dpoisson,
                                         frictionAngle = dfrictAng,
                                         epsCrackOnset = dreps,
                                         density = dden,
                                         relDuctility = 0))

#uplift
m_uplift = O.materials.append(CpmMat(young = 100*ryoung,
                                     poisson = rpoisson,
                                     frictionAngle = rfrictAng,
                                     epsCrackOnset = rreps,
                                     density = rden,
                                     relDuctility = 0))