from flask import Blueprint, request, jsonify
from src.services.implementation.SelectorService import SelectorService
import logging

selectorController = Blueprint('selectorController',__name__,url_prefix="/selector")
selectorService = SelectorService()


@selectorController.route("/")
def get_countries():
    service = selectorService.get
    return  jsonify({
        "message": "Selector Service retrieved successfully",
        "data" : service
    })

@selectorController.route("get-tocks")
def get_stocks():
    data=[]
    stock_value = request.args.get('stock_value')
    stock_type = request.args.get('stock_type')
    
    data["stock_value"] = stock_value
    data["stock_type"] = stock_type
    # redis & cache impleentation

    # use request to pull 
    # select_data=selectorService.get_stocks(data)

    return jsonify({
        "message": "Selector data retrieved successfully",
        "data": select_data
    })

@selectorController.route('get-value')
def get_value_stocks():
    pass

@selectorController.route("hold-request", methods=["POST"])
def hold_request():
    pass

@selectorController.route("sell", methods=["POST"])
def sell_request():
    pass