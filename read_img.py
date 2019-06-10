# -*- coding: utf-8 -*-
"""
@author: wenlihaoyu
"""
import json
import base64
from PIL import Image
import cv2
import  uuid
import os

def read_image_label(path):
    """
    read image and label
    """
    imageString = read_img(path)
    basename    = os.path.basename(path)
    txtpath     = path.replace(basename,basename.split('.')[0]+'.txt')
    label       = get_label(txtpath)
    return {'url':imageString,'label':label,'path':path}



def read_img(path,flag=True):
    try:
        f=open(path,'rb') #二进制方式打开图文件
        ls_f=base64.b64encode(f.read()) #读取文件内容，转换为base64编码
        f.close()
        return ls_f.decode('utf-8')
    except:
        
        return ''

def get_label(filetxt):
    """
    获取文本
    """
    try:
        with open(filetxt) as f:
            S = f.read()
    except:
       S=''
    return S.strip()


def set_image_status(path,statusDict,status=1):
    """
    1:纠偏中
    2:纠偏完成
    0:未纠偏
    """
    statusDict[path] =status

def correct_image(data,correctpath,statusDict,status=2):
    """
    写入完成纠偏的数据
    """
    if data!=[]:
        for i,lst in enumerate(data):
           imagepath = lst['path'].strip()
           label     = lst['text'].strip()
           flag     = lst['flag']##是否删除图像及标签
           path,filename =imagepath.split('/')[-2:]
           root = os.path.join(correctpath,path)
           if not os.path.exists(root):
               os.makedirs(root)
           
           img = Image.open(imagepath)
           imgP =os.path.join(root,filename)
           ##写入图像
           if not flag and label!='###':
               img.save(imgP)
               #cv2.imwrite(e,img)
               ##写入纠错文本
               basename    = os.path.basename(imgP)
               txtpath     = imgP.replace(basename,basename.split('.')[0]+'.txt')
               with open(txtpath,'w') as f:
                    f.write(label)
           set_image_status(imagepath,statusDict,status=status)
           os.remove(imagepath)
           if os.path.exists(imagepath.replace('.jpg','.txt')):
              os.remove(imagepath.replace('.jpg','.txt'))
                     
                     
                     
