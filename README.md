<img align="right" height="39" src="https://github.com/EL-BID/Modelo-de-prediccion-de-crecimiento-urbano-/blob/master/img/Vivid_logo.png"><img align="right" width="115" height="49" src="https://github.com/EL-BID/Modelo-de-prediccion-de-crecimiento-urbano-/blob/master/img/IDB_logo.jpg">

# Urban Growth Prediction Model

## Description and Context
This repo contains code for running a model that predicts urban growth using a spatially-explicit stochastic land change modelling framework to produce projections of urban growth in a designated urban area and its surroundings. 
The model is based on GIS-based frameworks such as (SLEUTH)[https://www.sciencedirect.com/science/article/pii/S019897150100014X?via%3Dihub] and (LEAM)[https://en.wikipedia.org/wiki/Land_Use_Evolution_and_Impact_Assessment_Model], which use raster data inputs (representing features like slope, no growth areas, transportation networks, and amenities) to forecast future urban land development patterns. Coupled sub-models integrate per-capita future housing demand with an urban suitability surface based on spatial drivers of urban change. 

The model extracts random samples of the defined area (which should include area beyond the current boundaries of the city), identifies thresholds for urban growth, and runs a spatial logistic regression to predict urban growth based on attractors (such as transport, quality of life, topography and amenities) and restrictors (such as bodies of water or regulated areas). 

The goal of this work is to accessibly generate development attractiveness maps and growth projections that are spatially-explicit, based on available datasets, and require little human intervention to produce. Such maps and projections can help inform policy decisions and elicit stakeholder input about growth and its effects. They can be used to plan optimized urban expansion, or estimate best- and worst-case scenarios regarding climate resilience.

The framework focuses on the following key implementation issues: 
(1) Accessibility: The model is user-friendly and can be run by someone with minimal training on the subject. This opens access for many small municipalities and local governments where urban growth modelling is currently not readily accessible and there is relatively little experience with formally forecasting future land-use patterns. 
(2) Modifiability: A variety of data inputs from a variety of sources – stakeholder inputs, variables extracted from satellite imagery, crowd-sourced geographic information (such as Open Street Maps) – can be accommodated in the framework. New data sources can be easily integrated and updated. 
(3) Expandability: The framework is extensible and future versions of this ever-improving model can integrate more dynamic implementation of spatial gradients and land use types. 
(4) Compatibility: The interface of the framework is designed to be interoperable with concurrent modelling efforts such as SLEUTH and can be extended to include further sub-modules. 


## User Guide
The simulation model takes the following as inputs:  
(1) the designated potential urbanization surface 
(2) the number of 30m urban cells needed per year or till the end year of simulation corresponding to the urban housing demand (in km2) 
(3) a coefficient denoting the weight of the attractiveness index,
(4) a coefficient denoting the weight of random or spontaneous growth,
(5) a coefficient denoting the agricultural penalty factor,
(6) raster inputs. The raster inputs can be prepared in QGIS or another comparable software, and can take three forms: 
•	continuous maps which are usually distance to certain features of interest such as transportation, 
•	density of features of interest such as restaurants,
•	dummy variables signifying zones where development is to be restricted (for instance, protected and highly flood-prone areas). 
Each image should only contain information on a single feature, as each will be assigned a positive or negative weight. Examples of some raster data as input can be seen in the table below:

<table>
    <thead>
        <tr>
            <th>Indices</th>
            <th>Attractors</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=7>Agglomeration</td>
            <td>Proximity to and density of employment locations</td>
        </tr>
        <tr>
            <td>Proximity to CBD and centre of commerce</td>
        </tr>
        <tr>
            <td>Proximity to markets</td>
        </tr>
        <tr>
            <td>Proximity to industrial areas</td>
        </tr>
        <tr>
            <td>Proximity to the river bank</td>
        </tr>
        <tr>
            <td>Proximity to Demerara bridge</td>
        </tr>
        <tr>
            <td>Proximity to airports</td>
        </tr>
        <tr>
            <td rowspan=4>Amenities</td>
            <td>Proximity to and density of consumption centres</td>
        </tr>
        <tr>
            <td>Proximity to and density of social services</td>
        </tr>
        <tr>
            <td>Proximity to Government Housing Schemes</td>
        </tr>
        <tr>
            <td>Proximity to Utilities</td>
        </tr>
        <tr>
            <td rowspan=3>Transport</td>
            <td>Proximity to primary, secondary and tertiary roads</td>
        </tr>
        <tr>
            <td>Density of all roads including residential</td>
        </tr>
        <tr>
            <td>Proximity to transport hubs</td>
        </tr>
        <tr>
            <td rowspan=3>Topography</td>
            <td>Elevation and slope</td>
        </tr>
        <tr>
            <td>Topographic Diversity Index</td>
        </tr>
        <tr>
            <td>Land surface temperature (day and night)</td>
        </tr>
        <tr>
            <td rowspan=4>Quality of Life</td>
            <td>Proximity to coasts</td>
        </tr>
        <tr>
            <td>Proximity to greenspaces</td>
        </tr>
        <tr>
            <td>Distance from landfill site</td>
        </tr>
        <tr>
            <td>Slope suitability</td>
        </tr>
        <tr>
            <td rowspan=2>Urban Extensions</td>
            <td>Proximity to urban areas</td>
        </tr>
        <tr>
            <td>Proximity to areas recently developed</td>
        </tr>
    </tbody>
</table>

The image below shows the physical map of Georgetown, Guyana and its surroundings, with higher altitude shown in lighter pixels: 
<p align="center">
  <img width="460" src="https://raw.githubusercontent.com/EL-BID/Modelo-de-prediccion-de-crecimiento-urbano-/master/img/physical.PNG?token=ACL46SIEMLFJ4AS6ABRQDZS4Y6FWW">
</p>

The heat map below shows the availability of transportation in the same city, with lighter pixels showing areas where transportation is more available: 
<p align="center">
  <img width="460" src="https://raw.githubusercontent.com/EL-BID/Modelo-de-prediccion-de-crecimiento-urbano-/master/img/transport.PNG?token=ACL46SNHQAMOOFWIEMQXAHC4Y6GBU">
</p>

As in any urban growth prediction model, attractors and restrictors of will vary from one metropolitan area to another, and thus inputs will also vary accordingly. This user-friendly script clearly designates an **inputs** section, the primary and often only section that will need to be updated to fit the model to a new urban area.

Using the designated inputs, a regularized spatial logistic regression model will predict urban growth on a pixel-by-pixel level within the determined boundaries, and output a binary raster file.

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
