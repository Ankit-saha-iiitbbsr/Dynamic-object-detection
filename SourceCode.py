# Object Detection

import cv2
import imutils
import imageio
import numpy as np

print(cv2.__version__)

def cartoonise(frame):
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    blurred=cv2.GaussianBlur(src=gray, ksize=(3,5),sigmaX= 0.5)  
    edges=cv2.Canny(blurred, 70,135)
    edges=~edges
    edges=cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    dst=cv2.addWeighted(frame, 0.7, edges, 0.3, 0)
    print("OK")
    return dst
    

cap=cv2.VideoCapture("Hackathon.mp4")
fps=cap.get(cv2.CAP_PROP_FPS)

writer=imageio.get_writer("Hackathon_output2.mp4",fps=fps)
frame_count=cap.get(cv2.CAP_PROP_FRAME_COUNT) #Total no of frames
frame_number=0
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
success, image1=cap.read()


while success and frame_number<=frame_count:                                           

    endFrame=frame_number+1

    cap.set(cv2.CAP_PROP_POS_FRAMES, endFrame)  
    success, image2=cap.read()
    
    print(success)
    if success:
        img_height = image1.shape[0]
                
        frame1=cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
         
            
           
        frame2=cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY) 
        gotFrame=cv2.absdiff(frame1, frame2)
        cv2.imwrite("change.jpg",gotFrame)
        thresh = cv2.threshold(gotFrame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]   
        """cv2.imshow("Threshold", thresh)"""
                
        kernel = np.ones((3,3), np.uint8) 
        dilate = cv2.dilate(thresh, kernel, iterations=2) 
        #opened=cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel) 
        cv2.imwrite("Dilate.jpg", dilate)
        #cv2.imwrite("opened.jpg", opened)     
    
        contours = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        contours = imutils.grab_contours(contours)
        contour_img= cv2.drawContours(image1, contours, -1,( 0,255,0), 3) 
        
        writer.append_data(image1)
        frame_number+=1
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)  
        success, image1=cap.read() 
        
    else:
        print("Img not found after frame no " +  str(frame_number)) 
        break
     
writer.close()        

         
    
    
    
    
  