import datetime
import logging
import os

import pytorch_lightning as pl
import torch
import torch.nn as nn
import torch.optim as optim
from pytorch_lightning.callbacks import LearningRateMonitor
from pytorch_lightning.callbacks.model_checkpoint import ModelCheckpoint
from pytorch_lightning.loggers import WandbLogger

import wandb
from config import CONFIG  # ,ModelCfg
from datasets.datasets import Dataset, build_dataset, get_dataset
# from models.vt.vit import CONFIGS_VIT,VisionTransformer
# from models.vt.configs import ConfigsVit
from models.simsiam.callback import KnnMonitorInsertWandb
from models.simsiam.pl_system_simsiam import PLSystemSimSiam
# from models.build_model import get_model
from models.simsiam_model import Classifier, SimSiamModel
from datasets.CIFAR10 import *
# from datasets.datasets import Dataset,build_dataset

def main():

   wandb_logger = WandbLogger(project='vit-self-train',
                              entity='dcastf01',
                              name=datetime.datetime.utcnow().strftime("%Y-%m-%d %X"),
                              # offline=True, #to debug
                              )
   
   # get dataloaders for training and testing
   dataset=get_dataset("C10")
   # train_loader,train_classifier_loader, test_loader, num_classes = \
   #    build_dataset(dataset=dataset,
   #                   batch_size=CONFIG.BATCH_SIZE,
   #                   )
   # use a GPU if available
   gpus = 1 if torch.cuda.is_available() else 0

   
      

   # config_vit=CONFIGS_VIT[ConfigsVit.ViT_B_16]
   # knn_monitor=KnnMonitorInsertWandb( train_loader,test_loader,
                                    
                                    # )
   
   learning_rate_monitor=LearningRateMonitor(logging_interval="epoch")
   
   checkpoint_callback = ModelCheckpoint(
      monitor='train_loss_ssl',
      dirpath=CONFIG.PATH_CHECKPOINT,
      filename='TransformerSimsiamGeneral-{epoch:02d}-{val_loss:.6f}',
      mode="min",
      save_last=True,
      save_top_k=3,
                     )

   
   system=SimSiamModel(dataloader_kNN=dataloader_train_kNN,img_size=32) 
   exist_checkpoint=False
   # exist_checkpoint=True
    
   if exist_checkpoint: 
      # checkpoint_path=None
      system=system.load_from_checkpoint(
         os.path.join(CONFIG.PATH_CHECKPOINT,"TransformerSimsiamGeneral-epoch=47-val_loss=0.0000.ckpt")
         ,img_size=32)
    
   trainer=pl.Trainer(logger=wandb_logger,
                     gpus=-1,
                     max_epochs=CONFIG.NUM_EPOCHS,
                     precision=16,
                  #    limit_train_batches=1, #only to debug
                  #    limit_val_batches=1, #only to debug
                  #    val_check_interval=1,
                     log_gpu_memory=True,
                     callbacks=[
                  #         # early_stopping ,
                           checkpoint_callback,
                  #         # knn_monitor,
                           learning_rate_monitor,
                                 ]
                     )
   trainer.fit(
         system,
         train_dataloader=dataloader_train_ssl,
         val_dataloaders=dataloader_test
      )
    
   #probar la parte linear del problema
   # system.eval()
   
   # checkpoint_callback = ModelCheckpoint(
   #    monitor='train_loss_fc',
   #    dirpath=CONFIG.PATH_CHECKPOINT,
   #    filename='TransformerSimsiamClassifier-{epoch:02d}-{val_loss:.2f}',
   #    mode="min",
   #    save_last=True,
   #    save_top_k=3,
   #                   )
   # wandb_logger._name="clasificador-"+wandb_logger._name
   # classifier = Classifier(system.model,CONFIG.NUM_EPOCHS)
   # trainer = pl.Trainer(logger=wandb_logger,
   #                   gpus=-1,
   #                   max_epochs=CONFIG.NUM_EPOCHS,
   #                   precision=16,
   #                #    limit_train_batches=1, #only to debug
   #                #    limit_val_batches=1, #only to debug
   #                #    val_check_interval=1,
   #                   log_gpu_memory=True,
   #                   callbacks=[
   #                         # early_stopping ,
   #                         checkpoint_callback,
   #                         learning_rate_monitor,
   #                         # knn_monitor
   #                               ]
   #                         )
   
   
   # trainer.fit(
   #    classifier,
   #    train_classifier_loader,
   #    test_loader
                  # )      
        
        
        
if __name__ == "__main__":
    main()
