from django.shortcuts import render
import pandas as pd
# Create your views here.
def get_advanced_df(data,brand,ub,lb,sort,Processor,RAM,screen,Hard_disk):
    table = pd.DataFrame(columns = data.columns)
    if ub==-1:
        table=data.loc[data['Price']>100000]
    elif lb>0 and ub>0:
        table=data.loc[(data['Price']>lb)&(data['Price']<=ub)]
    else:
        table=data
    del data
    if brand!='Any':
        table=table.loc[table['Brand']==brand]
    if sort=='Price_A':
        table=table.nsmallest(len(table),['Price'])
    elif sort=='Price_D':
        table=table.nlargest(len(table),['Price'])
    else:
        table=table.nlargest(len(table),[sort])
    if len(RAM)>1:
      RAM.remove('all')
      RAM=map(int,RAM)
      table=table.loc[table['RAM'].isin(RAM)]
    if len(Processor)>1:
      Processor.remove('all')
      table=table.loc[table['Processor'].isin(Processor)]
    if len(screen)>1:
      screen.remove('all')
      table=table.loc[table['Screen_size'].isin(screen)]
    if len(Hard_disk)>1:
      Hard_disk.remove('all')
      table=table.loc[table['Hard_drive'].isin(Hard_disk)]
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
    #sending data to website
    all_data=[]
    data = pd.read_csv('https://raw.githubusercontent.com/DibyaSadhukhan/Amazon_Review_Analysis/main/Data/Advanced_search.csv')
    data=data.drop(data.columns[0], axis=1)
    data=data.rename(columns={'number of reveiws':'number_of_reveiws'})
    Brand_list=list(data['Brand'].value_counts().index)
    screen_list=list(data['Screen_size'].value_counts().index)
    RAM_list=list(data['RAM'].value_counts().index)
    Processor_list=list(data['Processor'].value_counts().index)
    HD_list=list(data['Hard_drive'].value_counts().index)
    #receiving data from website
    #get_advanced_df(data,"Any",39999,1,"number of reveiws",Processor,RAM,screen,Hard_disk)
    try:
        lb=int(request.POST['Price_range'].split(',')[0])
        ub=int(request.POST['Price_range'].split(',')[1])
        brand=request.POST['Brand']
        sort=request.POST['sort']
        Processor=dict(request.POST)['Processor']
        RAM=dict(request.POST)['RAM']
        screen=dict(request.POST)['screen']
        Hard_disk=dict(request.POST)['Hard_disk']
        table=get_advanced_df(data,brand,ub,lb,sort,Processor,RAM,screen,Hard_disk)
        del data
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
    context={'data':all_data,'Brand':Brand_list,'RAM':RAM_list,'Processor':Processor_list,'screen':screen_list,'Hard_disk':HD_list,'query':message}
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