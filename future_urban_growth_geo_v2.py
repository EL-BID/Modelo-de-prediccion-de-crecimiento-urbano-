
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mar 12 09:22:16 2019

@author: NeerajBaruah
@Version: 2.0
"""


##############################################################
##############################################################
##                                                          ##
##                                                          ##
##                        IMPORTS                           ##
##                                                          ##
##                                                          ##
##############################################################
##############################################################

from osgeo import gdal, ogr, osr
from osgeo.gdalnumeric import *
from osgeo.gdalconst import *
import numpy as np
import os,time
import glob
import datetime
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.model_selection import cross_validate
import warnings


       
##############################################################
##############################################################
##                                                          ##
##                                                          ##
##                        GLOBALS                           ##
##                                                          ##
##                                                          ##
##############################################################
##############################################################
 
warnings.filterwarnings("ignore")


##############################################################
##############################################################
##                                                          ##
##                                                          ##
##                        FUNCTIONS                         ##
##                                                          ##
##                                                          ##
##############################################################
##############################################################

'''
    Get current date and time 
'''
def getDateTime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    


'''
    Get raster as band or array output from raster file name
'''
def getRaster(rst_nme, band=1, asArray=1):
    
    if isinstance(rst_nme, np.ndarray):
        arr = rst_nme
    else:        
        rst = gdal.Open(rst_nme)
        band_data = rst.GetRasterBand(band)
        arr = BandReadAsArray(band_data)     
        
    if asArray == 1:
        
        return arr
    else:
        return band

'''
    Convert array to a single band raster
'''        
def arr2rst(ref_rst, arr, output_file, file_type=gdal.GDT_Byte):
    
    ref = gdal.Open(ref_rst, GA_ReadOnly)
    band = ref.GetRasterBand(1)
    proj = ref.GetProjection()
    geotransform = ref.GetGeoTransform()
    xsize = band.XSize
    ysize = band.YSize
    
    gtiff = gdal.GetDriverByName('GTiff') 
    out = gtiff.Create(output_file, xsize, ysize, 1, file_type)
    out.SetProjection(proj)
    out.SetGeoTransform(geotransform)
    
    out.GetRasterBand(1).WriteArray(arr) 
    out = None

'''
    Convert potential raster to urban forecasts using number of pixels to convert
'''
def get_urban_threshold(potential_raster, pixels):
  
    urb_pot = getRaster(potential_raster)    
    urb_pot = urb_pot[urb_pot > 0]
    
    u,v = np.unique(urb_pot, return_counts=True)
    total_avail_pixels = sum(v)
    thresh = sorted(urb_pot, reverse=True)[:pixels][-1] 
    
    global logdata
    logdata.append("{0}  Total available land: {1} sq.km \n" .format(getDateTime(), round((total_avail_pixels*30*30)/1000000,2)))
    logdata.append("{0}  Threshold for the multi-criteria raster: {1} \n" .format(getDateTime(), thresh))
    
    return(thresh)


'''
    Threshold the potential surface using computed threshold
'''    
def threshold_raster(raster, thresh, convert_pixels):
    rst = getRaster(raster)
    t_rst = rst
    t_rst[t_rst >= thresh] = 1
    t_rst[t_rst != 1] = 0
    u,v = np.unique(t_rst, return_counts=True)
    outname = "urban_projection_binary.tif"
    arr2rst(raster, t_rst, outname)
    
    global logdata
    logdata.append("{0}  Urban built projections raster created \n" .format(getDateTime()))

'''
    Threshold the potential surface using computed threshold
'''    
def threshold_raster_subregions(rst, thresh, convert_pixels):
    t_rst = rst
    t_rst[t_rst >= thresh] = 1
    t_rst[t_rst != 1] = 0
    u,v = np.unique(t_rst, return_counts=True)
#    if v[-1] > convert_pixels:
#        
    
    return t_rst
    
#    global logdata
#    logdata.append("{0}  Urban built projections raster created \n" .format(getDateTime()))


'''
    Create random samples for logistic regression as a raster
'''
def create_random_sample(raster, samples=2000):
    rst = getRaster(raster)
    size = rst.shape
    tot = size[0]*size[1]
    prob_1 = samples/tot    
    rs = np.random.choice([0, 1], size=size, p=[1 - prob_1, prob_1])
    
    outname = "random_sample.tif"
    arr2rst(raster, rs, outname)
    
    global logdata
    logdata.append("{0}  Random samples with N={1} generated \n" .format(getDateTime(), samples))


def km2_to_pixels(demand):
#    demand = demand[0]
    pixels = int(round((demand*1000000.0)/(30*30),0))
    
    global logdata
    logdata.append("{0}  {1} pixels corresponding to {2} sq.km demand area to be met \n" .format(getDateTime(), pixels, demand))
    
    return pixels

'''
    Extract random sample values from the rasters
'''
def extract_random_sample_values(random_sample_rst, raster):
    r_rst = getRaster(random_sample_rst)
    rst = getRaster(raster)
    r_rst = r_rst.astype(np.float32, copy=False)
    
    r_rst[r_rst == 0] = np.NaN
    a = r_rst*rst
    a = a.flatten()
    a = a[~np.isnan(a)]
    return a

def data_for_log_regression(predictors, change):    
    values_for_reg_rasters = predictors
    values_for_reg_rasters.append(change)
    
    df = pd.DataFrame()
    for p in values_for_reg_rasters:
        nums = extract_random_sample_values('random_sample.tif', p)
        se = pd.Series(nums)
        df['{0}' .format(p)] = se.values
    return df
    

'''
    Run logistic regression
'''
def logistic_regression(file):
    global logdata
    logdata.append("{0}  Running model for weights ...\n" .format(getDateTime()))
    
    df = file 
    
    x = df.iloc[:, :-1].values
    y = df.iloc[:,-1].values
    
    model = LogisticRegression()
    model.fit(x, y)
    predicted_classes = model.predict(x)
    accuracy = metrics.accuracy_score(y.flatten(),predicted_classes)
    
    ### Introduction of cross-validation. More accurate measure of accuracy. 
    ### Next, we use lasso regression and other methods to choose the best logistic regression model 
    ### (and there could be many variants of logistic regression)
    cv_results = cross_validate(model, x, y, cv=300, return_train_score=False)   
    
    coeffs = model.coef_
    intercept = model.intercept_  ## to review the weighting procedure later based on RUG
   
    weights = [abs(a) for a in coeffs[0]]
    weights = [a/sum(weights) for a in weights]
    
    logdata.append("{0}  Accuracy of model: {1}% \n" .format(getDateTime(), round(mean(cv_results['test_score'])*100,2)))
    logdata.append("{0}  Computed weights: {1} \n" .format(getDateTime(), " ".join([str(round(w,3)) for w in weights])))
    
    return(weights) ##


'''
    Create attraction surface using multi-criteria evaluation
'''
def MCE(rasters, weights, ag_pen, ag_rst, ag_fac):

    rasters = [r for r in rasters if r != 'urban_change_90_17.tif'] 
    
    rst = getRaster(rasters[0])
    rst = rst*(weights[0])
    
    counter = 1

    for r in rasters[1:]:
        rst_n = getRaster(r)
        rst_n = rst_n*float(weights[counter])
        rst = rst + rst_n
        counter = counter + 1
    
    rst_n = (rst - np.amin(rst))/(np.amax(rst) - np.amin(rst))  ### normalise between 0 and 1

#    ########### to review the weight procedure based on RUG
#    rst = rst + intercept ##
#    rst_P = (np.exp(rst))/(1 + np.exp(rst)) ##
#    rst_O = np.power(rst_P, attraction_factor)*np.power(random.uniform(0,1), random_factor) ##
    

    attraction_factor = 0.9
    random_factor = 0.1
    
    rst_p = np.power(rst_n, attraction_factor)*np.power(np.random.rand(int(rst_n.shape[0]), int(rst_n.shape[1])), random_factor)
    
    if ag_pen == 1:
        agrst = getRaster(ag_rst)
        rst_p = rst_p*np.power(agrst, ag_fac)
        
    
    
    
    outname = "mce.tif"    
    arr2rst(rasters[0], rst_p, outname, file_type=gdal.GDT_Float64)
    
    global logdata
    logdata.append("{0}  Multi-criteria evaulation attraction raster created ... \n" .format(getDateTime()))


'''
    Create restrictions layer
'''
def restrictions_mask(rasters, mce_raster):
    rst = getRaster(rasters[0])
    
    for r in rasters[1:]:
        ar = getRaster(r)
        rst = rst*ar
    
    mce = getRaster(mce_raster)

    mce_mask = rst*mce
        
    outname_msk =  "res.tif"
    arr2rst(rasters[0], rst, outname_msk)
           
    outname_mce = "mce_res.tif"
    arr2rst(rasters[0], mce_mask, outname_mce, file_type=gdal.GDT_Float64)
    
    
    global logdata
    logdata.append("{0}  Restrictions layer created ... \n" .format(getDateTime()))


'''
    Spatial model run
'''
def execution(att, rest, dem, w, subr, subrm, ag_pen, ag_rst, ag_fac):
    MCE(att, w, ag_pen, ag_rst, ag_fac)
    restrictions_mask(rest, "mce.tif")
    if subr == 1:        
        m = getRaster('mce_res.tif')
        s = getRaster(subrm)

        bin_raster = np.zeros(m.shape)
        
        u,v = np.unique(s, return_counts=True)
        u = u[:-1]   
#        print(u)
        count = 0
        for i in u:
            zone = np.where(s == i, 1, 0)
            mce_zone = zone*m
            convertable_pixels = km2_to_pixels(dem[count])
            thresh = get_urban_threshold(mce_zone, pixels=convertable_pixels)
            mask_rst = threshold_raster_subregions(mce_zone, thresh, convertable_pixels)  
            z,b = np.unique(mask_rst, return_counts=True)
            bin_raster = bin_raster + mask_rst
            count = count + 1           
        
        arr2rst('mce_res.tif', bin_raster, "urban_projection_binary.tif")          
            
    else:
        convertable_pixels = km2_to_pixels(dem[0])
        thresh = get_urban_threshold("mce_res.tif", pixels=convertable_pixels)
        threshold_raster("mce_res.tif", thresh, convertable_pixels)  
        
'''
******** DO NOT CHANGE ANYTHING ABOVE THIS **********
        
##############################################################
##############################################################
##                                                          ##
##                                                          ##
##                        INPUTS                            ##
##                                                          ##
##                                                          ##
##############################################################
##############################################################
'''  

'''Input urban change map between years'''
change_map = ['urban_change_90_17.tif'] 

'''Input sub-region raster mask. If no sub-regions, include 'None' '''
subregion_map = ['region_mask_2.tif'] 

'''Input list of predictors - attraction layers'''   
attractors = ['urban.tif', 'transport.tif', 'quality_of_life.tif', 'physical.tif', 'amenities.tif', 'agglomeration.tif']

'''Input list of developmental controls - restriction layers. URBAN abd WATER compulsory'''
restrictors = ['bau.tif']

'''Agricultural penalty'''
ag_penalty = 1
ag_raster = ['agriculture_penalty.tif']
ag_factor = [0.2]

'''1 if weights user supplied or 0 if determined by logistic regression'''
user_supplied_weights = 0
weights = []

'''Random sample points if user supplied weights is 0'''
samples = 5000         
runs = 30

'''Sub-regional model. 1 if sub-region masks are used, 2 if only sub-region regression, and 3 for both.'''
sub_regions = 1
zone_field = []


'''Square km of land to convert. Enter as list if sub-regions are used in the same order.'''
demand_land = [10.40, 7.39, 5.87, 9.54, 1.36, 4.11, 0.73]

          



##############################################################
##############################################################
##                                                          ##
##                                                          ##
##                        RUN                               ##
##                                                          ##
##                                                          ##
##############################################################
##############################################################

start = time.time()

logdata = []
logdata.append("{0}  Initiating urban model ...\n" .format(getDateTime()))
logdata.append("{0}  Logging model inputs and parameters...\n" .format(getDateTime()))
logdata.append("{0}  Change map input: {1}\n" .format(getDateTime(), change_map[0].split('.')[0]))
logdata.append("{0}  Attractor inputs: {1}\n" .format(getDateTime(), " ".join([a.split('.')[0] for a in attractors])))
logdata.append("{0}  Restrictor inputs: {1}\n" .format(getDateTime(), " ".join([r.split('.')[0] for r in restrictors])))
logfile = open("model_log.txt", "w")

if user_supplied_weights == 1:
    execution(attractors, restrictors, demand_land, weights, sub_regions, subregion_map[0], ag_penalty, ag_raster[0], ag_factor[0])
    logdata.append("{0}  Weights supplied by user: {1}" .format(getDateTime(), weights))
else:
    weights = []
    for r in range(runs):
        create_random_sample(change_map[0], samples=samples)
        df = data_for_log_regression(predictors=attractors, change=change_map[0])
        weights_r=logistic_regression(df)
        weights.append(weights_r)
        
    w = np.array(weights)
    w_m = np.mean(w, axis=0)
    w_m = w_m.tolist()
    print(w_m)
    logdata.append("{0}  Final weights: {1} \n" .format(getDateTime(), " ".join([str(round(w,3)) for w in w_m])))
    execution(attractors, restrictors, demand_land, w_m, sub_regions, subregion_map[0], ag_penalty, ag_raster[0], ag_factor[0])
        
logfile.write("\n".join(logdata))
logfile.close()


end = time.time()

print("Processed in {0}s" .format(round(end - start,2)))




    


