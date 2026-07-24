import streamlit as st
import random

# Page Configuration
st.set_page_config(
    page_title="🎯 숫자 맞추기 게임",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom Styling (CSS)
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #1E88E5;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        text-align: center;
        color: #555555;
        font-size: 1.1rem;
        margin-bottom: 1.8rem;
    }
    .metric-card {
        background-color: #F8F9FA;
        border: 1px solid #E9ECEF;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    }
    .hint-box-up {
        background-color: #FFF3CD;
        border-left: 5px solid #FFC107;
        padding: 12px 18px;
        border-radius: 8px;
        font-weight: bold;
        color: #856404;
        margin-top: 10px;
    }
    .hint-box-down {
        background-color: #D1ECF1;
        border-left: 5px solid #17A2B8;
        padding: 12px 18px;
        border-radius: 8px;
        font-weight: bold;
        color: #0C5460;
        margin-top: 10px;
    }
    .hint-box-success {
        background-color: #D4EDDA;
        border-left: 5px solid #28A745;
        padding: 15px 18px;
        border-radius: 8px;
        font-weight: bold;
        color: #155724;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Session State Initialization
def init_game(reset_best=False):
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.history = []
    st.session_state.min_range = 1
    st.session_state.max_range = 100
    st.session_state.last_result = None
    if reset_best or 'best_score' not in st.session_state:
        st.session_state.best_score = None

if 'secret_number' not in st.session_state:
    init_game()

# Callback for making a guess
def process_guess():
    guess = st.session_state.user_guess
    if st.session_state.game_over:
        return

    st.session_state.attempts += 1
    attempts = st.session_state.attempts
    secret = st.session_state.secret_number

    if guess < secret:
        st.session_state.min_range = max(st.session_state.min_range, guess + 1)
        res = {"attempt": attempts, "guess": guess, "status": "UP 📈", "msg": f"{guess}보다 **더 큰** 숫자입니다!"}
        st.session_state.last_result = res
        st.session_state.history.insert(0, res)
    elif guess > secret:
        st.session_state.max_range = min(st.session_state.max_range, guess - 1)
        res = {"attempt": attempts, "guess": guess, "status": "DOWN 📉", "msg": f"{guess}보다 **더 작은** 숫자입니다!"}
        st.session_state.last_result = res
        st.session_state.history.insert(0, res)
    else:
        st.session_state.game_over = True
        is_new_record = False
        if st.session_state.best_score is None or attempts < st.session_state.best_score:
            st.session_state.best_score = attempts
            is_new_record = True

        res = {
            "attempt": attempts,
            "guess": guess,
            "status": "정답 🎉",
            "msg": f"축하합니다! **{attempts}회** 만에 정답({secret})을 맞추셨습니다!",
            "is_new_record": is_new_record
        }
        st.session_state.last_result = res
        st.session_state.history.insert(0, res)

# UI Layout
st.markdown('<div class="main-title">🎯 숫자 맞추기 게임</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">컴퓨터가 생각한 1부터 100 사이의 숫자를 맞춰보세요!</div>', unsafe_allow_html=True)

# Dashboard Metrics
col1, col2, col3 = st.columns(3)
with col1:
    best_disp = f"{st.session_state.best_score}회" if st.session_state.best_score is not None else "없음"
    st.metric("🏆 최고 기록", best_disp)

with col2:
    st.metric("🔢 현재 시도 횟수", f"{st.session_state.attempts}회")

with col3:
    range_disp = f"{st.session_state.min_range} ~ {st.session_state.max_range}"
    st.metric("💡 예상 정답 범위", range_disp)

st.divider()

# Input & Form Section
if not st.session_state.game_over:
    with st.form(key="guess_form", clear_on_submit=False):
        guess_val = st.number_input(
            "1부터 100 사이의 숫자를 입력하세요:",
            min_value=1,
            max_value=100,
            value=min(max(st.session_state.min_range, 50), st.session_state.max_range),
            step=1,
            key="user_guess"
        )
        submit_btn = st.form_submit_button("정답 확인 🚀", on_click=process_guess, use_container_width=True)
else:
    last = st.session_state.last_result
    if last and last["status"] == "정답 🎉":
        st.balloons()
        st.success(last["msg"])
        if last.get("is_new_record"):
            st.info(f"✨ 새로운 최고 기록 달성! ({st.session_state.best_score}회 시도)")

# Last Result Feedback Message
if not st.session_state.game_over and st.session_state.last_result:
    last = st.session_state.last_result
    if "UP" in last["status"]:
        st.markdown(f'<div class="hint-box-up">📈 <b>UP!</b> {last["msg"]}</div>', unsafe_allow_html=True)
    elif "DOWN" in last["status"]:
        st.markdown(f'<div class="hint-box-down">📉 <b>DOWN!</b> {last["msg"]}</div>', unsafe_allow_html=True)

st.write("") # Spacing

# Control Buttons Row
btn_col1, btn_col2 = st.columns(2)
with btn_col1:
    if st.button("🔄 새 게임 시작", use_container_width=True):
        init_game(reset_best=False)
        st.rerun()

with btn_col2:
    if st.button("🗑️ 기록 초기화", use_container_width=True):
        init_game(reset_best=True)
        st.rerun()

# History Log Section
if st.session_state.history:
    st.divider()
    st.subheader("📜 시도 기록")
    for item in st.session_state.history:
        col_att, col_guess, col_res = st.columns([1, 2, 4])
        with col_att:
            st.write(f"**{item['attempt']}회차**")
        with col_guess:
            st.write(f"입력: **{item['guess']}**")
        with col_res:
            st.write(f"{item['status']} - {item['msg']}")
