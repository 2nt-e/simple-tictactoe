import flask
import asyncio



data = {'data': 'MYDATYA'}
app = flask.Flask(__name__)

@app.route('/pushside', methods=['POST'])
def update_data():
    global data
    data = flask.request.json
    print(data)
    return {'status': 'success'}, 200            

@app.route('/getside', methods=['GET'])
def execute():
    global data
    return data, 200


if __name__ == '__main__':
    app.run(debug=True)