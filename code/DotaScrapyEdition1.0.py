#爬dotamax上面选手的比赛数据
#import urllib2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 23:34:08 2016

@author: yangzhou
"""

#首先我们需要main方法，不传入任何参数就返回各个战队的人员的数据对比
#然后我们需要三个列表(国内，国外，总)来储存各个战队国籍，战队名称，人员名称和dota2_id，这个需要人工维护，并且在main方法里面
#其次我们需要一个方法从网上爬取一个人员的比赛记录，输入参数为dota2_id，输出参数为一个表
#然后我们需要一个方法对这个表进行预处理，得到我们想要的表
#最后对于我们需要的每一个统计结果，我们都需要编一个方法，这些方法对应具体的功能：
#1.针对队员，我们想知道他们在一，二，三个月内的比赛情况：比赛次数，胜率，一周内的胜率，常用前三英雄及KDA。
#2.针对战队，我们想知道各个战队的拿手英雄和对应的人及KDA，我们还想知道各个战队的平均比赛次数，以及最勤奋的人。
#3.针对每个热门英雄，我们想知道哪个队伍的队员打的好。这里需要一个有关比赛次数和KDA的加权值来衡量。

import re
from bs4 import BeautifulSoup
import urllib
import pandas as pd
import time
import numpy as np
#这个方法返回单个战队的信息表
def team_get(team,teamname,nationality,player1,playere1id,player2,playere2id,
                     player3,playere3id,player4,playere4id,player5,playere5id):
    dotateam=pd.DataFrame(columns=('TeamName',
                                   'Nationality',
                                   'Player1',
                                   'Player1Id',
                                   'Player2',
                                   'Player2Id',
                                   'Player3',
                                   'Player3Id',
                                   'Player4',
                                   'Player4Id',
                                   'Player5',
                                   'Player5Id'),index=team)
    dotateam['TeamName'] =  teamname
    dotateam['Nationality'] =  nationality
    dotateam['Player1'] =  player1
    dotateam['Player1Id'] =  playere1id
    dotateam['Player2'] =  player2
    dotateam['Player2Id'] =  playere2id
    dotateam['Player3'] =  player3
    dotateam['Player3Id'] =  playere3id
    dotateam['Player4'] =  player4
    dotateam['Player4Id'] =  playere4id        
    dotateam['Player5'] =  player5
    dotateam['Player5Id'] =  playere5id                   
    return dotateam

#这个方法向列表中插入战队信息，并返回所有的战队信息表
def team_information(dotateam):
    vg=team_get(['vg'],'vg',1,'sylar',108382060,'cty',108376607,'rotk',91698091,'burning',90892734,'AAAMy',135384059)
    dotateam=dotateam.append(vg)
    lgd=team_get(['lgd'],'lgd',1,'Agressif',130416036,'Maybe',106863163,'xiao8',98887913,'greengreengreen',89598554,'MMY',89407113)
    dotateam=dotateam.append(lgd)
    ehome=team_get(['ehome'],'ehome',1,'LaNm',89423756,'oldchicken',135878232,'oldeLeVeN',134276083,'iceiceice',84772440,'Fenrir',113800818)
    dotateam=dotateam.append(ehome)
    newbee=team_get(['newbee'],'newbee',1,'Hao',88508515,'Mu',89157606,'kpii',87012746,'ChuaN',88553213,'陈世美',139876032)
    dotateam=dotateam.append(newbee)
    vgr=team_get(['vgr'],'vgr',1,'END',139280377,'two',80929738,'Yang',139937922,'ddc',114239371,'Fy',101695162)
    dotateam=dotateam.append(vgr)
    dotateam=dotateam.drop(0)
    return dotateam

#player_information(139937922)
#这个方法输入一个队员id，输出此队员的比赛信息表。
def player_information(playerid):
#    headers = {'Host': 'dotamax.com',
#               'Connection': 'keep-alive',
#               'Cache-Control': 'max-age=0',
#               'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
#                'Referer': 'http://www.so.com/link?url=http%3A%2F%2Fdotamax.com%2F&q=dotamax&ts=1460679784&t=befc8befa29e74189cd61868166e758&src=haosou',
#                'Accept-Encoding': 'gzip, deflate, sdch',
#                'Accept-Language': 'zh-CN,zh;q=0.8'}  
    headers = {'Host': 'dotamax.com',
               'Connection': 'keep-alive',
               'Referer': 'http://www.so.com/link?url=http%3A%2F%2Fdotamax.com%2F&q=dotamax&ts=1460679784&t=befc8befa29e74189cd61868166e758&src=haosou',
               'Cookie': 'csrftoken=VXu0WDRSEioXzYleDvH8BmDhUjsYIbxs; Hm_lvt_575895fe09d48554a608faa5ef059555=1460638550,1460679744,1460679773,1460681497; Hm_lpvt_575895fe09d48554a608faa5ef059555=1460681497; _ga=GA1.2.1700274043.1459144751; _gat=1',
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}  
#    req = urllib.request.Request(url=chaper_url, headers=headers)  
#    urllib.request.urlopen(req).read()
    url1='http://dotamax.com/player/match/'
    url2='/?skill=&ladder=&hero=-1'
    WebSheet=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
#构造最终数据表和中间数据表，首先把数据传递给中间数据表，
#然后把中间数据表贴在最终数据表底部，数据表的列数为WebColumn手动调整
    FinalDataFrame=pd.DataFrame(columns=('hero','matchnumber','time','result','KDA','type','quipement'),index=[0])
    MidDataFrame=pd.DataFrame(columns=('hero','matchnumber','time','result','KDA','type','quipement'),index=[0])
    for page in WebSheet:
        chaper_url=url1+str(playerid)+url2+'&p='+str(page)
#        print(chaper_url)
        req = urllib.request.Request(url=chaper_url, headers=headers)
        h=urllib.request.urlopen(req)
        soup = BeautifulSoup(h,"lxml")
        
        for tabb in soup.find_all('tr'):
            i=0;
            for tdd in tabb.find_all('td'):
                MidDataFrame.iat[0,i]=''.join(tdd.get_text().split())
                i = i+1
            FinalDataFrame=FinalDataFrame.append(MidDataFrame, ignore_index=True)
    FinalDataFrame=FinalDataFrame.drop(0)
    return FinalDataFrame

#这个方法对队员的比赛信心表预处理，输出此队员的初步统计信息表。
def player_compute_first(playerinformation):   
    
#截取比赛编号
    a1=playerinformation['matchnumber'].copy()
    i=1
    for matchnumber in a1:
        a1[i]=re.match(r'(\d{10})\D*',a1[i]).group(1)
        i+=1
    playerinformation['Number']=a1                  
    
#截取比赛类型
    a2=playerinformation['matchnumber'].copy()
    i=1
    for matchnumber in a2:
        a2[i]=re.match(r'\d*(\D*)',a2[i]).group(1)
        i+=1
    playerinformation['matchtype']=a2
    
#截取比赛时间
    a3=playerinformation['time'].copy()
    i=1
    for time in a3:
        if re.match(r'\d*小时前',a3[i]):
            a3[i]=int(1)
        elif re.match(r'\d*天前',a3[i]):
            a3[i]=int(re.match(r'(\d*)天前',a3[i]).group(1))
        elif re.match(r'\d*个月前',a3[i]):
            a3[i]=int(re.match(r'(\d*)个月前',a3[i]).group(1))*30
        else:
            a3[i]=int(999999999)
        i+=1
    playerinformation['ptime']=a3
    
#截取比赛结果
    a4=playerinformation['result'].copy()
    i=1
    for result in a4:
        if  a4[i] == '胜利':
            a4[i]=1
        else:
            a4[i]=0
        i+=1
    playerinformation['presult']=a4
    
#截取KDA
    a5=playerinformation['KDA'].copy()
    i=1
    for KDA in a5:
        a5[i]=float(re.match(r'(\d+\.\d+)\(\d+\/\d+\/\d+\)',a5[i]).group(1))
        i+=1
    playerinformation['pKDA']=a5
    
#截取KILL
    a6=playerinformation['KDA'].copy()
    i=1
    for KDA in a6:
        a6[i]=int(re.match(r'\d+\.\d+\((\d+)\/\d+\/\d+\)',a6[i]).group(1))
        i+=1
    playerinformation['KILL']=a6
    
#截取DEATH
    a7=playerinformation['KDA'].copy()
    i=1
    for KDA in a7:
        a7[i]=int(re.match(r'\d+\.\d+\(\d+\/(\d+)\/\d+\)',a7[i]).group(1))
        i+=1
    playerinformation['DEATH']=a7
    
#截取ASSISTANCE
    a8=playerinformation['KDA'].copy()
    i=1
    for result in a8:
        a8[i]=int(re.match(r'\d+\.\d+\(\d+\/\d+\/(\d+)\)',a8[i]).group(1))
        i+=1
    playerinformation['ASSISTANCE']=a8

#去除不必要的列，并修改列名
    playerinformation=playerinformation.drop(['matchnumber','time','result','KDA','quipement'],axis=1)
    playerinformation=playerinformation.rename(columns={'ptime':'time','presult':'result','pKDA':'KDA'})
    
    return playerinformation

#这个方法对队员的比赛信心表预处理，输出此队员的统计信息表。
def player_compute(playerteam,playername,playerinformation):  
#生成信息表
    playercompute=pd.DataFrame(columns=('playername',
                                        'playerteam',
                                        'MatchCount1',
                                        'WinRate1',
                                        'WeekHero1',
                                        'WeekKDA1',
                                        'WeekHero2',
                                        'WeekKDA2',
                                        'WeekHero3',
                                        'WeekKDA3',
                                        'MatchCount2',
                                        'WinRate2',
                                        'MonthHero1',
                                        'MonthKDA1',
                                        'MonthHero2',
                                        'MonthKDA2',
                                        'MonthHero3',
                                        'MonthKDA3'),index=[0])
    playercompute['playername']= playername 
    playercompute['playerteam']= playerteam 
    playerinformation=player_compute_first(playerinformation)
#我们只统计职业比赛或veryhigh的比赛
#1.针对队员，我们想知道他们在一，二，三个月内的比赛情况：比赛次数，胜率，一周内的胜率，常用前三英雄及KDA。
    playerinformation=playerinformation[(playerinformation.type=='VeryHigh')|(playerinformation.type=='职业')]
#统计2周内的比赛情况
    playerinformation1=playerinformation.copy()
    playerinformation1=playerinformation1[playerinformation1.time<15]
    playercompute['MatchCount1']=playerinformation1.hero.count()
    playercompute['WinRate1']=playerinformation1[playerinformation1.result==1].result.count()/playerinformation1.result.count()
    playercompute['WeekHero1']=playerinformation1.groupby('hero').hero.count().sort_values(ascending=False).head(3).index[0]
    playercompute['WeekHero2']=playerinformation1.groupby('hero').hero.count().sort_values(ascending=False).head(3).index[1]
    playercompute['WeekHero3']=playerinformation1.groupby('hero').hero.count().sort_values(ascending=False).head(3).index[2]
    playercompute['WeekKDA1']=round(playerinformation1[playerinformation1.hero==playercompute['WeekHero1'][0]].KDA.mean(),2)
    playercompute['WeekKDA2']=round(playerinformation1[playerinformation1.hero==playercompute['WeekHero2'][0]].KDA.mean(),2)
    playercompute['WeekKDA3']=round(playerinformation1[playerinformation1.hero==playercompute['WeekHero3'][0]].KDA.mean(),2)
    
#统计一个半月内的比赛情况
    playerinformation2=playerinformation.copy()
    playerinformation2=playerinformation2[playerinformation2.time<45]
    playercompute['MatchCount2']=playerinformation2.hero.count()
    playercompute['WinRate2']=playerinformation2[playerinformation2.result==1].result.count()/playerinformation2.result.count()
    playercompute['MonthHero1']=playerinformation2.groupby('hero').hero.count().sort_values(ascending=False).head(3).index[0]
    playercompute['MonthHero2']=playerinformation2.groupby('hero').hero.count().sort_values(ascending=False).head(3).index[1]
    playercompute['MonthHero3']=playerinformation2.groupby('hero').hero.count().sort_values(ascending=False).head(3).index[2]
    playercompute['MonthKDA1']=round(playerinformation2[playerinformation2.hero==playercompute['MonthHero1'][0]].KDA.mean(),2)
    playercompute['MonthKDA2']=round(playerinformation2[playerinformation2.hero==playercompute['MonthHero2'][0]].KDA.mean(),2)
    playercompute['MonthKDA3']=round(playerinformation2[playerinformation2.hero==playercompute['MonthHero3'][0]].KDA.mean(),2)
    
    return playercompute  

#这个方法遍历列表中的队员，输出一个所有队员的比赛信息表
def player_message(dotateam):
#创建一个新表
    allplayerscompute=pd.DataFrame(columns=('playername',
                                            'playerteam',
                                            'MatchCount1',
                                            'WinRate1',
                                            'WeekHero1',
                                            'WeekKDA1',
                                            'WeekHero2',
                                            'WeekKDA2',
                                            'WeekHero3',
                                            'WeekKDA3',
                                            'MatchCount2',
                                            'WinRate2',
                                            'MonthHero1',
                                            'MonthKDA1',
                                            'MonthHero2',
                                            'MonthKDA2',
                                            'MonthHero3',
                                            'MonthKDA3'),index=[0])
    players=dotateam.loc[:,['TeamName','Player1','Player1Id']].rename(columns={'Player1':'Player','Player1Id':'PlayerId'}).\
    append(dotateam.loc[:,['TeamName','Player2','Player2Id']].rename(columns={'Player2':'Player','Player2Id':'PlayerId'})).\
    append(dotateam.loc[:,['TeamName','Player3','Player3Id']].rename(columns={'Player3':'Player','Player3Id':'PlayerId'})).\
    append(dotateam.loc[:,['TeamName','Player4','Player4Id']].rename(columns={'Player4':'Player','Player4Id':'PlayerId'})).\
    append(dotateam.loc[:,['TeamName','Player5','Player5Id']].rename(columns={'Player5':'Player','Player5Id':'PlayerId'}))

    for playerid in  players['PlayerId']:
        print('正在爬取编号为%r的选手的比赛数据...' % str(int(playerid)))
        playerinformation=player_information(str(int(playerid)))
#        time.sleep(100)
        allplayerscompute=allplayerscompute.append(player_compute(players[players.PlayerId==playerid].TeamName[0],players[players.PlayerId==playerid].Player[0],playerinformation))
    return allplayerscompute

#1.针对队员，我们想知道他们在一，二，三个月内的比赛情况：比赛次数，胜率，一周内的胜率，常用前三英雄及KDA。
def players_compute(playermessage):
    weekplayers=playermessage.sort_values(['MatchCount1'],ascending=False).head(10)
    weekplayers=weekplayers.drop(['MatchCount2','WinRate2','MonthHero1','MonthKDA1','MonthHero2','MonthKDA2','MonthHero3','MonthKDA3'],axis=1)
    monthplayers=playermessage.sort_values(['MatchCount2'],ascending=False).head(10)
    monthplayers=monthplayers.drop(['MatchCount1','WinRate1','WeekHero1','WeekKDA1','WeekHero2','WeekKDA2','WeekHero3','WeekKDA3'],axis=1)
    return weekplayers , monthplayers

#2.针对战队，我们想知道各个战队的拿手英雄和对应的人及KDA，我们还想知道各个战队的总比赛次数，以及最勤奋的人。
def team_compute(dotateam,playermessage):
#创建一个新表
    teamcomputefinal=pd.DataFrame(columns=('teamname',
                                            'weekmatches',
                                            'weekdiligentplayer',
                                            'monthmatches',
                                            'monthdiligentplayer',
                                            'monthheroplayer1',
                                            'monthhero1',
                                            'monthherokda1',
                                            'monthheroplayer2',
                                            'monthhero2',
                                            'monthherokda2',
                                            'monthheroplayer3',
                                            'monthhero3',
                                            'monthherokda3',
                                            'monthheroplayer4',
                                            'monthhero4',
                                            'monthherokda4',
                                            'monthheroplayer5',
                                            'monthhero5',
                                            'monthherokda5'),index=[0])

    for teamname in dotateam.TeamName:
        teamcomputemid=pd.DataFrame(columns=('teamname',
                                            'weekmatches',
                                            'weekdiligentplayer',
                                            'monthmatches',
                                            'monthdiligentplayer',
                                            'monthheroplayer1',
                                            'monthhero1',
                                            'monthherokda1',
                                            'monthheroplayer2',
                                            'monthhero2',
                                            'monthherokda2',
                                            'monthheroplayer3',
                                            'monthhero3',
                                            'monthherokda3',
                                            'monthheroplayer4',
                                            'monthhero4',
                                            'monthherokda4',
                                            'monthheroplayer5',
                                            'monthhero5',
                                            'monthherokda5'),index=[1])
        teamcomputemid['teamname']=teamname
        teamcomputemid['weekmatches']=playermessage[playermessage.playername==dotateam[dotateam.TeamName==teamname].Player1[0]].MatchCount1[0]+\
                                      playermessage[playermessage.playername==dotateam[dotateam.TeamName==teamname].Player2[0]].MatchCount1[0]+\
                                      playermessage[playermessage.playername==dotateam[dotateam.TeamName==teamname].Player3[0]].MatchCount1[0]+\
                                      playermessage[playermessage.playername==dotateam[dotateam.TeamName==teamname].Player4[0]].MatchCount1[0]+\
                                      playermessage[playermessage.playername==dotateam[dotateam.TeamName==teamname].Player5[0]].MatchCount1[0]
        teamcomputemid['weekdiligentplayer']=playermessage[playermessage.playername==dotateam[dotateam.TeamName==teamname].Player1[0]].playername[0]
        if playermessage[playermessage.playername==teamcomputemid['weekdiligentplayer'][1]].MatchCount1[0]<playermessage[playermessage.playername==dotateam[dotateam.TeamName==teamname].Player2[0]].MatchCount1[0]:
            teamcomputemid['weekdiligentplayer']=playermessage[playermessage.playername==dotateam[dotateam.TeamName==teamname].Player2[0]].playername[0]
        elif playermessage[playermessage.playername==teamcomputemid['weekdiligentplayer'][1]].MatchCount1[0]<playermessage[playermessage.playername==dotateam[dotateam.TeamName==teamname].Player3[0]].MatchCount1[0]:
            teamcomputemid['weekdiligentplayer']=playermessage[playermessage.playername==dotateam[dotateam.TeamName==teamname].Player3[0]].playername[0]
        elif playermessage[playermessage.playername==teamcomputemid['weekdiligentplayer'][1]].MatchCount1[0]<playermessage[playermessage.playername==dotateam[dotateam.TeamName==teamname].Player4[0]].MatchCount1[0]:
            teamcomputemid['weekdiligentplayer']=playermessage[playermessage.playername==dotateam[dotateam.TeamName==teamname].Player4[0]].playername[0]
        elif playermessage[playermessage.playername==teamcomputemid['weekdiligentplayer'][1]].MatchCount1[0]<playermessage[playermessage.playername==dotateam[dotateam.TeamName==teamname].Player5[0]].MatchCount1[0]:
            teamcomputemid['weekdiligentplayer']=playermessage[playermessage.playername==dotateam[dotateam.TeamName==teamname].Player5[0]].playername[0]

        teamcomputemid['monthmatches']=playermessage[playermessage.playername==dotateam[dotateam.TeamName==teamname].Player1[0]].MatchCount2[0]+\
                                      playermessage[playermessage.playername==dotateam[dotateam.TeamName==teamname].Player2[0]].MatchCount2[0]+\
                                      playermessage[playermessage.playername==dotateam[dotateam.TeamName==teamname].Player3[0]].MatchCount2[0]+\
                                      playermessage[playermessage.playername==dotateam[dotateam.TeamName==teamname].Player4[0]].MatchCount2[0]+\
                                      playermessage[playermessage.playername==dotateam[dotateam.TeamName==teamname].Player5[0]].MatchCount2[0]
        teamcomputemid['monthdiligentplayer']=playermessage[playermessage.playername==dotateam[dotateam.TeamName==teamname].Player1[0]].playername[0]
        if playermessage[playermessage.playername==teamcomputemid['monthdiligentplayer'][1]].MatchCount1[0]<playermessage[playermessage.playername==dotateam[dotateam.TeamName==teamname].Player2[0]].MatchCount1[0]:
            teamcomputemid['monthdiligentplayer']=playermessage[playermessage.playername==dotateam[dotateam.TeamName==teamname].Player2[0]].playername[0]
        elif playermessage[playermessage.playername==teamcomputemid['monthdiligentplayer'][1]].MatchCount1[0]<playermessage[playermessage.playername==dotateam[dotateam.TeamName==teamname].Player3[0]].MatchCount1[0]:
            teamcomputemid['monthdiligentplayer']=playermessage[playermessage.playername==dotateam[dotateam.TeamName==teamname].Player3[0]].playername[0]
        elif playermessage[playermessage.playername==teamcomputemid['monthdiligentplayer'][1]].MatchCount1[0]<playermessage[playermessage.playername==dotateam[dotateam.TeamName==teamname].Player4[0]].MatchCount1[0]:
            teamcomputemid['monthdiligentplayer']=playermessage[playermessage.playername==dotateam[dotateam.TeamName==teamname].Player4[0]].playername[0]
        elif playermessage[playermessage.playername==teamcomputemid['monthdiligentplayer'][1]].MatchCount1[0]<playermessage[playermessage.playername==dotateam[dotateam.TeamName==teamname].Player5[0]].MatchCount1[0]:
            teamcomputemid['monthdiligentplayer']=playermessage[playermessage.playername==dotateam[dotateam.TeamName==teamname].Player5[0]].playername[0]

        teamcomputemid['monthheroplayer1']=dotateam[dotateam.TeamName==teamname].Player1[0]
        teamcomputemid['monthhero1']=playermessage[playermessage.playername==teamcomputemid['monthheroplayer1'][1]].MonthHero1[0]
        teamcomputemid['monthherokda1']=playermessage[playermessage.playername==teamcomputemid['monthheroplayer1'][1]].MonthKDA1[0]
        teamcomputemid['monthheroplayer2']=dotateam[dotateam.TeamName==teamname].Player2[0]
        teamcomputemid['monthhero2']=playermessage[playermessage.playername==teamcomputemid['monthheroplayer2'][1]].MonthHero1[0]
        teamcomputemid['monthherokda2']=playermessage[playermessage.playername==teamcomputemid['monthheroplayer2'][1]].MonthKDA1[0]
        teamcomputemid['monthheroplayer3']=dotateam[dotateam.TeamName==teamname].Player3[0]
        teamcomputemid['monthhero3']=playermessage[playermessage.playername==teamcomputemid['monthheroplayer3'][1]].MonthHero1[0]
        teamcomputemid['monthherokda3']=playermessage[playermessage.playername==teamcomputemid['monthheroplayer3'][1]].MonthKDA1[0]
        teamcomputemid['monthheroplayer4']=dotateam[dotateam.TeamName==teamname].Player4[0]
        teamcomputemid['monthhero4']=playermessage[playermessage.playername==teamcomputemid['monthheroplayer4'][1]].MonthHero1[0]
        teamcomputemid['monthherokda4']=playermessage[playermessage.playername==teamcomputemid['monthheroplayer4'][1]].MonthKDA1[0]
        teamcomputemid['monthheroplayer5']=dotateam[dotateam.TeamName==teamname].Player5[0]
        teamcomputemid['monthhero5']=playermessage[playermessage.playername==teamcomputemid['monthheroplayer5'][1]].MonthHero1[0]
        teamcomputemid['monthherokda5']=playermessage[playermessage.playername==teamcomputemid['monthheroplayer5'][1]].MonthKDA1[0]
        
        teamcomputefinal=teamcomputefinal.append(teamcomputemid)
    teamcomputefinal=teamcomputefinal.drop(0)
    teamcomputefinal=teamcomputefinal.sort_values(['weekmatches'],ascending=False)
    return teamcomputefinal
       
#3.针对每个热门英雄，我们想知道哪个队伍的队员打的好。这里需要一个有关比赛次数和KDA的加权值来衡量。
def hero_compute(dotateam,playermessage):
    hotheros=pd.DataFrame(['祈求者','主宰','灰烬之灵','大地之灵','斯拉克','兽王','德鲁伊','虚空假面','幻影长矛手','熊战士','幽鬼','莱恩','先知','魅惑魔女','殁境神蚀者','斯温'],columns=['hero'])    

#进行统计计算
    players=dotateam.loc[:,['TeamName','Player1','Player1Id']].rename(columns={'Player1':'Player','Player1Id':'PlayerId'}).\
    append(dotateam.loc[:,['TeamName','Player2','Player2Id']].rename(columns={'Player2':'Player','Player2Id':'PlayerId'})).\
    append(dotateam.loc[:,['TeamName','Player3','Player3Id']].rename(columns={'Player3':'Player','Player3Id':'PlayerId'})).\
    append(dotateam.loc[:,['TeamName','Player4','Player4Id']].rename(columns={'Player4':'Player','Player4Id':'PlayerId'})).\
    append(dotateam.loc[:,['TeamName','Player5','Player5Id']].rename(columns={'Player5':'Player','Player5Id':'PlayerId'}))
    
    players['matches']=0
    players['kda']=0
    players['score']=0
    hotheros['player1']='待定'
    hotheros['player2']='待定'
    hotheros['player3']='待定'
    hotheros['kda1']=0
    hotheros['kda2']=0
    hotheros['kda3']=0

#建立45天内所有队员的比赛信息总表
    ptime=0
    for playerid in  players.PlayerId:
        print('正在爬取并整合编号为%r的选手的45天内比赛数据...' % str(int(playerid)))
        playerinformationmid=player_information(str(int(playerid)))
        playerinformation=player_compute_first(playerinformationmid)
        playerinformation['type']=playerid
        playerinformation=playerinformation[playerinformation.time<45]
        playerinformation=playerinformation.rename(columns={'type':'PlayerId'})
#        time.sleep(100)
        if ptime==0:
            allplayersmonth=playerinformation.copy()
            ptime=1
        else:
            allplayersmonth=allplayersmonth.append(playerinformation)  

#每一场比赛相当于KDA最高者的KDA的五百分之一
    prow2=0
    for heros in hotheros.hero:
        prow=0
        for playerid in players.PlayerId:
            players.iloc[prow,3]=allplayersmonth[(allplayersmonth.PlayerId==playerid)&(allplayersmonth.hero==heros)].hero.count()
            players.iloc[prow,4]=allplayersmonth[(allplayersmonth.PlayerId==playerid)&(allplayersmonth.hero==heros)].KDA.mean()
            prow+=1
        prow1=0
        players=players.fillna(value=0)
        for playerid in players.PlayerId:
            if players.iloc[prow1,3]<5:
                players.iloc[prow1,5]=0
            else:
                players.iloc[prow1,5]=players.kda.max()/500+players.iloc[prow1,4]
            prow1+=1
        hotheros.iloc[prow2,1]=players.sort_values(['score'],ascending=False).Player[0]
        hotheros.iloc[prow2,2]=players.sort_values(['score'],ascending=False).Player[1]
        hotheros.iloc[prow2,3]=players.sort_values(['score'],ascending=False).Player[2]
        hotheros.iloc[prow2,4]=players.sort_values(['score'],ascending=False).kda[0]
        hotheros.iloc[prow2,5]=players.sort_values(['score'],ascending=False).kda[1]
        hotheros.iloc[prow2,6]=players.sort_values(['score'],ascending=False).kda[2]
        prow2+=1
        
    return hotheros
        
if __name__=='__main__':
#建立一个列表，向其中填入战队信息。
    DotaTeam=pd.DataFrame(columns=('TeamName',
                                   'Nationality',
                                   'Player1',
                                   'Player1Id',
                                   'Player2',
                                   'Player2Id',
                                   'Player3',
                                   'Player3Id',
                                   'Player4',
                                   'Player4Id',
                                   'Player5',
                                   'Player5Id'),index=[0])

#这个方法向列表中填入战队信息。
    DotaTeam=team_information(DotaTeam)

#这个方法遍历列表中的每个队员，并调用另外2个方法：从网上拖一个队员的信息和预处理
#这个方法传入一个数据信息表，然后输出一个所有队员的比赛信息表，之后的统计操作就按这个输出的表来。
    PlayerMessage=player_message(DotaTeam)
    
#对应上面的统计结果1
    PlayerStatisticsWeek,PlayerStatisticsMonth=players_compute(PlayerMessage)
    
#对应上面的统计结果2
    TeamStatistics=team_compute(DotaTeam,PlayerMessage)
    
#对应上面的统计结果3
    HeroStatistics=hero_compute(DotaTeam,PlayerMessage)
    
#这个方法把列表输出到excel表格
    PlayerStatisticsWeek.to_excel('周队员情况.xls', sheet_name='PlayerStatisticsWeek')      
    PlayerStatisticsMonth.to_excel('月队员情况.xls', sheet_name='PlayerStatisticsMonth')      
    TeamStatistics.to_excel('队伍情况.xls', sheet_name='TeamStatistics')      
    HeroStatistics.to_excel('英雄绝活情况.xls', sheet_name='HeroStatistics')      





















