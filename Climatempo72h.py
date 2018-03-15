#http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/3477/hours/72?token=efb5cef0622ef74e1308e759be0758e2
import matplotlib.pyplot as plt
import sqlite3
import requests
import json

connection = sqlite3.connect('Forecast.db')
c = connection.cursor()

city = input('Digite a cidade para ver a previsão: ')
response = requests.get('http://apiadvisor.climatempo.com.br/api/v1/locale/city?name=%s&token=efb5cef0622ef74e1308e759be0758e2' %city)

if response.status_code != 200: # 200 significa requisição OK
    print ('Erro na requisição de dados ou cidade não encontrada.')
    quit()
else:
    dicionario = json.loads(response.text)
    
print('ID:', dicionario[0]['id'])
response = requests.get('http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/%i/hours/72?token=efb5cef0622ef74e1308e759be0758e2' %dicionario[0]['id'])

if response.status_code != 200: # 200 significa requisição OK
    print ('Erro na requisição de dados ou cidade não encontrada.')
    quit()
else:
    dicionario = json.loads(response.text)

print('Data:', dicionario['data'][0]['date_br'])
print('Velocidade do vento:', dicionario['data'][0]['wind']['velocity'], 'Km/h')
print('Temperatura:', dicionario['data'][0]['temperature']['temperature'], '°C')
print('Precipitação de Chuva:', dicionario['data'][0]['rain']['precipitation'], 'mm')

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS cidade1 (id integer, cidade text, data text, vento float, temperatura float, chuva float)')

create_table()

def dataentry():
    i=0
    for i in range(71):
        c.execute("INSERT INTO cidade1 VALUES(?, ?, ?, ?, ?, ?)", (i+1, city, dicionario['data'][i]['date_br'], dicionario['data'][i]['wind']['velocity'], dicionario['data'][i]['temperature']['temperature'], dicionario['data'][i]['rain']['precipitation']))
    connection.commit()
dataentry()

c.execute('SELECT temperatura, chuva, vento, data FROM cidade1')
dados = c.fetchall()

temperatura = []
chuva = []
vento = []
data = []


for row in dados:
    temperatura.append(row[0])
    chuva.append(row[1])
    vento.append(row[2])
    data.append(row[3])

x = [1,2,3,4,5,6,7]
y = [1,2,3,4,5,6,7]
labelsx = [data[0], data[12], data[24], data[36], data[48], data[60], data[70]]
labelsy = [temperatura[0], temperatura[12], temperatura[24], temperatura[36], temperatura[48], temperatura[60], temperatura[70]]

plt.title(city)
plt.xlabel('Data/Hora')
plt.ylabel('Temperatura (°C)')
plt.plot(data, temperatura)
plt.xticks(rotation='vertical')
plt.grid(True)
plt.show()

c.execute('DROP TABLE IF EXISTS cidade1')
