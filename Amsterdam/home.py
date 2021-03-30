from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
#from PIL import Image
#import json
import requests
import altair as alt


# image = Image.open("C:/Users/Familia/PycharmProjects/Amsterdam/static/img/fondo.jpg")
st.sidebar.header('**Hola, bienvenido.**')
st.sidebar.header('**Ingrese parámetros**')




def get_input():
    aux_datetime = datetime.now()
    today_date = aux_datetime.date()
    treinta_dias_date = today_date - timedelta(days=30)

    get_fecha_desde = st.sidebar.text_input("Fecha Inicial", treinta_dias_date)
    get_fecha_hasta = st.sidebar.text_input("Fecha Final", today_date)
    option = st.sidebar.selectbox('Identificador', ('GOOGL', 'TSLA', 'ENIC','WMT','CCU','SQM','FDX','NTZ'))
    get_nemotecnico = option #st.sidebar.selectbox('Identificador', option)
    return get_fecha_desde, get_fecha_hasta, get_nemotecnico


# st.image(image, use_column_width=True)
def get_data(nemotecnico_empresa, fecha_desde, fecha_hasta):
    nemotecnico = nemotecnico_empresa


from_input_fecha_desde, from_input_fecha_hasta, from_input_nemotecnico = get_input()

fecha_desde = datetime.strptime(from_input_fecha_desde, '%Y-%m-%d')
fecha_hasta = datetime.strptime(from_input_fecha_hasta, '%Y-%m-%d')
nemotecnico = from_input_nemotecnico.upper()

fecha_desde_tmsp = str(round(datetime.timestamp(fecha_desde)))

fecha_hasta_tmsp = str(round(datetime.timestamp(fecha_hasta)))

# -------------------------------------------------------
# Formateando nemotécnicos
nemotecnico_formateado = ''
if nemotecnico == 'BCH:US':
    nemotecnico_formateado = 'IPSA: Banco de Chile'
elif nemotecnico == 'ENIC':
    nemotecnico_formateado = 'IPSA: ENEL'
elif nemotecnico == 'WMT':
    nemotecnico_formateado = 'Walmart'
elif nemotecnico == 'TSLA':
    nemotecnico_formateado = 'TESLA'
elif nemotecnico == 'GOOGL':
    nemotecnico_formateado = 'GOOGLE'
elif nemotecnico == 'BSAC':
    nemotecnico_formateado = 'IPSA: Banco Santander'
elif nemotecnico == 'ITBC':
    nemotecnico_formateado = 'IPSA: Banco ITAÚ'
elif nemotecnico == 'CCU':
    nemotecnico_formateado = 'IPSA: CCU (Compañía de Cervecerías Unidas)'
elif nemotecnico == 'LTM':
    nemotecnico_formateado = 'IPSA: LATAM'
elif nemotecnico == 'SQM':
    nemotecnico_formateado = 'IPSA: Sociedad Química y Minera de Chile'
elif nemotecnico == 'FDX':
    nemotecnico_formateado = 'Fedex'
elif nemotecnico == 'NTZ':
    nemotecnico_formateado = 'Natuzzi'
else:
    nemotecnico_formateado = 'Configurar nemotécnico'

# -------------------------------------------------------


# -------------------------------------------------------
st.write("""
   # Bienvenido a Ámsterdam
   **Mostrando información del mercado de acciones en vivo de la empresa**
   """ + '**' + nemotecnico_formateado + '**')

if nemotecnico == "":
    r = requests.get(
        'https://finnhub.io/api/v1/stock/candle?symbol=&resolution=1&from=0&to=0&token=btagn3v48v6vivh8p9n0')
    accionesJson = r.json()
else:
    r = requests.get(
        'https://finnhub.io/api/v1/stock/candle?symbol=' + nemotecnico + '&resolution=D&from=' + fecha_desde_tmsp + '&to=' + fecha_hasta_tmsp + '&token=btagn3v48v6vivh8p9n0')
    accionesJson = r.json()

open_values = accionesJson["o"]
close_values = accionesJson["c"]
close_values_rsi = accionesJson["c"]
fecha_values = accionesJson["t"]
fecha_values_size = len(fecha_values)
fecha_values_int = []
fecha_values_datetime = []

# print()
# print(open_values)
# print(close_values)

for x in range(0, fecha_values_size):
    fecha_values_int.append(int(fecha_values[x]))

for i in range(0, fecha_values_size):
    valor_aux = datetime.fromtimestamp((fecha_values_int[i]))
    fecha_values_datetime.append(valor_aux.strftime("%m/%d/%Y"))

data_ordenada = {'Apertura': open_values,
                 'Cierre': close_values,
                 'Fecha': fecha_values_datetime}
chart_data = pd.DataFrame(data_ordenada)

source = chart_data

alt_chart = alt.Chart(source).transform_fold(
    fold=['Apertura', 'Cierre']
).mark_line().encode(
    x=alt.X('Fecha:O', axis=alt.Axis(title="Fechas")),
    y=alt.Y('value:Q', scale=alt.Scale(zero=False), axis=alt.Axis(title="Valor")),
    tooltip=['Fecha', 'Apertura', 'Cierre'],
    color='key:N'
).interactive().properties(
    width=1000,
    height=600
)
st.write("", "", alt_chart)
# -------------------------------------------------------
# Cálculo de RSI
# Cálculo de Change
leng = len(close_values_rsi)
change_rsi = []

for i in range(leng):
    if i + 1 >= leng:
        break
    else:
        change_rsi.append(close_values_rsi[i + 1] - close_values_rsi[i])

# -------------------------------------------------------
# Cálculo de Upward Movement
upward_movement_rsi = []
for i in change_rsi:
    if i > 0:
        upward_movement_rsi.append(i)
    else:
        upward_movement_rsi.append(0)

# -------------------------------------------------------
# Cálculo de Downward Movement
downward_movement_rsi = []
for i in change_rsi:
    if i < 0:
        downward_movement_rsi.append(i * -1)
    else:
        downward_movement_rsi.append(0)

# -------------------------------------------------------
# Cálculo de AverageUpwardMovement
average_upward_movement_rsi = 0
average_upward_movement_rsi_suma = 0
for i in upward_movement_rsi:
    average_upward_movement_rsi_suma = average_upward_movement_rsi_suma + i
average_upward_movement_rsi = average_upward_movement_rsi_suma / (leng - 1)

# -------------------------------------------------------
# Cálculo de AverageDownwardMovement
average_downward_movement_rsi = 0
average_downward_movement_rsi_suma = 0
for i in downward_movement_rsi:
    average_downward_movement_rsi_suma = average_downward_movement_rsi_suma + i
average_downward_movement_rsi = average_downward_movement_rsi_suma / (leng - 1)

# -------------------------------------------------------
# Cálculo de Relative Strength
relative_strg_rsi = average_upward_movement_rsi / average_downward_movement_rsi_suma

# -------------------------------------------------------
# Cálculo de RSI
rsi_final = round((100 - 100 / (relative_strg_rsi + 1)), 2)
rsi_señal = ''
if rsi_final <= 30:
    rsi_señal = "**Comprar**"
elif rsi_final >= 70:
    rsi_señal = "**Vender**"
else:
    rsi_señal = "**Mantener**"
# -------------------------------------------------------
simulador_simple_ganancias = 0
simulador_primer_valor = open_values[0]
simulador_ultimo_valor = open_values[-1]

simulador_tasa_de_variacion = simulador_primer_valor / simulador_ultimo_valor

# -------------------------------------------------------
st.header('El RSI para el período consultado es de ' + str(rsi_final))
st.header('Se recomienda ' + rsi_señal)

valor_input_simulador = st.text_input("Ingrese valor a simular:",1000)
simulador_simple_ganancias = round(float(valor_input_simulador) * simulador_tasa_de_variacion, 2)
simulador_monto_total_inversion = round(simulador_simple_ganancias - float(valor_input_simulador), 2)

st.subheader('Invirtiendo un monto de '+valor_input_simulador+'$ retornarían $' + str(simulador_simple_ganancias))
st.subheader('Inversión inicial - ganancia = ' + str(simulador_monto_total_inversion))
# -------------------------------------------------------
st.header('**Puntos de interés**')
st.write(source.describe())
st.write()
st.markdown('**count**: Cantidad de registros evaluados')
st.markdown('**mean**: Media aritmética')
st.markdown('**std**: Desviación estándar')
st.markdown('**min**: Valor más bajo')
st.markdown('**25%**: Percentil 25 - Cuartil 1')
st.markdown('**50%**: Percentil 50 - Cuartil 2 o Mediana')
st.markdown('**75%**: Percentil 75 - Cuartil 3')
st.markdown('**max**: Valor más alto')
# -------------------------------------------------------

st.header('**Tabla de datos del período evaluado**')
st.dataframe(chart_data, 800, 750)





