import cv2
import numpy as np


class CVHelper:
    @staticmethod
    def roi(img_path):
        im = cv2.imread(img_path)

        r = cv2.selectROI(im)

        # Crop image
        imCrop = im[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

        return imCrop

    @staticmethod
    def draw(image, title="image"):
        cv2.imshow(title, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def threshold_zero(image):
        img_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = 100
        ret, thresh_img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        img_contours = np.zeros(image.shape)
        cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 1)
        cv_img = img_contours.astype(np.uint8)
        cv_gray = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY)
        return cv_gray

    @staticmethod
    def get_keypoints(img):
        sift = cv2.SIFT_create()
        kp, des = sift.detectAndCompute(img, None)

        # bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        # matches = bf.match(desB, desB)
        # matches = sorted(matches, key=lambda x: x.distance)
        # matched_image = cv2.drawMatches(imgA, kpA, imgB, kpB, matches, None, flags=2)
        img_kp = cv2.drawKeypoints(img, kp, cv2.DRAW_MATCHES_FLAGS_DEFAULT, color=(120, 157, 187))
        return img_kp

    @staticmethod
    def get_orb_sift_image_descriptors(img1, img2):
        sift = cv2.SIFT_create()
        orb = cv2.ORB_create()
        search_kp_orb = orb.detect(img1, None)
        idx_kp_orb = orb.detect(img2, None)
        kp1, des1 = sift.compute(img1, search_kp_orb)
        kp2, des2 = sift.compute(img2, idx_kp_orb)
        return kp1, des1, kp2, des2

    @staticmethod
    def threshold(img, thresh=127, mode='inverse'):
        im = img.copy()

        if mode == 'direct':
            thresh_mode = cv2.THRESH_BINARY
        else:
            thresh_mode = cv2.THRESH_BINARY_INV

        ret, thresh = cv2.threshold(im, thresh, 255, thresh_mode)

        return thresh

    @staticmethod
    def select_colorsp(img, colorsp='gray'):
        # Convert to grayscale.
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Split BGR.
        red, green, blue = cv2.split(img)
        # Convert to HSV.
        im_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # Split HSV.
        hue, sat, val = cv2.split(im_hsv)
        # Store channels in a dict.
        channels = {'gray': gray, 'red': red, 'green': green,
                    'blue': blue, 'hue': hue, 'sat': sat, 'val': val}

        return channels[colorsp]

    @staticmethod
    def get_bboxes(img):
        contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        # Sort according to the area of contours in descending order.
        sorted_cnt = sorted(contours, key=cv2.contourArea, reverse=True)
        # Remove max area, outermost contour.
        sorted_cnt.remove(sorted_cnt[0])
        bboxes = []
        for cnt in sorted_cnt:
            x, y, w, h = cv2.boundingRect(cnt)
            cnt_area = w * h
            bboxes.append((x, y, x + w, y + h))
        return bboxes

    @staticmethod
    def get_filtered_bboxes(img, min_area_ratio=0.001):
        contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        # Sort the contours according to area, larger to smaller.
        sorted_cnt = sorted(contours, key=cv2.contourArea, reverse=True)
        # Remove max area, outermost contour.
        sorted_cnt.remove(sorted_cnt[0])
        # Container to store filtered bboxes.
        bboxes = []
        # Image area.
        im_area = img.shape[0] * img.shape[1]
        for cnt in sorted_cnt:
            x, y, w, h = cv2.boundingRect(cnt)
            cnt_area = w * h
            # Remove very small detections.
            if cnt_area > min_area_ratio * im_area:
                bboxes.append((x, y, x + w, y + h))
        return bboxes

    @staticmethod
    def draw_annotations(img, bboxes, thickness=2, color=(0, 255, 0)):
        annotations = img.copy()
        for box in bboxes:
            tlc = (box[0], box[1])
            brc = (box[2], box[3])
            cv2.rectangle(annotations, tlc, brc, color, thickness, cv2.LINE_AA)

        return annotations

    @staticmethod
    def get_color_mask(img, lower=None, upper=None):
        if upper is None:
            upper = [0, 255, 255]
        if lower is None:
            lower = [0, 0, 0]
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        low = np.array(lower)
        up = np.array(upper)
        mask = cv2.inRange(img_hsv, low, up)
        inv_mask = 255 - mask

        return inv_mask

    @staticmethod
    def morph_op(img, mode='open', ksize=5, iterations=1):
        im = img.copy()
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))

        if mode == 'open':
            morphed = cv2.morphologyEx(im, cv2.MORPH_OPEN, kernel)
        elif mode == 'close':
            morphed = cv2.morphologyEx(im, cv2.MORPH_CLOSE, kernel)
        elif mode == 'erode':
            morphed = cv2.erode(im, kernel)
        else:
            morphed = cv2.dilate(im, kernel)

        return morphed

    @staticmethod
    def morph_threshold(img, morph_mode='open', ksize=5, iterations=1, thresh=110, threshold_mode='inverse',
                        colorsp='gray'):
        gray_stags = CVHelper.select_colorsp(img, colorsp=colorsp)
        thresh_stags = CVHelper.threshold(gray_stags, thresh=thresh, mode=threshold_mode)
        res = CVHelper.morph_op(thresh_stags, morph_mode, ksize, iterations)
        return res

    @staticmethod
    def detect_and_compute(img1, img2=None, approach=None):
        approach_obj = None
        if approach == "sift":
            approach_obj = cv2.SIFT_create()
        if approach == "orb":
            approach_obj = cv2.ORB_create()

        if not approach_obj:
            approach = "sift"
            approach_obj = cv2.SIFT_create()

        kp1, des1 = approach_obj.detectAndCompute(img1, None)
        if img2 is None:
            return kp1, des1
        kp2, des2 = approach_obj.detectAndCompute(img2, None)

        return kp1, des1, kp2, des2

    @staticmethod
    def knn_match(img1, img2, distance=0.8, approach=None):
        kp1, des1, kp2, des2 = CVHelper.detect_and_compute(img1, img2, approach)

        matches = []
        if approach == 'sift' or approach == 'orb_sift':
            bf = cv2.BFMatcher()
        else:
            bf = cv2.BFMatcher()
        if des1 is not None and des2 is not None:
            matches = bf.knnMatch(des1, des2, k=2)

        # Apply ratio test
        good = []

        for i in matches:
            if len(i) == 2:
                m, n = i
                if m.distance < distance * n.distance:
                    good.append([m])
            if len(i) == 1:
                if i[0].distance < distance:
                    good.append(i)

        return kp1, kp2, good

    @staticmethod
    def knn_match_and_draw(img1, img2, distance=0.8, approach=None):
        kp1, kp2, good = CVHelper.knn_match(img1, img2, distance, approach)

        img_res = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None,
                                     matchColor=(0, 255, 0), matchesMask=None,
                                     singlePointColor=(255, 0, 0), flags=0)

        return kp1, kp2, good, img_res

    @staticmethod
    def knn_match_and_draw_and_show(img1, img2, distance=0.8, approach=None):
        kp1, kp2, good, img_res = CVHelper.knn_match_and_draw(img1, img2, distance, approach)

        from matplotlib import pyplot as plt
        plt.imshow(img_res), plt.show()
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def get_similarity_from_desc(approach, search_desc, idx_desc):
        if approach == 'sift' or approach == 'orb_sift':
            bf = cv2.BFMatcher()
        else:
            bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        matches = bf.match(search_desc, idx_desc)
        # Distances between search and index features that match
        distances = [m.distance for m in matches]
        # Distance between search and index images
        distance = sum(distances) / len(distances)
        # If distance == 0 -> similarity = 1
        similarity = 1 / (1 + distance)
        return similarity

    @staticmethod
    def match(img1, img2, distance=200, approach=None):
        if isinstance(img2, str):
            des2 = CVHelper.read_descriptor(img2)
            kp2 = None
            kp1, des1 = CVHelper.detect_and_compute(img1, approach=approach)
        else:
            kp1, des1, kp2, des2 = CVHelper.detect_and_compute(img1, img2, approach)

        matches = []
        if approach == 'sift' or approach == 'orb_sift':
            bf = cv2.BFMatcher()
        else:
            bf = cv2.BFMatcher()
        if des1 is not None and des2 is not None:
            matches = bf.match(des1, des2)
            matches = sorted(matches, key=lambda x: x.distance)

        good = []

        for i in matches:
            if i.distance < distance:
                good.append(i)
        if isinstance(img2, str):
            return good
        else:
            return kp1, kp2, good

    @staticmethod
    def match_and_draw(img1, img2, distance=200, approach=None):
        kp1, kp2, good = CVHelper.match(img1, img2, distance, approach)

        img_res = cv2.drawMatches(img1, kp1, img2, kp2, good, None,
                                  matchColor=(0, 255, 0), matchesMask=None,
                                  singlePointColor=(255, 0, 0), flags=0)

        return kp1, kp2, good, img_res

    @staticmethod
    def write_descriptor(des, path):
        import pickle
        with open(path, 'wb') as f:
            pickle.dump(des, f)

    @staticmethod
    def read_descriptor(path):
        import pickle
        with open(path, 'rb') as f:
            descriptors = pickle.load(f)
        return descriptors
