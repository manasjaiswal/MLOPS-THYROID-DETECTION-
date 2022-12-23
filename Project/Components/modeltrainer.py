from Project.Logger.logging import logging
from Project.Exception.exception import ThyroidException
from Project.Entity.configentity import Model_Trainer_Entity
from Project.Entity.artifactentity import DataTransformationArtifact,ModelTrainerArtifact
from Project.Entity.modelfactory import ModelFactory,evaluate_classification_model,GridSearchedBestModel,MetricInfoArtifact2
import os,sys
from typing import List
from Project.Helper_functions.helper import loading_numpy_array_data,loading_object,saving_object
import pandas as pd
import numpy as np

class ThyroidPredictor:
    """
    This class combines the two objects i.e preprocessing and training and then returns the prediction on raw data
    """
    def __init__(self,preprocessing_object:object,training_object:object):
        try:
            self.preprocessing_object=preprocessing_object
            self.training_object=training_object
        except Exception as e:
            raise ThyroidException(e,sys) from e

    def predict(self,X)->np.ndarray:
        try:
            transformed_array=self.preprocessing_object.transform(X)
            return self.training_object.predict(transformed_array)
        except Exception as e:
            raise ThyroidException(e,sys) from e        
    
    def __str__(self):
        return (type(self.training_object).__name__)

    def __repr__(self):
        return (type(self.training_object).__name__)

class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact,model_trainer_config:Model_Trainer_Entity):
        try:
            logging.info(f"{':'*20}MODEL TRAINING LOG STARTED{':'*20}")
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_config=model_trainer_config
        except Exception as e:
            raise ThyroidException(e,sys) from e

    def model_training_steps(self)->ModelTrainerArtifact:
        try:
            logging.info("Creating object of Model factory class")
            mf=ModelFactory(model_config_path=self.model_trainer_config.model_config_file_path)
            logging.info("Reading transformed train and test arrays")
            train_arr=loading_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_path)
            test_arr=loading_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_path)
            logging.info("Loading preprocessing object from the file path")
            preprocessing_object=loading_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            logging.info("Splittng training and testing files into input and output array")
            train_input_arr=train_arr[:,:-1]
            test_input_arr=test_arr[:,:-1]
            train_output_arr=train_arr[:,-1]
            test_output_arr=test_arr[:,-1]
            logging.info(f"Expected Accuracy:{self.model_trainer_config.base_accuracy}")
            base_accuracy=self.model_trainer_config.base_accuracy
            logging.info('Applying grid search best model search on the training data and getting best model')
            best_model_train:GridSearchedBestModel=mf.get_best_model(X=train_input_arr,y=train_output_arr,base_accuracy=base_accuracy)
            logging.info(f"Best model details on training dataset:{best_model_train}")
            logging.info("Applying grid searched best models on the testing dataset and getting the best model")
            grid_model_list:List[GridSearchedBestModel]=mf.grid_searched_best_model_list
            model_list=[best_model.best_model for best_model in grid_model_list]
            best_model_test:MetricInfoArtifact2=evaluate_classification_model(model_list=model_list,X_train=train_input_arr,y_train=train_output_arr,X_test=test_input_arr,y_test=test_output_arr,base_accuracy=base_accuracy)
            logging.info(f"Best Model on testing dataset:{best_model_test}")
            logging.info('Combining preprocessing and training objects into one object for further use')
            training_object=best_model_test.model_object
            thyroid_model=ThyroidPredictor(preprocessing_object=preprocessing_object,training_object=training_object)
            logging.info(f"Saving {str(thyroid_model)} model in the trained model file path")
            saving_object(file_path=self.model_trainer_config.trained_model_file_path,ser_obj=thyroid_model)
            logging.info("Model saved successfully")
            if best_model_test is None:
                logging.info("No suitable model found on the testing dataset")
                model_trainer_artifact=None
            else:    
                model_trainer_artifact=ModelTrainerArtifact(
                best_model_name=best_model_test.model_name, 
                model_object=thyroid_model, 
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                model_accuracy=best_model_test.model_accuracy, 
                train_acc=best_model_test.train_accuracy,
                test_acc=best_model_test.test_accuracy,
                model_fbeta_score=best_model_test.model_fbeta,
                is_trained=True
                )    
            logging.info(f"\nModel Training Artifact:{model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise ThyroidException(e,sys) from e
    
    def initiate_model_training(self)->ModelTrainerArtifact:
        try:
            return self.model_training_steps()
        except Exception as e:
            raise ThyroidException(e,sys) from e 

    def __del__(self):
        logging.info(f"{':'*20}MODEL TRAINING LOG ENDED{':'*20}")        
