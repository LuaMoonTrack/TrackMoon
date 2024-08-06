import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from metpy.calc import vorticity
from metpy.units import units

# URL do servidor THREDDS do NOAA onde os dados GFS estão armazenados
url = 'https://nomads.ncep.noaa.gov/dods/gfs_0p25/gfs20230806/gfs_0p25_00z'

# Carregar os dados usando xarray
ds = xr.open_dataset(url)

# Selecionar variáveis de vento em diferentes níveis
pressure_level = '500mb'
u = ds[f'ugrd_{pressure_level}']
v = ds[f'vgrd_{pressure_level}']

# Selecionar uma área específica (latitude e longitude) e período
latitude_slice = slice(-30, 30)
longitude_slice = slice(-60, -30)
time_slice = slice('2023-08-06T00:00:00', '2023-08-10T00:00:00')

u_sel = u.sel(lat=latitude_slice, lon=longitude_slice, time=time_slice)
v_sel = v.sel(lat=latitude_slice, lon=longitude_slice, time=time_slice)

# Calcular a vorticidade relativa
vort = vorticity(u_sel, v_sel).metpy.dequantify()

# Encontrar a vorticidade mais intensa em cada timestep
max_vort = vort.max(dim=['lat', 'lon'])

# Traçar o caminho da vorticidade mais intensa
max_vort_lat = vort.where(vort == max_vort, drop=True)['lat'].values
max_vort_lon = vort.where(vort == max_vort, drop=True)['lon'].values
times = vort['time'].values

# Plotar o mapa e o tracking da vorticidade mais intensa
fig, ax = plt.subplots(figsize=(10, 6))

# Plotar os campos de vorticidade
vort.isel(time=0).plot(ax=ax, cmap='RdBu_r', extend='both')
ax.plot(max_vort_lon, max_vort_lat, 'k-', marker='o', markersize=5, label='Tracking da Vorticidade')

# Configurar o gráfico
ax.set_title('Tracking da Vorticidade Relativa Mais Intensa - 500 hPa')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.legend()

plt.show()
