import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import cv2
import mediapipe as mp

class PoseEstimationTransformer(VideoTransformerBase):
    def __init__(self):
        self.pose = mp.solutions.pose.Pose()

    def transform(self, frame):
        image = frame.to_ndarray(format="bgr24")
        
        # 画像をRGBに変換
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # ポーズ検出を実行
        results = self.pose.process(image)
        
        # 画像をBGRに戻す
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # 検出されたポーズを描画
        if results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                image, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)

        return image

def main():
    st.title("リアルタイム骨格検出 with MediaPipe")

    # WebRTCを使ったカメラ映像の取り込みと骨格検出の適用
    webrtc_streamer(key="example", video_transformer_factory=PoseEstimationTransformer)

if __name__ == "__main__":
    main()
