# Generating Clarifying Questions 
This Generating Clarification Questions System is based on the [Faspect Fascet Generation](https://github.com/algoprog/Faspect) and requires therefore this repository.


## - ClarificationQuestionGeneration

Trainer: This code is used to train a clarification question generation system based on the input of a query and a fascet
Predictor: You can use this as evaluator to test your model on your test-dataset

## - CrossEncoder
Trainer: This Trainer tries to train a Model that evaluates if each fascet is relevant with that clarifying question
pytrec: Is used to evaluate the Crossencoder Model 

## - DataPreprocessing
Some scripts to preprocess the data and to bring the data into a shape that is required for the other scripts

## - DBpedia
Script to call the DBpedia API for every data entry to get an alternative to purely fascets as input with the query for generating clarifying questions

## - Webpage
HTML Page with all the java script and CSS files as a Demo-Frontend for the Pipeline

## - Pipeline
This Pipeline is an assembly of all the components to build one functional base. Therefore it requires a CrossEncoder Model, a ClarificationQuestionGeneration Model and the [Faspect Fascet Generation](https://github.com/algoprog/Faspect). Just put all those models and files in this pipeline Folder and adjust the 'modelpath' and the 'CEmodel_path' if necessary and let the pipeline run. You can call the API directly via the provided IP (it shows it after startup) and a query or you could try it out via the hosted model running [Clarifying Question Generation (umass.edu)](http://goulburn.cs.umass.edu/).