# Project Name

A brief description of your Rasa and Flask project.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Remarks](#remarks)

## Installation

1. Clone this repository:

```bash
git clone <repository-url>
```
2. Install the required dependencies:
```cmd
pip install -r requirements.txt
```
## Usage

1. Update the `features.py` file:
   - Open the `features.py` file located in the project directory.
   - Find the placeholders for the OpenAI API key and MySQL database credentials.
   - Replace the placeholders with your actual API key and database credentials.

2. Start the Rasa servers:
   - Open a terminal and navigate to the `model_rasa_part2` folder.
   - Run the following command to start the Rasa server:

     ```bash
     rasa run
     ```

   - Open another terminal and navigate to the `model_rasa_part2` folder.
   - Run the following command to start the Rasa action server:

     ```bash
     rasa run actions
     ```

3. Start the Flask server:
   - Open a terminal and navigate to the `rasa` folder.
   - Run the following command to start the Flask server:

     ```bash
     flask run
     ```

4. Access the application:
   - Once the servers are running, you can access the application by navigating to `http://localhost:5000` in your web browser.

     Note: By default, the Flask server runs on port 5000. If you have modified the port configuration, please use the appropriate port number in the URL.

   - You should see the application interface and can interact with your Rasa and Flask project.

## Remarks
1. Use python 3.8 to setup the project
2. Make new enviournment before starting install dependencies

   Note: Make sure to follow the specific instructions provided in your project documentation for any additional steps or customization required for your application.

