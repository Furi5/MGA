import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


def create_group_cla(df):
    label_1 = df[df.iloc[:, 1]==1]
    label_0 = df[df.iloc[:, 1]==0]
    print('num of label 1:',len(label_1), 'num of label 0:',len(label_0))
    
    label_1_train, label_1_test= train_test_split(label_1, test_size=0.2, shuffle=True)
    label_1_test, label_1_valid= train_test_split(label_1_test, test_size=0.5, shuffle=True)

    label_0_train, label_0_test= train_test_split(label_0, test_size=0.2, shuffle=True)
    label_0_test, label_0_valid= train_test_split(label_0_test, test_size=0.5, shuffle=True)
    
    train_set = pd.concat([label_1_train, label_0_train])
    train_set['group'] = 'training'
    
    test_set = pd.concat([label_1_test, label_0_test])
    test_set['group'] = 'test'
    
    valid_set = pd.concat([label_1_valid, label_0_valid])
    valid_set['group'] = 'valid'
    
    return pd.concat([train_set, test_set, valid_set])

def create_group_reg(df):
    df_train, df_test= train_test_split(df, test_size=0.2, shuffle=True)
    df_test, df_valid= train_test_split(df_train, test_size=0.5, shuffle=True)
    df_train['group'] = 'training'
    df_test['group'] = 'test'
    df_valid['group'] = 'valid'
    return pd.concat([df_train, df_test, df_valid])


def concat_df(task):
    df = pd.DataFrame()
    for file in os.listdir(f'data/tox_v1/{task}'):
        if file == '.DS_Store':
            continue
        print(f'#-----------------------{file} start!----------------------#')
        sub_df = pd.read_csv(f'data/tox_v1/{task}/{file}')
        col_name = file.split('.')[0]
        if file in ['LOAEL.csv', 'ROA_LD50.csv', 'MRTD.csv',
                    'BCF.csv','algae_pEC50.csv','crustaceans_pLC50.csv', 'fish_pLC50.csv', 'IBC50.csv', 'LC50DM.csv', 'LC50FM.csv',
                    ]:
            sub_df = create_group_reg(sub_df)
        else:
            sub_df = create_group_cla(sub_df)
            
        df = pd.concat([df, sub_df[['SMILES',col_name,'group']]])
    cols = []
    if task == 'Drug':
        print(df.columns)
        cols = [col for col in df.columns if col not in ['ROA_LD50', 'LOAEL', 'MRTD', 'group']]
        print(cols)
        cols += ['ROA_LD50', 'LOAEL', 'MRTD', 'group']
    elif task == 'Environments':
        cols = [col for col in df.columns if col not in ['BCF','algae_pEC50','crustaceans_pLC50', 'fish_pLC50', 'IBC50', 'LC50DM', 'LC50FM', 'group']]
        cols += ['BCF','algae_pEC50','crustaceans_pLC50', 'fish_pLC50', 'IBC50', 'LC50DM', 'LC50FM', 'group']

    else:
        cols = [col for col in df.columns if col != 'group']
        cols.append('group')
    print(cols)
    # 重新安排 DataFrame 的列顺序
    df = df.reindex(columns=cols)
    df.rename(columns={'SMILES': 'smiles'}, inplace=True)
    df.to_csv(f'data/tox_data_v1/{task}/{task}.csv', index=False)



def precess_clinical_data():
    df = pd.DataFrame()
    for file in os.listdir(f'data/tox_v1/Clinical'):
        print('###############', 'file:', file, '###############')
        if file == '.DS_Store':
            continue
        elif file == 'sider.csv':
            sider_df = pd.read_csv(f'data/tox_v1/Clinical/{file}')
            sider_col = sider_df.columns
            sider_col = [col for col in sider_col if col != 'group']
            for col in sider_col:
                if col not in ['SMILES']:
                    print('processing:', col)
                    sub_df = sider_df[['SMILES', col]]
                    sub_df = sub_df.dropna()
                    sub_df = create_group_cla(sub_df)
                    df = pd.concat([df, sub_df[['SMILES',col,'group']]])
        else:
            sub_df = pd.read_csv(f'data/tox_v1/Clinical/{file}')
            sub_df = create_group_cla(sub_df)
            col_name = file.split('.')[0]
            df = pd.concat([df, sub_df[['SMILES',col_name,'group']]])
    cols = [col for col in df.columns if col != 'group']
    cols.append('group')
    # 重新安排 DataFrame 的列顺序
    df = df.reindex(columns=cols)
    df.rename(columns={'SMILES': 'smiles'}, inplace=True)
    df.to_csv(f'data/tox_data_v1/Clinical/Clinical.csv', index=False)
    

if __name__ == '__main__':
    # tasks = ['Environments']
    # for task in tasks:
    #     concat_df(task)
    #     print(f'{task} dataset created!')
    # precess_clinical_data()