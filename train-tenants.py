from azureml.core import Workspace, Environment, Experiment
from azureml.core.compute import ComputeTarget
from azureml.core.runconfig import RunConfiguration
from azureml.data import OutputFileDatasetConfig
from azureml.pipeline.steps import PythonScriptStep, ParallelRunConfig, ParallelRunStep
from azureml.pipeline.core import Pipeline

# workspace
ws = Workspace.from_config()

# compute clusters
fetch_ct = ComputeTarget(workspace=ws, name="cpu-2x-ds2v2")
train_ct = ComputeTarget(workspace=ws, name="cpu-2x-ds2v2")

# environments definitions
fetch_e = Environment.from_docker_image(
    name="fetch_env",
    image="mcr.microsoft.com/azureml/openmpi3.1.2-ubuntu18.04",
    conda_specification = "./fetch/conda.yml")

train_e = Environment.from_docker_image(
    name="train_env",
    image="mcr.microsoft.com/azureml/openmpi3.1.2-ubuntu18.04",
    conda_specification = "./train/conda.yml")

# tenant metadata
tenant_metadata_ofdc = OutputFileDatasetConfig(name="tenant_metadata")

# fetch step
fetch_rc = RunConfiguration()
fetch_rc.environment = fetch_e
fetch_pss = PythonScriptStep(
    name="fetch",
    script_name="./fetch/fetch.py",
    compute_target=fetch_ct,
    runconfig = fetch_rc,
    allow_reuse=True,
    outputs=[tenant_metadata_ofdc],
    arguments=["--tenant_metadata_folder", tenant_metadata_ofdc]
    )

# tenant parallel process step
train_prc = ParallelRunConfig(
    environment=train_e,
    entry_script="./train/train.py",
    output_action="summary_only",
    mini_batch_size="1",
    compute_target=train_ct,
    node_count=2,
    process_count_per_node=2,
    run_invocation_timeout=600,
    error_threshold=1,
    run_max_try=1,
)
train_prs = ParallelRunStep(
    name="train",
    parallel_run_config=train_prc,
    allow_reuse=True,
    inputs = [tenant_metadata_ofdc.as_input()]
)

# run experiment
expr = Experiment(ws,'train-tenants')
pipeline = Pipeline(workspace=ws, steps=[train_prs])
expr.submit(pipeline).wait_for_completion(show_output=True)