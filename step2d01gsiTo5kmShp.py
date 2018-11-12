#! /Library/Frameworks/Python.framework/Versions/3.3/bin
#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

# ------------------------------------------------------------- Sectin of Import
import sys, os, shutil, glob
import numpy as np                      # numpy
import pandas as pd
import geopandas as gpd

dir1 = "/Volumes/Research/12Report/Programs/" ;   dir2 =  "Cls/__pycache__"
sys.path.append(dir1)
import Cls.funcs      as fun

# ----- 10 ------ 20 ------ 30 ------ 40 ------ 50 ------ 60 ------ 70 ------ 80
# domain01を包含する17個の1時メッシュ達
fmc = [4828, 4829, 4830, 4831, 4928, 4929, 4930, 4931, 5029, 5030, 5031, 5129,
       5130, 5131, 5132, 5231, 5232]

# 5kmメッシュコードの下3桁の付与, 関数:fun_set_5kmMeshCode
code = fun.Set_5kmeshCode()

# ----- 10 ------ 20 ------ 30 ------ 40 ------ 50 ------ 60 ------ 70 ------ 80
"""
5kmメッシュのgeopandasデータフレームの生成
"""
for i in fmc:                                          # 17の1次メッシュでループ
    print (i)
    # シェープファイルの読み込み
    shpfile = '../../Input/GSIData/LandUse/L03-a-14_' + str(i) +'.shp'
    df = gpd.read_file(shpfile, encoding='shift-jis')
    
    # 後の処理のため3次メッシュを明示的に整数にしておく
    df['メッシュ'] = df['メッシュ'].apply(int)

    # 3次メッシュの順で自作5kmメッシュコード（7桁)の配列の生成
    myMesh = np.arange(len(df)).astype(np.int64)
    for idf in np.arange(len(df)):
        for ic in np.arange(len(code)):
            if (df.メッシュ[idf] % 10000 in code[ic]):
                fiveCode = str(i) + '%03d' %int(ic)
                myMesh[idf] = fiveCode
                break
            else:
                continue

    # Polygonの座標を四捨五入して小数点以下を整える 関数:fun_set_precision
    df['geometry'] = df['geometry'].apply(lambda g:fun.set_precision_shape(g,6))
    
    # 5km メッシュcolumnを追加
    df["5k_mesh"] = myMesh
    
    # geometry を集約
    df_geo = df[['5k_mesh','geometry']].dissolve(by='5k_mesh')
    # geometry以外の要素の合計を求める
    df_attr = df.groupby('5k_mesh').sum()
    # 5k_meshコードをキーにして結合させる
    df_5km = pd.concat([df_geo, df_attr], axis=1).reset_index()

    # 5kmメッシュのgeopandasファイルの整形
    df_5km = df_5km.drop(['メッシュ'], axis=1) # 三次メッシュコードの削除
    df_5km.index = np.arange(len(df_5km)).astype(np.int64) # 整数indexを付与

    # 1次メッシュ単位でのの結合
    if (i == 4828):
        df_after = df_5km
    else:
        df_after = pd.concat([df_before, df_5km], axis=0)
        
    df_before = df_after
    #dfg_before.to_csv("../Output/5kMesh" + str(i) + ".txt", sep='\t')

# 17の1次メッシュ内の5kmメッシュを緯度経度を有するファイルとして出力
#df_after.to_csv("../Output/5kMesh.txt", sep='\t')

"""
5kmメッシュ毎に最大面積を持つ土地利用利用区分を求める
"""
df = df_after
df.reset_index(drop=True)                                  # 単純増なindexにする

cols = [e for e in df.columns.tolist() if e not in ['geometry', 'メッシュ']]
df['landtype'] = df[cols].apply(lambda x: x.idxmax(), axis=1)

# 日本語の列名だと色々エラーとなるため、英語に変更
df.rename(columns={'メッシュ': 'mesh'}, inplace=True)

df['modis05'] = df['森林']
df['modis10'] = df['ゴルフ場']
df['modis12'] = df['田'] + df['他農用地']
df['modis13'] = df['建物用地'] + df['道路'] + df['鉄道'] + df['他用地']
df['modis14'] = df['荒地']
df['modis17'] = df['河川湖沼'] + df['海浜'] + df['海水域']

df['sum'] = df['modis05'] + df['modis10'] + df['modis12'] + df['modis13'] + df['modis14'] + df['modis17']

df['modis05'] = np.round(df['modis05'] / df['sum'], decimals=2)
df['modis10'] = np.round(df['modis10'] / df['sum'], decimals=2)
df['modis12'] = np.round(df['modis12'] / df['sum'], decimals=2)
df['modis13'] = np.round(df['modis13'] / df['sum'], decimals=2)
df['modis14'] = np.round(df['modis14'] / df['sum'], decimals=2)
df['modis17'] = np.round(df['modis17'] / df['sum'], decimals=2)


# Modisのlanduse category列を追記
''' lambda function to transform series data'''
landCat   = map(
            (lambda x: 5 if x  in {'森林'}
               else (10 if x in {'ゴルフ場'}
                 else (12 if x in {'田','その他の農用地','他農用地'}
                   else (13 if x in {'建物用地','道路','鉄道','その他の用地','他用地'}
                     else (14 if x in {'荒地'}
                       else (17 if x in {'河川地及び湖沼','河川湖沼','海浜','海水域'}
                             else 20) ) ) ) ) )
                ,df.landtype)
''' Add column for landcategory '''
addList = list(landCat)
df2 = df.assign(landCategory=addList)

df2 = df2[['5k_mesh','landtype','landCategory','modis05','modis10','modis12','modis13','modis14','modis17','geometry']]

# DataFrameをshapeファイル形式で出力
os.chdir("../../Output/Shape")
df2.to_file(filename=r'土地利用d01_5km区分.shp', driver='ESRI Shapefile', encoding='utf-8')

# ----- 10 ------ 20 ------ 30 ------ 40 ------ 50 ------ 60 ------ 70 ------ 80
shutil.rmtree(dir1+dir2)
