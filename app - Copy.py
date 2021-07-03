# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 15:20:34 2021

@author: Thrinesh Duvvuru
"""

from flask import Flask,request,render_template
import jsonify
import requests
import pickle
import sklearn
import numpy as np

app=Flask(__name__)

model = pickle.load(open('car_price.pkl', 'rb'))

@app.route('/',methods=["GET"])

def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])

def predict():
    if request.method=='POST':
        Year = int(request.form['Year'])
        car_age=2020-Year
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Owner=int(request.form['Owner'])
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
        elif(Fuel_Type_Petrol=='Diesel'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        else:
             Fuel_Type_Petrol=0
             Fuel_Type_Diesel=0
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0	
        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0
        prediction=model.predict([[Present_Price,Kms_Driven,Owner,car_age,Fuel_Type_Diesel,Fuel_Type_Petrol,
                                   Seller_Type_Individual,Transmission_Mannual]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="please check the data again")
        else:
            return render_template('index.html',prediction_text="approximate selling price is Rs {} Lakhs".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)    
        