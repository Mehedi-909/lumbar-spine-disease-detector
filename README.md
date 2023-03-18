<h2> Project Description </h2>
 This tool will be able to detect abnormalities and predict the severity of disease in lumbar vertebrae by using localization and segmentation approaches. The lumbar is a very vital part of our body for load transferring and mobility. Vertebrae localization and segmentation are useful in detecting spinal deformities and fractures. Understanding of automated medical imagery is of main importance to help doctors in handling the time-consuming manual or semi-manual diagnosis. Manual observation of these vertebrae often takes much time and sometimes causes human error to diagnose the disease at early stages due to lack of expertise and proper observation. This tool will be able to analyze Magnetic Resonance Imaging (MRI) reports of a patient, calculate the features needed and come to a decision whether the lumbar spine is in normal state or not. It is  hoped that this tool will be helpful to diagnose deformities at an early stage. This will be beneficial both for patients and new trainee doctors to learn and make further decisions.

<h2> Article Reference </h2>
https://www.mdpi.com/1424-8220/22/4/1547 </br>
https://www.sciencedirect.com/science/article/abs/pii/S1746809421008272 

<h2> Dataset Reference </h2>
https://data.mendeley.com/datasets/k3b363f3vz/2 </br>

<h2> Labelled Dataset by Me </h2>
https://app.roboflow.com/university-of-dhaka-ghmd0/segmentation-95qui/5/images/?split=train

<h2> The steps followed: </h2>

![spl32 drawio](https://user-images.githubusercontent.com/46414380/226093429-baebc683-bbf9-4fc1-a730-cb30a7fddd12.png)

![sp31 drawio](https://user-images.githubusercontent.com/46414380/226093444-c97c978d-8c72-40fb-8efd-dd6ee4f79c2a.png)


<h2> Training Result </h2>

![results](https://user-images.githubusercontent.com/46414380/226090927-349d410f-686d-47f3-86e3-daf57019c872.png)

![confusion_matrix](https://user-images.githubusercontent.com/46414380/226090950-e5d922ae-8944-45fe-876e-1a6d70a37f16.png)


<h2> Here are the steps to use the application. </h2>

 Step 1: Upload an MRI image of lumbar sagital disc 

![Capture4](https://user-images.githubusercontent.com/46414380/216777666-b9bf84d2-78c2-41f1-9546-e030b8d5e77a.PNG)


  Output 1: Localized Discs 
![Capture](https://user-images.githubusercontent.com/46414380/216777686-1bd898bd-08eb-4719-a566-c1a9da99a9d5.PNG)


 Output 2: Localized centroids, angles and area </h3> 
 ![Capture2](https://user-images.githubusercontent.com/46414380/216777706-d2942ab2-6101-4b43-a23f-07f67ca1c234.PNG)


  Output 3: Corner points 
  ![Capture3](https://user-images.githubusercontent.com/46414380/216777721-4bce13a3-d712-4375-b178-35858614d30f.PNG)


  Output 4: Patient's report 
![8](https://user-images.githubusercontent.com/46414380/215284146-2f3c5831-bd16-4068-9572-0be78d49717e.PNG)
