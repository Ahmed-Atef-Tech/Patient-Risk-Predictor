# Patient-Risk-Predictor

# Overview

**PatientRiskPredictorGUI** is a Qt-based desktop application designed to evaluate and predict patient health risk levels using a machine learning model powered by **H2O.ai**. This user-friendly GUI allows medical practitioners and researchers to input patient data, such as age, gender, medical conditions, and more, to generate an automated risk assessment. The application integrates machine learning to provide insights that assist in healthcare decision-making.

## Features

- **Intuitive GUI**: Built using PyQt6, featuring easy navigation and a clean, modern look.
- **H2O Model Integration**: Uses an H2O machine learning model to predict risk levels based on patient inputs.
- **Interactive Widgets**: Provides date selection via calendars, dropdown lists for gender, blood type, medical condition, and more.
- **Loading Dialog**: Displays a loading dialog to show progress during data processing and prediction.
- **Customizable Hospital List**: Allows users to load and update hospital information from external files.
- **Risk Prediction**: Offers clear visual indicators of patient risk (low, moderate, or high) with appropriate color-coding.

## Prerequisites

- **Python 3.12+**
- **H2O.ai** (version compatible with the included model)
- **PyQt6**
- **Pandas**

Ensure all dependencies are installed before running the application.

## Installation

1. Clone this repository:
   
   ```bash
   git clone https://github.com/Ahmed-Atef-Tech/Patient-Risk-Predictor.git
   ```

2. Install the necessary Python packages:
   
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure **H2O.ai** is properly initialized:
   
   - Follow the instructions on [H2O.ai](https://h2o-release.s3.amazonaws.com/h2o/latest_stable.html) to install the H2O package and initiate an H2O server instance.

## Usage

1. **Run the Application**
   
   ```bash
   python Main.py
   ```
![image](https://github.com/user-attachments/assets/4caf88ea-283d-40f0-8a18-e0e57266a15d)

2. **Input Patient Data**:
   
   - Enter information such as name, age, gender, medical condition, and more.
   - Select dates using the calendar widget and fill in other patient details.

3. **Risk Prediction**:
   
   - Click on the "Predict" button to obtain the risk assessment.
   - The result will be displayed, showing the predicted risk category along with a danger level indicated by colors (green for low, yellow for moderate, red for high).

## How It Works

- The application loads a pre-trained **Gradient Boosting Model (GBM)** from **H2O.ai**.
- Patient input data is collected from the GUI and converted into an H2O frame.
- The loaded model processes the data to predict the patient's health risk level.
- Results are presented in a clear and intuitive format on the GUI, with the risk level highlighted for better understanding.

## Customizing Hospital Levels

- You can update the list of hospitals by clicking on the **"Update Hospitals"** button.
- This allows you to load a new list from a text file, making the hospital information adaptable to your context.

## Known Issues

- **Core Detection Issue**: Occasionally, H2O may not detect all available CPU cores properly. Refer to the JVM log files for further debugging.
- **Model Not Found**: Ensure the H2O server is running and the model ID matches the one in the script. Otherwise, a model loading error will occur.

## Future Improvements

- Add more detailed error handling and validation for user inputs.
- Enhance model prediction accuracy by allowing custom model training within the application.
- Expand support for multiple machine learning models (e.g., Random Forest, Deep Learning).

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request for any features or bug fixes.

## Contact

- **Developer**: Ahmed Atef
- **Email** : [ahmed.atef.tech@gmail.com](mailto:your-email@example.com)

Feel free to reach out for any questions or support regarding this project.

GitHub Repository: [Patient-Risk-Predictor](https://github.com/Ahmed-Atef-Tech/Patient-Risk-Predictor.git)


