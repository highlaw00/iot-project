from flask import Flask, request
from flask_restx import Resource, Api
import pymysql
from utils import serializer
from utils.database_utils import DatabaseConnector, DatabaseQueryExecutor
from utils.validator import Validator
from utils.message_maker import Message
import sys

app = Flask(__name__)
api = Api(app)

@api.route('/health')
class Health(Resource):
    def get(self):
        return Message.Success("Health is good.")

@api.route('/seats')
class Seats(Resource):
    # 좌석 정보 반환 API
    def get(self):
        conn = DatabaseConnector().connect()
        
        if not conn:
            return Message.FailureDbConnection()
        
        try:
            result = DatabaseQueryExecutor.select_seats(conn)
            # 트랜잭션 결과 비어있는 경우
            if not result:
                result = Message.Failure("Seats table is empty.")
        except:
            result = Message.Failure("Error occured while executing select transaction.")
            
        return result
    
    # 좌석 삽입 api
    def post(self):
        
        pass
    
    # 좌석 정보 변동
    def put(self):
        
        
        # 현재 좌석 변동 (입장, 퇴장)
        # 1. 주어진 데이터 무결성 검사
        # 2. 유저 존재 유무 검사
        # 3. 트랜잭션 실행
        pass

@api.route('/register')
class Register(Resource):
    # 유저 정보 반환 Rest API
    def get(self):
        conn = DatabaseConnector().connect()
        if not conn:
            return Message.FailureDbConnection()
        
        try:
            result = DatabaseQueryExecutor.select_users(conn)
            if not result:
                result = Message.Failure("User table is empty.")
        except:
            result = Message.Failure("Error occured while executing select transaction.")
        
        return result

    # 새로운 유저 추가 Rest API
    def post(self):
        # 유효성 검사 실시
        json_obj = request.get_json()
        
        # id 유효성 검사
        try:
            print(json_obj, file=sys.stdout)
            user_id = str(json_obj["user_id"])
            username = json_obj["username"]
            if not Validator.validate_user(user_id, username):
                return Message.Failure("Invalid user_id and username."), 400
        except:
            return Message.Failure("user_id and username is not included in JSON body."), 400
        
        # DB 연결
        conn = DatabaseConnector().connect()
        
        if not conn:
            return Message.FailureDbConnection()
        
        try:
            result = DatabaseQueryExecutor.insert_user(conn, user_id, username)
            if result:
                result = Message.Success("Insert user excuted successfully.")
        except:
            result = Message.Failure("Error occured while executing insert transaction.")
        
        return result
        
app.run(debug=True, port=8080)