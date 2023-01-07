import streamlit as st
import pandas as pd
import numpy as np

# Page Setting
st.set_page_config(
    page_title="Car Cross Sell",
    page_icon="hhttps://previews.123rf.com/images/zoaarts/zoaarts1812/zoaarts181200016/114559818-vector-illustration-of-artificial-intelligence-landing-page-website-template-for-ai-machine-deep-lea.jpg",
    menu_items={
        "Get help": "mailto:hayrullahkaraman@gmail.com",
        "About": "For More Information\n" + "https://github.com/HayrullahKaraman"
    }
)

#Info
st.title("Car Cross Selling")
st.header("About Project")
st.markdown("AI Insurance Commany client is an Insurance company that has provided Health Insurance to its customers. Now Our company wants to enter the car insurance market, so it asks the IT department to develop a model, this model wants to develop a model that can predict that existing customers can buy car insurance")
st.image("https://5.imimg.com/data5/FU/IY/CZ/SELLER-63009613/vehicle-insurance-jpeg-500x500.jpeg",)

#Future İnfo
st.header("About Dictionary")
st.markdown("**Gender** : Gender of the customer")
st.markdown("**Age** : Age of the customer")
st.markdown("**Driving License** : 0 : Customer does not have Driving License, 1 : Customer already has Driving License")
st.markdown("**Region Code** : 	Unique code for the region of the customer")
st.markdown("**Previously Insured** : 	Unique code for the region of the customer1 : Customer already has Vehicle Insurance, 0 : Customer doesn't have Vehicle Insurance")
st.markdown("**Vehicle Age** : 	Age of the Vehicle")
st.markdown("**Vehicle Damage** : 1 : Customer got his/her vehicle damaged in the past. 0 : Customer didn't get his/her vehicle damaged in the past")
st.markdown("**Annual Premium**: The amount customer needs to pay as premium in the year")
st.markdown("**Policy Sales Channel** :	Anonymized Code for the channel of outreaching to the customer ie. Different Agents, Over Mail, Over Phone, In Person, etc")
st.markdown("**Annual Premium** : The amount customer needs to pay as premium in the year")
st.markdown("**Vintage**: Number of Days, Customer has been associated with the company")
st.markdown("**Response**: 1 : Customer is interested, 0 : Customer is not interested")


#Dataset
st.header("Simple Dataset")
df=pd.read_csv("train.csv")
st.table(df.sample(5,random_state=42))

#Sidebar future get 
st.sidebar.markdown("**Choose** the features below to see the result!")
dl=st.sidebar.radio("Do you have Driving Licance ?",('Yes','No'))
pi=st.sidebar.radio("Do you have past insurance?",('Yes','No'))
vin=st.sidebar.number_input("How many days have you been working with us?",max_value=299,min_value=10,format="%d",help="Minimum value 10, maximum value 299")
vechile_age=st.sidebar.selectbox("How many years your car",('Under 1 year old', 'Between 1 and 2 years old', 'Over 2 years old'))
annuel_prem= st.sidebar.number_input("How much is the last premium you paid?")
gendersel=st.sidebar.radio("What is your Gender?",('Female','Male'))
demage=st.sidebar.radio("have you had an accident in the past?",('Yes','No'))
age=st.sidebar.slider("Customer Age ", min_value=20, max_value=65)
channelsel=st.sidebar.selectbox("What communication channel did you reach us through? ",('Advise', 'Social Media', 'Customer agent'))
regionsel=st.sidebar.selectbox("what region are you in? ",('Region A', 'Region B', 'Region C'))


##Model İmport







def yes_no(val):
    if val == 'Yes':
     return 1
    else:
      return 0

def gender_(gender):
    if gender == 'Female':
     return 0
    else:
      return 1


def vehicleAge(vechile):
    if vechile == 'Over 2 years old':
        return  3
    elif vechile == 'Between 1 and 2 years old':
        return 2
    else:
        return  1

def channel_(channel):
    if channel == 'Advise':
     return 1
    elif channel=='Social Media':
        return 1
    else:
      return 0

def region_(region):
    if region == 'Region B':
     return 1
    elif channel=='Region C':
        return 1
    else:
      return 0


def age_(age):
    if age > 65:
        return 1
    else:
        return 0


drivinglicance= yes_no(dl)
previousinsuance=yes_no(pi)
damegevechile=yes_no(demage)
vechileage= vehicleAge(vechile_age)
channel=channel_(channelsel)
region=region_(regionsel)
gender=gender_(gendersel)
Age=age_(age)

input_df = pd.DataFrame({
    'driving_license' : [drivinglicance],
    'previously_insured' : [previousinsuance],
    'vintage':[vin],
    'Vehicle_Age':[vechileage],
    'Annual_Premium_Clean':[annuel_prem],
    'gender_Male':[gender],
    'vehicle_damage_Yes':[damegevechile],
    'Age_Group_OldAge':[Age],
    'Age_Group_YoungAge':[Age],
    'Policy_Sales_Channel_Categorical_Channel_B':[channel],
    'Policy_Sales_Channel_Categorical_Channel_C':[channel],
    'Region_Code_Categorical_Region_B':[region],
    'Region_Code_Categorical_Region_C':[region]
})

from joblib import load



model=load("xgbfinal.pkl")
pred=model.predict(input_df.values)

# Sonuç Ekranı
if st.sidebar.button("Submit"):

    # Info mesajı oluşturma
    st.info("You can find the result below.")

    # Sorgulama zamanına ilişkin bilgileri elde etme
    
    results_df = pd.DataFrame({
    'driving_license' : [drivinglicance],
    'previously_insured' : [previousinsuance],
    'vintage':[vin],
    'Vehicle_Age':[vechileage],
    'Annual_Premium_Clean':[annuel_prem],
    'gender_Male':[gender],
    'vehicle_damage_Yes':[damegevechile],
    'Age_Group_OldAge':[Age],
    'Age_Group_YoungAge':[Age],
    'Policy_Sales_Channel_Categorical_Channel_B':[channel],
    'Policy_Sales_Channel_Categorical_Channel_C':[channel],
    'Region_Code_Categorical_Region_B':[region],
    'Region_Code_Categorical_Region_C':[region],
    'Prediction':[pred]
    })

    results_df["Prediction"] = results_df["Prediction"].apply(lambda x: str(x).replace("0","Not_insurance"))
    results_df["Prediction"] = results_df["Prediction"].apply(lambda x: str(x).replace("1","insurance"))
    st.table(results_df)
else:
    st.markdown("Please click the *Submit Button*!")
