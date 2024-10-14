
Installation

1. Create a virtual environment (optional but recommended):

python -m venv venv


2. Activate the virtual environment:

On Windows:

venv\Scripts\activate

On macOS and Linux:

source venv/bin/activate



3. Install the required packages:

pip install -r requirements.txt


4. Set up your OpenAI API key:

Create a .env file in the root directory and add your OpenAI API key:

OPENAI_API_KEY=your_openai_api_key_here




Running the Application

To run the application, use the following command:

streamlit run main.py

After starting the app, you can access it at http://localhost:8501 in your web browser.

Docker

Building the Docker Image

To build the Docker image for the application, run the following command in the root directory:

docker build -t scd_analysis_app .

Running the Docker Container

After building the image, run the container with the following command:

docker run -p 8501:8501 --env-file .env scd_analysis_app

You can then access the application at http://localhost:8501.

Folder Structure

scd_analysis_app/
│
├── .env                   # Environment variables
├── Dockerfile             # Docker configuration file
├── requirements.txt       # Python dependencies
├── main.py                # Entry point for the Streamlit application
├── src/                   # Source files
│   ├── __init__.py       
│   ├── output/            # Output generation files
│   │   ├── __init__.py
│   │   └── scd_generator.py
│   ├── model/             # AI model files
│   │   ├── __init__.py
│   │   └── ai_model.py
│   └── utils/             # Utility functions
│       ├── __init__.py
│       └── helper_functions.py
└── README.md              # Project documentation

Contributing

We welcome contributions! If you have suggestions or improvements, please fork the repository and submit a pull request.

License

This project is licensed under the MIT License. See the LICENSE file for more details.

Acknowledgments

OpenAI for providing the API for AI capabilities.

Streamlit for the easy-to-use framework to create web applications.


Feel free to replace placeholders like `your_username` and `your_openai_api_key_here` with your actual information.
