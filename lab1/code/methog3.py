
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
            index = data.index('\n',index+1) # find index of endline
            data[index] = chr(127)+'\n'        # we add a special character (that don't show when we open document)      
        elif binary[i] == '1':
            index = data.index('\n',index+1) # find index of endline
            data[index] =  chr(8196)+'\n'              # we add a special character (that don't show when we open document)
    return ''.join(data) 

def finSecretText(data):
    result = ''
    index = -1
    while True:
        index1 = data.find( chr(127)+'\n',index+1)
        index2 = data.find(chr(8196)+'\n' ,index+1)
        if (index1 == -1) and (index2 == -1): break
        if ((index1 < index2) and (index1 != -1))or(index2 == -1):
            index = index1
            result += '0'  # add bit 0 to result
        elif index2 != -1:
            index = index2
            result += '1'  # add bit 1 to result
    return ChangetoString(result)
# ---------------------------------main programme--------------------------#
option = int(input('1.steganography\n2.find secret text\n'))
if option==1:
    file_in = open('orginal_document.txt',mode = 'r',encoding='UTF-8')
    file_out = open('output.txt',mode = 'w',encoding='UTF-8')
    data = file_in.read() # read data from container
    text = input('please enter secret text \n') # input the text, that we must encode 
    file_out.write( steganography(text,data))
    print('please open file output.txt!')
    file_in.close()
    file_out.close()
elif option==2:
    file_encode = open('output.txt',mode = 'r',encoding='UTF-8')
    data = file_encode.read()
    print('decode:')
    file_secret = open('SecretText.txt',mode = 'w',encoding='UTF-8')
    text_secret=finSecretText(data)
    file_secret.write(text_secret)
    print('Please open file SecretText.txt\n')
    file_secret.close()
    file_encode.close()


