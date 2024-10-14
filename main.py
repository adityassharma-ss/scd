# **SCD Analysis App**

**SCD Analysis App** is a powerful application designed to streamline and automate the generation of Standard Control Documentation (SCD). Using a combination of **Streamlit** for the frontend, and **OpenAI** for generating content based on the user’s input, this tool provides quick and efficient document generation for developers and analysts.

---

## **Table of Contents**
- [Features](#features)
- [Technologies](#technologies)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
  - [Run the Application](#run-the-application)
  - [Accessing the Application](#accessing-the-application)
- [Docker](#docker)
  - [Building the Docker Image](#building-the-docker-image)
  - [Running the Docker Container](#running-the-docker-container)
- [Folder Structure](#folder-structure)
- [Contributing](#contributing)
- [License](#license)

---

## **Features**

- **User-Friendly Interface**: Simple UI built with Streamlit to allow seamless SCD generation.
- **AI-Powered**: Utilizes OpenAI models to process and generate SCDs based on user prompts.
- **Real-time Updates**: Instant preview of generated SCDs.
- **Customizability**: Easily modifiable control and dataset parameters.
- **Dockerized**: Ready-to-deploy with a Docker setup.

---

## **Technologies**

- **Frontend**: Streamlit
- **Backend**: Python 3.12.7
- **OpenAI**: Integration for AI-powered text generation
- **Docker**: Containerization for easy deployment
- **dotenv**: Securely handle environment variables

---

## **Getting Started**

### **Prerequisites**

Before you can run the project, ensure you have the following installed:

- Python 3.12.x or later
- Docker (if running with containers)

### **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/scd-analysis-app.git
   cd scd-analysis-app
