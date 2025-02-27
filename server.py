from flask import Flask, request, jsonify, render_template_string
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dynamoDBHelper import DynamoDBHelper

app = Flask(__name__)

# Configuration de DynamoDB
table = DynamoDBHelper.table

@app.route('/', methods=['GET'])
def home():
    return "Bienvenue sur notre site ! Veuillez vous connecter via /login."

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"message": "Email and password are required"}), 400

        try:
            response = table.get_item(
                Key={
                    'email': email
                }
            )
            item = response.get('Item')

            if item and item['password'] == password:
                return jsonify({"message": "Login successful"}), 200
            else:
                return jsonify({"message": "Invalid email or password"}), 401

        except NoCredentialsError:
            return jsonify({"message": "AWS credentials not available"}), 500
        except PartialCredentialsError:
            return jsonify({"message": "Incomplete AWS credentials"}), 500
        except Exception as e:
            return jsonify({"message": str(e)}), 500
    else:
        return render_template_string('''
            <form method="post">
                Email: <input type="text" name="email"><br>
                Password: <input type="password" name="password"><br>
                <input type="submit" value="Login">
            </form>
        ''')

if __name__ == '__main__':
    app.run(debug=True)
