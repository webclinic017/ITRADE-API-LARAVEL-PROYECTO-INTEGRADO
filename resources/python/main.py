

import os
from stocker import Stocker
import matplotlib.pyplot as plt


#empresas = ["MSFT", "GOOGL","AMZN", "AAPL",
#"AMD","INTC","QCOM","DELL","FB","TSLA"] 


#num = [1,2,3,4]

empresas = ["MSFT"]
num = [1]


for empresa in empresas:
     empresaScience = Stocker(empresa)
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
