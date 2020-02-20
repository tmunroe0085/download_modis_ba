import subprocess
import os
import glob

windows = ['Win01', 'Win02', 'Win03', 'Win04', 'Win05', 'Win06', 'Win07', 'Win08', 'Win09', 'Win10', 'Win11', 'Win12', 'Win13', 'Win14', 'Win15', 'Win16', 'Win17', 'Win18', 'Win19', 'Win20', 'Win21', 'Win22', 'Win23', 'Win24']
years = ['2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']
days = ['001','032','060','091','121','152','182','213','244','274','305','335']



for year in years:

    outfolder = year+r"/"
    s3_path = r"s3://gfw-files/tmunroe/burn_scars/"+year+r"/"

    try:
        os.makedirs(outfolder)
    except:
        pass

    image_list = []

    for win in windows:
        for day in days:

            ftp_path = r"ftp://ba1.geog.umd.edu/Collection6/TIFF/"+win+r"/"+year+r"/"
            outname = "MCD64monthly.A"+year+day+"."+win+".006.burndate.tif"

            outpath = outfolder + outname
            file_name = ftp_path + outname

            print(file_name)

            cmd = ['wget', '--ftp-user=user', '--ftp-password=burnt_data', file_name]
            subprocess.check_call(cmd, shell=True)

            image_list.append(outname)

    os.chdir(outfolder)

    mosaic_file = "modis_burned_area_"+year+".tif"

    mosaic_vrt = "modis_burned_area_"+year+".vrt"

    cmd2 = ['gdalbuildvrt', mosaic_vrt, "*tif"]
    subprocess.check_call(cmd2, shell=True)

    cmd3 = ['gdalwarp', '-co', 'COMPRESS=LZW', mosaic_vrt, mosaic_file]
    subprocess.check_call(cmd3, shell=True)

    os.chdir("..")

    cmd4 = ['aws', 's3', 'mv', outfolder, s3_path, '--recursive']
    subprocess.check_call(cmd4, shell=True)

