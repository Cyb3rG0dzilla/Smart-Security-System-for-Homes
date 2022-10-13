import cv2
import numpy as np
from sklearn.metrics import pairwise


accumulated_weight = 0.5
roi_top = 20
roi_bottom = 300
roi_right = 300
roi_left = 600
shift = (roi_right, roi_top)


def calc_accum_avg(frame, background):    
    # Initialize background with a copy of frame
    if background is None:
        return frame.copy()

    # smooth background is the compute weighted average of consecutive background frames
    cv2.accumulateWeighted(frame, background.astype("float"), accumulated_weight)
    return background
    

def segment(frame, background, threshold=25):
    # Absolute Difference between the backgroud and frame increases focus on hand
    diff = cv2.absdiff(background, frame)

    # preprocessing image
    _ , thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        return None
    else:
        # the external contour with largest area should be the hand
        hand_segment = max(contours, key=cv2.contourArea)
        return (thresh, hand_segment)
        

def count_fingers(thresh, hand_segment):
    conv_hull = cv2.convexHull(hand_segment)
    
    top    = tuple(conv_hull[conv_hull[:, :, 1].argmin()][0])
    bottom = tuple(conv_hull[conv_hull[:, :, 1].argmax()][0])
    left   = tuple(conv_hull[conv_hull[:, :, 0].argmin()][0])
    right  = tuple(conv_hull[conv_hull[:, :, 0].argmax()][0])

    # finding center of hand (cX,cY) and mid of palm (cX,cY1)
    cX = (left[0] + right[0]) // 2
    cY = (top[1] + bottom[1]) // 2
    cY1 = (cY + bottom[1]) // 2
    
    # activity - draw convex-hull contours on image frame and check several group of contours around fingertips and wrist
    # consider one approx contour from every closely grouped contours
    peri=cv2.arcLength(conv_hull,True)
    approx=cv2.approxPolyDP(conv_hull,0.02*peri,True)

    # consider only the contours above the center of palm
    # this may not exactly point to the fingertips every time
    fingerTips=[]
    for pt in approx:
        x,y=pt[0]
        if y<cY1:
            fingerTips.append((x,y))

    # Now lets count fingers
    # create a circle around hand and overlap it upon hand threshold
    # the intersections on circle indicate fingers above the wrist
    distance = pairwise.euclidean_distances([(cX, cY)], Y=[left, right, top, bottom])[0]
    max_distance = distance.max()
    radius = int(0.9 * max_distance)
    circumference = (2 * np.pi * radius)
    circular_roi = np.zeros(thresh.shape[:2], dtype="uint8")
    res=cv2.circle(circular_roi, (cX, cY), radius, 255, 10)
    circular_roi = cv2.bitwise_and(thresh, thresh, mask=circular_roi)
    contours, hierarchy = cv2.findContours(circular_roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    count = 0
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)

        # Increment count of fingers based on two conditions:

        # 1. Contour region is above hand area (the wrist)
        out_of_wrist = ((cY + (cY * 0.25)) > (y + h))

        # 2. Number of points along the contour does not exceed 25% of the circumference of the circular ROI (otherwise we're counting points off the hand)
        limit_points = ((circumference * 0.25) > cnt.shape[0])

        if  out_of_wrist and limit_points:
            count += 1

    return (count, fingerTips, (cX,cY1))


def real_time_feed():
    background = None
    cam = cv2.VideoCapture(0)
    num_frames = 0
    while True:
        num_frames += 1
        ret, frame = cam.read()
        # flip the frame so that it is not the mirror view
        frame = cv2.flip(frame, 1)
        frame_copy = frame.copy()
        fingerTips = []
        roi = frame[roi_top:roi_bottom, roi_right:roi_left]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
    
        # Get an average background from the first 30 frames
        # the user is notified while this is happening
        if num_frames <= 60:
            background = calc_accum_avg(gray, background)
            if num_frames <= 60:
                cv2.putText(frame_copy, "WAIT! GETTING BACKGROUND AVG.", (200, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                cv2.imshow("Finger Count",frame_copy)
    
        else:
            # segment the hand region
            hand = segment(gray, background)

            if hand is not None:
                thresholded, hand_segment = hand
                res=cv2.drawContours(frame_copy, [hand_segment + (roi_right, roi_top)], -1, (255, 0, 0),1)
                fingers, fingerTips, centrePt = count_fingers(thresholded, hand_segment)
                centrePt = tuple(map(sum,zip(centrePt,shift)))
                cv2.putText(frame_copy, "Count = "+str(fingers), (100, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
                cv2.imshow("Thresholded", thresholded)
        res=cv2.rectangle(frame_copy, (roi_left, roi_top), (roi_right, roi_bottom), (0,0,255), 5)
        for tip in fingerTips:
            tip=tuple(map(sum,zip(tip,shift)))
            res=cv2.line(frame_copy, tip, centrePt, (0,0,255), 2)
        cv2.imshow("Finger Count", frame_copy)
        k = cv2.waitKey(1) & 0xFF
        # Close windows with Esc
        if k == 27:
            break
  
    cam.release()
    cv2.destroyAllWindows()


def check_gesture(bgPath, imagePath):
    background = cv2.imread(bgPath)
    grayBackground=cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
    grayBackground=cv2.GaussianBlur(grayBackground, (5, 5), 0)
    image = cv2.imread(imagePath)
    gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray, (5, 5), 0)
    hand = segment(gray, grayBackground)
    if hand is not None:
        thresh, hand_segment = hand
        res=cv2.drawContours(image, hand_segment, -1, (255, 0, 0), 1)
        fingers, fingerTips, centrePt = count_fingers(thresh, hand_segment)
        centrePt = tuple(map(sum,zip(centrePt,shift)))
        cv2.putText(image, "Count = "+str(fingers), (70, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        cv2.imshow("Thresholded", thresh)
    for tip in fingerTips:
        tip=tuple(map(sum,zip(tip,shift)))
        res=cv2.line(image, tip, centrePt, (0,0,255), 2)
    cv2.imshow("Finger Count", image)
    key=cv2.waitKey(0) & 0xFF
    cv2.destroyAllWindows()
