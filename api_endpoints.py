from flask import Flask, request, jsonify
import data_procession
from datetime import datetime

app = Flask(__name__)

@app.route('/api/stats/user/online_time', methods=['GET'])
def get_online_time():
    data_procession.fetch_and_update_data()
    userId = request.args.get('userId')
    previous_state = {}
    user_data = data_procession.update_user_data(userId, previous_state)
    
    if user_data is None:
        return jsonify({'error': 'Invalid userId'}), 404

    online_time = data_procession.calculate_online_time(user_data)
    return jsonify({'userId': userId, 'onlineTime': online_time})

@app.route('/api/stats/user/average', methods=['GET'])
def get_average_times():
    data_procession.fetch_and_update_data()
    userId = request.args.get('userId')
    user_data = data_procession.update_user_data(userId)
    
    if user_data is None:
        return jsonify({'error': 'Invalid userId'}), 404

    weekly_avg, daily_avg = data_procession.calculate_average_times(user_data)
    return jsonify({'userId': userId, 'weeklyAverage': weekly_avg, 'dailyAverage': daily_avg})

@app.route('/api/user/forget', methods=['POST'])
def forget_user():
    data_procession.fetch_and_update_data()
    userId = request.args.get('userId')
    data_procession.delete_user_data(userId)
    return jsonify({'userId': userId})

if __name__ == "__main__":
    app.run(debug=True)