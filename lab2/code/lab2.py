from PIL import Image
import math

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

def ModifyData(data,message):
    lenghtMessageBin=ConvertDecimalToBinary(len(message))
    for i in range(0,16):
        if(lenghtMessageBin[i]=='0'):
          if(data[i]%2==1):
            data[i]=data[i]-1
        else:
            if(data[i]%2==0):
                data[i]=data[i]+1

    messageBinary=ConvertStringToBinary(message)
    for i in range(0,len(messageBinary)):
        if(messageBinary[i]=='0'):
            if(data[i+16]%2==1):
                data[i+16]=data[i+16]-1
        else:
            if(data[i+16]%2==0):
                data[i+16]=data[i+16]+1
    return data


def ReadData(data):
    lengtMessageBinary=''
    for i in range(0,16):
        if(data[i]%2==0):
            lengtMessageBinary+='0'
        else:
            lengtMessageBinary+='1'
    lenghtMessage=ConvertBinaryToDecimal(lengtMessageBinary)
    message=''
    for i in range(16,16+lenghtMessage*8):
        if(data[i]%2==0):
            message+='0'
        else:
            message+='1'

    return message


def Encryto(fileImage,message):
    image=Image.open(fileImage,'r')
    newImage=image.copy()
    width,height=newImage.size
    data=ConvertDataToList(list(newImage.getdata()),height*width)

    data=ModifyData(data,message)


    dataImage=[]
    for j in range(0,height*width*3,3):
        dataImage.append(tuple(data[j:j+3]))
    newImage.putdata(dataImage)
    newImage.save('output.bmp')
    image.close()
    newImage.close()

def Decrypto(fileImage):
    image=Image.open(fileImage,'r')
    width,height =image.size
    data=ConvertDataToList(list(image.getdata()),height*width)
    message=ConvertBinarryToString(ReadData(data))
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
    PSNR=10*math.log((255*255/MSE),10)
    return PSNR
def Attack(fileImage):
    image=Image.open(fileImage,'r')
    newImage=image.copy()
    width,height=newImage.size
    data=ConvertDataToList(list(newImage.getdata()),height*width)
    for i in range(0,len(data)):
        if(data[i]%2==0):
            data[i]=0
        else: data[i]=255

    dataImage=[]
    for j in range(0,height*width*3,3):
        dataImage.append(tuple(data[j:j+3]))
    newImage.putdata(dataImage)
    newImage.save('attack.bmp')
    image.close()
    newImage.close()


 ##---------------------------------------main programme-----------------------------------------------------------------
print('-------------------------Steganography LSB--------------------------------------')
print ('1.steganography'+'\n'+'2.Find secret text from image \n'+'3.PSNR\n'+'4.Attack')
option=int(input())
if(option==1):
     image=input('Enter file image!\n')
     message=input('Enter secret text!\n')
     Encryto(image,message)
elif( option==2):
     Decrypto(input('Enter file image!\n'))
     print ('Please Open file SecretText!')
elif(option==3):
    print ('PSNR:')
    print (PSNR('input.bmp','output.bmp'))
elif(option==4):
    Attack(input('Enter file image!\n'))