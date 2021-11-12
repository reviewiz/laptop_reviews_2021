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
    del data
    return render(request, 'index.html',context)
def search(request):
    data = pd.read_csv('https://raw.githubusercontent.com/DibyaSadhukhan/Amazon_Review_Analysis/main/Data/Products.csv')
    data=data.drop(data.columns[0], axis=1)
    Brand_list=list(data['Brand'].value_counts().index)
    screen_list=list(data['Screen_size'].value_counts().index)
    RAM_list=list(data['RAM'].value_counts().index)
    Processor_list=list(data['Processor'].value_counts().index)
    HD_list=list(data['Hard_drive'].value_counts().index)
    context={'Brand':Brand_list,'RAM':RAM_list,'Processor':Processor_list,'screen':screen_list,'Hard_disk':HD_list,'query':'yo'}
    #return render(request, 'index.html',context)
    return render(request, 'Search.html',context) 
def product(request):
    data = pd.read_csv('https://raw.githubusercontent.com/DibyaSadhukhan/Amazon_Review_Analysis/main/Data/Master_df.csv')
    code=request.GET['code']
    data=data.drop(data.columns[0], axis=1)
    det=data.loc[data['Product_code']==code]
    del data
    det.rename(columns = {'Reveiw Link':'Review_link','number_of_reveiws':'number_of_reviews'}, inplace = True)
    try:
        det['rev_rat_dist']=det['rev_rat_dist'].apply(lambda x: x.split(' '))
        det['rev_tone_dist']=det['rev_tone_dist'].apply(lambda x: x.split(' '))
        det.iat[0,-2]=[int(ele) for ele in det.iloc[0]['rev_rat_dist']]
        det.iat[0,-1]=[int(ele) for ele in det.iloc[0]['rev_tone_dist']]
    except:
        det['rev_tone_dist']=None
        det['rev_rat_dist']=None
    det=dict(det.iloc[0])
    #context={'Image':det['Images'].values[0],'Name':det['Product_name'].values[0],'Rating':det['Rating'].values[0],
    #'numrev':det['number_of_reveiws'].values[0],'Price':det['Price'].values[0],'avgrat':str(det['Avg_rev_rating'].values[0])[:4],
    #'Product_link':det['Link'].values[0]}
    context={'data':det}
    return render(request, 'product.html',context)