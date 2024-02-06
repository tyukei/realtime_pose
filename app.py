import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import cv2
import mediapipe as mp
import av
import numpy as np

class PoseEstimationProcessor(VideoProcessorBase):
    def __init__(self) -> None:
        self.pose = mp.solutions.pose.Pose()
        self.frame_skip_ratio = 10
        self.frame_count = 0
        self.last_image = None
        self.last_pose_landmarks = None

    def recv(self, frame):
        self.frame_count += 1
        image = frame.to_ndarray(format="bgr24")
        
        if self.frame_count % self.frame_skip_ratio == 0 or self.last_image is None:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self.pose.process(image)
            self.last_pose_landmarks = results.pose_landmarks
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            if self.last_pose_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    image, self.last_pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
            self.last_image = image
        else:
            image = self.last_image.copy()
            if self.last_pose_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    image, self.last_pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)

        return av.VideoFrame.from_ndarray(image, format="bgr24")

def main():
    st.title("リアルタイム骨格検出 with MediaPipe")
    
    # 実行環境の選択
    is_local = st.checkbox("ローカルで実行しますか？", value=True)
    
    if is_local:
        webrtc_streamer(key="example", video_processor_factory=PoseEstimationProcessor)
    else:
        rtc_configuration = {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
        # クラウド環境用のSTUN/TURNサーバー設定をここに追加
        webrtc_streamer(key="example", video_processor_factory=PoseEstimationProcessor, rtc_configuration=rtc_configuration)

if __name__ == "__main__":
    main()
