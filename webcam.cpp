#include <opencv/cv.h>
#include <opencv/highgui.h>
#include <iostream>
 
int main(int argc, char *argv[])
{
    cv::VideoCapture capture(0);
 
    if( !capture.isOpened() ) {
        std::cerr << "Could not open camera" << std::endl;
        return 0;
    }
 
    cv::namedWindow("cam",1);
 
    while (true) {
        bool frame_valid = true;
 
        cv::Mat frame;
 
        try {
            capture >> frame; // get a new frame from webcam
        } catch(cv::Exception& e) {
            std::cerr << "Exception occurred. Ignoring frame... " << e.err
                      << std::endl;
            frame_valid = false;
        }
 
        if (frame_valid) {
            try {
 
                /*
                 * use 'frame' object for some vision tasks.
                 *
                 */
                cv::imshow("cam", frame);
 
            } catch(cv::Exception& e) {
                std::cerr << "Exception occurred. Ignoring frame... " << e.err
                          << std::endl;
            }
        }
        if (cv::waitKey(30) >= 0) break;
    }


    // VideoCapture automatically deallocate camera object
    return 0;
}

