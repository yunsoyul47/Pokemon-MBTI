import streamlit as st
import json

st.set_page_config(
    page_title="나만의 MBTI 단짝 포켓몬 찾기",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* 전체 배경 및 기본 폰트 설정 (따뜻한 크림/노란색 톤) */
    .stApp {
        background-color: #FFFDF0;
        font-family: 'Pretendard', 'Malgun Gothic', sans-serif;
        color: #2D3748;
    }
    
    /* 헤더 스타일링 */
    .main-header {
        text-align: center;
        padding: 2rem 1rem 1rem 1rem;
        background: linear-gradient(135deg, #FFF3BF 0%, #FFE066 100%);
        border-radius: 24px;
        box-shadow: 0 8px 20px rgba(245, 159, 0, 0.15);
        margin-bottom: 2rem;
        border: 2px solid #FFD43B;
    }
    
    .main-title {
        font-size: 2.3rem !important;
        font-weight: 800;
        color: #D9480F;
        margin-bottom: 0.5rem;
    }
    
    .sub-title {
        font-size: 1.2rem !important;
        color: #7950F2;
        font-weight: 600;
    }
    
    /* 포켓몬 카드 스타일 */
    .pokemon-card {
        background: #FFFFFF;
        border-radius: 24px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        border: 3px solid #FFE066;
        text-align: center;
        margin-top: 1.5rem;
        transition: all 0.3s ease;
    }
    
    /* 큰 글씨 레이블 */
    .badge-mbti {
        display: inline-block;
        background-color: #FF6B6B;
        color: white;
        font-size: 1.3rem;
        font-weight: bold;
        padding: 6px 18px;
        border-radius: 30px;
        margin-bottom: 12px;
    }
    
    .pokemon-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #2B8A3E;
        margin-bottom: 0.5rem;
    }
    
    .type-badge {
        display: inline-block;
        background-color: #E9ECEF;
        color: #495057;
        font-size: 1.1rem;
        font-weight: bold;
        padding: 6px 16px;
        border-radius: 20px;
        margin: 4px;
        border: 1px solid #CED4DA;
    }
    
    .section-box {
        background-color: #FFF9DB;
        border-radius: 16px;
        padding: 1.2rem;
        margin-top: 1rem;
        text-align: left;
        font-size: 1.15rem;
        line-height: 1.7;
        color: #343A40;
        border-left: 5px solid #FCC419;
    }
    
    /* 선택 상자 및 버튼 스타일링 조정 */
    .stSelectbox label {
        font-size: 1.3rem !important;
        font-weight: bold !important;
        color: #D9480F !important;
    }
    
    /* 이미지 스타일 */
    .pokemon-img-container img {
        max-width: 280px;
        filter: drop-shadow(0px 8px 12px rgba(0,0,0,0.15));
        transition: transform 0.3s ease;
    }
    
    .pokemon-img-container img:hover {
        transform: scale(1.05);
    }
    </style>
""", unsafe_allowed_html=True)

MBTI_POKEMON_DB = {
    "ISTJ": {
        "mbti_title": "신중하고 철저한 현실주의자",
        "name_ko": "거북왕",
        "name_en": "Blastoise",
        "id": 9,
        "type": ["물"],
        "traits": "묵묵하고 책임감이 강하며, 언제나 신뢰할 수 있는 든든한 방어력을 지닌 포켓몬.",
        "reason": "책임감이 강하고 규칙을 중시하는 ISTJ와 꼭 닮았습니다. 단단한 껍질처럼 흔들리지 않는 신념으로 서로의 뒤를 든든하게 지켜줄 최상의 파트너입니다."
    },
    "ISFJ": {
        "mbti_title": "성실하고 온화한 수호자",
        "name_ko": "해피너스",
        "name_en": "Blissey",
        "id": 242,
        "type": ["노말"],
        "traits": "상대방의 상처를 따뜻하게 보듬고 기쁨을 나누는 친절의 대명사.",
        "reason": "주변 사람들을 헌신적으로 챙기는 ISFJ의 따뜻한 마음씨와 완벽하게 일치합니다. 서로에게 무한한 위로와 보살핌을 건네는 따스한 유대감을 형성합니다."
    },
    "INFJ": {
        "mbti_title": "통찰력 있는 통합적 예언자",
        "name_ko": "가디안",
        "name_en": "Gardevoir",
        "id": 282,
        "type": ["에스퍼", "페어리"],
        "traits": "트레이너의 마음을 깊이 감지하며, 위험에 처했을 때 모든 힘을 다해 지켜내는 포켓몬.",
        "reason": "타인의 감정을 깊게 이해하고 영혼의 교감을 중요시하는 INFJ에게 가디안은 말없이도 서로의 마음을 읽어내는 깊은 영혼의 단짝이 되어줍니다."
    },
    "INTJ": {
        "mbti_title": "용의주도한 전략가",
        "name_ko": "뮤츠",
        "name_en": "Mewtwo",
        "id": 150,
        "type": ["에스퍼"],
        "traits": "뛰어난 지능과 독립적인 사고로 최선의 전략을 도출해내는 전설의 포켓몬.",
        "reason": "명확한 비전과 지적 탐구를 즐기는 INTJ에게 뮤츠의 깊은 통찰력과 독립적인 성향은 깊은 지적 공감대와 조화로운 호흡을 만들어냅니다."
    },
    "ISTP": {
        "mbti_title": "만능 재주꾼, 만능 해결사",
        "name_ko": "루카리오",
        "name_en": "Lucario",
        "id": 448,
        "type": ["루카리오", "강철"],
        "traits": "상황 판단이 빠르고 파동을 감지하여 효율적이고 완벽하게 임무를 수행함.",
        "reason": "냉철한 상황 판단력과 뛰어난 도구/기술 활용 능력을 가진 ISTP와 잘 맞습니다. 과묵하지만 실전에서 놀라운 합을 보여주는 단짝입니다."
    },
    "ISFP": {
        "mbti_title": "호기심 많은 예술가",
        "name_ko": "이브이",
        "name_en": "Eevee",
        "id": 133,
        "type": ["노말"],
        "traits": "다양한 가능성을 품고 있으며 온화하고 자유로운 감성을 지닌 포켓몬.",
        "reason": "자유로운 영혼과 온화한 예술가적 감성을 지닌 ISFP처럼 이브이는 어떤 형태로든 변화할 수 있는 무한한 가능성과 따스함을 공유합니다."
    },
    "INFP": {
        "mbti_title": "이상주의자 중재자",
        "name_ko": "님피아",
        "name_en": "Sylveon",
        "id": 700,
        "type": ["페어리"],
        "traits": "리본 모양의 촉수로 애정 어린 기운을 내뿜어 상대를 다정하게 다독임.",
        "reason": "풍부한 감수성과 낭만을 가진 INFP의 마음을 순식간에 녹여줍니다. 갈등 없는 평화롭고 따뜻한 세계를 함께 꿈꿀 수 있는 최고의 친구입니다."
    },
    "INTP": {
        "mbti_title": "아이디어 넘치는 논리술사",
        "name_ko": "후딘",
        "name_en": "Alakazam",
        "id": 65,
        "type": ["에스퍼"],
        "traits": "IQ 5000에 달하는 방대한 기억력과 완벽한 분석 능력을 자랑함.",
        "reason": "끊임없이 호기심을 갖고 원리를 탐구하는 INTP에게 최고의 호기심 해결사가 되어주며, 지적인 흥미를 함께 채워갈 수 있습니다."
    },
    "ESTP": {
        "mbti_title": "모험을 즐기는 수완가",
        "name_ko": "피카츄",
        "name_en": "Pikachu",
        "id": 25,
        "type": ["전기"],
        "traits": "에너지가 넘치고 순발력이 뛰어나며 늘 스릴 넘치는 현장에 앞장섬.",
        "reason": "액션과 스릴을 즐기는 ESTP처럼 넘치는 에너지와 빠른 행동력을 자랑합니다. 언제 어디서나 지루할 틈 없는 신나는 모험을 만들어갑니다."
    },
    "ESFP": {
        "mbti_title": "자유로운 영혼의 연예인",
        "name_ko": "푸린",
        "name_en": "Jigglypuff",
        "id": 39,
        "type": ["노말", "페어리"],
        "traits": "사람들의 시선을 사로잡는 것을 좋아하며 사랑스러운 분위기 메이커.",
        "reason": "어디서나 분위기를 밝게 만드는 ESFP와 완벽히 잘 어울립니다. 함께 있는 것만으로도 주변 사람들에게 웃음과 즐거움을 선사합니다."
    },
    "ENFP": {
        "mbti_title": "재기발랄한 활동가",
        "name_ko": "파모",
        "name_en": "Pawmi",
        "id": 921,
        "type": ["전기"],
        "traits": "호기심이 왕성하고 사랑스러우며 누구와도 금방 친구가 되는 스파크 포켓몬.",
        "reason": "통통 튀는 아이디어와 긍정 에너지가 넘치는 ENFP의 완벽한 짝꿍입니다. 지치지 않는 열정으로 새로운 스파크를 일으킵니다."
    },
    "ENTP": {
        "mbti_title": "뜨거운 열정의 변론가",
        "name_ko": "팬텀",
        "name_en": "Gengar",
        "id": 94,
        "type": ["고스트", "독"],
        "traits": "장난기 넘치고 재치 있는 장난으로 상대를 놀라게 만드는 창의적인 포켓몬.",
        "reason": "고정관념을 깨는 재치와 호기심을 지닌 ENTP에게 최고의 짝궁입니다. 톡톡 튀는 장난과 기발한 아이디어로 매일을 즐겁게 만들어줍니다."
    },
    "ESTJ": {
        "mbti_title": "엄격한 관리자",
        "name_ko": "윈디",
        "name_en": "Arcanine",
        "id": 59,
        "type": ["불꽃"],
        "traits": "위풍당당한 기품과 강한 리더십, 철저한 충성심을 가진 포켓몬.",
        "reason": "질서와 원칙을 중시하고 질서정연한 가이드를 이끄는 ESTJ에게 용맹함과 충성심으로 든든한 조력자가 되어줍니다."
    },
    "ESFJ": {
        "mbti_title": "사교적인 친선도모형",
        "name_ko": "토게키스",
        "name_en": "Togekiss",
        "id": 468,
        "type": ["페어리", "비행"],
        "traits": "서로 다투지 않는 평화로운 곳에 나타나 축복과 기쁨을 나누어줌.",
        "reason": "주변 사람들의 화합과 행복을 최우선으로 생각하는 ESFJ처럼, 따뜻한 마음과 은혜로운 미소로 주변에 행복을 퍼뜨립니다."
    },
    "ENFJ": {
        "mbti_title": "정의로운 리더",
        "name_ko": "망나뇽",
        "name_en": "Dragonite",
        "id": 149,
        "type": ["드래곤", "비행"],
        "traits": "넓은 바다를 아우르며 거친 풍랑 속에서도 사람들을 구조하는 다정한 리더.",
        "reason": "타인을 이끌고 돕는 데 망설임이 없는 ENFJ의 따뜻한 리더십과 어울립니다. 주변 사람들을 포근하게 끌어안아 주는 든든한 존재입니다."
    },
    "ENTJ": {
        "mbti_title": "대담한 통솔자",
        "name_ko": "리자몽",
        "name_en": "Charizard",
        "id": 6,
        "type": ["불꽃", "비행"],
        "traits": "강한 상대를 찾아 도전을 그치지 않으며 압도적인 열정으로 앞장서 이끎.",
        "reason": "원대한 목표를 향해 당차게 나아가는 ENTJ에게 어울립니다. 불타는 승부욕과 강인한 추진력으로 함께 최고의 자리를 향해 달려갑니다."
    }
}

# Header Section
st.markdown("""
    <div class="main-header">
        <div class="main-title">⚡ MBTI 단짝 포켓몬 찾기 ⚡</div>
        <div class="sub-title">성격 유형을 선택하면 나만의 어울리는 포켓몬 파트너를 찾아드려요!</div>
    </div>
""", unsafe_allowed_html=True)

# Selectbox Container
st.markdown("### 🔍 당신의 MBTI 성격 유형을 선택해주세요")

# Grid or Single Selectbox
selected_mbti = st.selectbox(
    "MBTI 목록",
    options=list(MBTI_POKEMON_DB.keys()),
    index=0,
    help="16가지 MBTI 유형 중 당신의 유형을 고르세요!"
)

if selected_mbti:
    pokemon_data = MBTI_POKEMON_DB[selected_mbti]
    
    # Trigger celebratory balloons/effects on recommendation!
    st.balloons()
    
    # Official PokeAPI high-resolution image URL
    img_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_data['id']}.png"
    
    # Layout using Streamlit columns for side-by-side or stacked view
    st.markdown("---")
    
    # Render main card container
    st.markdown(f"""
        <div class="pokemon-card">
            <div class="badge-mbti">✨ {selected_mbti} : {pokemon_data['mbti_title']} ✨</div>
            <div class="pokemon-title">{pokemon_data['name_ko']} <span style="font-size: 1.3rem; color: #868E96;">({pokemon_data['name_en']})</span></div>
            <div style="margin-bottom: 1rem;">
                {' '.join([f'<span class="type-badge">🏷️ {t}</span>' for t in pokemon_data['type']])}
            </div>
            <div class="pokemon-img-container">
                <img src="{img_url}" alt="{pokemon_data['name_ko']}" />
            </div>
            <div class="section-box">
                <strong>📌 포켓몬 특징</strong><br>
                {pokemon_data['traits']}
            </div>
            <div class="section-box" style="background-color: #FFF3BF; border-left-color: #FF922B;">
                <strong>💖 어울리는 이유</strong><br>
                {pokemon_data['reason']}
            </div>
        </div>
    """, unsafe_allowed_html=True)
    
    # Celebration Message below
    st.markdown("""
        <div style="text-align: center; margin-top: 1.5rem; font-size: 1.2rem; font-weight: bold; color: #E8590C;">
            🎉 축하합니다! 완벽한 단짝 포켓몬을 찾았습니다! 🎉
        </div>
    """, unsafe_allowed_html=True)

st.markdown("<br><br>", unsafe_allowed_html=True)
with st.expander("ℹ️ 스트림릿 클라우드(Streamlit Cloud) 배포 가이드"):
    st.write("""
    1. 이 코드파일을 **`main.py`** 이름으로 저장합니다.
    2. 깃허브(GitHub) 저장소를 새로 만들고 `main.py`와 아래 내용의 `requirements.txt`를 추가하세요:
       ```
       streamlit
       ```
    3. [Streamlit Community Cloud](https://share.streamlit.io/)에 접속하여 깃허브 계정으로 로그인합니다.
    4. **'New app'** 버튼을 누른 후, 저장소와 `main.py` 경로를 지정하면 인터넷에 무료로 앱이 배포됩니다!
    """)
