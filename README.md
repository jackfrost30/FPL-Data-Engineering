# FPL-Data-Engineering

## Description
This project automates the process of fetching, cleaning, and analyzing Fantasy Premier League (FPL) data. It uses an ETL pipeline to extract data from the FPL API, clean and transform it, and store it in a Dockerized PostgreSQL database. Apache Airflow is used to automate and data is visualized through Power BI dashboards and reports.

---

## Table of Contents
1. [Requirements](#requirements)
2. [Getting Started](#getting-started)
    - [Clone the Repository](#clone-the-repository)
    - [Modify `.env.example`](#modify-env-example)
    - [Install Docker Desktop](#install-docker-desktop)
    - [Run Docker Compose](#run-docker-compose)
3. [How It Works](#how-it-works)

---

## Requirements
- **Docker Desktop**: Make sure Docker Desktop is installed and running on your machine.
- **Git**: You'll need Git to clone the repository.
- **Python** (Optional): Depending on your project's setup, you may also need Python installed for any local development or testing.
  
---

## Getting Started

### Clone the Repository
1. Clone the repository to your local machine using the following command:
   ```bash
   git clone https://github.com/jackfrost30/FPL-Data-Engineering.git
   cd your-repository

### Modify .env.example
2. In the root of the project directory, you'll find a file named `.env.example`. **Rename** this file to `.env` and **modify** it with your own values.

   Example:
   ```bash
   POSTGRES_DB=airflow
   POSTGRES_USER=airflow
   POSTGRES_PASSWORD=airflow
   POSTGRES_HOST=postgres
   POSTGRES_PORT=5432
   AIRFLOW__CORE__LOAD_EXAMPLES=False
   AIRFLOW__CORE__EXECUTOR=SequentialExecutor
   AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres:5432/airflow
   AIRFLOW__WEBSERVER_BASE_URL=http://localhost:8080
   AIRFLOW__WEBSERVER__SECRET_KEY=YOUR_SECRET_KEY

### Install Docker Desktop
3. Ensure that **Docker Desktop** is installed on your machine. You can download it from the official Docker website. After installation, make sure Docker Desktop is running.


### Run Docker Compose
4. Once Docker is set up and the `.env` file is configured, you can start the project services using **Docker Compose**.

   Run the following command to bring up the services defined in `docker-compose.yml`:

   ```bash
   docker-compose up

   This command will build the Docker containers and start the application. If this is the first time you're running it, Docker may need to pull the required images, which could take a few minutes. Once the containers are 
   up, the application will be available and running locally, and you can access it through the designated ports specified in the docker-compose.yml.
   To run the containers in detached mode (background), use the following command:

   ```bash
   docker-compose up -d

   To shut down the containers when you're done:

   ```bash
   docker-compose down


## How It Works
This project automates the process of fetching, cleaning, and visualizing Fantasy Premier League (FPL) data through an end-to-end solution. Here's a breakdown of how it works:

### 1. **Data Extraction (ETL Process)**
   - **Extract:**  The process starts by fetching raw data from the Fantasy Premier League (FPL) API. This API provides data on teams, fixtures, events, and player statistics, which is essential for FPL analysis.
   - **Transform:** The raw data is then cleaned and transformed. This includes:
     - Converting the data into a suitable format for analysis.
     - Handling missing or incorrect values.
     - Structuring the data in a way that makes it easy to use for reporting and analysis.
   - **Load:** The cleaned data is loaded into a PostgreSQL database, which is hosted using Docker. This step ensures that all the data is stored in one place and can be accessed easily for further analysis.
     
### 2. **Data Automation with Apache Airflow**
   - The ETL process is automated using **Apache Airflow**, a workflow orchestration tool. Airflow schedules and manages the running of tasks such as:
     - Fetching data from the API.
     - Cleaning and transforming the data.
     - Loading the data into the PostgreSQL database.
   - This automation ensures that data updates happen at regular intervals without manual intervention.

### 3. **Data Visualization with Power BI**
   - After the data is loaded into the database, **Power BI** is used to create interactive dashboards and reports. These dashboards provide insights into:
     - Gameweek performance.
     - Team statistics and fixtures.
     - Opponent difficulty and other key metrics.
   - Users can filter and explore the data through dynamic visualizations, making it easier to analyze trends and performance over time.

### 4. **Containerization with Docker**
   - The entire project is containerized using **Docker**. Docker allows the project to run consistently across different environments by packaging the application (including the PostgreSQL database and Apache Airflow) 
     into containers.
   - This setup makes it easier to deploy and manage the project in various environments, ensuring that the database and Airflow DAGs are isolated and can run independently.

### 5. **Repository Workflow**
   - The **GitHub repository** contains:
     - Code for fetching and cleaning data from the FPL API.
     - Docker configuration files to run the PostgreSQL database and Airflow.
     - Power BI reports and dashboards.
     - Instructions for running the ETL pipeline and setting up the project.
