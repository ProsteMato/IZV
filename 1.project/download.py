"""
This module contains class DataDownloader.
Prints statistics about few regions from dataset when started as main program.
"""
import requests
import gzip
import pickle
import csv
import zipfile
import os
import sys
import re
import numpy as np
from bs4 import BeautifulSoup
from io import TextIOWrapper
import platform


__author__ = "Martin Koči"
__email__ = "xkocim05@stud.fit.vutbr.cz"

class DataDownloader:
    """Class that downloads and parsed data from specified url and save them into specified folder"""

    def __init__(self, url="https://ehw.fit.vutbr.cz/izv/", folder="data", cache_filename="data_{}.pkl.gz"):
        """
        Keyword Arguments:
        url -- url to download data from (default https://ehw.fit.vutbr.cz/izv/)
        folder -- folder to store downloaded and cached data (default data)
        cache_filename -- format of cache filename (default data_{}.pkl.gz)
        """
        
        if not os.path.isdir(folder):
            os.mkdir(folder)
        self.__url = url
        self.__folder = folder
        self.__cache = cache_filename
        self.__files = self.__get_files()
        self.__stored_data = {}
        self.__types = [(np.unicode_, 3), np.int64, np.int8, np.int8, 'datetime64[D]', np.int8, np.int16, np.int8, np.int8, np.int8, np.int8, np.int8, np.int8,
        np.int16, np.int8, np.int8, np.int8, np.int16, np.int8, np.int8, np.int8, np.int8, np.int8, np.int8, np.int8, np.int8, np.int8, np.int8, np.int8, np.int8,
        np.int8, np.int8, np.int8, np.int8, np.int8, np.int8, np.int8, np.int8, np.int8, np.int8, np.int8, np.int8, np.int16, np.int8, np.int8, np.int8, np.int8,
        np.float32, np.float32, np.float32, np.float32, np.float32, (np.unicode_, 30), (np.unicode_, 30), (np.unicode_, 30), (np.unicode_, 30), (np.unicode_, 30),
        np.int32, (np.unicode_, 30), (np.unicode_, 30), (np.unicode_, 30), np.int64, np.int64, (np.unicode_, 30), np.int8]
        

    def download_data(self):
        """Checks if all files with specific names are downloaded.
        If some of them are not present it downloads them form specified url and saves them into given folder.        
        """
        
        for file in self.__files:
            file_to_download = os.path.join(self.__folder, os.path.basename(file))
            if not os.path.isfile(file_to_download):
                self.__download_file(file)

    def __download_file(self, filename):
        """Downloads file with specified filename from url and saves it into specified folder.
        
        Arguments:
        filename -- name of the file that is downloaded
        """
        
        respons = requests.get(self.__url + filename, stream=True)
        save_filename = os.path.join(self.__folder, os.path.basename(filename))
        with open(save_filename, 'wb') as output_file:
            for chunk in respons.iter_content(chunk_size=128):
                output_file.write(chunk)
                
    def __get_files(self):
        """Gets all filenames that needs to be downloaded from specified url."""
        
        files = []
        with requests.Session() as s:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            respons = s.get(self.__url, headers=headers).text
            soup = BeautifulSoup(respons, 'html.parser')
            data_files = [link.get('href') for link in soup.find_all('a', class_="btn-primary")]
            for year in soup.find_all('td', class_="align-middle"):
                regex = re.compile(r"data/data-?gis({year}|\-rok\-{year})\.zip".format(year=year.text))
                if any((match := regex.match(link)) for link in data_files):
                    files.append(match.group(0))
                else:
                    files.append(data_files[-1])
        return files

    def parse_region_data(self, region):
        """Downloads and parses data for specified region and returns them in tuple of list[str] that represents lables
        in list[numpy.ndarray] that is second element in tuple. 
        
        Argument:
        region -- region to parse
        """
        
        self.download_data()
        region_filename = self.__get_region_filename(region)
        list_str = ["region", "p1", "p36", "p37", "p2a", "weekday(p2a)", "p2b", "p6", "p7", "p8", "p9", "p10", 
        "p11", "p12", "p13a", "p13b", "p13c", "p14", "p15", "p16", "p17", "p18","p19", "p20", "p21", 
        "p22", "p23", "p24", "p27", "p28", "p34", "p35", "p39", "p44", "p45a", "p47", "p48a", "p49", 
        "p50a", "p50b", "p51", "p52", "p53", "p55a", "p57", "p58", "a", "b", "d", "e", "f", "g", "h", 
        "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "p5a"]
        
        row_count = self.__get_files_row_count(region)
        list_arrays = [np.zeros(row_count, dtype=dt) for dt in self.__types]
        row_index = 0
        for file in self.__files:
            file_to_parse = os.path.join(self.__folder, os.path.basename(file))
            with zipfile.ZipFile(file_to_parse, "r") as zf:
                with zf.open(region_filename, 'r') as csv_file:
                    reader = csv.reader(TextIOWrapper(csv_file, 'windows-1250'), delimiter=';', quotechar='"')
                    for row in reader:
                        list_arrays[0][row_index] = region
                        for col_index, col in enumerate(row):
                            try:
                                list_arrays[col_index + 1][row_index] = col
                            except ValueError:
                                if list_arrays[col_index + 1][row_index].dtype == np.int64:
                                    list_arrays[col_index + 1][row_index] = -1
                                elif list_arrays[col_index + 1][row_index].dtype == 'datetime64[D]':
                                    print('Error2:', col)
                                elif list_arrays[col_index + 1][row_index].dtype == np.float64:
                                    if type(col) != str:
                                        list_arrays[col_index + 1][row_index] = col.replace(',', '.')
                                    else:
                                        list_arrays[col_index + 1][row_index] = float("nan")
                        row_index += 1
                        
        return (list_str, list_arrays)
    
    def __get_files_row_count(self, region):
        """Counts and returns sum of all rows for specific reagion in all files.
        
        Arguments:
        region -- specific region
        """
        
        count = 0
        for file in self.__files:
            file_to_parse = os.path.join(self.__folder, os.path.basename(file))
            with zipfile.ZipFile(file_to_parse, "r") as zf:
                with zf.open(self.__get_region_filename(region), 'r') as csv_file:
                    reader = csv.reader(TextIOWrapper(csv_file, 'windows-1250'), delimiter=';', quotechar='"')
                    count += sum(1 for row in reader)
        return count
                    
                
    def __get_region_filename(self, region):
        """Returns a filename that represents region
        
        Arguments:
        region -- specified region for translation.
        """
        
        return {
            'PHA': '00.csv',
            'STC': '01.csv',
            'JHC': '02.csv',
            'PLK': '03.csv',
            'KVK': '19.csv',
            'ULK': '04.csv',
            'LBK': '18.csv',
            'HKK': '05.csv',
            'PAK': '17.csv',
            'OLK': '14.csv',
            'MSK': '07.csv',
            'JHM': '06.csv',
            'ZLK': '15.csv',
            'VYS': '16.csv',
        }[region]

    def get_list(self, regions = None):
        """Returns tuple (list[str], list[numpy.ndarray]) for specific regions
        where list[str] contains labels for each numpy.ndarray in list[numpy.ndarray]
        
        Keyword Arguments:
        regions -- list of region codes to parse (default None)
        """
        
        data = []
        if regions is None:
            regions = ['PHA','STC','JHC','PLK','KVK','ULK','LBK','HKK','PAK','OLK','MSK','JHM','ZLK','VYS']
        for region in regions:
            cache_file = os.path.join(self.__folder, self.__cache.format(region))
            if region in self.__stored_data.keys():
                data.append(self.__stored_data[region])
            elif os.path.isfile(cache_file):
                with gzip.open(cache_file, "rb") as file_data:
                    self.__stored_data[region] = pickle.load(file_data)
                    data.append(self.__stored_data[region])
            else:
                parsed_data = self.parse_region_data(region)
                with gzip.open(cache_file, "wb") as file_data:
                    pickle.dump(parsed_data, file_data, protocol=-1)
                self.__stored_data[region] = parsed_data
                data.append(parsed_data)
        concatenated_data = []
        for j in range(65):
            concatenated_data.append(np.concatenate([data[i][1][j] for i in range(len(data))]))
        return (data[0][0], concatenated_data)
    
if __name__ == "__main__":
    regions = ['PHA','STC','JHC']
    labels, data = DataDownloader().get_list(regions)
    print("Labels:", labels, sep="\n")
    print("Number of records: " + str(data[0].size))
    print("Regions in dataset: " + regions.__repr__())


    