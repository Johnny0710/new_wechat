import os
def qr_callback(uuid,status,qrcode):
    print(uuid)
    path = os.path.join(os.getcwd(),'qrcode','{}.png'.format(uuid))
    with open(path,'wb') as qrcode_file:
        qrcode_file.write(qrcode)