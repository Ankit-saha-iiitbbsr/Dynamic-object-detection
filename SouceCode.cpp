#include <iostream>
#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/video.hpp>

using namespace std;
using namespace cv;

int main(int argc, char* argv[]) {     
    VideoCapture cap(argv[1]);    
    double* fps=new double; 
    *fps = cap.get(CAP_PROP_FPS);
    
    if (!cap.isOpened()) {
        cout << "Error opening video file" << endl;
        return -1;
    }

   VideoWriter writer("Hackathon_output2.mp4", VideoWriter::fourcc('M', 'J', 'P', 'G'), *fps, Size(cap.get(CAP_PROP_FRAME_WIDTH), cap.get(CAP_PROP_FRAME_HEIGHT)));

    Mat *image1=new Mat;
    Mat *image2=new Mat;
    
    int *frame_number = new int(0);
    double frame_count = cap.get(CAP_PROP_FRAME_COUNT);
    cap.set(CAP_PROP_POS_FRAMES, *frame_number);
    cap >> *image1;

    while (*frame_number <= frame_count) {
        int endFrame = *frame_number + 1;
        cap.set(CAP_PROP_POS_FRAMES, endFrame);
        cap >> *image2;

        if (!(*image2).empty()) {
            Mat *gotFrame=new Mat;
            Mat *frame1=new Mat;
            Mat *frame2=new Mat;
            cvtColor(*image1, *frame1, COLOR_BGR2GRAY);
            cvtColor(*image2, *frame2, COLOR_BGR2GRAY);
            absdiff(*frame1, *frame2, *gotFrame);

            Mat *thresh=new Mat;
            threshold(*gotFrame, *thresh, 0, 255, THRESH_BINARY | THRESH_OTSU);

            Mat *kernel=new Mat;
            *kernel = getStructuringElement(MORPH_RECT, Size(3, 3));
            Mat *dilate=new Mat;    
            dilate(*thresh, *dilate, kernel, Point(-1, -1), 2);

            vector<vector<Point>> contours;
            findContours((*dilate).clone(), contours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);

            Mat *contour_img= new Mat;
            *contour_img = (*image1).clone();
            drawContours(*contour_img, contours, -1, Scalar(0, 255, 0), 3);

            writer.write(*contour_img);   

            *frame_number++;
            *image1 = (*image2).clone();
            free(image2);   
            free(gotFrame);
            free(frame1);
            free(frame2);
            free(kernel);
            free(dilate);
            free(thresh);
            free(contour_img);

        } else {
            cout << "Image not found after frame number " << *frame_number << endl;
            break;
        }
    }

    writer.release();
    cap.release();
    delete fps;
    delete image1;
    return 0;
}
