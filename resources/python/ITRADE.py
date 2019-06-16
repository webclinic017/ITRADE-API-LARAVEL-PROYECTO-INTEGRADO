import io

import quandl
import pandas as pd
import numpy as np
import fbprophet
import requests
import matplotlib.pyplot as plt
import matplotlib
import requests
import datetime



class Itrade():

    precioPrevisto = "none"
    ticker = "none"
    # TICKER : Nombre de la empresa

    # Constructor de la clase Stocker (__init__)
    def __init__(self, ticker, exchange='WIKI'):
        
        # Forzamos mayusculas en el nombre del activo que sera pasado por parametro
        ticker = ticker.upper()
        #self.precioPrevisto2 = precioPrevisto
        # self : referencia a la clase Stocker
        self.symbol = ticker

        # Peticion para extraer los datos de la API
        url_csv = 'https://www.worldtradingdata.com/api/v1/history?symbol=' + ticker + '&sort=newest&api_token' \
                                                                                       '=vGpNTjAR6hDVlerUKGFEfjUx52wPSiQuszj4bdIVEpRLNF1hDw9zpohcarfl&output=csv&date_from=2014-01-02'
        print("la url es " + str(url_csv))

        response = requests.get(url_csv).content

        # decodificamos el request convirtiendolo en un dataframe valido para ser trabajado con Pandas
        dfHistorialPrecios = pd.read_csv(io.StringIO(response.decode('utf-8')))

        #dfHistorialPrecios = pd.read_csv('tabla.csv')

        dfHistorialPrecios['Date'] = pd.to_datetime(dfHistorialPrecios.Date, format='%Y-%m-%d')

        dfHistorialPrecios = dfHistorialPrecios.reset_index(level=0)

        #print(dfHistorialPrecios)

        # Convertimos la columna de fecha a ds la cual es requerida en Prophet
        dfHistorialPrecios['ds'] = dfHistorialPrecios['Date']

        if 'Adj. Close' not in dfHistorialPrecios.columns:
            dfHistorialPrecios['Adj. Close'] = dfHistorialPrecios['Close']
            dfHistorialPrecios['Adj. Open'] = dfHistorialPrecios['Open']


        dfHistorialPrecios['y'] = dfHistorialPrecios['Adj. Close']
        dfHistorialPrecios['Daily Change'] = dfHistorialPrecios['Adj. Close'] - dfHistorialPrecios['Adj. Open']

        # Asignamos los datos al atributo de la clase Stocker

        self.stock = dfHistorialPrecios.copy()

        # Minimos y maximos datos en el rango permitido
        self.min_date = pd.to_datetime(min(dfHistorialPrecios['Date']))
        self.max_date = pd.to_datetime(max(dfHistorialPrecios['Date']))

        #print(type(self.min_date))
        #9print(type(self.max_date))

        # Encuentra precios maximos y minimos y fechas en las que ocurrieron.
        self.max_price = np.max(self.stock['y'])
        self.min_price = np.min(self.stock['y'])

        self.min_price_date = self.stock[self.stock['y'] == self.min_price]['Date']
        self.min_price_date = self.min_price_date[self.min_price_date.index[0]]
        self.max_price_date = self.stock[self.stock['y'] == self.max_price]['Date']
        self.max_price_date = self.max_price_date[self.max_price_date.index[0]]

        # El precio inicial (comenzando con el precio de apertura)
        self.starting_price = float(self.stock.loc[0, 'Adj. Open'])

        # El precio mas reciente
        self.most_recent_price = float(self.stock.loc[self.stock.index[-1], 'y'])

        # Redondeo de fechas
        self.round_dates = True

        #  Numero de anos de entrenamiento
        self.training_years = 3

        # Prophet parametros
        self.changepoint_prior_scale = 0.05
        self.weekly_seasonality = False
        self.daily_seasonality = False
        self.monthly_seasonality = True
        self.yearly_seasonality = True
        self.changepoints = None

        print('Stocker Inicializado. Datos recopilados de {} desde el {}.'.format(self.symbol,
                                                                                  self.min_date,
                                                                                  self.max_date))

        # METODO ENCARGADO DE LA MANIPULACION DE LAS FECHAS

    def handle_dates(self, start_date, end_date):

        # Las fechas de inicio y finalizacion predeterminadas son el comienzo y el final de los datos.
        if start_date is None:
            start_date = self.min_date
        if end_date is None:
            self.max_date = pd.to_datetime(self.max_date)

        try:
            # Convertir a pandas datetime para indexar el dataframe
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)

            #print(type(start_date))
            #print(start_date)
            #print(type(end_date))
            #print(end_date)

        except Exception as e:
            print('Introduce las fechas en el formato correcto para su manipulacion con Pandas')
            print(e)
            return

        valid_start = False
        valid_end = False

        # Mientras que las fechas no sea validas se seguiran ingresando
        while (not valid_start) & (not valid_end):
            valid_end = True
            valid_start = True

            #print(type(end_date))
            #print(type(start_date))

            if end_date < start_date:
                print('La fecha de finalizacion debe ser posterior a la fecha de inicio.')
                start_date = pd.to_datetime(input('Ingrese una nueva fecha de inicio: '))
                end_date = pd.to_datetime(input('Ingrese una nueva fecha de finalizacion: '))
                valid_end = False
                valid_start = False

            else:
                if end_date > self.max_date:
                    print('La fecha de finalizacion excede el rango de datos')
                    end_date = pd.to_datetime(input('Ingrese una nueva fecha de finalizacion: '))
                    valid_end = False

            if start_date < self.min_date:
                print('La fecha de inicio es anterior al intervalo de fechas')
                start_date = pd.to_datetime(input('Ingrese una nueva fecha de inicio: '))
                valid_start = False

        return start_date, end_date

    """
        Devuelve el dataframe recortado al rango especificado.
    """

    def make_df(self, start_date, end_date, df=None):

        global trim_df 

        #print(type(start_date))
        #print(type(end_date))

        if not df:
            df = self.stock.copy()

        start_date, end_date = self.handle_dates(start_date, end_date)

        #print(start_date)
        #print(end_date)

        # realizar un seguimiento de si las fechas de inicio y finalizacion estan en los datos
        start_in = True
        end_in = True

        # Si el usuario quiere redondear fechas (comportamiento predeterminado)
        if self.round_dates:

            # Si ambos estan en el dataframe, no se redondea
            trim_df = df[(df['Date'] >= start_date) &
                                 (df['Date'] <= end_date)]
            #print(trim_df['Adj. Open'])

            #trim_df = df[(df['Date'] >= start_date) &
             #            (df['Date'] <= end_date.date)]
            #print("EL FINALLLL", trim_df)
        return trim_df

    #  RESET DE LA GRAFICA
    @staticmethod
    def reset_plot():

        # Resetear los parametros a default
        matplotlib.rcdefaults()

        # Personalizacion grafica (parametros)
        matplotlib.rcParams['figure.figsize'] = (8, 5)
        matplotlib.rcParams['axes.labelsize'] = 10
        matplotlib.rcParams['xtick.labelsize'] = 8
        matplotlib.rcParams['ytick.labelsize'] = 8
        matplotlib.rcParams['axes.titlesize'] = 14
        matplotlib.rcParams['text.color'] = 'k'

    # Metodo para interpolar linealmente los precios en los fines de semana.
    @staticmethod
    def resample(dataframe):
        # CCambiar el indice y remuestrear a nivel diario.
        dataframe = dataframe.set_index('ds')
        dataframe = dataframe.resample('D')
        # Restablecer el indice e interpolar valores nan
        dataframe = dataframe.reset_index(level=0)
        dataframe = dataframe.interpolate()
        return dataframe

    # Removemos los findes de semana del dataframe
    @staticmethod
    def remove_weekends(dataframe):
        # Reset index para usar ix
        dataframe = dataframe.reset_index(drop=True)
        weekends = []
        # Encontrar todos los fines de semana
        for i, date in enumerate(dataframe['ds']):
            if (date.weekday()) == 5 | (date.weekday() == 6):
                weekends.append(i)
        # Dropeamos los findes de semana
        dataframe = dataframe.drop(weekends, axis=0)
        return dataframe


    # ----------------------------------------CREACION DEL MODELO------------------------------------------------------------
    # Creacion del modelo sin entenamiento

    def create_model(self):

        # Creacion del modelo
        model = fbprophet.Prophet(daily_seasonality=self.daily_seasonality,
                                  weekly_seasonality=self.weekly_seasonality,
                                  yearly_seasonality=self.yearly_seasonality,
                                  changepoint_prior_scale=self.changepoint_prior_scale,
                                  changepoints=self.changepoints)

        if self.monthly_seasonality:
            # Anadir estacionalidad mensual
            model.add_seasonality(name='monthly', period=30.5, fourier_order=5)

        return model

        # Modelo Prophet basico para un numero especifico de dias.
    def create_prophet_model(self, days=0, resample=False):


            

            self.reset_plot()

            model = self.create_model()

            # Encaja en el historial de stock de self.training_years numero de anos
            stock_history = self.stock[self.stock['Date'] > (self.max_date - pd.DateOffset(years=self.training_years))]

            if resample:
                stock_history = self.resample(stock_history)

            model.fit(stock_history)

            # Hacer y predecir para el proximo ano con datos futuros.
            future = model.make_future_dataframe(periods=days, freq='D')
            future = model.predict(future)

            if days > 0:                
                # Pintar prediccion de precio
                self.precioPrevisto = 'Se estima que para la fecha {} = ${:.2f}'.format(
                    future.loc[future.index[-1], 'ds'], future.loc[future.index[-1], 'yhat'])

                print('Precio previsto en {} = ${:.2f}'.format(
                    future.loc[future.index[-1], 'ds'], future.loc[future.index[-1], 'yhat']))

                title = '%s PREDICCION DE PRECIOS' % self.symbol
            else:
                title = '%s PREDICCION DE PRECIOS' % self.symbol

            # Configurar la Grafica
            fig, ax = plt.subplots(1, 1)

            # Pintar los valores actuales
            ax.plot(stock_history['ds'], stock_history['y'], 'ko-', linewidth=1.4, alpha=0.8, ms=1.8,
                    label='Observaciones')

            # Pintar las predicciones de precio
            ax.plot(future['ds'], future['yhat'], 'forestgreen', linewidth=2.4, label='Modelado');

            # Pintar el intervalo de incertidumbre como una cinta
            ax.fill_between(future['ds'].dt.to_pydatetime(), future['yhat_upper'], future['yhat_lower'], alpha=0.3,
                            facecolor='g', edgecolor='k', linewidth=1.4, label='Intervalo de confianza')

            # Formateado de la grafica
            plt.legend(loc=2, prop={'size': 10})
            plt.xlabel('Fecha')
            plt.ylabel('Precio $')
            plt.grid(linewidth=0.6, alpha=0.6)
            plt.title(title)
            #plt.savefig("images/"+str(ticker)+ str(x) + str(".png"))
            #plt.savefig("img/grafica2.svg")
            #plt.show()

            return model, future

    def getPlt(self):
        return  plt

    
    def getPrediccionPrecio(self):

        return self.precioPrevisto


    # CREACION DE LA GRAFICA con los datos pasados por parametro
    def plot_stock(self, start_date=None, end_date=None, stats=None, plot_type='basic'):

        if stats is None:
            stats = ['Adj. Close']
        self.reset_plot()

        if start_date is None:
            start_date = self.min_date
            print("La fecha de inicio es " + str(start_date))

        if end_date is None:
            end_date = self.max_date
            print("La fecha final es " + str(end_date))

        stock_plot = self.make_df(start_date, end_date)

        #print("he pasado el llamamiento de make_df " , stock_plot)

        colors = ['r', 'b', 'g', 'y', 'c', 'm']


        for i, stat in enumerate(stats):
            stat_min = min(stock_plot[stat])
            stat_max = max(stock_plot[stat])

            stat_avg = np.mean(stock_plot[stat])

            date_stat_min = stock_plot[stock_plot[stat] == stat_min]['Date']
            date_stat_min = date_stat_min[date_stat_min.index[0]]
            date_stat_max = stock_plot[stock_plot[stat] == stat_max]['Date']
            date_stat_max = date_stat_max[date_stat_max.index[0]]

            print('Maximum {} = {:.2f} on {}.'.format(stat, stat_max, date_stat_max))
            print('Minimum {} = {:.2f} on {}.'.format(stat, stat_min, date_stat_min))
            print(
                'Current {} = {:.2f} on {}.\n'.format(stat, self.stock.loc[self.stock.index[-1], stat], self.max_date))

            if plot_type == 'pct':
                plt.style.use('fivethirtyeight')
                if stat == 'Daily Change':
                    plt.plot(stock_plot['Date'], 100 * stock_plot[stat],
                             color=colors[i], linewidth=2.4, alpha=0.9,
                             label=stat)
                else:
                    plt.plot(stock_plot['Date'], 100 * (stock_plot[stat] - stat_avg) / stat_avg,
                             color=colors[i], linewidth=2.4, alpha=0.9,
                             label=stat)

                plt.xlabel('Fecha');
                plt.ylabel('Cambio Relativo al Promedio (%)')
                plt.title('%s Historia de Precios' % self.symbol)
                plt.legend(prop={'size': 10})
                plt.grid(color='k', alpha=0.4)

            # Stat y-axis
            elif plot_type == 'basic':
                plt.style.use('fivethirtyeight')
                plt.plot(stock_plot['Date'], stock_plot[stat], color=colors[i], linewidth=3, label="Precio de Cierre", alpha=0.8)
                plt.xlabel('Fecha')
                plt.ylabel('Precio en US $')
                plt.title('%s Historial de precios' % self.symbol);
                plt.legend(prop={'size': 10})
                plt.grid(color='k', alpha=0.4)

        #plt.savefig("images/"+str(ticker)+str(".svg"))
        #plt.show()


