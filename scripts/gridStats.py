import netCDF4
import argparse

parser = argparse.ArgumentParser(description='Plot grid.')
parser.add_argument('-i', dest='inputFile', type=str, default='/nesi/nobackup/mocean02574/NZB_N50/nz5km_avg_200601.nc',
                    help='input netcdf file')
parser.add_argument('-v', dest='variableName', type=str, default='mask_rho', 
	                help='variable name')
args = parser.parse_args()

# open the netcdf file
f = netCDF4.Dataset(args.inputFile)
# read
lonName, latName = f.variables[args.variableName].coordinates.split()
lon = f.variables[lonName][:]
lat = f.variables[latName][:]
f.close()

dLon0 = lon[:1, :] - lon[0:-1, :]
dLon1 = lon[:, 1:] - lon[:, 0:-1]

dLat0 = lat[:1, :] - lat[0:-1, :]
dLat1 = lat[:, 1:] - lat[:, 0:-1]

print(f'lon min, max: {lon.min()} {lon.max()}')
print(f'lat min, max: {lat.min()} {lat.max()}')

print(f'lon diff 0 (min/max/std): {dLon0.min()} {dLon0.max()} {dLon0.std()}')
print(f'lon diff 1 (min/max/std): {dLon1.min()} {dLon1.max()} {dLon1.std()}')
print(f'lat diff 0 (min/max/std): {dLat0.min()} {dLat0.max()} {dLat0.std()}')
print(f'lat diff 1 (min/max/std): {dLat1.min()} {dLat1.max()} {dLat1.std()}')

