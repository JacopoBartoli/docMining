# !!! Need to change this file.
def run():
    out = open('./icdar_train.txt', "w+")
    for i in range(0, 159):
        if i >= 100:
            out.write('./ICDAR_Darknet_format/images/POD_0'+str(i)+'.jpg'+'\n')
        elif i >= 10:
            out.write('./ICDAR_Darknet_format/images/POD_00'+str(i)+'.jpg'+'\n')
        elif i < 10:
            out.write('./ICDAR_Darknet_format/images/POD_000'+str(i)+'jpg'+'\n')
    out.close()

if __name__=='__main__':
    run()