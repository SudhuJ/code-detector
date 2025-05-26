import numpy as np
import cv2
import streamlit as st

st.set_page_config(page_title="Code Scanner", layout="centered")
st.title("QR & Barcode Scanner")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    mode = st.radio("Choose scanning mode:", ["QR Code", "Barcode (EAN-13 Format)"], horizontal=True)


uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Placeholder for result
result_placeholder = st.empty()
image_placeholder = st.empty()

def process_qr(image):
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(image)

    if data:
        result_placeholder.success("QR Code Detected.")
        st.code(data, language="text")
        if bbox is not None:
            # Draw bounding box
            n = len(bbox)
            for i in range(n):
                pt1 = tuple(bbox[i][0].astype(int))
                pt2 = tuple(bbox[(i + 1) % n][0].astype(int))
                cv2.line(image, pt1, pt2, (0, 255, 0), 2)
    else:
        result_placeholder.warning("No QR Detected.")

    return image


def process_barcode(image):
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    detector = cv2.barcode_BarcodeDetector()
    data, bbox, _ = detector.detectAndDecode(image)

    if data:
        result_placeholder.success("Barcode Detected.")
        st.code(data, language="text")
        if bbox is not None:
            # Draw bounding box
            n = len(bbox)
            for i in range(n):
                pt1 = tuple(bbox[i][0].astype(int))
                pt2 = tuple(bbox[(i + 1) % n][0].astype(int))
                cv2.line(image, pt1, pt2, (0, 255, 0), 2)
    else:
        result_placeholder.warning("No Barcode Detected.")
    return image


def process_image(image_bgr):
    if mode == "QR Code":
        return process_qr(image_bgr)
    elif mode == "Barcode":
        return process_barcode(image_bgr)
    
if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    output = process_image(image_bgr)
    image_placeholder.image(output, channels="BGR")