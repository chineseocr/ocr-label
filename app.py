# -*- coding: utf-8 -*-
"""
@author: wenlihaoyu
"""
import web
import time
import sys
import os
from PIL import Image
import json
from glob import glob
import traceback
from read_img import read_image_label,correct_image,set_image_status
from config import IMAGEPATH,correctpath,Nmax,timeOut,ocrAuto
if ocrAuto:
    ##是否自动调用OCR引擎进行纠偏
   from crnn.crnn_torch import crnnOcr
else:
     crnnOcr=None


imagefiles =glob(IMAGEPATH)##需要纠偏的图像
imageNum = len(imagefiles)
statusDict={}##每张图片的状态
timeDict={}##每张图片的完成时间，如果超过最大时间仍然未完成纠偏，那么重新放入纠偏池

def read_batch():
    data = []
    index = 0
    num = 0
    while True:
         p =imagefiles[index]
         status = statusDict.get(p,0)
         if status==1:
            ##纠偏中
             if time.time()-timeDict.get(p)>timeOut:
                 timeDict[p] = time.time()
                 line = read_image_label(p)
                 set_image_status(p,statusDict,status=1)
                 line['index'] =num
                 data.append(line)
                 num+=1
         elif status==0:
                 timeDict[p] = time.time()
                 line = read_image_label(p)
                 set_image_status(p,statusDict,status=1)
                 line['index'] =num
                 data.append(line)
                 num+=1
                
         index+=1
         if num == Nmax-1 or  index>imageNum-1:
                   break
    return data






class OCR:
    """
    调用OCR引擎
    """
    def POST(self):
        data = web.data()
        data = json.loads(data)
        path = data['path']
        im   = Image.open(path).convert('L')
        res  = ''
        if crnnOcr is not None:
            res  = crnnOcr(im)
        return res



class Label:
    
    def GET(self):  
        
        data =read_batch()
        if data !=[]:
            post = {'data':data,'labelUrl':'label','ocrUrl':'ocr'}
            return render.label(post)
        else:
            post = {'labelUrl':'label','ocrUrl':'ocr'}
            return render.label(post)

    def POST(self):
        """
        纠正图像中文字
        """
        data = web.data()
        try:
           data = json.loads(data)
           labelImageS = data.get('data')
           correct_image(labelImageS,correctpath,statusDict,status=2)
        except:
                   pass

        return ''

#指定模板目录，并设定公共模板
urls = (
        '/label', 'Label',
        '/ocr','OCR'
        )

app = web.application(urls, globals())

render = web.template.render('templates', base='base')
import json
if __name__ == '__main__':  
    app.run()  
