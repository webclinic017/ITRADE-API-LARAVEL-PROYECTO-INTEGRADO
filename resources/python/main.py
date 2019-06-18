#!/usr/bin/env python
import sys
import os
import matplotlib.pyplot as plt
#import pip
from ITRADE import Itrade
import re

empresa = sys.argv[1]

meses = 0

x = empresa.split("-")

print("letras ", x[0])
print("Meses" , x[1])


empresaScience = Itrade('MSFT')
empresaScience.plot_stock()

if (x[1] == '1'):
    meses = 30
elif(x[1] == '3'):
    meses = 90
elif(x[1] == '6'):
    meses = 120
elif(x[1] == '9'):
    meses = 270
elif(x[1] == '12'):
    meses = 360
else:
    print('fecha invalida')

model, model_data = empresaScience.create_prophet_model(days=meses)
plot = empresaScience.getPlt()
precioPrevisto = empresaScience.getPrediccionPrecio()

file = open("../resources/python/images/"+empresa +".txt","w") 
file.write(precioPrevisto)
file.close()

plot.savefig("../resources/python/images/"+ empresa + ".png")

"""
empresaScience = Itrade(empresa)
empresaScience.plot_stock()
model, model_data = empresaScience.create_prophet_model(days=30)
plot = empresaScience.getPlt()
precioPrevisto = empresaScience.getPrediccionPrecio()

file = open("../resources/python/images/"+ empresa + ".txt","w") 
file.write(precioPrevisto)
file.close()

plot.savefig("../resources/python/images/"+ empresa + ".png")

"""

"""
for empresa in empresas:
     empresaScience = Itrade(empresa)
     empresaScience.plot_stock()
     for x in num:
        if(x ==0):
            temp = 30*(x+1)
        else:
            temp = 30*(x*3)

        model, model_data = empresaScience.create_prophet_model(days=temp)
        plot = empresaScience.getPlt()
        precioPrevisto = empresaScience.getPrediccionPrecio()

        file = open("../resources/python/images/"+ empresa + str(x) + ".txt","w") 
        file.write(precioPrevisto)
        file.close()

        #plot.show()

        plot.savefig("../resources/python/images/"+ empresa + str(x) + ".png")
"""