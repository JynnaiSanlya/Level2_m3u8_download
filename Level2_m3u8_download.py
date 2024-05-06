# Level2_m3u8_download.py

import re
import os
import subprocess

# ts_path: 下载好的一堆ts文件的文件夹
# combine_path: 组合好的文件的存放位置
# file_name: 组合好的视频文件的文件名
# combine函数把文件列表读取并且合成为视频输出
def combine(ts_path, combine_path, file_name):
    # 调用file_walker函数获取文件夹中的文件并且按照指定方式列表输出
    file_list = file_walker(ts_path)
    print(file_list)
    # 设置合成后的视频输出内容
    file_path = combine_path + file_name + '.ts'
    # 读取列表信息合成视频并输出
    with open(file_path, 'wb+') as fw:
        for i in range(len(file_list)):
            fw.write(open(file_list[i], 'rb').read())
            print(i)
    print('合并完成')

def checkFileExist(filenameAbsolute):
    if not os.path.exists(filenameAbsolute):
        with open(filenameAbsolute, 'w'):
            pass

def downloadVideo(url_list,headers3,path,mp4name):
    for i in url_list:
        new_url = str(i).rsplit('/', 1)[0]  # 从右侧分割一次，取第一个部分
        print(new_url)
        m3u8_response = requests.get(i)
        m3u8_content = m3u8_response.text
        m3u82_compile=re.compile('chunklist_(.*?)m3u8')
        m3u82site=re.findall(m3u82_compile,m3u8_content)
        m3u82url=str(new_url)+'/'+'chunklist_'+str(m3u82site)[2:-2]+'m3u8'
        m3u82_response = requests.get(m3u82url)
        print('-----')
        #print(m3u82_content)
        ts_list = get_ts(m3u82url,headers3)
        print(ts_list)
        # 调用dow_ts下载视频到本地
        d = dow_ts(m3u82url,ts_list,path)
        # 合并所有的.ts为一个新的总ts
        tsFileName=str(path+'*.ts')
        newTsFileName=str(path+'new.ts')
        checkFileExist(newTsFileName)
        subprocess.call(['copy','/b',tsFileName,newTsFileName],shell=True)
        # 使用FFmpeg将所有.ts文件合并为一个MP4文件
        mp4FileName=str(path+mp4name+'.mp4')
        # Maybe unnecessary. If you uncomment this, you need to configure the behaviour of rewriting files.
        # checkFileExist(mp4FileName)
        subprocess.call(['ffmpeg','-i',newTsFileName,'-vcodec','copy','-acodec','copy', mp4FileName],shell=True)
        # 删除所有.ts,如果要保留.ts可以自行修改但是注意后续的重叠
        # subprocess.call(['cmd','rm',path+'*.ts'],shell=True)