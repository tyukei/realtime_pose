# realtime_pose



## Setup
this is code for mac os

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## library
- [straemlit](https://streamlit.io/)
- [opencv](https://opencv.org/)
- [mediapipe](https://github.com/google/mediapipe)


## Streamlit Cloud
I found solution to run this app on streamlit cloud
- make packages.txt
- use pip install opencv-python-headless
- set STUN/TURN server