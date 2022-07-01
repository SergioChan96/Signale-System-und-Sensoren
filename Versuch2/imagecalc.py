import numpy as np
import cv2
import copy

IMAGE = "./Versuch2/image.jpg"
# name, x, y
SCALE = [("black", 0, 0), ("dark grey", 125, 0), ("middle gray", 265, 0), ("light gray", 405, 0), ("white", 565, 0)]
# use to crop
SCALEWIDTH = 100
SCALEHEIGHT = 479

def read_img(img_path):
    return cv2.imread(img_path)


def sliceGrayPicture():
    greyImages = []
    imgSlices = []
    for i in range(10):
        image = read_img(f"./Versuch2/opencv_frame_{i}.png")
        greyimg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        greyImages.append(greyimg)
    for col in SCALE:
        for img in greyImages:
            cropimg = img[col[2]:col[2] + SCALEHEIGHT, col[1]:col[1] + SCALEWIDTH]
            imgSlices.append(cropimg)

    averages = []
    std = []
    for img in imgSlices:
        averages.append(np.average(img))
        std.append(np.std(img))

    for i in range(10 * 5):
        if (i % 10 == 0):
            print(f"av: {averages[i]}, std: {std[i]}")

def getAvgBlackImg():
    blackImgs = []
    for i in range(10):
        image = read_img(f"./Versuch2/opencv_black_{i}.png")
        blackimg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blackImgs.append(blackimg)
    avgBlackImg = copy.deepcopy(blackImgs[0])
    for i in range(len(blackImgs[0])):
        for j in range(len(blackImgs[0][i])):
            sum = 0
            for img in blackImgs:
                sum += float(img[i][j])
            avgBlackImg[i][j] = sum / len(blackImgs)

    return avgBlackImg


def getAvgWhiteImg():
    whiteImgs = []
    for i in range(1,11):
        image = read_img(f"./Versuch2/opencv_white_{i}.png")
        whiteimg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        whiteImgs.append(whiteimg)
    avgWhiteImg = copy.deepcopy(whiteImgs[1])
    for i in range(len(whiteImgs[0])):
        for j in range(len(whiteImgs[0][i])):
            sum = 0.0
            for img in whiteImgs:
                sum += float(img[i][j])
            avgWhiteImg[i][j] = sum / len(whiteImgs)
    avgBlackImg = getAvgBlackImg()
    for i in range(len(avgWhiteImg)):
        for j in range(len(avgWhiteImg[i])):
            avgWhiteImg[i][j] = avgWhiteImg[i][j] - avgBlackImg[i][j]

    return avgWhiteImg




def normieren(weissbild):
    whiteImgMean = np.mean(weissbild)
    weissbild = weissbild / whiteImgMean
    return weissbild

def capture_img():
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    img_counter = 0
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
       # cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            img_name = "opencv_white_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            read_img(f"opencv_white_{img_counter}.png")
            print("{} written!".format(img_name))
            img_counter += 1

    cam.release()

    cv2.destroyAllWindows()

def correctImage(inputImage):
    blackImg = getAvgBlackImg()
    corrcetionImg = getAvgBlackImg()
    for i in np.arange(len(inputImage)):
        for j in np.arange(len(inputImage[i])):
            corrcetionImg[i][j] = inputImage[i][j] - blackImg[i][j]
    whiteImg = getAvgWhiteImg()
    whiteImg = normieren(whiteImg)
    for i in np.arange(len(inputImage)):
        for j in np.arange(len(inputImage[i])):
            if (whiteImg[i][j] == 0):
                print(f"{i},{j}")
            corrcetionImg[i][j] = inputImage[i][j] / whiteImg[i][j]

    return corrcetionImg

def showWhiteBlackImg():
    avgBlackImg = getAvgBlackImg()
    avgBlackImg  = avgBlackImg - avgBlackImg.min()
    cv2.imshow("kontrastmaximiert schwarz",avgBlackImg / avgBlackImg.max())
    cv2.waitKey(0)
    avgWhiteImg = getAvgWhiteImg()
    avgWhiteImg = avgWhiteImg - avgWhiteImg.min()
    cv2.imshow("kontrastmaximiert weiss",avgWhiteImg / avgWhiteImg.max())
    cv2.waitKey(0)

def correctGreyImg():
    image = read_img(f"./Versuch2/opencv_frame_0.png")
    greyimg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    greyimg = correctImage(greyimg)
    cv2.imshow("correctet gray image",greyimg)
    cv2.waitKey(0)
    print("start of slicing")
    imgSlices = []
    for col in SCALE:
        cropimg = greyimg[col[2]:col[2] + SCALEHEIGHT, col[1]:col[1] + SCALEWIDTH]
        imgSlices.append(cropimg)
    for img in imgSlices:
        print(f"av: {np.average(img)}, std: {np.std(img)}")

    #for i in range(len(greyImgs)):
        #cv2.imwrite(f"corrected_greyimage_{i}.png", greyImgs[i])

def detectStuckDeadPixel():
    blackImage = getAvgBlackImg()
    for i in np.arange(len(blackImage)):
        for j in np.arange(len(blackImage[i])):
            if blackImage[i][j] > 20:
                print(f"black image dead pixel at i: {i} j:{j}")
    whiteImage = getAvgWhiteImg()
    for i in np.arange(len(whiteImage)):
        for j in np.arange(len(whiteImage[i])):
            if whiteImage[i][j] == 0:
                print(f"white image dead pixel at i: {i} j:{j}")


def main():
    sliceGrayPicture()
    showWhiteBlackImg()
    detectStuckDeadPixel()
    correctGreyImg()


if __name__ == "__main__": main()
