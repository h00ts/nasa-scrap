__author__ = 'h00ts aka Rus G'

from bs4 import BeautifulSoup
import requests, xlsxwriter, csv

## Para cuando agregue la opcion individual
#print("Latitud:")
#lat = input() #"22.252"
#print("Longitud:")
#lon = input() #"-104.516"

data = []
line = []

print("Leyendo Datos...")
with open('coord.csv', 'r', encoding='utf-8') as f:
  reader = csv.reader(f)
  coords = list(reader)

#coords.pop(0) por si existe encabezado
for lat, lon in coords:
    print("Procesando... "+lat+","+lon)
    page = requests.get('https://eosweb.larc.nasa.gov/cgi-bin/sse/grid.cgi?&num=076113&submit=Submit&hgt=100&veg=17&sitelev=&email=skip@larc.nasa.gov&p=grid_id&p=ret_tlt0&p=T10M&p=wspd50m&p=RAIN&step=2&lat='+lat+'&lon='+lon)
    soup = BeautifulSoup(page.content, 'html.parser')
    # Esto es una joda para encontrar el dato que necesitas por la estructura del sitio(circa 1990)
    ang = list(soup.select("table tr")[17].contents)
    avg_temp = list(soup.select("table tr")[20].contents)
    min_temp = list(soup.select("table tr")[21].contents)
    max_temp = list(soup.select("table tr")[22].contents)
    max_wind = list(soup.select("table tr")[27].contents)
    prec = list(soup.select("table tr")[30].contents)
    ## Ahora si DALE
    angle = [d.get_text() for d in ang[:-1]]
    avg_temp = [d.get_text() for d in avg_temp]
    min_temp = [d.get_text() for d in min_temp]
    max_temp = [d.get_text() for d in max_temp[:-1]]
    max_wind = [d.get_text() for d in max_wind[:-1]]
    prec = [d.get_text() for d in prec[:-1]]
    el = soup.select("table tr td b")[7]
    line.append(lat)
    line.append(lon)
    line.append(el.get_text())
    line.append(max_temp[13])
    line.append(avg_temp[13])
    line.append(min_temp[13])
    line.append(max_wind[13])
    line.append(prec[13])
    angle.pop(0)
    line.append([angle])
    data.append(line)
    line = []

workbook = xlsxwriter.Workbook('NASA-Scrap.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write('A1', 'Latitud')
worksheet.write('B1', 'Logitud')
worksheet.write('C1', 'Altitud')
worksheet.write('D1', 'Temperatura max')
worksheet.write('E1', 'Temperatura prom')
worksheet.write('F1', 'Temperatura min')
worksheet.write('G1', 'Viento max')
worksheet.write('H1', 'Precipitacion')
worksheet.write('I1', 'Angulo Enero')
worksheet.write('J1', 'Angulo Febrero', )
worksheet.write('K1', 'Angulo Marzo')
worksheet.write('L1', 'Angulo Abril')
worksheet.write('M1', 'Angulo Mayo')
worksheet.write('N1', 'Angulo Junio')
worksheet.write('O1', 'Angulo Julio')
worksheet.write('P1', 'Angulo Agosto')
worksheet.write('Q1', 'Angulo Septiembre')
worksheet.write('R1', 'Angulo Octubre')
worksheet.write('S1', 'Angulo Novimbre')
worksheet.write('T1', 'Angulo Diciembre')
worksheet.write('U1', 'Angulo promedio')
row = 1
col = 0

for latitud, longitud, altitud, temp_max, temp_prom, temp_min, viento, precipitacion, angle in data:
    worksheet.write(row, col, latitud)
    worksheet.write(row, col + 1, longitud)
    worksheet.write(row, col + 2, altitud)
    worksheet.write(row, col + 3, temp_max)
    worksheet.write(row, col + 4, temp_prom)
    worksheet.write(row, col + 5, temp_min)
    worksheet.write(row, col + 6, viento)
    worksheet.write(row, col + 7, precipitacion)
    for jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dic, avg in angle:
        worksheet.write(row, col + 8, jan)
        worksheet.write(row, col + 9, feb)
        worksheet.write(row, col + 10, mar)
        worksheet.write(row, col + 11, apr)
        worksheet.write(row, col + 12, may)
        worksheet.write(row, col + 13, jun)
        worksheet.write(row, col + 14, jul)
        worksheet.write(row, col + 15, aug)
        worksheet.write(row, col + 16, sep)
        worksheet.write(row, col + 17, oct)
        worksheet.write(row, col + 18, nov)
        worksheet.write(row, col + 19, dic)
        worksheet.write(row, col + 20, avg)

    row += 1

workbook.close()