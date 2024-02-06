import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import cv2
import mediapipe as mp
import av
import numpy as np


class PoseEstimationProcessor(VideoProcessorBase):
    def __init__(self) -> None:
        self.pose = mp.solutions.pose.Pose()
        self.frame_skip_ratio = 100
        self.frame_count = 0  # 処理されたフレームのカウント
        self.last_image = None  # 最後に処理された画像を保存
        self.last_pose_landmarks = None  # 最後に検出されたポーズのランドマークを保存

    def recv(self, frame):
        self.frame_count += 1
        image = frame.to_ndarray(format="bgr24")
        
        if self.frame_count % self.frame_skip_ratio == 0 or self.last_image is None:
            # 画像をRGBに変換
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # ポーズ検出を実行
            results = self.pose.process(image)
            self.last_pose_landmarks = results.pose_landmarks
            
            # 画像をBGRに戻す
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # 検出されたポーズを描画
            if self.last_pose_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    image, self.last_pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
            
            self.last_image = image
        else:
            # 前回の検出結果を再利用
            image = self.last_image.copy()
            if self.last_pose_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    image, self.last_pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)

        return av.VideoFrame.from_ndarray(image, format="bgr24")

def main():
    global frame_skip_ratio
    st.title("リアルタイム骨格検出 with MediaPipe")
    # WebRTCを使ったカメラ映像の取り込みと骨格検出の適用
    webrtc_streamer(key="example", video_processor_factory=PoseEstimationProcessor)

if __name__ == "__main__":
    main()
