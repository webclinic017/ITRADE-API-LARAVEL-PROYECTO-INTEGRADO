

import os
from stocker import Stocker
import matplotlib.pyplot as plt


empresas = ["MSFT", "GOOGL","AMZN", "AAPL",
"AMD","INTC","QCOM","DELL","FB","TSLA"] 



for empresa in empresas:
     temp = Stocker(empresa)
     temp.plot_stock()
     for x in 4:
        if(x ==0):
            temp = 30*(x+1)
        else:
            temp = 30*(x*3)

        model, model_data = temp.create_prophet_model(days=temp)
        temp = 30 * x
        plt.savefig("./images/"+str(empresa)+ str(x) + str(".svg"))
