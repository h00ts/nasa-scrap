__author__ = 'h00ts aka Rus G'

from bs4 import BeautifulSoup
import requests, xlsxwriter, csv

print("Latitud:")
lat = input() #"22.252"
print("Longitud:")
lon = input() #"-104.516"

page = requests.get('https://eosweb.larc.nasa.gov/cgi-bin/sse/grid.cgi?&num=076113&submit=Submit&hgt=100&veg=17&sitelev=&email=skip@larc.nasa.gov&p=grid_id&p=ret_tlt0&p=T10M&p=wspd50m&p=RAIN&step=2&lat='+lat+'&lon='+lon)
soup = BeautifulSoup(page.content, 'html.parser')

# Esto es una joda por la estructura del sitio(circa 1990)
el = soup.select("table tr td b")[7]
ang = list(soup.select("table tr")[17].contents)
avg_temp = list(soup.select("table tr")[20].contents)
min_temp = list(soup.select("table tr")[21].contents)
max_temp = list(soup.select("table tr")[22].contents)
max_wind = list(soup.select("table tr")[27].contents)
prec = list(soup.select("table tr")[30].contents)

## Ahora si DALE

for r in ang:
  if (r.string is "</td>"):
    r.string = ' '

for r in avg_temp:
  if (r.string is "</td>"):
    r.string = ' '

angle = [d.get_text() for d in ang[:-1]]
avg_temp = [d.get_text() for d in avg_temp]
min_temp = [d.get_text() for d in min_temp]
max_temp = [d.get_text() for d in max_temp[:-1]]
max_wind = [d.get_text() for d in max_wind[:-1]]
prec = [d.get_text() for d in prec[:-1]]


print(angle)
print("Temperatura promedio: "+avg_temp[13])
print("Temperatura minima: "+min_temp[13])
print("Temperatura maxima: "+max_temp[13])
print("Viento max: "+max_wind[13])
print("Precipitacion: "+prec[13])
print("Elevation: "+el.get_text())

#workbook = xlsxwriter.Workbook('Lat'+lat+'Lon'+lon+'.xlsx')
#worksheet = workbook.add_worksheet()

#worksheet.write('A1', angle)
#worksheet.write('B1', "Elevation")
#worksheet.write('B2', el.get_text())

#workbook.close()