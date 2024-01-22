#Graphs Show amount of neutrons reflected, captured and transmitted (R,A,T)
#you will be seeing R,A,T repeated throughout the code.
#If this code is executed properly you should get 3 distributions of probabilities for each
#of the situations mentioned above.

import numpy as np
rdm=np.random
import matplotlib.pyplot as plt

#############   Fonction principale     ######################################
def particule(pa,ps,lam,d,N):
    sr,sa,st=0,0,0  #compteurs de refelxion,absorbtion et transmission
    for i in range(N):  #boucle sur les differents neutrons
        x,costheta=0.,1. #initialisation du neutron
        while True: #boucle conditionnelle sur déplacement...
            r=rdm.random()  #nombre random pour calculer l
            l=-lam*np.log(r)    
            x+=(l*costheta)
            if x<0:     #reflexion
                sr+=1
                break
            elif x>d:   #transmission
                st+=1
                break
            else:       #neutron encore dans la plaque
                r2=rdm.random()
                if r2<pa:    #absobtion dans la plaque
                    sa+=1
                    break
                elif pa<=r2<pa+ps:   #reflexion dans la plaque
                    costheta=1-2*r  
    R,A,T=sr/N,sa/N,st/N
    #print(R,A,T)
    sigR=np.sqrt((R*(1-R))/(N-1))
    sigA=np.sqrt((A*(1-A))/(N-1))
    sigT=np.sqrt((T*(1-T))/(N-1))
    return R,A,T,sigR,sigA,sigT
    
############### MAIN #########################################################
            
itermax=500     #nombre d'iterations max
tabR=np.zeros(itermax)#tableaux R,A,T
tabA=np.zeros(itermax)
tabT=np.zeros(itermax)

for i in range(0,itermax):
    R,A,T,sigR,sigA,sigT=particule(0.2,0.1, 0.2, 1, 1000)
    tabR[i]=R
    tabA[i]=A
    tabT[i]=T
    
#histogrammes
plt.figure(1)
plt.subplot(1,3,1)  #histogramme R
plt.hist(tabR,bins=23)
plt.ylabel("Nombre de neutrons")
plt.xlabel("probabilité d'être réfléchi")
plt.subplot(1,3,2)  #histogramme A
plt.hist(tabA,bins=23,color="yellow")
plt.xlabel("probabilité d'être absorbé")
plt.subplot(1,3,3)  #histogramme T
plt.hist(tabT,bins=23,color="red")
plt.xlabel("probabilité d'être transmis")
plt.savefig("histogrammes.png")

                     
pa=0.2
ps_arr=np.arange(0,1.1-pa,0.1)    #tableau des val de ps
tabR=np.zeros(ps_arr.size)  #tableau pour valeurs de R,A,T
tabA=np.zeros(ps_arr.size)
tabT=np.zeros(ps_arr.size)
tabsigR=np.zeros(ps_arr.size)   #tableau pour incertitudes
tabsigA=np.zeros(ps_arr.size)
tabsigT=np.zeros(ps_arr.size)

k=0 #compteur
while k<ps_arr.size:
    R,A,T,sigR,sigA,sigT=particule(0.2, ps_arr[k], 0.2, 1,10000)
    tabR[k]=R #plugger les valeurs
    tabA[k]=A #dans les bons tableau
    tabT[k]=T
    tabsigR[k]=sigR #meme chose que 3 lignes
    tabsigA[k]=sigA #precedentes mais pour incertitudes
    tabsigT[k]=sigT
    k+=1
    
plt.figure(2)#graphique avec barres d'erreur
plt.errorbar(ps_arr,tabR, yerr=tabsigR)
plt.errorbar(ps_arr,tabA, yerr=tabsigA)
plt.errorbar(ps_arr,tabT, yerr=tabsigT)
plt.xlabel("Probabilité de dispersion")
plt.ylabel("Fraction de neutrons dans R,A,T")
plt.savefig("prob-erreur.png")

plt.show()

    











