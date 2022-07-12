# azureml-parallel-training

Quick demo of AzureML ParallelRunStep
This simulates a very simple mock pipeline which:
- has a first step which prepares job files (simulates getting data say from a database and creating one json job file per training job, here we're simulating needing to train a model for each 'tenant' of a specific SaaS business solution)
- feeds the job json files to a ParallelRunStep, which would contain the training code for that data
- in a real life scenarios, you'll probably have the data extraction prep / engineering either done in Synapse Pipelines (DataFlows) and/or AML extra pipeline steps before the parallel training on top of the individual data files (job files)

If you're running this script on a non AML Compute Intance compute (for example your local computer):
- Go to your AML workspace (ml.azure.com), click on the drop down top right with the name of the workspace, and 'download config file'. Place that file in the root of this repo.
- Then build a local conda environment file to run the pipeline build script from:
> cd to the root of the repo
> conda env create -f conda.yml
> conda activate aml-parallel-training
> python train-tenants.py

The pipeline output will stream to the console, or you can go to your AML workspace to monitor the pipeline run.