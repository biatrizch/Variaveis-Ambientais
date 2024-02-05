#!/usr/bin/env/python
# -*- coding: iso-8859-9 -*-
#Esse programa lê arquivos de dados, particularmente da CETESB, e calcula as principais estatísticas
#Media anual, mensal, horaria, boxplot, histograma, percentil, maximas e minimas
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import StrMethodFormatter
from netCDF4 import Dataset
from matplotlib.ticker import AutoMinorLocator
	
# Initial variables
anoini = 2002
anofim = 2022

# Main variables
pp   = np.zeros((anofim+1-anoini,13,32,25))
uv   = np.zeros((anofim+1-anoini,13,32,25))
vv   = np.zeros((anofim+1-anoini,13,32,25))
nox  = np.zeros((anofim+1-anoini,13,32,25))
mp25 = np.zeros((anofim+1-anoini,13,32,25))
pr   = np.zeros((anofim+1-anoini,13,32,25))
ur   = np.zeros((anofim+1-anoini,13,32,25))
tp   = np.zeros((anofim+1-anoini,13,32,25))
rd   = np.zeros((anofim+1-anoini,13,32,25))

# Monthly averages
ppmonth = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
uvmonth = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
vvmonth = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
noxmonth = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
mp25month = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
prmonth = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
urmonth = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
tpmonth = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
rdmonth = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
# Hourly averages
pphour  = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
uvhour  = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
vvhour  = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
noxhour  = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
mp25hour  = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
prhour  = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
urhour  = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
tphour  = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
rdhour  = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
# All
pptudo = []
uvtudo = []
vvtudo = []
noxtudo = []
mp25tudo = []
prtudo = []
urtudo = []
tptudo = []
rdtudo = []

ultdia = [0,31,28,31,30,31,30,31,31,30,31,30,31]

# Initiate arrays with nan
pp[:][:][:][:]   = np.nan
uv[:][:][:][:]   = np.nan
vv[:][:][:][:]   = np.nan
nox[:][:][:][:]  = np.nan
mp25[:][:][:][:] = np.nan
pr[:][:][:][:]   = np.nan
ur[:][:][:][:]   = np.nan
tp[:][:][:][:]   = np.nan
rd[:][:][:][:]   = np.nan

# Abre arquivos de entrada e lê dados de todos os anos
for an in range(anoini,anofim+1): 
	nomearq = str(an)+'.csv'
	print (nomearq)
	entra = open(nomearq,'r',encoding='iso-8859-9')
	ct = 0
	for line in entra:
		ct += 1
#		print(ct)
		if line[:4] != 'Esta' and line[2:6] != 'digo' and line[:4] != 'Data' and line[:4] != 'Data' and line[:4] != 'Nome' and len(line) > 1:
			print (line)
			EST,DATAHORA,VV10,VV2,DV,RAD,REFL,GRD,UR,TP,TS03,TS06,TS18,PRESS,PRECIP = line.split(';')
			DATA,HORA = DATAHORA.split(' ')
			if len(DATA) > 0 and len(HORA) > 0:
				axano,axmes,axdia = DATA.split('-')
				axhora,axminutos,segundos  = HORA.split(':')
				dd = int(axdia)
				mm = int(axmes)
				aa = int(axano)
				hh = int(axhora)
				if hh == 0:
					hh = 24
					dd -= 1
					if dd == 0:
						mm -= 1
						if mm == 0:
							mm = 12
							aa -= 1
						dd = ultdia[mm]
						if mm == 2 and (aa == 2012 or aa == 2016 or aa == 2020):
							dd += 1
				if len(TP) > 0:
					if TP != np.nan and TP != '\\N':
						if float(TP) < 50. and float(TP) > -10.:
							tp[aa-anoini][mm][dd][hh] = float(TP)
							tpmonth[mm].append(float(TP))
							tphour[hh].append(float(TP))
							tptudo.append(float(TP))
							if float(TP) > 40.:
								print(ct,line)
				if len(UR) > 0:
					if UR != np.nan:
						if float(UR) > 0.:
							ur[aa-anoini][mm][dd][hh] = float(UR)
							urmonth[mm].append(float(UR))
							urhour[hh].append(float(UR))
							urtudo.append(float(UR))
				if len(PRESS) > 0:
					if PRESS != np.nan and PRESS != '\\N':
						if float(PRESS) > 0. and float(PRESS) < 1050.:
							pr[aa-anoini][mm][dd][hh] = float(PRESS)
							prmonth[mm].append(float(PRESS))
							prhour[hh].append(float(PRESS))
							prtudo.append(float(PRESS))
				axvv =np.nan
				axdv =np.nan
				if len(VV2) > 0:
					if VV2 != np.nan:
						axvv = float(VV2)
				if len(DV) > 0 and DV != '\n':
					if DV != np.nan and DV != '\n':
						axdv = float(DV)
				if axvv != np.nan and axdv != np.nan and axvv > 0.:
					axu = -abs(axvv)*math.sin((math.pi/180.)*axdv)
					axv = -abs(axvv)*math.cos((math.pi/180.)*axdv)
					uv[aa-anoini][mm][dd][hh] = axu
					uvmonth[mm].append(axu)
					uvhour[hh].append(axu)
					uvtudo.append(axu)
					vv[aa-anoini][mm][dd][hh] = axv
					vvmonth[mm].append(axv)
					vvhour[hh].append(axv)
					vvtudo.append(axv)
				if len(RAD) > 0 and RAD != '\n':
					if RAD != np.nan and RAD != '\n':
						if float(RAD) >= 0. and float(RAD) < 1350.:
							rd[aa-anoini][mm][dd][hh] = float(RAD)
							rdmonth[mm].append(float(RAD))
							rdhour[hh].append(float(RAD))
							rdtudo.append(float(RAD))

				if len(PRECIP) > 0 and PRECIP != '\n':
					if PRECIP != np.nan and PRECIP != '\n':
						if float(PRECIP) >= 0.:
							pp[aa-anoini][mm][dd][hh] = float(PRECIP)
							ppmonth[mm].append(float(PRECIP))
							pphour[hh].append(float(PRECIP))
							pptudo.append(float(PRECIP))
	entra.close()
# Report
report = open('Relat-CIIAGRO-Rib-Preto.txt','w')
report.write('Relatório das variáveis medidas pela CIIAGRO em Ribeirão Preto (lat , lon )\n')
report.write('Período: de '+str(anoini)+' a '+str(anofim)+'\n')
report.write(' \n')

# Annual averages
ppyearave = []
ppyearstd = []
noxyearave = []
noxyearstd = []
mp25yearave = []
mp25yearstd = []
ppyearave = []
ppyearstd = []
tpyearave = []
tpyearstd = []
uryearave = []
uryearstd = []
rdyearave = []
rdyearstd = []
uvyearave = []
uvyearstd = []
vvyearave = []
vvyearstd = []
pryearave = []
pryearstd = []
report.write('Medias anuais \n')
for an in range(anoini,anofim+1):
	report.write('PRECIP-> '+str(an)+' '+str(np.nansum(pp[an-anoini][:][:][:]))+' '+str(pp[an-anoini].size-np.count_nonzero(np.isnan(pp[an-anoini])))+'\n')
	ppyearave.append(np.nansum(pp[an-anoini][:][:][:]))
	report.write('TP-> '+str(an)+' '+str(np.nanmean(tp[an-anoini][:][:][:]))+' '+str(tp[an-anoini].size-np.count_nonzero(np.isnan(tp[an-anoini])))+' '+str(np.nanstd(tp[an-anoini][:][:][:]))+'\n')
	tpyearave.append(np.nanmean(tp[an-anoini][:][:][:]))
	tpyearstd.append(np.nanstd(tp[an-anoini][:][:][:]))
	report.write('UR-> '+str(an)+' '+str(np.nanmean(ur[an-anoini][:][:][:]))+' '+str(ur[an-anoini].size-np.count_nonzero(np.isnan(ur[an-anoini])))+' '+str(np.nanstd(ur[an-anoini][:][:][:]))+'\n')
	uryearave.append(np.nanmean(ur[an-anoini][:][:][:]))
	uryearstd.append(np.nanstd(ur[an-anoini][:][:][:]))
	report.write('Rad-> '+str(an)+' '+str(np.nanmean(rd[an-anoini][:][:][:]))+' '+str(rd[an-anoini].size-np.count_nonzero(np.isnan(rd[an-anoini])))+' '+str(np.nanstd(rd[an-anoini][:][:][:]))+'\n')
	rdyearave.append(np.nanmean(rd[an-anoini][:][:][:]))
	rdyearstd.append(np.nanstd(rd[an-anoini][:][:][:]))
	report.write('U-> '+str(an)+' '+str(np.nanmean(uv[an-anoini][:][:][:]))+' '+str(uv[an-anoini].size-np.count_nonzero(np.isnan(uv[an-anoini])))+' '+str(np.nanstd(uv[an-anoini][:][:][:]))+'\n')
	uvyearave.append(np.nanmean(uv[an-anoini][:][:][:]))
	uvyearstd.append(np.nanstd(uv[an-anoini][:][:][:]))
	report.write('V-> '+str(an)+' '+str(np.nanmean(vv[an-anoini][:][:][:]))+' '+str(vv[an-anoini].size-np.count_nonzero(np.isnan(vv[an-anoini])))+' '+str(np.nanstd(vv[an-anoini][:][:][:]))+'\n')
	vvyearave.append(np.nanmean(vv[an-anoini][:][:][:]))
	vvyearstd.append(np.nanstd(vv[an-anoini][:][:][:]))
	report.write('Press > '+str(an)+' '+str(np.nanmean(pr[an-anoini][:][:][:]))+' '+str(pr[an-anoini].size-np.count_nonzero(np.isnan(pr[an-anoini])))+' '+str(np.nanstd(pr[an-anoini][:][:][:]))+'\n')
	pryearave.append(np.nanmean(pr[an-anoini][:][:][:]))
	pryearstd.append(np.nanstd(pr[an-anoini][:][:][:]))

#Monthly averages
ppmonthave = []
ppmonthstd = []
noxmonthave = []
noxmonthstd = []
mp25monthave = []
mp25monthstd = []
tpmonthave = []
tpmonthstd = []
urmonthave = []
urmonthstd = []
rdmonthave = []
rdmonthstd = []
prmonthave = []
prmonthstd = []
uvmonthave = []
uvmonthstd = []
vvmonthave = []
vvmonthstd = []
report.write('Medias mensais \n')
for mm in range (1,13):
	report.write('PRECIP-> '+str(mm)+' '+str(np.sum(ppmonth[mm]))+' medidas validas: '+str(len(ppmonth[mm]))+'\n')
	ppmonthave.append(np.sum(ppmonth[mm]))
	report.write('TP-> '+str(mm)+' '+str(np.mean(tpmonth[mm]))+' medidas validas: '+str(len(tpmonth[mm]))+' '+str(np.std(tpmonth[mm]))+'\n')
	tpmonthave.append(np.mean(tpmonth[mm]))
	tpmonthstd.append(np.std(tpmonth[mm]))
	report.write('UR-> '+str(mm)+' '+str(np.mean(urmonth[mm]))+' medidas validas: '+str(len(urmonth[mm]))+' '+str(np.std(urmonth[mm]))+'\n')
	urmonthave.append(np.mean(urmonth[mm]))
	urmonthstd.append(np.std(urmonth[mm]))
	report.write('Rad-> '+str(mm)+' '+str(np.mean(rdmonth[mm]))+' medidas validas: '+str(len(rdmonth[mm]))+' '+str(np.std(rdmonth[mm]))+'\n')
	rdmonthave.append(np.mean(rdmonth[mm]))
	rdmonthstd.append(np.std(rdmonth[mm]))
	report.write('U-> '+str(mm)+' '+str(np.mean(uvmonth[mm]))+' medidas validas: '+str(len(uvmonth[mm]))+' '+str(np.std(uvmonth[mm]))+'\n')
	uvmonthave.append(np.mean(uvmonth[mm]))
	uvmonthstd.append(np.std(uvmonth[mm]))
	report.write('V-> '+str(mm)+' '+str(np.mean(vvmonth[mm]))+' medidas validas: '+str(len(vvmonth[mm]))+' '+str(np.std(vvmonth[mm]))+'\n')
	vvmonthave.append(np.mean(vvmonth[mm]))
	vvmonthstd.append(np.std(vvmonth[mm]))
	report.write('Press-> '+str(mm)+' '+str(np.mean(prmonth[mm]))+' medidas validas: '+str(len(prmonth[mm]))+' '+str(np.std(prmonth[mm]))+'\n')
	prmonthave.append(np.mean(prmonth[mm]))
	prmonthstd.append(np.std(prmonth[mm]))

#Hourly averages
noxhourave = []
noxhourstd = []
mp25hourave = []
mp25hourstd = []
tphourave = []
tphourstd = []
urhourave = []
urhourstd = []
rdhourave = []
rdhourstd = []
uvhourave = []
uvhourstd = []
vvhourave = []
vvhourstd = []
prhourave = []
prhourstd = []
report.write('Medias horarias \n')
for hh in range (1,25):
	report.write('TP-> '+str(hh)+' '+str(np.mean(tphour[hh]))+' medidas validas: '+str(len(tphour[hh]))+' '+str(np.std(tphour[hh]))+'\n')
	tphourave.append(np.mean(tphour[hh]))
	tphourstd.append(np.std(tphour[hh]))
	report.write('UR-> '+str(hh)+' '+str(np.mean(urhour[hh]))+' medidas validas: '+str(len(urhour[hh]))+' '+str(np.std(urhour[hh]))+'\n')
	urhourave.append(np.mean(urhour[hh]))
	urhourstd.append(np.std(urhour[hh]))
	report.write('Rad-> '+str(hh)+' '+str(np.mean(rdhour[hh]))+' medidas validas: '+str(len(rdhour[hh]))+' '+str(np.std(rdhour[hh]))+'\n')
	rdhourave.append(np.mean(rdhour[hh]))
	rdhourstd.append(np.std(rdhour[hh]))
	report.write('U-> '+str(hh)+' '+str(np.mean(uvhour[hh]))+' medidas validas: '+str(len(uvhour[hh]))+' '+str(np.std(uvhour[hh]))+'\n')
	uvhourave.append(np.mean(uvhour[hh]))
	uvhourstd.append(np.std(uvhour[hh]))
	report.write('V-> '+str(hh)+' '+str(np.mean(vvhour[hh]))+' medidas validas: '+str(len(vvhour[hh]))+' '+str(np.std(vvhour[hh]))+'\n')
	vvhourave.append(np.mean(vvhour[hh]))
	vvhourstd.append(np.std(vvhour[hh]))
	report.write('Press-> '+str(hh)+' '+str(np.mean(prhour[hh]))+' medidas validas: '+str(len(prhour[hh]))+' '+str(np.std(prhour[hh]))+'\n')
	prhourave.append(np.mean(prhour[hh]))
	prhourstd.append(np.std(prhour[hh]))

# Graphics
years = np.arange(anoini,anofim+1)
months = np.arange(1,13)
hours = np.arange(1,25)
# Precipitation
# Averages
fig,axs = plt.subplots(2,2)
axs[0,0].plot(years,ppyearave)
axs[0,1].plot(months,ppmonthave)
	
# Histogram
#valores,bandejas = np.histogram(o3tudo,bins = 10)
axs[1,1].hist(pptudo)
plt.savefig('Precipitation.png')
plt.show()
plt.close()

# Temperature
# Averages
fig,axs = plt.subplots(2,2)
axs[0,0].plot(years,tpyearave)
axs[0,0].errorbar(years,tpyearave,tpyearstd)
axs[0,1].plot(months,tpmonthave)
axs[0,1].errorbar(months,tpmonthave,tpmonthstd)
axs[1,0].plot(hours,tphourave)
axs[1,0].errorbar(hours,tphourave,tphourstd)
	
# Histogram
#valores,bandejas = np.histogram(o3tudo,bins = 10)
axs[1,1].hist(tptudo)
plt.savefig('Temperature.png')
plt.show()
plt.close()

# Relative humidity
# Averages
fig,axs = plt.subplots(2,2)
axs[0,0].plot(years,uryearave)
axs[0,0].errorbar(years,uryearave,uryearstd)
axs[0,1].plot(months,urmonthave)
axs[0,1].errorbar(months,urmonthave,urmonthstd)
axs[1,0].plot(hours,urhourave)
axs[1,0].errorbar(hours,urhourave,urhourstd)
	
# Histogram
#valores,bandejas = np.histogram(o 3tudo,bins = 10)
axs[1,1].hist(urtudo)
plt.savefig('RelativeHumidity.png')
plt.show()
plt.close()

# Radiation
# Averages
fig,axs = plt.subplots(2,2)
axs[0,0].plot(years,rdyearave)
axs[0,0].errorbar(years,rdyearave,rdyearstd)
axs[0,1].plot(months,rdmonthave)
axs[0,1].errorbar(months,rdmonthave,rdmonthstd)
axs[1,0].plot(hours,rdhourave)
axs[1,0].errorbar(hours,rdhourave,rdhourstd)
	
# Histogram
#valores,bandejas = np.histogram(o3tudo,bins = 10)
axs[1,1].hist(rdtudo)
plt.savefig('Radiation.png')
plt.show()
plt.close()

# Zonal component
# Averages
fig,axs = plt.subplots(2,2)
axs[0,0].plot(years,uvyearave)
axs[0,0].errorbar(years,uvyearave,uvyearstd)
axs[0,1].plot(months,uvmonthave)
axs[0,1].errorbar(months,uvmonthave,uvmonthstd)
axs[1,0].plot(hours,uvhourave)
axs[1,0].errorbar(hours,uvhourave,uvhourstd)
	
# Histogram
#valores,bandejas = np.histogram(o3tudo,bins = 10)
axs[1,1].hist(uvtudo)
plt.savefig('Zonal.png')
plt.show()
plt.close()

# Meridional component
# Averages
fig,axs = plt.subplots(2,2)
axs[0,0].plot(years,vvyearave)
axs[0,0].errorbar(years,vvyearave,vvyearstd)
axs[0,1].plot(months,vvmonthave)
axs[0,1].errorbar(months,vvmonthave,vvmonthstd)
axs[1,0].plot(hours,vvhourave)
axs[1,0].errorbar(hours,vvhourave,vvhourstd)
	
# Histogram
#valores,bandejas = np.histogram(o3tudo,bins = 10)
axs[1,1].hist(vvtudo)
plt.savefig('Meridional.png')
plt.show()
plt.close()

# Pressure
# Averages
fig,axs = plt.subplots(2,2)
axs[0,0].plot(years,pryearave)
axs[0,0].errorbar(years,pryearave,pryearstd)
axs[0,1].plot(months,prmonthave)
axs[0,1].errorbar(months,prmonthave,prmonthstd)
axs[1,0].plot(hours,prhourave)
axs[1,0].errorbar(hours,prhourave,prhourstd)
	
# Histogram
#valores,bandejas = np.histogram(o3tudo,bins = 10)
axs[1,1].hist(prtudo)
plt.savefig('Pressure.png')
plt.show()
plt.close()

# Percentil
report.write('Percentil 95 \n')
report.write('Precipitacao: '+str(np.percentile(pptudo,95))+'\n')
report.write('Temp: '+str(np.percentile(tptudo,95))+'\n')
report.write('UR: '+str(np.percentile(urtudo,95))+'\n')
report.write('Rad: '+str(np.percentile(rdtudo,95))+'\n')
report.write('U: '+str(np.percentile(uvtudo,95))+'\n')
report.write('V: '+str(np.percentile(vvtudo,95))+'\n')
report.write('Press: '+str(np.percentile(prtudo,95))+'\n')
# Maximum
report.write('Maximo \n')
report.write('Precipitacao: '+str(np.amax(pptudo))+'\n')
report.write('Temp: '+str(np.amax(tptudo))+'\n')
report.write('UR: '+str(np.amax(urtudo))+'\n')
report.write('Rad: '+str(np.amax(rdtudo))+'\n')
report.write('U: '+str(np.amax(uvtudo))+'\n')
report.write('V: '+str(np.amax(vvtudo))+'\n')
report.write('Press: '+str(np.amax(prtudo))+'\n')
#for i in range(len(noxtudo)):
#	if noxtudo[i] > 300:
#		print(noxtudo[i])
report.close()

