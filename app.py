import streamlit as st
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer

def main():
    st.title("リアルタイムカメラ")

    # WebRTCを使ったカメラ映像の取り込み
    webrtc_streamer(key="example")

if __name__ == "__main__":
    main()
