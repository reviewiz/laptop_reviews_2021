from django.shortcuts import render
import pandas as pd
# Create your views here.
def get_advanced_df(data,brand,ub,lb,sort):
    table = pd.DataFrame(columns = data.columns)
    if ub==-1:
        table=data.loc[data['Price']>100000]
    elif lb>0 and ub>0:
        table=data.loc[(data['Price']>lb)&(data['Price']<=ub)]
    else:
        table=data
    
    if brand!='Any':
        table=table.loc[table['Brand']==brand]
    if sort=='Price_A':
        table=table.nsmallest(len(table),['Price'])
    elif sort=='Price_D':
        table=table.nlargest(len(table),['Price'])
    else:
        table=table.nlargest(len(table),[sort])
    return table
def index(request):
    all_data=[]
    data = pd.read_csv('https://raw.githubusercontent.com/DibyaSadhukhan/Amazon_Review_Analysis/main/Data/Top_products.csv')
    data=data.drop(data.columns[0], axis=1)
    message="Top 5 most reveiwed products"
    for i in range(data.shape[0]):
        all_data.append(dict(data.iloc[i]))
    context={'data':all_data,'query':message}
    return render(request, 'index.html',context)
def search(request):
    data = pd.read_csv('https://raw.githubusercontent.com/DibyaSadhukhan/Amazon_Review_Analysis/main/Data/Products.csv')
    data=data.drop(data.columns[0], axis=1)
    drop_down=list(data['Brand'].value_counts().index)
    all_data=[]
    message=""
    try:
        lb=int(request.POST['Price_range'].split(',')[0])
        ub=int(request.POST['Price_range'].split(',')[1])
        brand=request.POST['Brand']
        sort=request.POST['sort']
        table=get_advanced_df(data,brand,ub,lb,sort)
        
        if brand=='Any' and sort=='number_of_reveiws' and lb==0 and ub==0:
            message="Top 5 most reveiwed laptops"
        
        if table.shape[0]!=0:
            if table.shape[0]==1:
                message="We found "+str(table.shape[0])+" Laptop"
            else:
                message="We found "+str(table.shape[0])+" Laptops"
        else:
            message="Believe me! I looked everywhere and all I found was this. :( "
    except:
        table=data.nlargest(5, ['number_of_reveiws'])
        message="Top 5 most reveiwed products"
    for i in range(table.shape[0]):
        all_data.append(dict(table.iloc[i]))
        
    context={'select':drop_down,'data':all_data,'query':message}
    #return render(request, 'index.html',context)
    return render(request, 'Search.html',context) 