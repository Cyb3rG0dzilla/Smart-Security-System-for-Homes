import cv2
import glob


cascade = cv2.CascadeClassifier("../cascade/cascade.xml")

# test_path = "/home/nick/projects.python/boobs/pics/test/*.jpg"
# test_path = "/home/external/moderation-porn-detector/pornPornolab/*.jpg"
test_path = "/home/external/moderation-porn-detector/boobs-oboobs/*.jpg"
# test_path = "/home/external/moderation-porn-detector/user/*.jpg"

for img_file in glob.glob(test_path):
    image = cv2.imread(img_file, cv2.CV_LOAD_IMAGE_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    rects = cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    print "Found {0} faces in {1}".format(len(rects), img_file)

    if len(rects) > 0:
        for (x, y, w, h) in rects:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow("Rects found", image)
        cv2.waitKey(0)


cv2.destroyAllWindows()
