import cv2

# plays video while indicating frame number. Takes in video file as videopath.
def show_frames(videopath):
    vid = cv2.VideoCapture(videopath)
    count = 0
    
    if(not vid.isOpened()):
        print("Error opening file")
    
    while(vid.isOpened()):
        flag, img = vid.read()
        cv2.imshow('Frame', img)
        print("frame: " + str(count))
        
        # press 'q' to exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        count+=1
        
    vid.release()
    cv2.destroyAllWindows()

# creates images from specified frames in frame_list from a video videopath
def get_frames(videopath, frame_list):
    vid = cv2.VideoCapture(videopath)
    count = 0

    if(not vid.isOpened()):
        print("Error opening file")
    
    while(vid.isOpened()):
        flag, img = vid.read()
        if flag:
            if count in frame_list:
                cv2.imwrite("frame%d.jpg" % count, img)
        else:
            break
        count+=1
        
    vid.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    #show_frames("mov1.mp4")
    frame_nums = [30, 151, 202, 350, 557, 800, 974, 1200, 1300, 1605,
                 1800, 2077, 2333, 2598, 2700, 2900, 3100, 3462, 3820,
                 4100, 4300, 4500, 4601, 4838, 5175, 5339, 5600, 5800,
                 6159, 6402, 6651, 6948, 7297, 7451, 7630, 7694, 8000,
                 8262, 8400, 8683, 8855]  # selected frames
    get_frames("mov1.mp4", frame_nums)
