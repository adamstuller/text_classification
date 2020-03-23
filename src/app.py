from flask import Flask, request
app = Flask(__name__)

@app.route('/classification/predict', methods=['POST'])
def predict():
    app.logger.info(request.get_json())
    return {
        "tag": "hoco"
    }

if __name__ == "__main__":
    app.config.from_object('config.DevelopmentConfig') 
    app.run(host='0.0.0.0', port=5000)
