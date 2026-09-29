from html import escape
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import streamlit as st
import os
from langchain_core.prompts import load_prompt

load_dotenv()

st.set_page_config(page_title='PaperLens AI', page_icon='AI', layout='wide')

st.markdown(
    """
    <style>
        :root {
            --bg: #060b14;
            --bg-2: #0a1220;
            --panel: rgba(15, 23, 35, 0.82);
            --line: rgba(140, 184, 255, 0.18);
            --text: #edf5ff;
            --muted: #aab8cf;
            --cyan: #73dcff;
            --blue: #6ea8ff;
            --shadow: rgba(99, 161, 255, 0.3);
        }

        .stApp {
            background: radial-gradient(circle at 15% 15%, rgba(73, 128, 255, 0.16), transparent 20%),
                        radial-gradient(circle at 80% 20%, rgba(77, 223, 255, 0.16), transparent 25%),
                        linear-gradient(180deg, #050a12 0%, #07111d 100%);
            color: var(--text);
        }

        .main .block-container {
            max-width: 1280px;
            padding-top: 0 !important;
            padding-bottom: 0 !important;
        }

        [data-testid="stSidebar"] { display: none; }

        .paperlens-shell {
            min-height: auto;
            display: block;
            padding: 0;
            margin: 0;
        }

        .paperlens-hero {
            width: 100%;
            display: grid;
            grid-template-columns: 1.1fr 0.9fr;
            align-items: center;
            gap: 2.8rem;
            position: relative;
        }

        .paperlens-visual {
            position: relative;
            height: 540px;
            border-radius: 34px;
            border: 1px solid var(--line);
            background: linear-gradient(180deg, rgba(10, 17, 29, 0.9), rgba(7, 12, 20, 0.72));
            box-shadow: inset 0 0 0 1px rgba(130, 169, 255, 0.08), 0 30px 80px rgba(0,0,0,0.35), 0 0 30px rgba(79,166,255,0.14);
            overflow: hidden;
            animation: float 6s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }

        .paperlens-visual::before {
            content: "";
            position: absolute;
            inset: 20px 18px;
            border-radius: 24px;
            border: 1px solid rgba(146, 179, 255, 0.12);
            background: linear-gradient(180deg, rgba(9, 16, 28, 0.52), rgba(7, 11, 18, 0.25));
        }

        .paperlens-ring {
            position: absolute;
            inset: 50% auto auto 50%;
            width: 440px;
            height: 440px;
            transform: translate(-50%, -50%);
            border-radius: 50%;
            border: 1px solid rgba(99, 209, 255, 0.25);
            box-shadow: 0 0 35px rgba(88, 197, 255, 0.12);
        }

        .ring-2 {
            width: 560px;
            height: 560px;
            border-color: rgba(118, 153, 255, 0.14);
        }

        .paperlens-brain {
            position: absolute;
            left: 50%;
            top: 50%;
            width: 250px;
            height: 250px;
            transform: translate(-50%, -50%);
            border-radius: 50%;
            background: radial-gradient(circle at 50% 45%, rgba(120, 229, 255, 0.9), rgba(94, 146, 255, 0.52) 28%, rgba(15, 24, 37, 0.9) 62%, rgba(7, 12, 20, 1) 100%);
            border: 1px solid rgba(134, 196, 255, 0.32);
            box-shadow: 0 0 30px rgba(73, 181, 255, 0.32), inset 0 0 30px rgba(142, 220, 255, 0.15);
        }

        .paperlens-brain::before, .paperlens-brain::after {
            content: "";
            position: absolute;
            inset: 18px;
            border-radius: 50%;
            border: 1px solid rgba(125, 208, 255, 0.18);
        }

        .paperlens-brain::after {
            inset: 42px;
            border-color: rgba(142, 204, 255, 0.12);
        }

        .paperlens-network {
            position: absolute;
            inset: 0;
        }

        .node {
            position: absolute;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: linear-gradient(180deg, #dff9ff, #6ad7ff);
            box-shadow: 0 0 16px rgba(113, 216, 255, 0.9);
        }

        .node.n1 { left: 24%; top: 24%; }
        .node.n2 { left: 50%; top: 16%; }
        .node.n3 { right: 23%; top: 24%; }
        .node.n4 { left: 16%; top: 50%; }
        .node.n5 { left: 50%; top: 50%; }
        .node.n6 { right: 18%; top: 50%; }
        .node.n7 { left: 28%; bottom: 18%; }
        .node.n8 { left: 50%; bottom: 12%; }
        .node.n9 { right: 26%; bottom: 18%; }

        .line {
            position: absolute;
            height: 1px;
            background: linear-gradient(90deg, rgba(135, 195, 255, 0), rgba(135, 195, 255, 0.7), rgba(135, 195, 255, 0));
            opacity: 0.9;
        }

        .line.l1 { width: 200px; left: 30%; top: 24%; transform: rotate(18deg); }
        .line.l2 { width: 180px; left: 37%; top: 20%; transform: rotate(-28deg); }
        .line.l3 { width: 210px; left: 25%; top: 50%; transform: rotate(8deg); }
        .line.l4 { width: 160px; left: 42%; top: 48%; transform: rotate(-16deg); }
        .line.l5 { width: 170px; left: 30%; top: 64%; transform: rotate(-28deg); }
        .line.l6 { width: 180px; left: 46%; top: 64%; transform: rotate(26deg); }

        .chip {
            position: absolute;
            padding: 10px 16px;
            border-radius: 999px;
            background: rgba(8, 17, 31, 0.8);
            border: 1px solid rgba(124, 184, 255, 0.26);
            color: #d9edff;
            font-size: 0.68rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            box-shadow: 0 0 22px rgba(88, 163, 255, 0.12);
        }

        .chip.top-left { left: 11%; top: 18%; }
        .chip.bottom-right { right: 11%; bottom: 15%; }

        .paperlens-copy {
            max-width: 560px;
        }

        .mini-label {
            display: inline-block;
            margin: 0 0 1rem;
            font-size: 0.7rem;
            letter-spacing: 0.28em;
            text-transform: uppercase;
            color: var(--cyan);
            font-weight: 600;
        }

        .paperlens-copy h1 {
            margin: 0;
            font-size: clamp(3rem, 4vw, 5.2rem) !important;
            line-height: 0.96 !important;
            letter-spacing: -0.07em !important;
            color: var(--text) !important;
        }

        .paperlens-copy .tagline {
            display: block;
            margin-top: 0.5rem;
            letter-spacing: -0.04em;
            color: #deebff;
            font-weight: 500;
        }

        .paperlens-copy p {
            margin: 1.5rem 0 2rem;
            color: var(--muted);
            font-size: 1.08rem;
            line-height: 1.75;
            max-width: 510px;
        }

        div[data-testid="stSelectbox"] > div {
            background: rgba(14, 22, 34, 0.9);
            border: 1px solid rgba(141, 180, 255, 0.24);
            border-radius: 16px;
            min-height: 54px;
            box-shadow: none;
        }

        div[data-testid="stSelectbox"] label {
            color: #cfe0ff !important;
            font-size: 1.02rem !important;
            margin-bottom: 0.5rem !important;
        }

        div[data-testid="stBaseButton-secondary"],
        button[kind="secondary"],
        button[kind="primary"] {
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(123, 196, 255, 0.8);
            border-radius: 999px;
            color: #edf7ff;
            font-weight: 600;
            height: 52px;
            padding: 0 1.5rem;
            box-shadow: 0 0 18px rgba(90, 170, 255, 0.12);
            transition: all 0.2s ease;
        }

        button[kind="secondary"]:hover,
        button[kind="primary"]:hover {
            transform: translateY(-1px);
            box-shadow: 0 0 24px rgba(90, 170, 255, 0.2);
            border-color: rgba(148, 216, 255, 1);
        }

        .stButton {
            margin-top: 0.25rem;
        }

        .result-box {
            margin-top: 1.5rem;
            padding: 1rem 1.1rem;
            border-radius: 18px;
            border: 1px solid rgba(123, 191, 255, 0.24);
            background: rgba(10, 18, 28, 0.7);
            color: #dfeeff;
            box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02);
        }

        .result-box h3 {
            margin: 0 0 0.75rem;
            color: #e9f6ff;
            font-size: 1rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .result-box p {
            margin: 0;
            line-height: 1.8;
            color: #dfeafc;
        }

        @media (max-width: 980px) {
            .paperlens-hero {
                grid-template-columns: 1fr;
                gap: 1.2rem;
            }

            .paperlens-copy {
                text-align: center;
                margin: 0 auto;
            }

            .paperlens-copy p {
                margin-left: auto;
                margin-right: auto;
            }

            .paperlens-visual {
                height: 500px;
            }
        }

        @media (max-width: 640px) {
            .paperlens-visual {
                height: 390px;
            }

            .paperlens-ring {
                width: 290px;
                height: 290px;
            }

            .ring-2 {
                width: 360px;
                height: 360px;
            }

            .paperlens-brain {
                width: 165px;
                height: 165px;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def build_prompt(paper_input: str, style_input: str, length_input: str):
    template = load_prompt('template.json')
    return template.invoke(
        {
            'paper_input': paper_input,
            'style_input': style_input,
            'length_input': length_input,
        }
    )


with st.container():
    st.markdown('<div class="paperlens-shell">', unsafe_allow_html=True)
    left_col, right_col = st.columns([1.15, 0.85], gap='large')

    with left_col:
        st.markdown(
            """
            <div class="paperlens-visual">
                <div class="paperlens-ring"></div>
                <div class="paperlens-ring ring-2"></div>
                <div class="paperlens-network">
                    <div class="line l1"></div>
                    <div class="line l2"></div>
                    <div class="line l3"></div>
                    <div class="line l4"></div>
                    <div class="line l5"></div>
                    <div class="line l6"></div>
                    <div class="node n1"></div>
                    <div class="node n2"></div>
                    <div class="node n3"></div>
                    <div class="node n4"></div>
                    <div class="node n5"></div>
                    <div class="node n6"></div>
                    <div class="node n7"></div>
                    <div class="node n8"></div>
                    <div class="node n9"></div>
                </div>
                <div class="chip top-left">Neural Core</div>
                <div class="chip bottom-right">Insight Engine</div>
                <div class="paperlens-brain"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right_col:
        st.markdown('<div class="paperlens-copy">', unsafe_allow_html=True)
        st.markdown('<div class="mini-label">RESEARCH INTELLIGENCE</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <h1>PaperLens AI<br><span class="tagline">Turn Research Into Clarity</span></h1>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <p>An AI-powered research tool that reads and summarizes research papers, helping you quickly understand complex ideas, findings, and key insights.</p>
            """,
            unsafe_allow_html=True,
        )

        paper_input = st.selectbox(
            'Select your paper',
            [
                'Attention is All you need',
                'BERT: Pre training of deep bidirectional transformers',
                'GPT-3: Language models are Few shot learners',
                'Diffusion Models Beats GANs on image synthesis',
            ],
        )
        style_input = st.selectbox(
            'Select your input style',
            ['Beginer friendly', 'Technical', 'Code oriented', 'Mathematics'],
        )
        length_input = st.selectbox(
            'Select your input length',
            ['Short (1-2 paragraph)', 'Medium (3-5 paragraph)', 'Long detailed knowledge'],
        )

        if st.button('Explore Research →', use_container_width=True):
            token = os.getenv('huggingface_api_key')
            if not token:
                st.error('Missing Hugging Face token. Add huggingface_api_key to your .env file.')
            else:
                try:
                    llm = HuggingFaceEndpoint(
                        repo_id='TinyLlama/TinyLlama-1.1B-Chat-v1.0',
                        task='text-generation',
                        huggingfacehub_api_token=token,
                        temperature=0.7,
                        max_new_tokens=256,
                    )
                    model = ChatHuggingFace(llm=llm)
                    prompt = build_prompt(paper_input, style_input, length_input)
                    with st.spinner('Analyzing research paper...'):
                        result = model.invoke(prompt)
                    summary = escape(result.content if hasattr(result, 'content') else str(result))
                    summary = summary.replace('\n', '<br>')
                    st.markdown(
                        f"""
                        <div class="result-box">
                            <h3>Research Summary</h3>
                            <p>{summary}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                except Exception as exc:
                    st.error(f'Failed to generate summary. Please try again.\n\n{exc}')

        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
