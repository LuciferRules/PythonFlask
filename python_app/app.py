from flask import Flask, render_template, jsonify
import subprocess
import logging

# Configure logging to also write to a file
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file named app.log
        logging.StreamHandler()  # Also log to console
    ]
)

app = Flask(__name__)

def get_hive_data():
    try:
        beeline_command = [
            'beeline',
            '-u', 'jdbc:hive2://',
            '-e', 'USE hive_database; SELECT * FROM managed_table'
        ]
        result = subprocess.run(beeline_command, capture_output=True, text=True)

        if result.returncode != 0:
            logging.error(f"Error executing Beeline: {result.stderr}")
            return []

        # Log the raw output from Beeline
        logging.debug(f"Raw Beeline output:\n{result.stdout}")

        lines = result.stdout.strip().split('\n')


        # Clean lines by removing unwanted characters (like '|' and '+')
        cleaned_lines = [line.strip().replace('|', '').strip() for line in lines if line and not line.startswith('+')]

        # Log cleaned lines for debugging
        logging.debug(f"Cleaned lines: {cleaned_lines}")

        # # TODO: For test data only
        # cleaned_lines=['managed_table.id   managed_table.name   managed_table.salary', '1                  Ben                  10000.0', '2                  Sally                20000.0', '3                  Marcus               30333.0', '4                  Cindy                444.0', '5                  Donky                555.0', '6                  Elly                 666.0', '7                  Fork                 99.0', '8                  Google               999.0', '9                  Hadoop               9999.0', '10                 MVP                  99.0', '11                 SWoRD                999.0', '12                 WiZZard              9999.0', '13                 NEW1                 11.0', '14                 NEW2                 222.0', '15                 NEW3                 3333.0', '16                 onesix               11.0', '17                 oneseven             222.0', '18                 oneeight             3333.0', '19                 onenine              19.0', '20                 twozero              20.0', '21                 twoone               21.0']

        # Extract columns from the header line
        columns = [col.split('.')[-1] for col in cleaned_lines[0].split()]  # Keep only the last part for column names
        data = []

        # Extract data from the remaining lines
        for line in cleaned_lines[1:]:  # Start from 1 to skip header
            row_data = line.split()
            if len(row_data) == len(columns):  # Ensure the row has the right number of columns
                data.append(dict(zip(columns, row_data)))  # Use the cleaned column names here

        # Log the final data structure before returning
        logging.debug(f"Data returned: {data}")

        return data
    except Exception as e:
        logging.error(f"Error fetching data from Hive: {e}")
        return []


@app.route('/data')
def data():
    # Fetch data from Hive and return as JSON
    data = get_hive_data()
    return jsonify(data)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

