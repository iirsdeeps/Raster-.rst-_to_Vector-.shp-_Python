#-------------------------------------------------------------------------------
# Name:        dataprocessing
# Purpose:     .rst(raster, input)  to .shp(vector, output) conversion
#              Output file names are same as that of the input
#              If there is corrupt files in input directory, the script
#              will mention it in the log file.
#
# Author:      SHIKHAR
#
# Created:     20/03/2016
# Copyright:   (c) SHIKHAR 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import gdal,sys, ogr, osr,os

#-------------------------------------------------------------------------------
#configuration
input_data_folder  = r'D:\ahmedabad\Example_data'
output_data_folder = r'D:\ahmedabad\shapefile_data'
log_file = output_data_folder+ r'\log.txt'

#-------------------------------------------------------------------------------


def main():
    with open(log_file, 'w+') as log_data: # opening the log file
        for in_file in os.listdir(input_data_folder): # getting the all files from the inputfolder
            if in_file.endswith('.rst'): # checking if the filename is .rst
                print "file " + in_file+ " being processed"
                filename = in_file.split('.')[0] # extracting the filename

                error_counter = 0   # counter to verify if the input file has proper data
                dataset = gdal.Open(input_data_folder+ '\\'+ in_file)# opening the file

                if dataset is None: # if there is no data then mentioning it in the log file
                    log_data.write(filename+'.rst' +' has no data \n')
                    error_counter=1
                try:    # check for the corrupt data in the .rst file
                    if dataset:
                        band = dataset.GetRasterBand(1)
                except Exception as error :
                    log_data.write(filename+'.rst' + ' cannot be read \n')
                    error_counter=2

                if error_counter==0: # if the .rst has proper data then only it will be processed further

                    # getting the projection from the input .rst file

                    wkt = dataset.GetProjectionRef()
                    src = osr.SpatialReference()
                    src.ImportFromWkt(wkt)
                    src.MorphToESRI()

                    # creating the output shapefile

                    op_layer = output_data_folder+'\\'+ filename
                    driver = ogr.GetDriverByName("ESRI Shapefile")

                    # if the file already exists removing it
                    op_layer_name = op_layer+".shp"
                    if os.path.isfile( op_layer_name):
                        os.remove(op_layer_name)

                    driver_ds = driver.CreateDataSource(op_layer_name)
                    dst_lyr = driver_ds.CreateLayer(op_layer, srs = src )

                    # using polygonize function converting raster to vector
                    gdal.Polygonize(band, None, dst_lyr, -1,[], callback= None)


if __name__ == '__main__':
    main()
