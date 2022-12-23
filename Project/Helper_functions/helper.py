#Thisfile contains all the helper fuctions required for the Project
import os,sys
from Project.Exception.exception import ThyroidException
from Project.Logger.logging import logging
import yaml
import pandas as pd
import numpy as np
import dill

def read_yaml_file(file_path:str)->dict:
    """
    Returns the dictionary 
    after reading the yaml file
    """
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)

    except Exception as e:
        raise ThyroidException(e,sys)

def write_yaml_file(file_path:str,content:dict)->None:
    """
    Writes the content of dict
    type in yaml file
    """
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w') as yaml_file:
            yaml.dump(content,yaml_file)

    except Exception as e:
        raise ThyroidException(e,sys)

def reading_csv_file(file_path:str)->pd.DataFrame:
    """
    This function reads the csv file and returns the dataframe structure
    """
    try:
        if os.path.exists(file_path):
            return pd.read_csv(file_path,header=None,na_values='?')
        else:
            raise Exception(f"No file exists")    
    except Exception as e:
        raise ThyroidException(e,sys) from e

def saving_numpy_array_data(file_path:str,array:np.ndarray)->None:
    """
    This function saves the numpy array in the desired file path
    """
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'wb') as array_file:
            np.save(file=array_file,arr=array)

    except Exception as e:
        raise ThyroidException(e,sys) from e

def loading_numpy_array_data(file_path:str)->np.ndarray:
    """
    This function loads the numpy array data from the provided file path
    """
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'rb') as array_file:
            return np.load(file=array_file)
    except Exception as e :
        raise ThyroidException(e,sys) from e

def loading_object(file_path:str)->object:
    """
    This function loads the serialized object from file path 
    and returns the same
    """
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'rb') as object_file:
            return dill.load(file=object_file)
    except Exception as e:
        raise ThyroidException(e,sys) from e

def saving_object(file_path:str,ser_obj:object)->None:
    """
    This function saves the desired object in a serialized format in 
    the desired file path
    """
    try:
       os.makedirs(os.path.dirname(file_path),exist_ok=True)
       with open(file_path,'wb') as object_file:
            dill.dump(file=object_file,obj=ser_obj)
    except Exception as e:
        raise ThyroidException(e,sys) from e