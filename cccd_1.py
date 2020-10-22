# -*- coding:utf-8 -*-
import cv2
import time
import numpy as np
from statistics import mean

from drive_ocr import ocr

def runtime(func, params):
    start = time.time()
    func(params)                # job
    print("====================")
    print("... runtime: {t}s\n\n".format(
        t=round(time.time() - start,3)))

def plot(list_dat, frame_name):
    import matplotlib.pyplot as plt
    plt.plot(list_dat)
    plt.ylabel(frame_name)
    plt.show()

def ocr_boxes(type, img_path, boxes):
    binary_img = cv2.imread(img_path,0)
    img = cv2.bitwise_not(binary_img)
    
    if type=="drive":
        for (x,y,w,h) in boxes:
            roi = img[y:y+h, x:x+w]
            cv2.imwrite("roi.jpg", roi)
            print(ocr('roi.jpg'))

    elif type=="local_tesseract":
        import pytesseract
        config = ("-l vie")
        orig = img.copy()

        for (x,y,w,h) in boxes:
            print(
                pytesseract.image_to_string(
                    orig[y:y+h,x:x+w]
                    , config=config ))

def save_n_img(img_path, res):
    bgr_img = cv2.imread(img_path)
    rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
    count = 0
    for (x,y,w,h) in res:
        # cv2.rectangle(
        #     img,(x,y),(x+w,y+h),(200,0,0),1)
        # cv2.imshow('',img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        cv2.imwrite(
            '{c}.jpg'.format(c=count)
            , rgb_img[y:y+h, x:x+w] )
        count+=1
    return "ok"

def merge_img(img_count):
    import os
    from PIL import Image
    from drive_ocr import ocr
    files = [
        "{i}.jpg".format(
            i=i) for i in range(img_count)]
    # tìm w và h cho ảnh nền
    total_h, total_w = 0, []
    for f in files:
        path = os.path.expanduser(f)
        img = Image.open(path)
        img.thumbnail(
            (400, 400), Image.ANTIALIAS)
        w,h = img.size
        total_h+=h
        total_w+=[w]
    result = Image.new("RGB", (max(total_w), total_h))
    # result.show()
    x,y=0,0
    for _, f in enumerate(files):
        path = os.path.expanduser(f)
        img = Image.open(path)
        img.thumbnail((400, 400), Image.ANTIALIAS)
        w,h = img.size
        result.paste(img, (x, y, x + w, y + h))
        y += h
    # result.show()
    result.save('prepare_ocr.jpg')
    # for i in files:
    #     os.remove(i)
    return ocr('prepare_ocr.jpg')

def extract_info(strs):
    '''
    last_change:
    test1 = test1.replace("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM Độc lập - Tự do - Hạnh phúc", "")
    test1 = test1.replace("Số", "")
    test1 = test1.replace("Có giá trị đến", "")
    test1 = test1.replace("Nơi thường trú", "")
    test1 = test1.replace("Quê quán", "")
    test1 = test1.replace("quán", "")
    test1 = test1.replace("Quốc tịch", "")
    test1 = test1.replace("tịch", "")
    test1 = test1.replace("Dân tộc", "")
    test1 = test1.replace("Giới tính", "")
    test1 = test1.replace("Ngày, tháng, năm sinh", "")
    test1 = test1.replace("Họ và tên khai sinh", "")
    test1 = test1.replace("Họ và tên gọi khác", "")
    test1 = test1.replace("Họ và tên", "")
    test1 = test1.replace("-", "")
    test1 = test1.replace("|", "")
    '''
    test1 = strs
    test1 = test1.replace("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM Độc lập - Tự do - Hạnh phúc", "")
    test1 = test1.replace("Ngày, tháng, năm sinh", "")
    test1 = test1.replace("Họ và tên khai sinh", "")
    test1 = test1.replace("Họ và tên gọi khác", "")
    test1 = test1.replace("Có giá trị đến", "")
    test1 = test1.replace("Nơi thường trú", "")
    test1 = test1.replace("Quốc tịch", "")
    test1 = test1.replace("Giới tính", "")
    test1 = test1.replace("Họ và tên", "")
    test1 = test1.replace("khai sinh", "")
    test1 = test1.replace("Quê quán", "")
    test1 = test1.replace("năm sinh", "")
    test1 = test1.replace("gọi khác", "")
    test1 = test1.replace("Dân tộc", "")
    test1 = test1.replace("thường", "")
    test1 = test1.replace("tháng", "")
    test1 = test1.replace("quán", "")
    test1 = test1.replace("tịch", "")
    test1 = test1.replace("tính", "")
    test1 = test1.replace("khai", "")
    test1 = test1.replace("sinh", "")
    test1 = test1.replace("năm", "")
    test1 = test1.replace("gọi", "")
    test1 = test1.replace("tộc", "")
    test1 = test1.replace("trú", "")
    test1 = test1.replace("giá", "")
    test1 = test1.replace("trị", "")
    test1 = test1.replace("đến", "")
    test1 = test1.replace("Số", "")
    test1 = test1.replace("-", "")
    test1 = test1.replace("|", "")
    test1 = test1.replace('''"''', "")

    result = []

    key = [i for i, letter in enumerate(test1) if letter == ":"]
    key.append(len(test1))
    key = key[::-1]
    key.append(0)
    key = key[::-1]

    setns = [
        (key[i],key[i+1]) 
        for i in range(len(key)-1) ]

    for k in setns:
        result.append(test1[k[0]+1:k[1]])
    
    if "CĂN CƯỚC" in result[0] or "CÔNG DÂN" in result[0] or "CĂN" in result[0] or "CƯỚC" in result[0]:
        result[0] = "CĂN CƯỚC CÔNG DÂN"
    elif "CHỨNG MINH" in result[0] or "NHÂN DÂN" in result[0] or "CHỨNG" in result[0] or "MINH" in result[0]:
        result[0] = "CHỨNG MINH NHÂN DÂN"
    else:
        result[0] = "unknown"

    return result


def check(strs):
    def helper(string, char_list):
        for i in string:
            if i in char_list:
                return True
        return False
    info, new_strs = {}, []
    # the
    info['the'] = strs[0]
    # so
    id_pos = [
        i for i in range(len(strs))
        if helper(
            strs[i]
            , ['0','1','2','3','4','5','6','7','8','9'])]
    info['so'] = ''.join([
        i for i in strs[min(id_pos)]
        if i in ['0','1','2','3','4','5','6','7','8','9']])

    # co_gia_tri_den
    info['co_gia_tri_den'] = strs[len(strs)-1]
    # noi_thuong_tru & que quan
    info['ho_ten'] = ''.join([
        i for i in strs[len(strs)-7]
        if i not in ['0','1','2','3','4','5','6','7','8','9']])
    info['gioi_tinh'] = strs[len(strs)-5]
    info['quoc_tich'] = strs[len(strs)-4]
    info['que_quan'] = strs[len(strs)-3]
    info['noi_thuong_tru'] = strs[len(strs)-2]

    # ngay-sinh
    id_pos = [
        i for i in range(len(strs))
        if helper(strs[i], ['/']) ]
    info['ngay_sinh'] = ''.join([
        i for i in strs[min(id_pos)]
        if i in ['/','0','1','2','3','4','5','6','7','8','9']])

    return info


'''
    TODO: đọc ảnh, tiền xử lí 
    & return contour
'''

def read_image(img_path):
    try:
        print("... doc anh & chuan bi boxes")

        binary_img = cv2.imread(img_path,0)
        img = cv2.bitwise_not(binary_img)
        # lay nguong
        ret, thresh = cv2.threshold(
            img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU )
        # tim contour
        (contours, _) = cv2.findContours(
            image = thresh, 
            mode = cv2.RETR_EXTERNAL,
            method = cv2.CHAIN_APPROX_SIMPLE )
        
        boxes = []
        min_area, max_area = 50, 10000
        for contour in contours:
            box = cv2.boundingRect(contour)
            x,y,w,h = box[0], box[1], box[2], box[3]
            # loai bo cac box qua to hoac nho
            if min_area <= w*h <= max_area:
                boxes.append((x,y,w,h))
            # neu muon kiem tra thi lay tat ca cac box
            # & comment 2 loai bo boxes
            # boxes.append((x,y,w,h))
        return "ok",boxes

    except Exception as err:
        return "err",err

'''
    TODO: Tách box theo dòng & merge
'''
def spliter(boxes,img_path):
    print("... tach box theo dong & merge")
    '''
        TODO: split theo Y (tach dong)
    '''
    # sắp xếp lại theo trục Y để tách từng hàng
    boxes.sort(key=lambda x: x[1])

    # tìm khoảng cách giữa các box liên tiếp
    distance = [
        boxes[i+1][1]-boxes[i][1] 
        for i in range(len(boxes)-1) ]
    
    # tách box nếu chạm index vượt quá giới hạn 
    # (các dòng không cách nhau quá 20 pixel)
    setn_index = [0]
    setn_index += [
        i+1 for i in range(len(distance)) 
        if distance[i]>20 ] 
    setn_index.append(len(boxes))

    # tạo các list box chứa từng câu
    setns = [
        (setn_index[i],setn_index[i+1]) 
        for i in range(len(setn_index)-1) ]
    # print(setns)
    
    # một số trường hợp, detect ra contour mắt và merge cùng ngày tháng
    # năm sinh, hoặc merge cả phần nơi thường trú và có giá trị đến 
    # nên cần kiểm tra nếu 'độ dài khoảng đó theo x' gần bằng chiều rộng thẻ
    # thì tách tiếp theo trục x
    '''
        TODO: split theo X (tách dữ liệu)
    '''
    binary_img = cv2.imread(img_path,0)
    img = cv2.bitwise_not(binary_img)
    
    res = []
    for i in setns[::-1]:
        def check_len_x(data, img_path):
            ''' Kiểm tra xem len của list box đó theo X 
                có vượt quá 75% thẻ hay không
                nếu có nghĩa là đã merge nhầm các vùng khác 
            '''
            len_data_by_x = data[len(data)-1][0] - data[0][0]
            img_width = cv2.imread(img_path, cv2.IMREAD_UNCHANGED).shape[1]
            if len_data_by_x*100/img_width>70:
                return True
            return False
        def merge_box(contours):
            '''
                chuyển list các box thành 1 box với quy ước
                x_box = vị trí đầu tiên của hàng (sắp xếp dãy theo x)
                w_box = x_end - x_first + x_end_w (sắp xếp dãy theo x) 
                y_box = min_y của hàng (sắp xếp dãy theo y)
                h_box = max(y) (sắp xếp dãy theo y)
            '''
            # sx theo X
            contours.sort(key=lambda x: x[0])		
            x_box = contours[0][0]
            w_box = contours[len(contours)-1][0] - contours[0][0] + contours[len(contours)-1][2]

            # sx theo Y
            contours.sort(key=lambda x: x[1])		
            y_box = contours[0][1]
            h_box = max([y+h for (_,y,_,h) in contours ]) - y_box

            return (x_box, y_box, w_box, h_box)

        # xét từng cặp setn
        data = boxes[i[0]:i[1]]

        # sắp xếp theo x
        data.sort(key=lambda x: x[0])

        # nếu có list box nào có chiều dài vượt quá 75% width 
        # thì split theo X:
        if check_len_x(data, img_path)==True:
            # tìm khoảng cách giữa các box liên tiếp theo x
            distance = [
                data[i+1][0]-data[i][0] 
                for i in range(len(data)-1) ]

            # tách box nếu chạm index vượt quá trung bình
            setn_index = [0]
            setn_index += [
                i+1 for i in range(len(distance)) 
                if distance[i]>72 ] 
            setn_index.append(len(data))

            # tạo các list box chứa từng câu
            setns = [
                (setn_index[i],setn_index[i+1]) 
                for i in range(len(setn_index)-1) ]

            contour_list = [
                merge_box(data[i[0]:i[1]]) for i in setns]
            res += contour_list
        else:
            res += [merge_box(data)]
    return res

    # for (x,y,w,h) in res:
    #     cv2.rectangle(
    #         img,(x,y),(x+w,y+h),(200,0,0),1)
    # cv2.imshow('',img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


'''
    TODO:
    Tests passed:
    ["5.jpg" , "4.jpeg" , "t5.png" , "23.jpg" , "22.jpg" , "11.jpg" , "27.png", "29.jpg", "49.jpg", "t8.png"]
'''

def cccd(img_path):
    start = time.time()

    print("=====\n {img} \n=====".format(img=img_path))
    # tìm box
    _, boxes = read_image(img_path)
    # list các box đã merge
    res = spliter(boxes,img_path)
    # print(res)
    # ghép các box thành new img
    save_n_img(img_path, res[::-1])
    # OCR new img đó
    cccd_info = {}
    data = merge_img(len(res))
    result = check(
        extract_info(data))

    return {
        "runtime":round(time.time() - start,3)
        , "info":result
    }

# for 1 test
# runtime(cccd, "uploads/5.jpg")

# # for list test_cases
# test_cases = ["5.jpg" , "4.jpeg" , "t5.png" , "23.jpg" , "22.jpg" , "11.jpg" , "27.png", "29.jpg", "t8.png"]
# test_cases = ["images/"+i for i in test_cases]
# for i in test_cases:
#     runtime(cccd, i)