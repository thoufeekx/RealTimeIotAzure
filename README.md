
# Assignment 2 - Real-time Monitoring System for Rideau Canal Skateway

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Prerequisites](#prerequisites)
4. [Setting Up the Environment](#setting-up-the-environment)
    - [Install Dependencies](#1-install-dependencies)
5. [Creating Azure Resources](#creating-azure-resources)
    - [Create Azure IoT Hub](#step-1-create-azure-iot-hub)
    - [Configure Sensor Python Files](#step-2-configure-sensor-python-files)
    - [Create Azure Stream Analytics Job](#step-3-create-azure-stream-analytics-job)
    - [Create Azure Blob Storage](#step-4-create-azure-blob-storage)
6. [Running the IoT Sensor Simulation](#running-the-iot-sensor-simulation)
7. [Accessing Stored Data](#accessing-stored-data)
8. [Screenshots](#screenshots)
9. [Reflection](#reflection)

---

## Overview

### Scenario Description: Rideau Canal Skateway Monitoring

The **Rideau Canal Skateway**, a UNESCO World Heritage site in Ottawa, is the world’s largest outdoor skating rink, attracting thousands of skaters every winter. To ensure safety, the National Capital Commission (NCC) needs continuous monitoring of ice conditions, which can fluctuate due to weather changes. Currently, manual monitoring methods are not sufficient for real-time decision-making.

This project implements a **real-time monitoring system** using simulated IoT sensors at three key locations:

1. **Dow's Lake**
2. **Fifth Avenue**
3. **NAC**

This project aims to measure:

- **Ice Thickness** (in cm)
- **Surface Temperature** (in °C)
- **Snow Accumulation** (in cm)
- **External Temperature** (in °C)

The sensor data will be sent to **Azure IoT Hub**, processed through **Azure Stream Analytics**, and stored in **Azure Blob Storage**. This system will help detect unsafe conditions, ensure skater safety, and allow the NCC to respond quickly to any hazards, improving both safety and operational efficiency. 

---

## System Architecture

![System Architecture Diagram](./images/1.png)

### Data Flow:

1. **IoT Sensors**:
   These simulated sensors are deployed at three key locations along the Rideau Canal Skateway: **Dow's Lake**, **Fifth Avenue**, and **NAC** (National Arts Centre). Each sensor mimics real-world conditions by generating telemetry data at regular intervals (every 10 seconds). The data generated includes critical safety parameters such as **ice thickness**, **surface temperature**, **snow accumulation**, and **external temperature**. This data provides real-time insights into the environmental conditions along the canal and helps monitor skater safety.

2. **Azure IoT Hub**:
   **Azure IoT Hub** acts as the central hub for receiving real-time telemetry from the IoT sensors. It securely ingests the data sent by the sensors at Dow's Lake, Fifth Avenue, and NAC. IoT Hub enables bi-directional communication between the IoT devices and the cloud, ensuring that the data is transmitted reliably and securely. This step is crucial for ensuring data integrity and scalability, as IoT Hub can handle data streams from multiple sensors simultaneously.

3. **Azure Stream Analytics**:
   Once the data is ingested by IoT Hub, **Azure Stream Analytics** is used to process this incoming data in real-time. Stream Analytics applies SQL-like queries to the data to calculate key metrics such as **average ice thickness**, **maximum snow accumulation**, and other important safety indicators over a rolling 5-minute window. The processed data helps identify unsafe conditions, such as thin ice or excessive snow buildup, and enables timely alerts or actions.

4. **Azure Blob Storage**:
   After the data is processed by Azure Stream Analytics, the aggregated results are stored in **Azure Blob Storage**. Blob Storage provides a scalable, cost-effective solution for storing large amounts of structured and unstructured data. The processed telemetry data is stored in **JSON format**, allowing for easy access, querying, and further analysis by stakeholders, such as data analysts or public safety teams. The structured data in Blob Storage can also be used for historical analysis, trend detection, or reporting.

---

## Prerequisites

1. **Python**: Ensure Python 3.8 or higher is installed.
2. **Azure Account**: Set up a free or paid Azure account.
3. **Required Python Libraries**: Install dependencies using `requirements.txt`.

---

## Setting Up the Environment

### 1. Clone the git repo
Run the following command to clone the repo:
```bash
git clone <repo link>
```


### 2. Install Dependencies
Run the following command to install the necessary libraries:
```bash
pip install -r requirements.txt
```

---

## Creating Azure Resources

### **Step 1: Create Azure IoT Hub**
1. Log in to the [Azure Portal](https://portal.azure.com).
2. Search for **IoT Hub** in the search bar and click **Create**.
3. Fill in the required details:
   - **Subscription**: Select your subscription.
   - **Resource Group**: Create a new one or select an existing one.
   - **Region**: Choose the region closest to your project.
   - **IoT Hub Name**: Provide a unique name.
4. Click **Review + Create** and then **Create**.
5. After deployment, navigate to the IoT Hub and create a new **Device** under **IoT devices**.
6. Copy the **Device Connection String** from the device details page.

### **Step 2: Configure Sensor Python Files**
1. Open each sensor simulation file:
   - `sensor1_DOWS_Lake.py`
   - `sensor2_Fifth_Avenue.py`
   - `sensor3_NAC.py`
2. Locate the placeholder for the IoT Hub connection string:
   ```python
   CONNECTION_STRING = "PASTE_YOUR_CONNECTION_STRING_HERE"
   ```
3. Replace the placeholder with the connection string copied from Azure IoT Hub.

---

### **Step 3: Create Azure Stream Analytics Job**
1. Search for **Stream Analytics Job** in the Azure Portal and click **Create**.
2. Fill in the required details:
   - **Job Name**: Give your job a unique name.
   - **Region**: Use the same region as your IoT Hub.
   - **Streaming Units**: Start with 1 (adjust as needed).
3. Click **Review + Create** and then **Create**.
4. After deployment:
   - Configure **Input**:
     - Type: IoT Hub.
     - Select the IoT Hub created earlier.
   - Configure **Output**:
     - Type: Blob Storage.
     - Provide the connection string and container details of your Azure Blob Storage.
   - Add **Query**:
     ```sql
     SELECT
       location,
       AVG(iceThickness) AS avgIceThickness,
       MAX(snowAccumulation) AS maxSnowAccumulation,
       System.Timestamp AS aggregationTime
     INTO
       [YourBlobOutputAlias]
     FROM
       [YourIoTHubInputAlias]
     GROUP BY
       location, TumblingWindow(Duration(minutes, 5))
     ```

---

### **Step 4: Create Azure Blob Storage**
1. Search for **Storage Account** in the Azure Portal and click **Create**.
2. Fill in the required details:
   - **Resource Group**: Use the same one as the IoT Hub.
   - **Storage Account Name**: Provide a unique name.
   - **Region**: Use the same region as your other resources.
3. Click **Review + Create** and then **Create**.
4. After deployment:
   - Navigate to **Containers** and create a new container (e.g., `processed-data`).
   - Note the container name for configuring the Stream Analytics job output.

---

## Running the IoT Sensor Simulation

1. Navigate to the cloned repository:
   ```bash

   cd <path to folder>
   ```
2. Ensure that each sensor script (`sensor1_DOWS_Lake.py`, `sensor2_Fifth_Avenue.py`, `sensor3_NAC.py`) has the correct Azure IoT Hub **Device Connection String**.

3. Start the simulation in three seperate terminals :
   ```bash
   python3 sensor1_DOWS_Lake.py
   python3 sensor2_Fifth_Avenue.py
   python3 sensor3_NAC.py
   ```

---

## Accessing Stored Data

1. Navigate to your Blob Storage container in the Azure Portal.
2. Locate the JSON files generated by the Stream Analytics job.
3. Download and analyze the data.

---

## Screenshots

Include the following screenshots in the [`screenshots`](./screenshots) directory:

1. **Azure IoT Hub Configuration**:
   - IoT Hub overview page.
   - Device details page showing the connection string.
2. **Azure Stream Analytics Job**:
   - Input configuration.
   - Output configuration.
   - Query editor with SQL query.
3. **Azure Blob Storage**:
   - Container structure.
   - Sample JSON/CSV files stored.

---

## Reflection

- **Challenges**:
  - Setting up real-time connections between sensors and Azure IoT Hub.
  - Writing optimized queries in Azure Stream Analytics.
- **Solutions**:
  - Used Azure documentation and community forums to resolve configuration issues.
  - Tested queries with sample datasets before deployment.

---

This Table of Contents should make navigation easy and clear. Let me know if there’s anything else to add!