from flask import Blueprint
from app.controllers import predict,training

router = Blueprint("router",__name__)

@router.route('/')
def home():
    return 'Welcome to the Address Validator!'

@router.route('/classify', methods = ['POST'])
def model_prediction():
    return  predict.classify()

@router.route('/train', methods = ['POST'])
def model_training():
    return  training.train_model()