## 环境配置，支持linux\macOs           
conda create -n chineseocr python=3.6 pip scipy numpy  ##运用conda 创建python环境      
source activate chineseocr      
pip install opencv-contrib-python==4.0.0.21  -i https://pypi.tuna.tsinghua.edu.cn/simple/        
pip install -U pillow -i https://pypi.tuna.tsinghua.edu.cn/simple/         
pip install web.py==0.40.dev0       
pip installl pytorch torchvision 


