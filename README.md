# QuantileX



## Workflows

1. Download Data from Yahoo Finance:
        Retrieve financial data from Yahoo Finance using an API or web scraping.

2.  Transform:
        Clean the downloaded data, handle missing values, and format it for further processing.

3. Validate:
        Perform data validation to ensure data quality and consistency. This may involve checking for outliers, verifying data integrity, and validating against predefined criteria.

4. Train Model:
        Train machine learning models using the preprocessed data.
        Split the dataset into training and testing sets.
        Train various machine learning models and evaluate their performance.
    4.1. Track Metrics using MLflow and Save Model:
        Use MLflow to track experiment metrics, parameters, and artifacts.
        Save the trained model along with relevant metadata.
    4.2. Orchestrate it Daily Basis in Airflow:
        Use Apache Airflow to schedule and automate the entire workflow on a daily basis.
        Define DAGs (Directed Acyclic Graphs) to represent the workflow steps and their dependencies.
        Set up tasks for each step, ensuring proper orchestration and execution.
5. Deploy it to Amazon Web Services using CI/CD:
        Implement Continuous Integration/Continuous Deployment (CI/CD) pipelines for automated deployment to AWS.
        Package the trained model and associated code into deployable artifacts.
        Utilize AWS services such as Amazon SageMaker for model deployment.
        Implement version control and automated testing within the CI/CD pipeline.
6. Inference:
        After deployment, the model is ready for inference.
    Send new data to the deployed model for prediction or classification.
    Monitor model performance in production and iterate on improvements as necessary.



# How to run?
### STEPS:

Clone the repository

```bash
https://github.com/datasinner/QuantileX.git
```
### STEP 01- Create a conda environment after opening the repository

```bash
conda create -n quantilex python=3.10 -y
```

```bash
conda activate quantilex
```


### STEP 02- install the requirements
```bash
pip install -r requirements.txt
```


```bash
# Finally run the following command
python app.py
```

Now,
```bash
open up you local host and port
```




# AWS-CICD-Deployment-with-Github-Actions

## 1. Login to AWS console.

## 2. Create IAM user for deployment

	#with specific access

	1. EC2 access : It is virtual machine

	2. ECR: Elastic Container registry to save your docker image in aws


	#Description: About the deployment

	1. Build docker image of the source code

	2. Push your docker image to ECR

	3. Launch Your EC2 

	4. Pull Your image from ECR in EC2

	5. Lauch your docker image in EC2

	#Policy:

	1. AmazonEC2ContainerRegistryFullAccess

	2. AmazonEC2FullAccess

	
## 3. Create ECR repo to store/save docker image
    - Save the URI: https://983727701212.dkr.ecr.ap-northeast-2.amazonaws.com/quantilex

	
## 4. Create EC2 machine (Ubuntu) 

## 5. Open EC2 and Install docker in EC2 Machine:
	
	
	#optinal

	sudo apt-get update -y

	sudo apt-get upgrade
	
	#required

	curl -fsSL https://get.docker.com -o get-docker.sh

	sudo sh get-docker.sh

	sudo usermod -aG docker ubuntu

	newgrp docker
	
# 6. Configure EC2 as self-hosted runner:
    setting>actions>runner>new self hosted runner> choose os> then run command one by one


# 7. Setup github secrets:

    AWS_ACCESS_KEY_ID=

    AWS_SECRET_ACCESS_KEY=

    AWS_REGION = 

