<img align="right" height="39" src="https://github.com/EL-BID/Modelo-de-prediccion-de-crecimiento-urbano-/blob/master/img/Vivid_logo.png"><img align="right" width="115" height="49" src="https://github.com/EL-BID/Modelo-de-prediccion-de-crecimiento-urbano-/blob/master/img/IDB_logo.jpg">

# Urban Growth Prediction Model

## Description and Context
This repo contains code for running a model that predicts urban growth using heat maps and urban feature maps selected by the modeler. 
The model extracts random samples of the defined area (which should include area beyond the current boundaries of the city), identifies thresholds for urban growth, and runs a spatial logistic regression to predict urban growth based on attractors (such as transport, quality of life, topography and amenities) and restrictors (such as bodies of water or regulated areas). 
Predictions can be used to plan optimized urban expansion, or estimate best- and worst-case scenarios regarding climate change.

## User Guide
As inputs, the model uses monochrome images with standardized size and boundaries prepared from satellite images of an urban area. These images can be physical maps, density maps, or maps denoting legislative or social boundaries, depending on the conditions of the urban area and the modeler’s discretion. Each image should only contain information on a single feature, as each will be assigned a positive or negative weight. Using these inputs, a regularized spatial logistic regression model will predict urban growth on a pixel-by-pixel level within the determined boundaries, and outputs a binary raster file.

The image below shows the physical map of Georgetown, Guyana and its surroundings, with higher altitude shown in lighter pixels: 
<p align="center">
  <img width="460" src="https://raw.githubusercontent.com/EL-BID/Modelo-de-prediccion-de-crecimiento-urbano-/master/img/physical.PNG?token=ACL46SIEMLFJ4AS6ABRQDZS4Y6FWW">
</p>

The heat map below shows the availability of transportation in the same city, with lighter pixels showing areas where transportation is more available: 
<p align="center">
  <img width="460" src="https://raw.githubusercontent.com/EL-BID/Modelo-de-prediccion-de-crecimiento-urbano-/master/img/transport.PNG?token=ACL46SNHQAMOOFWIEMQXAHC4Y6GBU">
</p>

As in any urban growth prediction model, attractors and restrictors of will vary from one metropolitan area to another, and thus inputs will also vary accordingly. This user-friendly script clearly designates an **inputs** section, the primary and often only section that will need to be updated to fit the model to a new urban area.

## Installation Guide
This model can be run from the Anaconda prompt using the simple command `<python path\future_urban_growth_geo_v2.py>`

#### Dependencies
All inputs should be housed in the same folder with the .py script. In addition to the basic Anaconda software, the following modules will be required to run the model:

`<osgeo>` 

`<numpy>`

`<pandas>`

`<sklearn>`

## How to Contribute
## Code of Conduct
## Authors
@ngbaruah

## License
The Documentation of Support and Use of the software is licensed under Creative Commons IGO 3.0 Attribution-NonCommercial-NoDerivative (CC-IGO 3.0 BY-NC-ND)

The codebase of this repo uses [AM-331-A3 Software License](LICENSE).

## Limitation of responsibilities
The IDB is not responsible, under any circumstance, for damage or compensation, moral or patrimonial; direct or indirect; accessory or special; or by way of consequence, foreseen or unforeseen, that could arise:

I. Under any concept of intellectual property, negligence or detriment of another part theory; I

ii. Following the use of the Digital Tool, including, but not limited to defects in the Digital Tool, or the loss or inaccuracy of data of any kind. The foregoing includes expenses or damages associated with communication failures and / or malfunctions of computers, linked to the use of the Digital Tool.
