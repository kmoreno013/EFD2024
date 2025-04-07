# Edmonton Food Drive Project

![Edmonton Food Drive Logo](https://github.com/kmoreno013/MyProjects/blob/main/logo_efd.png?raw=true)

## Project Overview
The Edmonton Food Drive Project aims to develop a machine learning solution to optimize the management of food donation activities in Edmonton, AB. The project focuses on enhancing the efficiency and effectiveness of drop-off and pick-up processes, streamlining route planning, and improving resource allocation.

## Problem Statement
The current food donation management system in Edmonton faces challenges in coordinating drop-off locations, pick-up processes, and route planning. There is a need to automate and optimize these processes to ensure timely collection of donations and minimize logistical complexities.

## Objectives
- **Optimize Drop-off Locations**: Develop a machine learning model to identify the best drop-off locations based on geographic distribution and donation density.
- **Automate Pick-up Route Planning**: Implement a system for assigning and optimizing pick-up routes based on geographic structure and donation counts.
- **Enhance Stakeholder Coordination**: Streamline communication and coordination between Regional Coordinators, Stake Food Drive Representatives, and Ward Food Drive Representatives.
- **Improve Data Collection and Analysis**: Enhance data collection mechanisms to gain insights into donation patterns, resource utilization, and areas of improvement.

## Solution Approach
1. **Data Analysis and Machine Learning**: 
   - Utilize historical donation data and geographic information to identify optimal drop-off locations using clustering algorithms.
   
2. **Route Planning Algorithm**: 
   - Develop an efficient routing algorithm considering donation density, distance, and time constraints using VRP solutions.

3. **Data Collection Mechanism**: 
   - Integrate real-time data collection to monitor donation counts, route progress, and resource utilization.

## Data Sources
- 2023 and 2024 Edmonton Food Drive Dataset from Google and Microsoft Survey Forms

## EFD Dashboard
- Explore the [Edmonton Food Drive Dashboard](https://public.tableau.com/app/profile/kendrick.kent.moreno/viz/EFD2024Dashboard/EFDDashboard-Main) to gain insights into donation patterns and project performance.

## Contributors
- Kendrick Moreno - Team Member
- Roe Alincastre - Team Member
- Catrina Llamas - Team Member
- Professor Uchenna Mgbaja - Faculty Advisor

## Docker Information: How to Run the App

To run the Edmonton Food Drive API using Docker, follow the instructions below:
1. Pull the Docker Images
First, pull the required images from Docker Hub:
```
docker pull kmoreno013/efd_2024:ml-app-final
docker pull kmoreno013/efd_2024:mlflow-final
docker pull kmoreno013/efd_2024:grafana-final
docker pull kmoreno013/efd_2024:prometheus-final
```

2. Run the ml_app Container (Donation Bag Predictions)
Start the ml_app container, which handles donation bag predictions and provides an API:
```
docker run -d --name efd_ml_app -p 6060:6060 kmoreno013/efd_2024:ml-app-final
```

3. Run the run_with_metric.sh Script to Monitor Training
To track your model training metrics, use the run_with_metric.sh script. This will send training metrics to Prometheus for monitoring in Grafana:
```
./run_with_metric.sh
```
Ensure that this script is executed in the correct directory where it can access the necessary resources and configuration files for model training.

4. Verify the Containers are Running
To check that both containers are running, use the following command:
```
docker ps
```
5. Access the MLflow Web UI, Prometheus and Grafana Dashboards
You can access the MLflow server by opening your browser and navigating to:
```
http://localhost:5000
```

To access Prometheus, open your browser and go to:
```
http://localhost:9090
```

To access Grafana, open your browser and go to:
```
http://localhost:3000
```
Default Login for Grafana:
* Username: admin
* Password: password

Accessing the Dashboards in Grafana:
EFD API Dashboard: This dashboard displays key metrics about the API usage and performance, including prediction times and HTTP request statistics.
Once in Grafana, navigate to the EFD API Dashboard.
EFD Training Metrics Dashboard: This dashboard tracks the training progress of the machine learning models, including metrics like MSE, RMSE, MAE, and R2 for both Polynomial Regression and Decision Trees.


6. Access the Application: Once the container is running, you can access the API through the following commands:
* Home Endpoint: `GET http://localhost:6060/efd2024_home`
* Health Status: `GET http://localhost:6060/health_status`
* Prediction (Polynomial Regression): `POST http://localhost:6060/v1/predict -H "Content-Type: application/json" -d @configs/request.json`
* Prediction (Decision Tree): `POST http://localhost:6060/v1/predict -H "Content-Type: application/json" -d @configs/request.json`
