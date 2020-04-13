from os.path import getsize
size_before=getsize('orginal_document.txt')
size_after=getsize('output.txt')
print(f'size before steganography:{size_before}')
print(f'size after steganography: {size_after}')
