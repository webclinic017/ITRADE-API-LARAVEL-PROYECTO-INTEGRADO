#ARTICULOS DE INTERES

#https://scholarworks.sjsu.edu/cgi/viewcontent.cgi?referer=https://www.google.com/&httpsredir=1&article=1639&context=etd_projects

#https://towardsdatascience.com/stock-prediction-in-python-b66555171a2

#SENTIMENTAL ANALISIS
#https://www.aclweb.org/anthology/W18-3102


from stocker import Stocker
#from xdss import  Stocker


variable = ['MSFT',]

empresa = Stocker('MSFT')

empresa.plot_stock()

model, model_data = empresa.create_prophet_model(days=360)

""""

amazon = Stocker('MSFT')

amazon.plot_stock()

# predict days into the future
model, model_data = amazon.create_prophet_model(days=360)

"""
