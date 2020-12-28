#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 28 December 2020 (update)

This source code is provided by Richard J Smith 'as is' and 'with all faults'. The provider makes no 
representations or warranties of any kind concerning the safety, suitability, inaccuracies, 
typographical errors, or other harmful components of this software.
"""

import matplotlib.pyplot as plt
import numpy as np
from pyXSteam.XSteam import XSteam

steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS)

print('Rankine superheat cycle analysis with 1 closed feedheater')

PowerOutput = 100 #MW electrical generation
p1 = 0.2 #condenser pressure (bar)
p2 = 160 #pump 1 and 2 discharge pressure (bar)
p61 = 5 #extraction pressure in bar
p3 = 160 #feedwater pressure (bar)
p4 = 160 #main steam pressure (bar)

s1 = steamTable.sL_p(p1)
T1 = steamTable.t_ps(p1, s1)
h1 = steamTable.hL_p(p1)
print('\nPoint 1 - Condenser outlet before pump 1')
print(f"P1: {round(float(p1),1)} bar")
print(f"T1: {round(float(T1),1)} degC")
print(f"H1: {round(float(h1),1)} kJ/kg")
print(f"S1: {round(float(s1),3)} kJ/kg K")

v1 = 1/steamTable.rhoL_p(p1)*100
w_p1 = v1*(p3-p1)
print(f"Work required by pump 1: {round(float(w_p1),2)} kJ/kg")

print('\nPoint 2')
h2 = h1+w_p1
T2 = steamTable.t_ph(p2, h2)
s2 = s1
print(f"P2: {round(float(p2),1)} bar")
print(f"T2: {round(float(T2),1)} degC")
print(f"H2: {round(float(h2),1)} kJ/kg")
print(f"S2: {round(float(s2),3)} kJ/kg K")

p21 = p61
p23 = p3
v2 = 1/steamTable.rhoL_p(p21)*100
h21 = steamTable.hL_p(p21)
T21 = steamTable.tsat_p(p21)
s21 = steamTable.sL_p(p21)
print('\nPoint 21 - feedheater drain outlet before pump 2')
print(f"P21: {round(float(p21),1)} bar")
print(f"T21: {round(float(T21),1)} degC")
print(f"H21: {round(float(h21),1)} kJ/kg")
print(f"S21: {round(float(s21),3)} kJ/kg K")

w_p2 = v2*(p23-p21)
print(f"Work required by pump 2: {round(float(w_p2),2)} kJ/kg")

h23 = h21+w_p2
print('\nPoint 23 - feedheater drain outlet after pump 2')
print(f"P23: {round(float(p23),1)} bar")
print(f"T23: {round(float(T21),1)} degC")
print(f"H23: {round(float(h23),1)} kJ/kg")

#feedwater line conditions after closed feedheater
t23 = steamTable.tsat_p(p61) #saturation temp of feedheater drain line
h22 = steamTable.h_pt(p3, t23)
print('\nPoint 22 feed heater outlet')
print(f"P22: {round(float(p2),1)} bar")
print(f"T22: {round(float(t23),1)} degC") #XXXXXX check
print(f"H22: {round(float(h22),1)} kJ/kg")

#boiler evaporator outlet before superheating conditions
h4 = steamTable.hV_p(p4)
s4 = steamTable.sV_p(p4)
T4 = steamTable.tsat_p(p4)
print('\nPoint 4')
print(f"P4: {round(float(p3),1)} bar")
print(f"T4: {round(float(T4),1)} degC")
print(f"H4: {round(float(h4),1)} kJ/kg")
print(f"S4: {round(float(s4),3)} kJ/kg K")

#turbine inlet conditions
p5 = p4
T5 = 540
h5 = steamTable.h_pt(p5, T5)
s5 = steamTable.s_pt(p5, T5)
print('\nPoint 5 - main steam conditions')
print(f"P5: {round(float(p5),1)} bar")
print(f"T5: {round(float(T5),1)} degC")
print(f"H5: {round(float(h5),1)} kJ/kg")
print(f"S5: {round(float(s5),3)} kJ/kg K")

#turbine extraction point conditions
s61 = s5 #assume isentropic expansion in turbine
T61 = steamTable.t_ps(p61,s61)
x61 = (s61 - steamTable.sL_p(p61))/(steamTable.sV_p(p61)-steamTable.sL_p(p61))
h61 = steamTable.h_px(p61,x61)

#h31 = steamTable.h_pt(p31,T31) #XXXXXXXXXXXXXx need to fix this value
print('\nPoint 61 - extraction steam point (also point 63 and 7 the same values)')
print(f"P61: {round(float(p61),1)} bar")
print(f"T61: {round(float(T61),1)} degC")
print(f"H61: {round(float(h61),1)} kJ/kg")
print(f"S61: {round(float(s61),3)} kJ/kg K")
print(f"x61: {round(float(x61),2)} ")

#conditions in 2nd half of steam turbine
h7 = h61

#turbine outlet conditions
p8 = p1
s8 = s5 #assume isentropic expansion in turbine
T8 = steamTable.t_ps(p8, s8)
x8 = steamTable.x_ps(p8, s8)
h8 = steamTable.h_px(p8, x8)
print('\nPoint 4 - turbine exhaust conditions')
print(f"P8: {round(float(p8),1)} bar")
print(f"T8: {round(float(T8),1)} degC")
print(f"H8: {round(float(h8),1)} kJ/kg")
print(f"S8: {round(float(s8),3)} kJ/kg K")
print(f"x8: {round(float(x8),4)} ")

# differing mass flow rates at various points
mbDIVmc = ((h21-h61)/(h2-h22))
print(f"\nmbDIVmc mass flow ratio: {round(float(mbDIVmc),4)} ")

mbDIVma = mbDIVmc/(mbDIVmc+1)
print(f"mbDIVma mass flow ratio: {round(float(mbDIVma),4)} ")

mcDIVma = mbDIVma/mbDIVmc
print(f"mcDIVma mass flow ratio: {round(float(mcDIVma),4)} ")

#conditions after mixing chamber
h24 = (mbDIVma*h22)+((1-mbDIVma)*h23)
p24 = p2
T24 = t23
s24 = steamTable.s_pt(p24, T24)
print('\nPoint 24 - feedwater before economiser')
print(f"T24: {round(float(T24),1)} degC")
print(f"p24: {round(float(p24),1)} bar")
print(f"H24: {round(float(h24),1)} kJ/kg")
print(f"S24: {round(float(s24),3)} kJ/kg K")

#boiler drum inlet conditions
h3 = (mbDIVma*h22)+((1-mbDIVma)*h23)
s3 = steamTable.sL_p(p3)
T3 = steamTable.tsat_p(p3)

print('\nPoint 3')
print(f"P3: {round(float(p2),1)} bar")
print(f"T3: {round(float(T3),1)} degC")
print(f"H3: {round(float(h3),1)} kJ/kg")
print(f"S3: {round(float(s3),3)} kJ/kg K")

print('\nSummary')
q_H = (h5-h24)
print(f"Heat input by boiler: {round(float(q_H),1)} kJ/kg")

q_L = (h1-h8)
print(f"Heat rejected to condenser: {round(float(q_L),1)} kJ/kg")

w_HPt = (1*(h5-h61))+(mbDIVma*(h7-h8))
print(f"Work generated by turbine: {round(float(w_HPt),1)} kJ/kg")

Wnett = (h5-h61)+(mbDIVma*(h7-h8))-(mcDIVma*w_p2)-(mbDIVma*w_p1)
print(f"Thermal efficiency is: {round(float(Wnett),1)} kJ/kg")

eta_th = Wnett/(h5-h24)*100
print(f"Thermal efficiency is: {round(float(eta_th),1)} %")

HRcycle = 3600*100/eta_th
print(f"HR rankine cycle: {round(float(HRcycle),1)} kJ/kWh")

MassFlow = PowerOutput*1000/Wnett
print(f"Required steam flow: {round(float(MassFlow),1)} kg/s")

font = {'family' : 'Times New Roman',
        'size'   : 22}

plt.figure(figsize=(15,10))
plt.title('T-s Diagram - Rankine Superheat Cycle (1 closed feed heater)')
plt.rc('font', **font)

plt.ylabel('Temperature (C)')
plt.xlabel('Entropy (s)')
plt.xlim(-2,10)
plt.ylim(0,600)

T = np.linspace(0, 373.945, 400) # range of temperatures
# saturated vapor and liquid entropy lines
svap = [s for s in [steamTable.sL_t(t) for t in T]]
sliq = [s for s in [steamTable.sV_t(t) for t in T]]

plt.plot(svap, T, 'b-', linewidth=2.0)
plt.plot(sliq, T, 'r-', linewidth=2.0)

plt.plot([s1, s2, s24, s3, s4, s5, s8, s1],[T1, T2, T24, T3, T4, T5, T8, T1], 'black', linewidth=2.0)
plt.plot([s61, s21],[T61, T21], 'green', linewidth=2.0) #feed heater line

plt.savefig('images/05_rankine_superheat_cycle-closed_heater-TSdiagram.png')

CWflow = 5000 #kg/s

QL = (MassFlow* mbDIVma) * q_L*-1
print(f"Heat rejected to condenser (total): {round(float(QL),1)} kJ")

DeltaTcw = QL/(CWflow * 4.18)
print(f"Temperature increase of cooling water: {round(float(DeltaTcw),1)} Deg C")
