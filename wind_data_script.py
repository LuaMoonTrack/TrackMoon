pip install xarray netCDF4 requests
import xarray as xr

# URL do servidor THREDDS do NOAA onde os dados GFS estão armazenados
url = 'https://nomads.ncep.noaa.gov/dods/gfs_0p25/gfs20230806/gfs_0p25_00z'

# Carregar os dados usando xarray
ds = xr.open_dataset(url)

# Lista de níveis de pressão que queremos
pressure_levels = [
    '1000mb', '975mb', '950mb', '925mb', '900mb', '875mb', '850mb', 
    '825mb', '800mb', '775mb', '750mb', '725mb', '700mb', '675mb', 
    '650mb', '625mb', '600mb', '575mb', '550mb', '525mb', '500mb'
]

# Dicionários para armazenar dados de vento em diferentes níveis
u_wind = {}
v_wind = {}

# Iterar sobre cada nível de pressão e obter os dados de vento
for level in pressure_levels:
    u_key = f'ugrd_{level}'
    v_key = f'vgrd_{level}'
    u_wind[level] = ds[u_key]
    v_wind[level] = ds[v_key]

# Exemplo de como selecionar uma área específica (latitude e longitude) e período
latitude_slice = slice(-30, 30)
longitude_slice = slice(-60, -30)
time_slice = slice('2023-08-06T00:00:00', '2023-08-10T00:00:00')

u_wind_sel = {level: u.sel(lat=latitude_slice, lon=longitude_slice, time=time_slice) for level, u in u_wind.items()}
v_wind_sel = {level: v.sel(lat=latitude_slice, lon=longitude_slice, time=time_slice) for level, v in v_wind.items()}

# Salvar os dados selecionados em arquivos NetCDF (opcional)
for level in pressure_levels:
    u_wind_sel[level].to_netcdf(f'u_wind_{level}_data.nc')
    v_wind_sel[level].to_netcdf(f'v_wind_{level}_data.nc')

print("Dados de vento (u, v) em diferentes níveis atmosféricos baixados com sucesso.")
