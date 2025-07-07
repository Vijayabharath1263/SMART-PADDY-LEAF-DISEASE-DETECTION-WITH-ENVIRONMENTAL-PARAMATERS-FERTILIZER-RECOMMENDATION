import os
import shutil
import cv2
import numpy as np
import matplotlib.pylab as plt
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
from numpy import asarray
import sample_data
from m_bpnn import BPNNetwork


def read_first_data():
    csv_file_path = askopenfilename()
    if not csv_file_path:
        return

    fpath = os.path.dirname(os.path.abspath(csv_file_path))
    fname = os.path.basename(csv_file_path)
    fsize = os.path.getsize(csv_file_path)

    txt.delete(0, END)
    txt.insert(0, fpath)
    txt2.delete(0, END)
    txt2.insert(0, fname)
    sample_data.student.file_path = csv_file_path

def next_page():
    root.destroy()
    import image_grayscale


def rotate_bound(image, angle):
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
    return cv2.warpAffine(image, M, (nW, nH))

def roi():
    image = cv2.imread('data/morphological.png')
    original = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (127, 127), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=2)
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return

    contours = max(contours, key=lambda x: cv2.contourArea(x))
    cv2.drawContours(image, [contours], -1, (255, 255, 0), 2)
    hull = cv2.convexHull(contours, returnPoints=False)
    defects = cv2.convexityDefects(contours, hull)

    if defects is not None:
        for i in range(defects.shape[0]):
            _, _, farthest_point_index, distance = defects[i, 0]
            if distance > 50000:
                farthest_point = contours[farthest_point_index][0]
    else:
        sample_data.student.bpnn -= 1

    plt.imsave('Detected.png', image)

def read_first_data1():
    lbl2.delete(0, END)
    lbl2.insert(0, str(sample_data.student.bpnn))
    labe_rou.place(x=370, y=200)

def run_feature_extraction():
    img = cv2.imread('data/morphological.png', 0)
    numpydata = asarray(img)
    z = [int(val) for row in numpydata for val in row]

    nn = BPNNetwork([2, 2, 1])
    nn.glcm_extract(z)
    sample_data.student.bpnn = nn.result()
    roi()

def feature_extraction_page():
    root = Tk()
    run_feature_extraction()
    w, h = 750, 550
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x, y = (ws - w) // 2, (hs - h) // 2
    root.geometry(f'{w}x{h}+{x}+{y}')
    root.title(sample_data.student.title)
    root.configure(background=sample_data.student.background)
    root.resizable(False, False)

    Label(root, text=sample_data.student.titlec, fg=sample_data.student.text_color,
          bg=sample_data.student.background, width=35, height=3,
          font=('times', 30, 'italic bold')).place(x=0, y=20)

    Label(root, text="Morphological", fg=sample_data.student.text_color,
          bg=sample_data.student.background, font=('times', 10, 'italic bold')).place(x=100, y=170)

    Label(root, text="Feature-Extraction", fg=sample_data.student.text_color,
          bg=sample_data.student.background, font=('times', 10, 'italic bold')).place(x=400, y=170)

    ri2 = Image.open('data/morphological.png').resize((200, 200), Image.LANCZOS)
    r2 = ImageTk.PhotoImage(ri2)
    Label(root, image=r2, background=sample_data.student.background).place(x=100, y=200)

    global lbl2
    lbl2 = Entry(root)
    lbl2.place(x=400, y=400)

    ri3 = Image.open('Detected.png').resize((200, 200), Image.LANCZOS)
    global labe_rou
    r23 = ImageTk.PhotoImage(ri3)
    labe_rou = Label(root, image=r23)

    Button(root, text="extraction", width=16, command=read_first_data1, height=1,
           fg="#000", bg=sample_data.student.background, activebackground="#ff8000",
           activeforeground="white", font=('times', 15, 'bold')).place(x=100, y=450)

    Button(root, text="Next", width=16, command=next_page, height=1, fg="#000",
           bg=sample_data.student.background, activebackground="#ff8000",
           activeforeground="white", font=('times', 15, 'bold')).place(x=400, y=450)

    root.mainloop()
