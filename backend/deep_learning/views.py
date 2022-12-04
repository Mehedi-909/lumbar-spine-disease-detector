from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from deep_learning.segmentation.yolov5 import detect2
from fpdf import FPDF
from datetime import date
from shapely.geometry import Polygon
import json
import numpy as np
import pandas as pd
import cv2
import math
import statistics
from math import atan2, degrees, radians

gLLA = 0.00
gLSA = 0.00
# Create your views here.
def image_processing(request):
    return HttpResponse('Hello from deep learning')

def slopeCalculation(x1, y1, x2, y2):
    m = (y2-y1)/(x2-x1)
    #m = (324-(y2-y1))/(x2-x1)
    return m

def angleCalculation(slope1, slope2):
    slope = (slope1 - slope2) / (1 + slope1 * slope2)
    angle = np.arctan(abs(slope))
    return angle

def angleOf3Points(A, B, C):
    Ax, Ay = A[0]-B[0], A[1]-B[1]
    Cx, Cy = C[0]-B[0], C[1]-B[1]
    a = atan2(Ay, Ax)
    c = atan2(Cy, Cx)
    if a < 0: a += math.pi*2
    if c < 0: c += math.pi*2
    return (math.pi*2 + c - a) if a > c else (c - a)

def yolo(request):
    import subprocess
    import os
    import shutil
    # folder = 'media/result/'
    # for filename in os.listdir(folder):
    #     file_path = os.path.join(folder, filename)
    #     try:
    #         if os.path.isfile(file_path) or os.path.islink(file_path):
    #             os.unlink(file_path)
    #         elif os.path.isdir(file_path):
    #             shutil.rmtree(file_path)
    #     except Exception as e:
    #         print('Failed to delete %s. Reason: %s' % (file_path, e))
    fileObj=request.FILES['filePath']
    fs=FileSystemStorage()
    filePathName=fs.save(fileObj.name,fileObj)
    filePathName=fs.url(filePathName)
    #dirspot = os.getcwd()
    #print dirspot
    #file = dirspot + '/' + filePathName
    process = subprocess.run(["python", "deep_learning/segmentation/yolov5/detect2.py", "--save-crop", "--hide-labels", "--name=result", "--project=media/", "--weights", "deep_learning/segmentation/yolov5/best.pt", "--source", './'+filePathName], stdout=subprocess.PIPE)
    #hello
    #return HttpResponse('Hello from yolo')
    listOfImages=os.listdir('./media/result/crops/')
    # for i in listOfImages:
    #     x = re.search("^fileObj.name.*6$", i)
    #     if x:
    #         listOfImagesPath=['/media/result/crops/'+i]

    listOfImagesPath=['/media/result/crops/'+i for i in listOfImages]
    context={'filePathName':filePathName,'listOfImagesPath':listOfImagesPath}
    return render(request,'viewCrop.html',context)

def crop_image(request):
    import subprocess
    import os
    import shutil
    folder = 'media/'
    global angleList
    global meanAngle
    global sd
    global posterior
    global anterior


    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    fileObj=request.FILES['filePath']
    fs=FileSystemStorage()
    filePathName=fs.save(fileObj.name,fileObj)
    filePathName=fs.url(filePathName)
    
    process = subprocess.run(["python", "deep_learning/segmentation/yolov5/detect2.py", "--save-crop", "--hide-labels", "--save-txt", "--save-conf", "--name=result", "--project=media/", "--weights", "deep_learning/segmentation/yolov5/best.pt", "--source", './'+filePathName], stdout=subprocess.PIPE)
    #hello
    #return HttpResponse('Hello from yolo')
    markedImage=os.listdir('./media/result/')
    markedImagePath = []
    for i in markedImage:
        if os.path.isfile('./media/result/' +i):
            markedImagePath=['/media/result/'+ i ]
        elif os.path.isdir('./media/result/' +i):
            print(i)
            print("Is directory")
        else:
            print(i)
            print("Is nothing")

    listOfImages=os.listdir('./media/result/crops/')
    listOfImagesPath=['/media/result/crops/'+i for i in listOfImages]


    #methodology2..................................................
    df = pd.read_csv('./media/coordinates.csv')
    img = cv2.imread('./media/'+fileObj.name)
    
    centroid1 = ( int((df.iloc[0,2]+df.iloc[0,4])/2), int((df.iloc[0,3]+df.iloc[0,5])/2) )
    perpendicular1 = ( int((df.iloc[0,2]+df.iloc[0,4])/2), int((df.iloc[0,3]+df.iloc[0,5])/2) + 25 )

    centroid2 = ( int((df.iloc[1,2]+df.iloc[1,4])/2), int((df.iloc[1,3]+df.iloc[1,5])/2) )
    perpendicular2 = ( int((df.iloc[1,2]+df.iloc[1,4])/2), int((df.iloc[1,3]+df.iloc[1,5])/2) + 25 )

    centroid3 = ( int((df.iloc[2,2]+df.iloc[2,4])/2), int((df.iloc[2,3]+df.iloc[2,5])/2) )
    perpendicular3 = ( int((df.iloc[2,2]+df.iloc[2,4])/2), int((df.iloc[2,3]+df.iloc[2,5])/2) + 25 )

    centroid4 = ( int((df.iloc[3,2]+df.iloc[3,4])/2), int((df.iloc[3,3]+df.iloc[3,5])/2) )
    perpendicular4 = ( int((df.iloc[3,2]+df.iloc[3,4])/2), int((df.iloc[3,3]+df.iloc[3,5])/2) + 25 )

    centroid5 = ( int((df.iloc[4,2]+df.iloc[4,4])/2), int((df.iloc[4,3]+df.iloc[4,5])/2) )
    perpendicular5 = ( int((df.iloc[4,2]+df.iloc[4,4])/2), int((df.iloc[4,3]+df.iloc[4,5])/2) + 25 )

    centroid6 = ( int((df.iloc[5,2]+df.iloc[5,4])/2), int((df.iloc[5,3]+df.iloc[5,5])/2) )
    perpendicular6 = ( int((df.iloc[5,2]+df.iloc[5,4])/2), int((df.iloc[5,3]+df.iloc[5,5])/2) + 25 )


    centroidList = [centroid1, centroid2, centroid3, centroid4, centroid5, centroid6]
    centroidList = sorted(centroidList , key=lambda k: [k[1], k[0]])
    print(centroidList)

    perpendicularList = [perpendicular1, perpendicular2, perpendicular3, perpendicular4, perpendicular5, perpendicular6]
    perpendicularList = sorted(perpendicularList , key=lambda k: [k[1], k[0]])
    print(perpendicularList)

    centroid1 = centroidList[0]
    centroid2 = centroidList[1]
    centroid3 = centroidList[2]
    centroid4 = centroidList[3]
    centroid5 = centroidList[4]
    centroid6 = centroidList[5]

    perpendicular1 = perpendicularList[0]
    perpendicular2 = perpendicularList[1]
    perpendicular3 = perpendicularList[2]
    perpendicular4 = perpendicularList[3]
    perpendicular5 = perpendicularList[4]
    perpendicular6 = perpendicularList[5]

    angleL1 = angleOf3Points(centroid2,centroid1,perpendicular1)
    angleL2 = angleOf3Points(centroid3,centroid2,perpendicular2)
    angleL3 = angleOf3Points(centroid4,centroid3,perpendicular3)
    angleL4 = angleOf3Points(centroid5,centroid4,perpendicular4)
    angleL5 = angleOf3Points(centroid6,centroid5,perpendicular5)

    angleList = [angleL1, angleL2, angleL3, angleL4, angleL5]
    meanAngle = statistics.mean(angleList)
    sd = statistics.stdev(angleList)

    anterior = meanAngle + sd
    posterior = meanAngle - sd
    
    i=0
    print("Normal range: " + str(posterior) + " - " + str(anterior))
    for angle in angleList:
        i=i+1
        if angle > anterior:
            print("Anterior " + "dislocation of L"+str(i) + "\tAngle: "+ str(angle))
        elif angle < posterior:
            print("Posterior " + "dislocation of L"+str(i) + "\tAngle: "+ str(angle))
        elif angle < anterior and angle > posterior:
            print("Normal " + "position of L" +str(i) + "\tAngle: "+ str(angle))

    # Green color in BGR
    color = (0, 255, 0)
    colorR = (255, 0, 0)

    # Line thickness of 9 px
    thickness = 2

    # Using cv2.line() method
    # Draw a diagonal green line with thickness of 1 px
    line_imageL1 = cv2.line(img, centroid1, centroid2, color, thickness)
    line_imageL1 = cv2.line(line_imageL1, centroid1, perpendicular1, colorR, thickness)

    line_imageL1 = cv2.line(line_imageL1, centroid2, centroid3, color, thickness)
    line_imageL1 = cv2.line(line_imageL1, centroid2, perpendicular2, colorR, thickness)

    line_imageL1 = cv2.line(line_imageL1, centroid3, centroid4, color, thickness)
    line_imageL1 = cv2.line(line_imageL1, centroid3, perpendicular3, colorR, thickness)

    line_imageL1 = cv2.line(line_imageL1, centroid4, centroid5, color, thickness)
    line_imageL1 = cv2.line(line_imageL1, centroid4, perpendicular4, colorR, thickness)

    line_imageL1 = cv2.line(line_imageL1, centroid5, centroid6, color, thickness)
    line_imageL1 = cv2.line(line_imageL1, centroid5, perpendicular5, colorR, thickness)

    cv2.imwrite('./media/angleImage.png', line_imageL1)
    #angleImage = cv2.imread('./media/angleImage.png')
    angleImagePath = ['/media/angleImage.png']

    #area methodology.........................................
    img = cv2.imread('./media/'+fileObj.name)
    area_image = cv2.line(img, centroid1, centroid2, color, thickness)

    line_imageL1 = cv2.line(area_image, centroid2, centroid3, color, thickness)

    area_image = cv2.line(area_image, centroid3, centroid4, color, thickness)

    area_image = cv2.line(area_image, centroid4, centroid5, color, thickness)

    area_image = cv2.line(area_image, centroid5, centroid6, color, thickness)

    area_image = cv2.line(area_image, centroid6, centroid1, color, thickness)

    cv2.imwrite('./media/areaImage.png', line_imageL1)
    areaImagePath = ['/media/areaImage.png']

    context={'filePathName':filePathName,'listOfImagesPath':listOfImagesPath, 'markedImagePath':markedImagePath, 'angleImagePath':angleImagePath, 'areaImagePath':areaImagePath}

    if request.method == "POST":
        if 'count' in request.POST:
            count=request.POST['count']
            print("hello")
            print("count status ",count)
            return HttpResponse('Success')
    return render(request,'viewCrop.html',context)


def get_data(request):
    global degreeLLA
    global degreeLSA
    print(request)
    data = json.loads(request.body)
    # print(data)
    # print(data['l1'][0][1])
    
    # print('count', request.POST['count'])
    # if request.method == "POST":
    #     print('hae post')
    #     if 'count' in data:
    #         count=data['count']
    #         print("hello")
    #         print("count status ", count)
    #         return HttpResponse('Success')
    #     else:
    #         print('asheni')
    # return HttpResponse('Fail')
    l1x1 = data['l1'][0][0]
    l1y1 = data['l1'][0][1]
    l1x2 = data['l1'][1][0]
    l1y2 = data['l1'][1][1]

    l5x1 = data['l5'][0][0]
    l5y1 = data['l5'][0][1]
    l5x2 = data['l5'][1][0]
    l5y2 = data['l5'][1][1]

    s1x1 = data['s1'][0][0]
    s1y1= data['s1'][0][1]
    s1x2 = data['s1'][1][0]
    s1y2= data['s1'][1][1]

    #print(data)
    #print(s1y2)
    #slope calculation
    slopeL1 = slopeCalculation(l1x1,l1y1,l1x2,l1y2)
    slopeS1 = slopeCalculation(s1x1,s1y1,s1x2,s1y2)
    slopeL5 = slopeCalculation(l5x1,l5y1,l5x2,l5y2)

    angleLLA = angleCalculation(slopeL1, slopeS1)
    degreeLLA = math.degrees(angleLLA)
    gLLA = degreeLLA
    #print('LLA Angle')
    #print(degreeLLA)

    angleLSA = angleCalculation(slopeL5, slopeS1)
    degreeLSA = math.degrees(angleLSA)
    gLSA = degreeLSA
    #print('LSA Angle')
    #print(degreeLSA)

    

    #return render(request,'reportForm.html',context)
    return HttpResponse('Successfull')

def report(request):
    if request.method == "POST":
        #return HttpResponse('POST Success')
        #context={'degreeLLA':gLLA,'degreeLSA':gLSA}
        pname = request.POST.get("pname", "")
        age = request.POST.get("age", "")

        i=0
        range = "Normal range: " + str(posterior) + " - " + str(anterior)
        reportComment = []
        for angle in angleList:
            i=i+1
            if angle > anterior:
                #text = "Anterior " + "dislocation of L"+str(i) + "\tAngle: "+ str(angle)
                text = "L"+str(i) + "\t\t\t\t\t"+ str("{:.2f}".format(angle)) +"\t\t\t\t\tAnterior dislocation"
                reportComment.append(text)
            elif angle < posterior:
                text = "L"+str(i) + "\t\t\t\t\t"+ str("{:.2f}".format(angle)) +"\t\t\t\tPosterior dislocation"
                reportComment.append(text)
            elif angle < anterior and angle > posterior:
                text = "L"+str(i) + "\t\t\t\t\t"+ str("{:.2f}".format(angle)) +"\t\t\t\tNormal"
                reportComment.append(text)


        pdf = FPDF()
        pdf.add_page()
        # set font style and size for pdf
        pdf.set_font('Arial', size= 12)

        if degreeLLA < 39:
            commentLLA = "Hypolordosis"
        elif degreeLLA > 53:
            commentLLA = "Hyperlordosis"
        else:
            commentLLA = "Normal" 

        # creating cell
        pdf.cell(200, 10, txt = "Patient's Report", ln=2, align='C')
        pdf.cell(200, 10, txt = "\n\n", ln=2, align='L')
        #pdf.cell(200, 10 , txt = 'Date: '+ '09 dec', border = 0, ln = 0, align = 'L', fill = False, link = '')
        #pdf.cell(200, 10 , txt = 'Patient Name: '+ str(pname), border = 0, ln = 0, align = 'L', fill = False, link = '')
        #pdf.cell(200, 10 , txt = "Patient Age: "+ str(age), border = 0, ln = 0, align = 'L', fill = False, link = '')
        pdf.cell(200, 10, txt = "Date: "+ str(date.today()), ln=2, align='L')
        pdf.cell(200, 10, txt = "Patient's Name: " + str(pname), ln=2, align='L')
        pdf.cell(200, 10, txt = "Patient's Age: " + str(age), ln=2, align='L')
        pdf.cell(200, 10, txt = "\n\n", ln=2, align='L')
        pdf.cell(200, 10, txt = "LLA \t\t\t\t\t\tRemarks \t\t\t\t\t\tNormal Range", ln=2, align='L')
        pdf.cell(200, 10, txt = str("{:.2f}".format(degreeLLA)) + "\t\t\t\t\t\t\t\t\t" + commentLLA+ "\t\t\t\t\t\t\t\t\t39 - 53" , ln=2, align='L')
        #pdf.cell(200, 10, txt = "Lumsacral Angle: " + str(degreeLSA), ln=2, align='L')

        pdf.cell(200, 10, txt = "\n\n", ln=2, align='L')
        #pdf.cell(200, 10, txt = range, ln=2, align='L')
        textTitle = "Disc"+ "\t\t\tAngle: " +"\t\t\tRemarks"
        pdf.cell(200, 10, txt = textTitle, ln=2, align='L')
        for comment in reportComment:
            pdf.cell(200, 10, txt = comment, ln=2, align='L')
        pdf.cell(200, 10, txt = range, ln=2, align='L')
        # save file with extension
        pdf.output('./media/report.pdf')
        reportPath=['/media/report.pdf' ]


        context={'degreeLLA':degreeLLA,'degreeLSA':degreeLSA,'report':reportPath}
        return render(request,'reportForm.html',context)
    #return render(request,'reportForm.html')

def get_image(request):
    return render(request,'index.html')

def predictImage(request):
    import os
    #return render(request,'index.html')
    fileObj=request.FILES['filePath']
    fs=FileSystemStorage()
    filePathName=fs.save(fileObj.name,fileObj)
    filePathName=fs.url(filePathName)
    #context={'filePathName':filePathName}
    #return render(request,'index.html',context)
    #return HttpResponse('Hello from deep learning')

    
    listOfImages=os.listdir('./media/result/')
    listOfImagesPath=['/media/result/'+i for i in listOfImages]
    context={'filePathName':filePathName,'listOfImagesPath':listOfImagesPath}
    return render(request,'index.html',context)

def viewDataBase(request):
    import os
    listOfImages=os.listdir('./media/result/')
    listOfImagesPath=['/media/result/'+i for i in listOfImages]
    context={'listOfImagesPath':listOfImagesPath}
    return render(request,'viewCrop.html',context)
    