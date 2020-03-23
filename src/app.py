from flask import Flask, request
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)


@app.route('/classification/predict', methods=['POST'])
def predict():
    app.logger.info(request.get_json())
    return request.get_json()


if __name__ == "__main__":
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.run(host='0.0.0.0', port=5000)
