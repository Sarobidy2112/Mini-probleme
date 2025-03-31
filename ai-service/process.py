from flask import Flask, jsonify
import pandas as pd
from sklearn.datasets import load_iris

app = Flask(__name__)

@app.route('/stats', methods=['GET'])
def get_stats():
    data = load_iris()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    stats = df.describe().to_dict()
    return jsonify(stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
