import streamlit as st
import ollama

st.set_page_config(page_title="AI 챗봇", page_icon="🤖", layout="wide")

with st.sidebar:
    st.header("챗봇 설정")

    system_prompts = {
        "일반 대화": "당신은 친절하고 도움이 되는 AI 어시스턴트입니다. 한국어로 답변해주세요.",
        "파이썬 튜터": "당신은 친절한 파이썬 프로그래밍 튜터입니다. 대학생 눈높이에 맞춰 쉽게 설명하고, 코드 예시를 포함해주세요.",
        "데이터 분석가": "당신은 데이터 분석 전문가입니다. Pandas, 시각화, 통계 분석에 대해 전문적으로 답변해주세요.",
        "영어 선생님": "당신은 영어 회화 선생님입니다. 사용자가 한국어로 질문하면 영어로 답변하고, 한국어 해설을 아래에 추가해주세요.",
        "논문 도우미": (
            "당신은 박사급 학술 연구 전문가입니다. 이공계·사회과학·인문학 전 분야의 논문 작성과 분석을 도울 수 있습니다.\n\n"
            "요청 유형별 대응 방식:\n"
            "- 논문 요약 요청: 연구 목적 / 방법론 / 핵심 결과 / 한계점 순으로 구조화하여 요약\n"
            "- 글쓰기 도움: 사용자 문장을 학술적 표현으로 다듬고, 수정 전후를 함께 제시\n"
            "- 논문 구조 설계: 서론(연구 배경·목적·가설) → 이론적 배경 → 연구 방법 → 결과 및 논의 → 결론 순으로 개요 작성\n"
            "- 인용·참고문헌: APA / MLA / Chicago 등 형식에 맞게 안내\n"
            "- 논리 검토: 주장과 근거의 연결이 약한 부분을 지적하고 보완 방향 제시\n\n"
            "항상 객관적이고 중립적인 학술 어조를 유지하며, 불확실한 내용은 추측임을 명시하세요. 한국어로 답변해주세요."
        ),
    }

    selected_role = st.selectbox("AI 역할 선택", list(system_prompts.keys()))

    # 직접 입력 옵션
    custom_prompt = st.text_area(
        "또는 직접 입력:",
        placeholder="AI에게 부여할 역할을 입력하세요...",
        height=100
    )

    # Temperature 조절 (Ollama의 options 파라미터로 전달됨)
    temperature = st.slider("Temperature", 0.0, 1.5, 0.7, 0.1)

    st.divider()

    # 대화 초기화 버튼
    if st.button("대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # 대화 통계
    if "messages" in st.session_state:
        user_msgs = sum(1 for m in st.session_state.messages if m["role"] == "user")
        st.caption(f"대화 수: {user_msgs}턴")

# ── 시스템 프롬프트 결정 ──
system_prompt = custom_prompt.strip() if custom_prompt.strip() else system_prompts[selected_role]

# ── 메인 화면 ──
st.title("AI 챗봇")
st.caption(f"현재 역할: {selected_role} | Temperature: {temperature}")

# ── 대화 기록 초기화 ──
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── 기존 대화 표시 ──
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ── 사용자 입력 ──
user_input = st.chat_input("메시지를 입력하세요")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Ollama에 전달할 메시지 (시스템 프롬프트 + 대화 기록)
    ollama_messages = [
        {"role": "system", "content": system_prompt}
    ] + st.session_state.messages

    with st.chat_message("assistant"):
        stream = ollama.chat(
            model="gemma3:4b",
            messages=ollama_messages,
            stream=True,
            options={"temperature": temperature}  # options: Ollama 모델 동작 제어 (temperature, top_k, top_p 등을 딕셔너리로 전달)
        )

        def stream_generator():
            for chunk in stream:
                yield chunk["message"]["content"]

        full_response = st.write_stream(stream_generator())

    st.session_state.messages.append({"role": "assistant", "content": full_response})