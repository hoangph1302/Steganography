from PIL import Image
import numpy as np
import cv2

import math

QUANTIZATION_TABLE = np.array([
[16, 12, 14, 14, 18, 24, 49, 72],
[11, 12, 13, 17, 22, 35, 64, 92],
[10, 14, 16, 22, 37, 55, 78, 95],
[16, 19, 24, 29, 56, 64, 87, 98],

[24, 26, 40, 51, 68, 81, 103, 112],
[40, 58, 57, 87, 109, 104, 121, 100],
[51, 60, 69, 80, 103, 113, 120, 103],
[61, 55, 56, 62, 77, 92, 101, 99]
])

def ConvertStringToBinary(string):
    binary= ''
    for i in string:
        binary+=(format(ord(i), '08b'))
    return binary

def ConvertBinarryToString(binary):
    string = ""
    for i in range(0,len(binary),8):
        integer = int(binary[i:i+8], 2)
        character = chr(integer)
        string += character
    return string

def ConvertDecimalToBinary(number):
    binary=[]
    binray= "{0:016b}".format(number)
    return binray

def ConvertBinaryToDecimal(binary):
    dec=int(binary, 2)
    return dec


def ConvertDataToList(data,lenght):
    dataList=[]
    for i in range(0,lenght):
        dataList+=list(data[i])
    return dataList

def breakImageIntoBlocks(data,lenghtMessage):
    blocks=[]
    blocks=np.reshape(data,(lenghtMessage,8,8))
    blocks = np.float32(blocks)
    blockDCT=[]
    for i in range(0,lenghtMessage):
        blockDCT.append(cv2.dct(blocks[i]))

    blockDCT=np.asarray(blockDCT)  
    blocksQuantized=[]
    for i in range(0,lenghtMessage):
        blocksQuantized.append(np.divide(blockDCT[i],QUANTIZATION_TABLE))
    blocksQuantized=np.asarray(blocksQuantized)
  
    return blocksQuantized
    

def retrievingImage(blocks,lenghtMessage):
    blocksMultiply=[]
    for i in range(0,lenghtMessage):
        blocksMultiply.append(np.multiply(blocks[i],QUANTIZATION_TABLE))
    
    blocksInverseDCT=[]

    for i in range(0,lenghtMessage):
        blocksInverseDCT.append(np.uint8(np.round(cv2.idct(blocksMultiply[i]))))
   
    blocksInverseDCT=np.around(blocksInverseDCT).ravel()   
    dataImage=list(np.uint8(blocksInverseDCT)) 
    return dataImage

def ModifyData(data,message,index):
    
    lenghtMessageBin=ConvertDecimalToBinary(len(message))

    for i in range(0,16):
        if(lenghtMessageBin[i]=='0'):
          if(data[i]%2==1):
            data[i]=data[i]-1
        else:
            if(data[i]%2==0):
                data[i]=data[i]+1

    messageBinary=ConvertStringToBinary(message)
    dataBlock=data[17:(17+64*3*len(messageBinary)):3]
    
    blocksQuantized=breakImageIntoBlocks(dataBlock,len(messageBinary))
    for i in range(0,len(messageBinary)):
        if(messageBinary[i]=='0'):
            if(np.round(blocksQuantized[i][index[0]][index[1]])%2==1):
                blocksQuantized[i][index[0]][index[1]]=np.round(blocksQuantized[i][index[0]][index[1]])
                blocksQuantized[i][index[0]][index[1]]-=1
        else:
           if(np.round(blocksQuantized[i][index[0]][index[1]])%2==0):
                blocksQuantized[i][index[0]][index[1]]=np.round(blocksQuantized[i][index[0]][index[1]])
                blocksQuantized[i][index[0]][index[1]]+=1 
    dataBlockInverseDCT=retrievingImage(blocksQuantized,len(messageBinary))
    j=0
    for i in range (17,17+64*3*len(messageBinary),3):
        data[i]=dataBlockInverseDCT[j]
        j+=1
       
    return data


def ReadData(data,index):
    
    lengtMessageBinary=''
    for i in range(0,16):
        if(data[i]%2==0):
            lengtMessageBinary+='0'
        else:
            lengtMessageBinary+='1'
    lenghtMessage=ConvertBinaryToDecimal(lengtMessageBinary)
    message=''

    dataBlock=data[17:(17+64*3*lenghtMessage*8):3]
    
    blocksQuantized=breakImageIntoBlocks(dataBlock,lenghtMessage*8)

    for i in range(0,lenghtMessage*8):
        if(np.round(blocksQuantized[i][index[0]][index[1]])%2==0):
            message+='0'
        else:
            message+='1'

    return message


def Encryto(fileImage,message,index):
    image=Image.open(fileImage,'r')
    newImage=image.copy()
    width,height=newImage.size
    data=ConvertDataToList(list(newImage.getdata()),height*width)
    data=ModifyData(data,message,index)
    dataImage=[]
    for j in range(0,height*width*3,3):
        dataImage.append(tuple(data[j:j+3]))
    newImage.putdata(dataImage)
    newImage.save('output.bmp')
    image.close()
    newImage.close()

def Decrypto(fileImage,index):
    image=Image.open(fileImage,'r')
    width,height =image.size
    data=ConvertDataToList(list(image.getdata()),height*width)
    message=ConvertBinarryToString(ReadData(data,index))
    file_secret = open('SecretText.txt',mode = 'w',encoding='UTF-8')
    file_secret.write(message)
    file_secret.close()
    image.close()

def PSNR(image1,image2):
    imageAfer=Image.open(image1,'r')
    imageBefor=Image.open(image2,'r')
    width,height=imageAfer.size
    dataAfter=ConvertDataToList(list(imageAfer.getdata()),height*width)
    dataBefor=ConvertDataToList(list(imageBefor.getdata()),height*width)
    sum=0
    for i in range(0,len(dataAfter)):
        sum+=math.pow((dataAfter[i]-dataBefor[i]),2)
    MSE=sum/(width*height)
    RMSE=math.sqrt(MSE)
    PSNR=10*math.log((255*255/MSE),10)
    result=[RMSE,PSNR]
    return result

    Decrypto(input('Enter file image!\n'))


 ##---------------------------------------main programme-----------------------------------------------------------------
print('-------------------------Steganography DCT--------------------------------------')
print ('1.steganography'+'\n'+'2.Find secret text from image \n'+'3.RMSE and PSNR\n')
option=int(input())
if(option==1):
    image=input('Enter file image!\n')
    message=input('Enter secret text!\n')
    index=[]
    index.append(int(input('Enter index of coefficient!\n')))
    index.append(int(input()))
    Encryto(image,message,index)
elif( option==2):
    image=input('Enter file image!\n')
    index=[]
    index.append(int(input('Enter index of coefficient!\n')))
    index.append(int(input()))
    Decrypto(image,index)
    print ('Please Open file SecretText!')
elif(option==3):
    result=PSNR('input.bmp','output.bmp')
    print('RMSE: ',result[0])
    print ('PSNR: ',result[1])
    
