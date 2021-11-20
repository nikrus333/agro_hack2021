import cv2
import json

global count
def reverse_resize(data, scale_percent):
    mass = [[data[0][0] / (scale_percent / 100), data[0][1] / (scale_percent / 100)], [data[1][0] / (scale_percent / 100), data[1][1] / (scale_percent / 100)]]
    return mass

count = 0    
dot = (0, 0)
def draw_circle(event,x,y,flags,param):
    global count
    global dot
    if event == cv2.EVENT_LBUTTONDBLCLK:
        dot = (x, y)
        count+=1

rectangle_water_1 = [(154, 132), (192, 169)]
rectangle_water_2 = [(458, 111), (481, 151)]

rectangle_eat = [(207, 130), (416, 208)]
rectangle_wall = [(111, 130), (785, 700)]
cap = cv2.VideoCapture('train/Movie_3.mkv')
cap_test = cv2.VideoCapture('train/Movie_10.mkv')
count = 0
while(cap.isOpened()):
    try:
        ret, frame = cap.read()
        #ret_test, frame_test = cap_test.read()
        if ret == True:
            scale_percent = 50
        
            width = int(frame.shape[1] * scale_percent / 100)
            height = int(frame.shape[0] * scale_percent / 100)
        
            dim = (width, height)

            resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        
            cv2.namedWindow('resized')
            cv2.setMouseCallback('resized',draw_circle)
            if count == 1:
                rectangle_water_1[0] = dot
            if count == 2:
                rectangle_water_1[1] = dot
            if count == 3:
                rectangle_water_2[0] = dot
            if count == 4:
                rectangle_water_2[1] = dot
            if count == 5:
                rectangle_eat[0] = dot
            if count == 6:
                rectangle_eat[1] = dot
            
            #print(rectangle_eat / (scale_percent / 100))
            color1 = (255, 0, 0)
            color2 = (255, 255, 0)
            color3 = (0, 0, 255)
            thickness = 2
        
            frame = cv2.rectangle(resized, rectangle_water_1[0], rectangle_water_1[1], color1, thickness)
            frame = cv2.rectangle(resized, rectangle_water_2[0], rectangle_water_2[1], color1, thickness)
            frame = cv2.rectangle(resized, rectangle_eat[0], rectangle_eat[1], color2, thickness)
            frame = cv2.rectangle(resized, rectangle_wall[0], rectangle_wall[1], color3, thickness)

            # resized_test = cv2.resize(frame_test, dim, interpolation = cv2.INTER_AREA)
            # frame_test = cv2.rectangle(resized_test, rectangle_water_1[0], rectangle_water_1[1], color1, thickness)
            # frame_test = cv2.rectangle(resized_test, rectangle_water_2[0], rectangle_water_2[1], color1, thickness)
            # frame_test = cv2.rectangle(resized_test, rectangle_eat[0], rectangle_eat[1], color2, thickness)

            cv2.imshow('resized', frame)
            #cv2.imshow('test', frame_test)
            rectangle_water_1_old = reverse_resize(rectangle_water_1, 50)
            rectangle_water_2_old = reverse_resize(rectangle_water_2, 50)
            rectangle_eat_old = reverse_resize(rectangle_eat, 50)
            rectangle_wall_old= reverse_resize(rectangle_wall, 50)

            with open('data.json', 'w') as outfile:
                json.dump({
                "water_1":rectangle_water_1_old,
                "water_2":rectangle_water_2_old,
                "eat":rectangle_eat_old,
                "wall":rectangle_wall_old
                }, outfile)
    except Exception as e:
        print(e)
   
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

