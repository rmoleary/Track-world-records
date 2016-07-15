
# coding: utf-8

# In[1]:

get_ipython().magic(u'pylab inline')


# In[2]:

import pandas as pd


# In[232]:

#Original Data downloaded from: http://web.archive.org/web/20110629134819/http://www.iaaf.org/mm/document/competitions/competition/05/15/63/20090706014834_httppostedfile_p345-688_11303.pdf


# In[233]:

#2015 data from here:http://iaaf-ebooks.s3.amazonaws.com/2015/Beijing-2015-Statistics-Handbook/index.htm


# In[234]:

dn = '2015worldrecords/'
fns = ['100m.txt','200m.txt','400m.txt','800m.txt','1000m.txt','1500m.txt','mile.txt',
            '2000m.txt','3000m.txt','5000m.txt','10km.txt','20km.txt','halfmarathon.txt','25km.txt','marathon.txt',
      '100mf.txt','200mf.txt','400mf.txt','800mf.txt','1000mf.txt','1500mf.txt','milef.txt',
            '2000mf.txt','3000mf.txt','5000mf.txt','10kmf.txt','20kmf.txt','halfmarathonf.txt','25kmf.txt','marathonf.txt']


# In[235]:

fns


# In[242]:

distance = array([100.,200.,400.,800.,1000.,1500.,1609.34,2000.,3000.,5000.,1.e4,2.e4,21097.5,2.5e4,2*21097.5,
                  100.,200.,400.,800.,1000.,1500.,1609.34,2000.,3000.,5000.,1.e4,2.e4,21097.5,2.5e4,2*21097.5])


# In[243]:

Ndistance = array(['100 m','200 m','400 m','800 m','1000 m','1500 m','Mile','2000 m',
                   '3000 m','5000 m','10 km','20 km','Half\nMarathon','25 km','Marathon'])


# In[244]:

dd = distance


# In[245]:

dd


# In[246]:

len(distance)


# In[ ]:




# In[247]:

gender = []
for i in arange(len(distance)/2.):
    gender.append('m')
for i in arange(len(distance)/2.):
    gender.append('f')
    
    


# In[317]:

df2 = pd.DataFrame(columns=('Distance','Gender','Time', 'Name', 'Date', 'Year') )
for i in arange(len(fns)):
    print i, fns[i]
    lines = [line.rstrip('\n').replace('y .','.').replace('+ .','.').replace('+.','.').replace('y.','.').replace('. ','!').split('!') for line in open(dn+fns[i])]
    ind = len(lines)
    df = pd.DataFrame(index=np.arange(0, ind), columns=('Distance','Gender','Time', 'Name', 'Date', 'Year') )

    for j in arange(len(lines)):
        vals = pd.unique(lines[j])
        #print j, len(vals),vals
        try:
            df.loc[j]["Time"] = float(vals[0])
        except:
            vv = vals[0].split(':')
            v0 = 0
            for k in arange(len(vv)):
                try:
                    v0 = v0+60**k*float(vv[-k-1])
                except:
                    print "badtime",i,j,vv
            df.loc[j]["Time"] = v0
        try:
            df.loc[j]["Date"] = pd.Timestamp(vals[-1])
        except:
            print "badyear", i, j, vals[-1], vals
        yr= pd.Timestamp(vals[-1]).year + pd.Timestamp(vals[-1]).month/12.
        if((j<8) and (yr > 1975) and (gender[i]=='m')):
            if( ((i==10)==False) and ((i==12)==False)):
                yr = yr - 100
                    
        if((yr>2016)):
            yr = yr - 100
        #if(j < 10):
        try:
            df.loc[j]["Year"] = float(yr)
            df.loc[j]["Name"] = vals[-4]
            df.loc[j]["Distance"] = distance[i]
            df.loc[j]["Gender"] = gender[i]
        except:
            print "bad",i,fns[i],j,vals
    df.to_csv(dn+fns[i]+'.csv')
    df2 = df2.append(df,ignore_index=True)


# In[318]:

df2.to_csv(dn+'allrecords.csv')


# In[284]:

plot(df["Year"],df["Time"]/60)


# In[ ]:




# In[285]:

for i in distance:
   print  i, df2["Year"][df2["Distance"]==i].min(),df2["Year"][df2["Distance"]==i].max()


# In[286]:

years = arange(1908,2015)


# In[287]:

pps = zeros((years.size,distance.size/2))
ppsf = zeros((years.size,distance.size/2))
for i in arange(years.size):
    for j in arange(distance.size/2):
        #print i,j#,df2["Time"][(df2["Distance"]==distance[j])*(df2["Year"]<years[i])][-1]
        try:
            #print years[i], distance[j], df2["Time"][(df2["Distance"]==distance[j])*(df2["Year"]<years[i])].values[-1]
            pps[i,j] = df2["Time"][(df2["Gender"]=='m')*(df2["Distance"]==distance[j])*(df2["Year"]<years[i])].values[-1]/distance[j]*1609.34/60.
            
        except:
            #print "bad"
            pps[i,j] = nan#df2["Time"][(df2["Distance"]==distance[j])].values[0]/distance[j]*1609.34/60.
            #print i,j,"didn't work"#, df2["Time"][(df2["Distance"]==distance[j])*(df2["Year"]<years[i])]
        try:
            #print years[i], distance[j], df2["Time"][(df2["Distance"]==distance[j])*(df2["Year"]<years[i])].values[-1]
            ppsf[i,j] = df2["Time"][(df2["Gender"]=='f')*(df2["Distance"]==distance[j])*(df2["Year"]<years[i])].values[-1]/distance[j]*1609.34/60.
            
        except:
            #print "bad"
            ppsf[i,j] = nan#df2["Time"][(df2["Distance"]==distance[j])].values[0]/distance[j]*1609.34/60.
            #print i,j,"didn't work"#, df2["Time"][(df2["Distance"]==distance[j])*(df2["Year"]<years[i])]
        


# In[289]:

for i in arange(years.size):
    figure()
    if(i > 0):

        semilogx(distance[:distance.size/2],pps[0,:],lw=.5,c='b')
        semilogx(distance[:distance.size/2],ppsf[0,:],lw=.5,c='r')

    if(i > 25):

        semilogx(distance[:distance.size/2],pps[25,:],lw=.5,c='b')
        semilogx(distance[:distance.size/2],ppsf[25,:],lw=.5,c='r')

    if(i > 50):
        semilogx(distance[:distance.size/2],pps[50,:],lw=.5,c='b')
        semilogx(distance[:distance.size/2],ppsf[50,:],lw=.5,c='r')

    if(i > 75):
        semilogx(distance[:distance.size/2],pps[75,:],lw=.5,c='b')
        semilogx(distance[:distance.size/2],ppsf[75,:],lw=.5,c='r')
        
    semilogx(distance[:distance.size/2],pps[i,:],lw=2,c='b')
    semilogx(distance[:distance.size/2],ppsf[i,:],lw=2,c='r')

    scatter(distance[:distance.size/2],pps[i,:],marker='^',c='b',edgecolor='b',s=70)
    scatter(distance[:distance.size/2],ppsf[i,:],marker='*',c='r',edgecolor='r',s=70)

    text(150,5.70,years[i])
    axis([100,1.e5,2,6])
    xlabel('Distance (m)')
    ylabel('Minutes per mile')
    savefig('worldrecords/png/'+str(years[i])+'.png')


# In[291]:

dyear = zeros(distance.size/2)
for i in arange(distance.size/2):
    #check date when men had same time as latest women's record
    min_ind = df2['Time'][(df2['Gender']=='f')*(df2['Distance']==distance[i])].argmin()
    f_year = df2['Year'][min_ind]
    f_time = df2['Time'][min_ind]
    try:
        m_year = df2['Year'][(df2['Gender']=='m')*(df2['Distance']==distance[i])*(df2['Time']>=f_time)].values[-1]
    except:
        m_year = f_year+1
    dyear[i] = f_year-m_year
    print distance[i],f_year, f_year-m_year


# In[292]:

def extend_year(x,year=2015):
    return append(x,year)
def extend_data(x):
    return append(x,x[-1])
targ = []
def eplot(*args, **kwargs):
   
    argtmp = [extend_year(args[0]),extend_data(args[1])]
    for i in args[2:]:
        argtmp.append(i)
    argtmp = tuple(argtmp)
    plot(*argtmp,**kwargs)


# In[319]:

for i in arange(distance.size/2):
    figure()
    mtime = (df2['Gender']=='m')*(df2['Distance']==distance[i])
    ftime = (df2['Gender']=='f')*(df2['Distance']==distance[i])
    eplot(df2['Year'][mtime].values,df2['Time'][mtime].values,'b-',lw=2)
    eplot(df2['Year'][ftime].values,df2['Time'][ftime].values,'r-',lw=2)
    if(dyear[i]>0):
        plot(df2['Year'][mtime].values+dyear[i],df2['Time'][mtime].values,'b--',lw=1)
    xlabel(r'Year')
    ylabel(r'Time [s]')
    xlim([1900,2050])
    yup = axis()[3]
    ybt = axis()[2]
    text(2000,(.9)*(yup-ybt)+ybt,Ndistance[i])
    # label()


# In[297]:

for i in [0]:
    figure()
    mtime = (df2['Gender']=='m')*(df2['Distance']==distance[i])
    ftime = (df2['Gender']=='f')*(df2['Distance']==distance[i])
    eplot(df2['Year'][mtime].values,df2['Time'][mtime].values,'b-',lw=2)
    eplot(df2['Year'][ftime].values,df2['Time'][ftime].values,'r-',lw=2)
    scatter(1988.75,9.79)
    if(dyear[i]>0):
        plot(df2['Year'][mtime].values+dyear[i],df2['Time'][mtime].values,'b--',lw=1)
    xlabel(r'Year')
    ylabel(r'Time [s]')
    xlim([1900,2050])
    yup = axis()[3]
    ybt = axis()[2]
    text(2000,(.9)*(yup-ybt)+ybt,Ndistance[i])
    # label()


# In[295]:

for i in [14]:
    figure()
    mtime = (df2['Gender']=='m')*(df2['Distance']==distance[i])
    ftime = (df2['Gender']=='f')*(df2['Distance']==distance[i])
    eplot(df2['Year'][mtime].values,df2['Time'][mtime].values,'b-',lw=2)
    eplot(df2['Year'][ftime].values,df2['Time'][ftime].values,'r-',lw=2)
#    scatter(2016,2*60*60+15*60+25,marker='*',c='r')
    if(dyear[i]>0):
        plot(df2['Year'][mtime].values+dyear[i],df2['Time'][mtime].values,'b--',lw=1)
    xlabel(r'Year')
    ylabel(r'Time [s]')
    xlim([1900,2050])
    ylim([7000,10000])
    yup = axis()[3]
    ybt = axis()[2]
    text(2000,(.9)*(yup-ybt)+ybt,Ndistance[i])
    # label()


# ### 

# In[316]:

print i


# In[321]:

df2['Year'].count()


# In[325]:

2015-1988


# In[331]:

1988-27


# In[342]:

mrecords_after_88 = zeros(distance.size/2)
frecords_after_88 = zeros(distance.size/2)
mrecords_before_88 = zeros(distance.size/2)
frecords_before_88 = zeros(distance.size/2)
mrecords_long = zeros(distance.size/2)
frecords_long = zeros(distance.size/2)
for i in arange(distance.size/2):
    mtime = (df2['Gender']=='m')*(df2['Distance']==distance[i])
    ftime = (df2['Gender']=='f')*(df2['Distance']==distance[i])
    frecords_after_88[i] =  df2['Year'][ftime*(df2['Year']>1988)].count()
    mrecords_after_88[i] =   df2['Year'][mtime*(df2['Year']>1988)].count()
    frecords_before_88[i] =  df2['Year'][ftime*(df2['Year']<=1988)*(df2['Year']>1961)].count()
    mrecords_before_88[i] =  df2['Year'][mtime*(df2['Year']<=1988)*(df2['Year']>1961)].count()
    if(df2['Year'][ftime].min() < 1962):
        frecords_long[i] = 1
    if(df2['Year'][mtime].min() < 1962):
        mrecords_long[i] = 1
    
    # label()


# In[343]:

df2['Year'][ftime].min()


# In[345]:

frecords_long


# In[368]:

plot(distance[(frecords_long==1.0)*(mrecords_long==1.0)], 
     frecords_before_88[[(frecords_long==1.0)*(mrecords_long==1.0)]],'r-')
plot(distance[(frecords_long==1.0)*(mrecords_long==1.0)], 
     frecords_after_88[[(frecords_long==1.0)*(mrecords_long==1.0)]],'r-')
for i in arange(distance.size/2)[(frecords_long==1.0)*(mrecords_long==1.0)]:
    #print Ndistance[i]
    scatter(distance[i],frecords_after_88[i],color='r')

    scatter(distance[i],frecords_before_88[i],color='None',marker='s',edgecolor='r')
    xlim(0,900)
    ylim(-1,25)
    xlabel('Distance [m]')
    ylabel('World Record Races')


# In[369]:

for i in arange(distance.size/2)[(frecords_long==1.0)*(mrecords_long==1.0)]:
    #print Ndistance[i]
    scatter(distance[i],mrecords_after_88[i],color='b')
    scatter(distance[i],mrecords_before_88[i],color='None',marker='s',edgecolor='b')
    xlim(0,1100)
    ylim(-1,25)


# In[350]:

mean(frecords_after_88)


# In[336]:

frecords_before_88


# In[334]:

mean(frecords_before_88)


# In[329]:

mean(mrecords_after_88)


# In[ ]:



