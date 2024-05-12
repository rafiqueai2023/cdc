import os
import urllib.request as request
from zipfile import ZipFile
import tensorflow as tf
from ChickenDisease.entity.config_entity import EvaluationConfig
from ChickenDisease.utils.common import save_json
from pathlib import Path


class Evaluation:
    def __init__(self, config: EvaluationConfig):
        self.config = config
    

    def _valid_generator(self):

        datagenerator_kwargs = dict(
            rescale = 1./255,
            validation_split = 0.30
        )

        dataflow_kwargs = dict(
            target_size = self.config.params_image_size[:-1],
            batch_size = self.config.params_batch_size,
            interpolation = "bilinear"
        )

        valid_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs #type: ignore
            )
        
        self.valid_generator = valid_datagenerator.flow_from_directory(
            directory = self.config.training_data,
            subset = "validation",
            shuffle = False,
            **dataflow_kwargs #type: ignore
            )
    @staticmethod
    def load_model(path: Path) -> tf.keras.Model:
        return tf.keras.models.load_model(path) #type: ignore
    
    def evaluation(self):
        self.model = self.load_model(self.config.path_of_model)
        self._valid_generator()
        self.score = self.model.evaluate(self.valid_generator)  #type: ignore
    
    def save_score(self):
        scores = {"loss": self.score[0], "accuracy": self.score[1]}
        save_json(path = Path("scores.json"), data = scores)