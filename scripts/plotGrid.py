import vtk
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

nlon, nlat = lon.shape
numPoints = nlon * nlat

# create the pipeline
coords = vtk.vtkDoubleArray()
pts = vtk.vtkPoints()
grid = vtk.vtkStructuredGrid()
edges = vtk.vtkExtractEdges()
tubes = vtk.vtkTubeFilter()
edgeMapper = vtk.vtkPolyDataMapper()
edgeActor = vtk.vtkActor()

# settings
tubes.SetRadius(0.01)

# construct the grid
grid.SetDimensions(nlon, nlat, 1)

# construct the points
coords.SetNumberOfComponents(3)
coords.SetNumberOfTuples(numPoints)
k = 0
for j in range(nlat):
    for i in range(nlon):
        coords.SetTuple(k, (lon[i, j], lat[i, j], 0.0))
        k += 1

# connect
pts.SetNumberOfPoints(numPoints)
pts.SetData(coords)
grid.SetPoints(pts)
edges.SetInputData(grid)
tubes.SetInputConnection(edges.GetOutputPort())
edgeMapper.SetInputConnection(tubes.GetOutputPort())
edgeActor.SetMapper(edgeMapper)

# show
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
# add the actors to the renderer, set the background and size
ren.AddActor(edgeActor)
ren.SetBackground(0.5, 0.5, 0.5)
renWin.SetSize(400, 300)
iren.Initialize()
renWin.Render()

