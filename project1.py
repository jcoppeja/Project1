import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from matplotlib import pyplot as plt
import rasterio
from rasterio.plot import show
from rasterio.windows import Window
import pyproj
from pyproj import Proj, transform
import plotly.graph_objects as go

#input gathering
xdeg=input("please input the lattitude \nenter the degrees: ")
xmin=input("enter the minutes: ")
xsec=input("enter the seconds: ")

ydeg=input("please input the longitude \nenter the degrees: ")
ymin=input("enter the minutes: ")
ysec=input("enter the seconds: ")


#input into single variables
input_x=xdeg+"."+xmin+xsec
input_y=ydeg+"."+ymin+ysec


#opening the height map
fp = r'DHMVIIDSMRAS1m_k13.tif'
img = rasterio.open(fp)


#getting the coords in the correct format
transformer=pyproj.Proj.from_crs('epsg:4326','epsg:31370')
a=transformer.transform(input_x,input_y)

x_coor=a[0]
y_coor=a[1]


#setting the box around the inputcoords
sz=15

left= x_coor-sz
right=x_coor+sz
bottom=y_coor-sz
top=y_coor+sz

#grabbing the box from the map
map=img.read(1, window=rasterio.windows.from_bounds(left,bottom,right,top,img.transform))

#turn it into nums
df=pd.DataFrame(map)
#dataFrame reversal courtesy of Lucas en Nathan
df=df[::-1]

#plotly likes csv's so here you go
df.to_csv('data2.csv')
z_data = pd.read_csv('data2.csv')

#making the actual figure (x and y seem to be inferred)
fig = go.Figure(data=[go.Surface(z=z_data.values)])

fig.update_layout(title='Brugge', autosize=False,
                  width=1000, height=1000, scene_camera_eye=dict(x=1.30, y=0.88, z=0.10),
                  margin=dict(l=65, r=50, b=65, t=90))

fig.show()