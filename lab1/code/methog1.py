def ChangeLetterToBinnary(letter):
    binary=''
    binary = '{0:08b}'.format(ord(letter)-1040) 
    return binary


# transform string text to binary
def ChangeToBinary(text):
    binary = ''
    for i in range(len(text)):
        binary = binary + ChangeLetterToBinnary(text[i])
    return binary

# transform binary to string text
def ChangetoString(text):
    result = ''
    for i in range(len(text)//8):
        a = text[i*8:(i+1)*8] # every symbol using a 8bit-encode
        b = int(a,2)
        result += chr(b+1040)
    return result


def steganography(text,data):
    binary = list(ChangeToBinary(text))
    data = list(data)
    index = -1
    for i in range(len(binary)):
        if binary[i] == '0':
            index = data.index('с',index+1) # find index of symbol c in russian
            data[index] = 'c'               # change to c in english
        elif binary[i] == '1':
            index = data.index('р',index+1) # find index of symbol p in russian
            data[index] =  'p'              # change to p in english
    return ''.join(data) 


def findSecretText(data):
    result = ''
    index = -1
    while True:
        index_c = data.find('c',index+1)
        index_p = data.find('p',index+1)
        if (index_c == -1) and (index_p == -1): break
        if ((index_c < index_p) and (index_c != -1))or(index_p == -1):
            index = index_c
            result += '0'  # add bit 0 to result
        elif index_p != -1:
            index = index_p
            result += '1'  # add bit 1 to result
    return ChangetoString(result)
# ---------------------------------main programme--------------------------#

option = int(input('1.steganography \n2.find secret text\n'))
if option==1:
    file_in = open('orginal_document.txt',mode = 'r',encoding='UTF-8')
    file_out = open('output.txt',mode = 'w',encoding='UTF-8')
    data = file_in.read() # read data from orginal_document
    text = input('please enter secret text \n') # input the text, that we must encode 
    cipher_text = steganography(text,data)
    file_out.write(cipher_text)
    print('please open file output.txt!')
    file_in.close()
    file_out.close()
elif option==2:
    file_encode = open('output.txt',mode = 'r',encoding='UTF-8')
    data = file_encode.read()
    file_secret = open('SecretText.txt',mode = 'w',encoding='UTF-8')
    text_secret=findSecretText(data)
    file_secret.write(text_secret)
    print('Please open file SecretText.txt\n')
    file_secret.close()
    file_encode.close()


