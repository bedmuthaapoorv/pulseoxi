import pandas as pd #for reading csv
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt 
import numpy as np
from sklearn.metrics import silhouette_score
from sklearn.neighbors import KNeighborsClassifier
from math import sqrt
import dash
import random
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_core_components as dcc
import base64
import os
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
ALLOWED_TYPES = (
    "text", "number", "password", "email", "search",
    "tel", "url", "range", "hidden",
)
app = dash.Dash(__name__)
dataframe=pd.read_csv('train-data.csv')

dataframe=dataframe.drop('Unnamed: 0',axis=1) #we dropped 'Unnamed: 0' column because it was irrelavent

#print(dataframe.isnull().sum()) #here we checked how many columns had null values

#let's drop rows with null values

#print(dataframe.shape)

dataframe=dataframe[dataframe['Mileage'].notna()]
dataframe=dataframe[dataframe['Engine'].notna()]
dataframe=dataframe[dataframe['Power'].notna()]
dataframe=dataframe[dataframe['Seats'].notna()]

#we'll drop new peices column since it has a lot of null values
dataframe=dataframe.drop('New_Price',axis=1) #we dropped 'Unnamed: 0' column because it was irrelavent

#the name column can be mined down into more important information
dataframe=dataframe.reset_index(drop=True)
for i in range(dataframe.shape[0]):
    dataframe.at[i, 'Company'] = dataframe['Name'][i].split()[0]
    dataframe.at[i, 'Mileage(km/kg)'] = dataframe['Mileage'][i].split()[0]
    dataframe.at[i, 'Engine(CC)'] = dataframe['Engine'][i].split()[0]
    dataframe.at[i, 'Power(bhp)'] = dataframe['Power'][i].split()[0]

#print(dataframe.head())

dataframe['Mileage(km/kg)'] = dataframe['Mileage(km/kg)'].astype(float)
#dataframe['Power(bhp)'] = dataframe['Power(bhp)'].astype(float)
dataframe['Engine(CC)'] = dataframe['Engine(CC)'].astype(float)

x = 'n'
count = 0
position = []
dataframe=dataframe.reset_index(drop=True)
for i in range(dataframe.shape[0]):
    if dataframe['Power(bhp)'][i]=='null':
        x = 'Y'
        count = count + 1
        position.append(i)
#        dataframe = dataframe.drop(dataframe.index[position])
 #       dataframe = dataframe.reset_index(drop=True) 
dataframe = dataframe.drop(dataframe.index[position])
dataframe = dataframe.reset_index(drop=True) 

dataframe['Power(bhp)'] = dataframe['Power(bhp)'].astype(float)

#dataframe.drop(["Name"],axis=1,inplace=True)
dataframe.drop(["Mileage"],axis=1,inplace=True)
dataframe.drop(["Engine"],axis=1,inplace=True)
dataframe.drop(["Power"],axis=1,inplace=True)

Location = dataframe[['Location']]
Location = pd.get_dummies(Location,drop_first=True)
#print(Location.head())
Fuel_t = dataframe[['Fuel_Type']]
Fuel_t = pd.get_dummies(Fuel_t,drop_first=True)
#print(Fuel_t.head())

Transmission = dataframe[['Transmission']]
Transmission = pd.get_dummies(Transmission,drop_first=True)



dataframe.replace({"First":1,"Second":2,"Third": 3,"Fourth & Above":4},inplace=True)

dataframe.drop(["Company"],axis=1,inplace=True)



final_train= pd.concat([dataframe,Location,Fuel_t,Transmission],axis=1)

final_train.drop(["Location","Fuel_Type","Transmission"],axis=1,inplace=True)
#print(final_train.shape)

test_data=pd.read_csv('test-data.csv')

test_data = test_data.iloc[:,1:]

#print("Shape of test data Before dropping any Row: ",dataframe.shape)
test_data = test_data[test_data['Mileage'].notna()]
#print("Shape of test data After dropping Rows with NULL values in Mileage: ",test_data.shape)
test_data = test_data[test_data['Engine'].notna()]
#print("Shape of test data After dropping Rows with NULL values in Engine : ",test_data.shape)
test_data = test_data[test_data['Power'].notna()]
#print("Shape of test data After dropping Rows with NULL values in Power  : ",test_data.shape)
test_data = test_data[test_data['Seats'].notna()]
#print("Shape of test data After dropping Rows with NULL values in Seats  : ",test_data.shape)
#print('Droping null done')

test_data = test_data.reset_index(drop=True)
#print('Index reset done')
for i in range(test_data.shape[0]):
    test_data.at[i, 'Mileage(km/kg)'] = test_data['Mileage'][i].split()[0]
    test_data.at[i, 'Engine(CC)'] = test_data['Engine'][i].split()[0]
    test_data.at[i, 'Power(bhp)'] = test_data['Power'][i].split()[0]
#print('Split Done') 

test_data['Mileage(km/kg)'] = test_data['Mileage(km/kg)'].astype(float)
test_data['Engine(CC)'] = test_data['Engine(CC)'].astype(float)

#print('casting 1 Done') 

position = []
for i in range(test_data.shape[0]):
    if test_data['Power(bhp)'][i]=='null':
        position.append(i)
        
test_data = test_data.drop(test_data.index[position])
test_data = test_data.reset_index(drop=True) 
test_data['Power(bhp)'] = test_data['Power(bhp)'].astype(float)
#print('casting 2 Done') 

for i in range(test_data.shape[0]):
    if pd.isnull(test_data.loc[i,'New_Price']) == False:
        test_data.at[i,'New_car_Price'] = test_data['New_Price'][i].split()[0]

test_data['New_car_Price'] = test_data['New_car_Price'].astype(float)

test_data.drop(["Name"],axis=1,inplace=True)
test_data.drop(["Mileage"],axis=1,inplace=True)
test_data.drop(["Engine"],axis=1,inplace=True)
test_data.drop(["Power"],axis=1,inplace=True)
test_data.drop(["New_Price"],axis=1,inplace=True)

var = 'Location'
Location = test_data[[var]]
Location = pd.get_dummies(Location,drop_first=True)
Location.head()
var = 'Fuel_Type'
Fuel_t = test_data[[var]]
Fuel_t = pd.get_dummies(Fuel_t,drop_first=True)
Fuel_t.head()

var = 'Transmission'
Transmission = test_data[[var]]
Transmission = pd.get_dummies(Transmission,drop_first=True)
Transmission.head()

test_data.replace({"First":1,"Second":2,"Third": 3,"Fourth & Above":4},inplace=True)
test_data.head()

final_test= pd.concat([test_data,Location,Fuel_t,Transmission],axis=1)
final_test.head()

final_test.drop(["Location","Fuel_Type","Transmission","New_car_Price"],axis=1,inplace=True)
final_test.head()

#print("Final Test Size: ",final_test.shape)
#print(final_test.head())
#x=dataframe.iloc[,[]]
X = final_train.loc[:,['Year', 'Kilometers_Driven', 'Owner_Type', 'Seats',
       'Mileage(km/kg)', 'Engine(CC)', 'Power(bhp)', 
       'Location_Bangalore', 'Location_Chennai', 'Location_Coimbatore',
       'Location_Delhi', 'Location_Hyderabad', 'Location_Jaipur',
       'Location_Kochi', 'Location_Kolkata', 'Location_Mumbai',
       'Location_Pune', 'Fuel_Type_Diesel', 'Fuel_Type_LPG',
       'Fuel_Type_Petrol', 'Transmission_Manual','Price']]
'''
g=[]
for i in range(X.shape[0]):
    h=[]
    for j in range(X.shape[1]):
        h.append(X[X.columns[j]][i])
    g.append(h)

wcss = []
for i in range(1,20):
 kmeans = KMeans(n_clusters=i,init='k-means++',max_iter=300,n_init=10,random_state=0)
 kmeans.fit(g)
 wcss.append(kmeans.inertia_)
 print("Cluster", i, "Inertia", kmeans.inertia_)
plt.plot(range(1,20),wcss)
plt.title('The Elbow Curve')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS') ##WCSS stands for total within-cluster sum of square
plt.savefig('./assets/elbow.png')
'''
kmeans = KMeans(n_clusters=5,init='k-means++',max_iter=300,n_init=10,random_state=0)
y_kmeans=kmeans.fit(X)
gg=kmeans.fit_predict(X)
print(y_kmeans.cluster_centers_)
#print(X.iloc[:,21],X.iloc[:,4])
plt.scatter(X.iloc[:,21],X.iloc[:,3],c=gg,cmap='rainbow')
#plt.scatter(y_kmeans.cluster_centers_[:,0],y_kmeans.cluster_centers_[:,1],marker='*',c='red')
#plt.show()
plt.savefig('./assets/plot.png', dpi=300, bbox_inches='tight') 
#plt.scatter(X.iloc[:,21],X.iloc[:,3],c=gg,cmap='rainbow')
index_closest=-1
def recommendation(km):
    diff = np.array(y_kmeans.cluster_centers_) - np.array(km)[0]  # NumPy broadcasting
    #print(diff)
    dist = np.sqrt(np.sum(diff**2, axis=-1))  # Euclidean distance
    print(dist)
    closest_centroid = np.array(y_kmeans.cluster_centers_)[np.argmin(dist),]
    '''print("closest centroid:\n",closest_centroid)'''

    for i in range(5):
        if(np.array(y_kmeans.cluster_centers_)[i]==closest_centroid).all():
            global index_closest
            index_closest=i
            break
#recommendation()
    cluster_map=pd.DataFrame()
    cluster_map['cluster'] = y_kmeans.labels_
    print("recommended ",(np.array(cluster_map[cluster_map.cluster == index_closest].head().index)))
    ii=random.random()*(len(np.array(cluster_map[cluster_map.cluster == index_closest].index))-1)
    ii=int(ii)
    #for i in range(len(np.array(cluster_map[cluster_map.cluster == index_closest].index))):
    return dataframe['Name'][ii]
#print(np.array(y_kmeans.cluster_centers_))
#print(abs(closest_centroid[-1]-np.array(X)[1,:][-1]))
#print(y_kmeans.inertia_)
Distances=100000000
index=[]
def KNN(test_data):
    global final_train,index,Distances,index
    final_train = final_train.loc[:,['Year', 'Kilometers_Driven', 'Owner_Type', 'Seats',
        'Mileage(km/kg)', 'Engine(CC)', 'Power(bhp)', 
        'Location_Bangalore', 'Location_Chennai', 'Location_Coimbatore',
        'Location_Delhi', 'Location_Hyderabad', 'Location_Jaipur',
        'Location_Kochi', 'Location_Kolkata', 'Location_Mumbai',
        'Location_Pune', 'Fuel_Type_Diesel', 'Fuel_Type_LPG',
        'Fuel_Type_Petrol', 'Transmission_Manual','Price']]
    f_t=np.array(final_train)
    print("Yayy",f_t,test_data)
    for i in range(5000):
        dd=0
        for j in range(21):
            dd=dd+sqrt(abs(f_t[i][j]**2-test_data[j]**2))
            #print(dd)
        if(dd<Distances):
            Distances=dd
            index.append(f_t[i][-1])
    print(index[0])
    return sum(index) / len(index)
'''print('closest_neighbour',index[-1],test_data[-1])'''
#fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])
#encoded_image = base64.b64encode(open('/home/dell/ddd/minipro/plot.png', 'rb').read())
app.layout = html.Div(style={'position':'absolute','top':'7vh','left':'45vw'},children=[
    dcc.Input(
            id="text1",
            type="text",
            placeholder="Year",
            style={'borderStyle':'solid','height':'5vh','textAlign':'center'}
        ),
        html.P(''),
        dcc.Input(
            id="text2",
            type="text",
            placeholder="Kilometers Driven",
            style={'borderStyle':'solid','height':'5vh','textAlign':'center'}
        ),
        html.P(''),
        dcc.Input(
            id="text3",
            type="text",
            placeholder="Times Resold",
            style={'borderStyle':'solid','height':'5vh','textAlign':'center'}
        ),
        html.P(''),
                dcc.Input(
            id="text4",
            type="text",
            placeholder="Seats",
            style={'borderStyle':'solid','height':'5vh','textAlign':'center'}
        ),
        html.P(''),
        dcc.Input(
            id="text5",
            type="text",
            placeholder="Mileage(km/kg)",
            style={'borderStyle':'solid','height':'5vh','textAlign':'center'}
        ),
        html.P(''),
        dcc.Input(
            id="text6",
            type="text",
            placeholder="Engine(CC)",
            style={'borderStyle':'solid','height':'5vh','textAlign':'center'}
        ),
        html.P(''),
        dcc.Input(
            id="text7",
            type="text",
            placeholder="Power(bhp)",
            style={'borderStyle':'solid','height':'5vh','textAlign':'center'}
        ),
        html.P(''),
        dcc.Input(
            id="text8",
            type="text",
            placeholder="City",
            style={'borderStyle':'solid','height':'5vh','textAlign':'center'}
        ),
        html.P(''),
        dcc.Input(
            id="text9",
            type="text",
            placeholder="Fuel type",
            style={'borderStyle':'solid','height':'5vh','textAlign':'center'}
        ),
        html.P(''),
        dcc.Input(
            id="text10",
            type="text",
            placeholder="Transmission",
            style={'borderStyle':'solid','height':'5vh','textAlign':'center'}
        ),
        html.P('',id='output'),
        html.P(''),
        html.P('',style={'backgroundImage':'url("/assets/elbow.png")','height':'500px','width':'500px','backgroundSize':'cover','position':'relative','left':'-20vw'}),
        #html.P('elbow method results'),
        html.P('',style={'backgroundImage':'url("/assets/plot.png")','height':'500px','width':'500px','backgroundSize':'cover','position':'relative','left':'-20vw'})
        ,html.P('mileage vs prices'),
        html.P('',style={'backgroundImage':'url("/assets/engine.png")','height':'500px','width':'500px','backgroundSize':'cover','position':'relative','left':'-20vw'}),
        html.P('engine vs prices'),
])
@app.callback(
    Output("output", "children"),
    Input("text1", "value"),
    Input("text2", "value"),
    Input("text3", "value"),
    Input("text4", "value"),
    Input("text5", "value"),
    Input("text6", "value"),
    Input("text7", "value"),
    Input("text8", "value"),
    Input("text9", "value"),
    Input("text10", "value"),
    
)
def update_output(text1, text2,text3,text4,text5,text6,text7,text8,text9,text10):
    if text1 is None:
        raise dash.exceptions.PreventUpdate
    if text2 is None:
        raise dash.exceptions.PreventUpdate
    if text3 is None:
        raise dash.exceptions.PreventUpdate    
    if text4 is None:
        raise dash.exceptions.PreventUpdate
    if text5 is None:
        raise dash.exceptions.PreventUpdate
    if text6 is None:
        raise dash.exceptions.PreventUpdate
    if text7 is None:
        raise dash.exceptions.PreventUpdate
    if text8 is None:
        raise dash.exceptions.PreventUpdate
    if text9 is None:
        raise dash.exceptions.PreventUpdate
    if text10 is None:
        raise dash.exceptions.PreventUpdate
    else:
        t8={'Banglore':1,'Chennai': 2,'Coimbatore': 3,
            'Delhi': 4,'Hyderabad': 5,'Jaipur': 6,'Kochi': 7,
            'Kolkata': 8,'Mumbai': 9,'Pune': 10}
        t9={'Diesel': 0,'LPG': 1,'Petrol': 2}
        t10={'Automatic': 0,'Manual': 1}
        if text8 not in t8:
            return "invalid entry at city"
        if text9 not in t9:
            return "invalid entry at Fuel"
        if text10 not in t10:
            return "invalid entry at transmission"
        try:
            text1=float(text1)
            text2=float(text2)
            text3=float(text3)
            text4=float(text4)
            text5=float(text5)
            text6=float(text6)
            text7=float(text7)
        except:
            return "invalid entry,please check the values entered"
        text8=t8[text8]
        text9=t9[text9]
        text10=t10[text10]
        text3=text3+1
        a1=[text1,text2,text3,text4,text5,text7]
        for i in range(text8):
            a1.append(0)
        a1.append(1)
        
        for j in range(text8+1,11):
            a1.append(0)
        for k in range(text9):
            a1.append(0)
        a1.append(1)
        for k in range(text9+1,3):
            a1.append(0)
        a1.append(text10)
        gg=KNN(a1)
        km=recommendation(a1)
        return ("Predicted Price: ",gg," Recommended Car:",km)
        
    


if __name__ == '__main__':
    app.run_server(debug=True)