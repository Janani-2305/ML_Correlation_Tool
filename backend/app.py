from flask import Flask, request, jsonify
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  


def compute_correlations(df, target_column, method): 

    if target_column not in df.columns:
        return {"error": "Target column not found in the dataset."}

    # Convert target column to numeric if necessary
    string_columns = df.select_dtypes(include=['object']).columns

    # Initialize LabelEncoder
    label_encoder = LabelEncoder()

    # Apply LabelEncoder to each string column
    for col in string_columns:
        df[col] = label_encoder.fit_transform(df[col])

    # Drop rows with NaN values in target column
    df = df.dropna(subset=[target_column])

    # Compute correlations
    correlations = df.corr(method=method)[target_column]

    # Create a dictionary with correlation results
    result = {}
    for column, corr_value in correlations.items():
        if column == target_column:
            continue
        color = 'green' if abs(corr_value) >= 0.5 else 'red'
        result[column] = {"correlation": corr_value, "color": color}

    return result

@app.route('/upload', methods=['POST'])
def upload_dataset():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}) # 0 string empty value
    
    target_column = request.form['target_column']
    method = request.form['method']
    
    # Read the file into a Pandas DataFrame
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.filename.endswith('.xlsx'):
            df = pd.read_excel(file)
        else:
            return jsonify({"error": "Unsupported file type"})
    except Exception as e:
        return jsonify({"error": str(e)})
    
    # Compute correlations
    print("Entering correlation")
    correlation_result = compute_correlations(df, target_column, method)
    print(correlation_result)
    
    return jsonify(correlation_result)

if __name__ == '__main__':
    app.run(debug=True)
