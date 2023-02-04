# Spark and Data Lakes

## Introduction
In this project, I built a data lakehouse solution for sensor data that trains a machine learning model. I extracted the data produced by the STEDI Step Trainer sensors and the mobile app, and curate them into a data lakehouse solution on AWS so that Data Scientists can train the learning model.


## Data Generation
To simulate the data from various sources, the following S3 directories must be created:

- customer_landing
- step_trainer_landing
- accelerometer_landing

The data must be copied to these directories as a starting point.

## Glue Tables
Two Glue tables will be created for the customer_landing and accelerometer_landing zones. The SQL scripts used to create these tables must be shared in Git, and the resulting data must be captured as screenshots and named customer_landing and accelerometer_landing.

## Glue Jobs
Two AWS Glue Jobs will be created to sanitize the customer and accelerometer data from the landing zones and only store records from customers who agreed to share their data for research purposes. The sanitized customer data will be stored in a Glue table called ```customer_trusted```, and the sanitized accelerometer data will be stored in a Glue table called ```accelerometer_trusted```. The success of the Glue job must be verified by querying the ```customer_trusted``` table with Athena and capturing the data as a screenshot named ```customer_trusted```.

## Data Quality Issue
A data quality issue has been discovered with the customer data where the serial number used in the fulfillment website is not unique and is used over and over again for different customers. To address this issue, a Glue job will be created to sanitize the customer data in the Trusted Zone and create a Glue table in the Curated Zone that only includes customers who have accelerometer data and agreed to share their data for research purposes. This table will be named ```customers_curated```.

## Glue Studio Jobs
Two Glue Studio Jobs will be created to populate the step_trainer_trusted table with Step Trainer Records data for customers who have accelerometer data and agreed to share their data for research. The second Glue Studio Job will create an aggregated table called ```machine_learning_curated``` that contains Step Trainer readings and the associated accelerometer readings for the same timestamp, but only for customers who have agreed to share their data.
