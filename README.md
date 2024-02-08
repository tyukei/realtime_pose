# realtime_pose

<img width="256" alt="image" src="https://github.com/tyukei/realtime_pose/assets/63638636/98b563a9-bc66-4851-8027-ae4d13c330d9">


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
