import streamlit as st
import subprocess
import json

st.set_page_config(page_title="LaTeX Learning App", page_icon="📝", layout="wide")

# -----------------------------
# LLM via Ollama CLI
# -----------------------------
OLLAMA_MODEL = "llama3"

def ask_llm_ollama(prompt: str, model: str = OLLAMA_MODEL):
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        st.error("⚠️ AI model error. Please check your Ollama setup.")
        print(f"Ollama error: {e.stderr}")  # Logs for debugging
        return ""

# -----------------------------
# Styles
# -----------------------------
st.markdown("""
<style>
.block-container {padding-top: 2rem; padding-bottom: 3rem;}
textarea, .stTextArea>div>textarea {font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;}
[data-testid="stMetricValue"] {font-weight: 700;}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LaTeX Helpers
# -----------------------------
PAIR_MAP = {"{": "}", "(": ")", "[": "]"}

def validate_latex(s: str):
    stack = []
    for i, ch in enumerate(s):
        if ch in PAIR_MAP:
            stack.append(ch)
        elif ch in PAIR_MAP.values():
            if not stack:
                return False, f"Unmatched closing bracket/brace at position {i}."
            last = stack.pop()
            if PAIR_MAP[last] != ch:
                return False, f"Mismatched brackets/braces at position {i}."
    if stack:
        return False, f"Unmatched opening bracket/brace: {stack[-1]}"
    if s.strip() == "":
        return False, "Input is empty."
    return True, ""

def render_latex(s: str):
    ok, msg = validate_latex(s)
    if not ok:
        st.error(f"⚠️ {msg}")
        return
    try:
        st.latex(s)
    except Exception as e:
        st.error(f"⚠️ LaTeX rendering error: {e}")

# ==============================
# Shared Topics & Quiz Bank
# ==============================
# ==============================
# Shared Topics & Quiz Bank
# ==============================
TOPICS = {
    "Basics": (
        "Introduction to LaTeX document structure, classes, and comments.\n"
        "Learn how to set up a minimal LaTeX document and include comments for clarity.",
        r"""
\documentclass{article}          % Defines the document class
\begin{document}                  % Start of document content
Hello World!                       % Simple text output
% This is a comment                % Comments start with %
\end{document}                    % End of document
"""
    ),

    "Math Mode": (
        "Learn how to typeset mathematics in LaTeX.\n"
        "Inline math uses `$...$` while display math can use `$$...$$` or `\[...\]` for better formatting.",
        r"""
% Inline math example
$a^2 + b^2 = c^2$

% Display math example
\[
\sum_{i=1}^n i^2
\]
"""
    ),

    "Text Formatting": (
        "Formatting text using bold, italics, underline, and lists.\n"
        "Useful for emphasizing content in your documents.",
        r"""
\textbf{Bold Text}, \textit{Italic Text}, \underline{Underlined Text}

\begin{itemize}                  % Bullet list
    \item First item
    \item Second item
\end{itemize}
"""
    ),

    "Symbols": (
        "Common mathematical symbols and Greek letters.\n"
        "Essential for writing equations and scientific notation.",
        r"""
Greek letters: \alpha, \beta, \gamma

Mathematical symbols: \infty, \pm, \le, \ge
"""
    ),

    "Equations": (
        "Using equation environments to create numbered or aligned equations.\n"
        "Best practice: use `amsmath` for multi-line equations.",
        r"""
\begin{align}
a + b &= c \\
x + y &= z
\end{align}
"""
    ),

    "Figures & Tables": (
        "Insert and format figures and tables using float environments.\n"
        "Allows captions, labels, and positioning for clarity.",
        r"""
\begin{figure}[h]
\centering
\includegraphics[width=0.5\textwidth]{example.png}
\caption{Sample Figure}
\end{figure}

\begin{table}[h]
\centering
\begin{tabular}{|c|c|}
\hline
A & B \\
\hline
1 & 2 \\
\hline
\end{tabular}
\caption{Sample Table}
\end{table}
"""
    ),

    "Fractions & Roots": (
        "Learn to typeset fractions, square roots, and nth roots.\n"
        "Important for mathematical derivations and scientific writing.",
        r"""
\frac{a+b}{c}           % Fraction
\sqrt{x^2 + y^2}        % Square root
\sqrt[n]{x}             % nth root
"""
    ),

    "Summations & Integrals": (
        "Summation and integral notation.\n"
        "Widely used in mathematics, physics, and engineering documents.",
        r"""
\sum_{k=1}^{n} k^2       % Summation
\int_0^1 x^2 \, dx       % Definite integral
"""
    ),

    "Limits": (
        "Express limits and use arrows correctly.\n"
        "Important for calculus and analysis.",
        r"""
\lim_{x \to 0} \frac{\sin x}{x} = 1
"""
    ),

    "Matrices": (
        "Create matrices using environments like `bmatrix` or `pmatrix`.\n"
        "Essential for linear algebra and system equations.",
        r"""
\begin{bmatrix}
1 & 2 \\
3 & 4
\end{bmatrix}

\begin{pmatrix}
1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & 1
\end{pmatrix}
"""
    ),

    "Cases": (
        "Define piecewise functions using the `cases` environment.\n"
        "Useful for conditional mathematical expressions.",
        r"""
f(x) = 
\begin{cases} 
x^2 & x \ge 0 \\
-x & x < 0
\end{cases}
"""
    ),

    "Vectors": (
        "Represent vectors in LaTeX using arrows or bold symbols.\n"
        "Widely used in physics and engineering notation.",
        r"""
\vec{v} = \langle 1, 2, 3 \rangle
\mathbf{u}                 % Bold vector
\mathbf{u} \cdot \mathbf{v}  % Dot product
\|v\|                     % Vector norm
"""
    ),

    "Alignment": (
        "Align equations for readability using the `aligned` environment.\n"
        "Helps in showing step-by-step derivations neatly.",
        r"""
\begin{aligned}
a + b &= c \\
d - e &= f
\end{aligned}
"""
    ),
}


QUIZ = {
    "Basics": [
        {"q": "Which command defines the document class?", "a": r"\documentclass{article}", "options": [r"\begin{document}", r"\documentclass{article}", r"\maketitle", r"\usepackage{article}"]},
        {"q": "Which environment encloses the document body?", "a": r"\begin{document}...\end{document}", "options": [r"\begin{body}...\end{body}", r"\begin{text}...\end{text}", r"\begin{document}...\end{document}", r"\document{...}"]},
        {"q": "What symbol starts a comment?", "a": r"%", "options": ["#", "%", "//", "$"]},
        {"q": "Minimal hello world class line?", "a": r"\documentclass{article}", "options": [r"\document{article}", r"\documentclass{article}", r"\class{article}", r"\usepackage{article}"]},
        {"q": "Write a TODO comment.", "a": r"% TODO", "options": [r"\/TODO", r"% TODO", r"$ TODO", r"# TODO"]},
    ],
    "Math Mode": [
        {"q": "Inline math delimiters?", "a": r"$...$", "options": [r"$...$", r"$$...$$", r"\(...\)", r"\[...\]"]},
        {"q": "Display math (preferred LaTeX)?", "a": r"\[...\]", "options": [r"$...$", r"$$...$$", r"\[...\]", r"\display{...}"]},
        {"q": "Write E=mc^2 inline.", "a": r"$E=mc^2$", "options": [r"$E=mc^2$", r"\[E=mc^2\]", r"$$E=mc^2$$", r"E=mc^2"]},
        {"q": "Sum i=1..n of i^2 (display).", "a": r"\[\sum_{i=1}^{n} i^2\]", "options": [r"$\sum_{i=1}^{n} i^2$", r"\[\sum_{i=1}^{n} i^2\]", r"\display{\sum i^2}", r"\{ \sum i^2 \}"]},
        {"q": "Escape recommended for dx spacing?", "a": r"\,", "options": [r"\:", r"\;", r"\,", r"\!"]},
    ],
    "Text Formatting": [
        {"q": "Bold ‘Hello’.", "a": r"\textbf{Hello}", "options": [r"\bold{Hello}", r"\textbf{Hello}", r"\bf{Hello}", r"\strong{Hello}"]},
        {"q": "Italic ‘World’.", "a": r"\textit{World}", "options": [r"\italic{World}", r"\em{World}", r"\textit{World}", r"\emph{World}"]},
        {"q": "Underline ‘LaTeX’.", "a": r"\underline{LaTeX}", "options": [r"\ul{LaTeX}", r"\uline{LaTeX}", r"\underline{LaTeX}", r"\textul{LaTeX}"]},
        {"q": "Start itemized list.", "a": r"\begin{itemize}", "options": [r"\begin{list}", r"\begin{items}", r"\begin{itemize}", r"\begin{enumerate}"]},
        {"q": "End itemized list.", "a": r"\end{itemize}", "options": [r"\end{items}", r"\end{list}", r"\end{enumerate}", r"\end{itemize}"]},
    ],
    "Symbols": [
        {"q": "Alpha and beta commands.", "a": r"\alpha \; \beta", "options": [r"\a \; \b", r"\alpha \; \beta", r"\greek{alpha,beta}", r"\ab"]},
        {"q": "Infinity symbol.", "a": r"\infty", "options": [r"\inf", r"\infin", r"\infty", r"\Infinity"]},
        {"q": "Plus-minus.", "a": r"\pm", "options": [r"\plusminus", r"\pm", r"\pmm", r"\mp"]},
        {"q": "Less-than-or-equal.", "a": r"\le", "options": [r"\le", r"\lte", r"\<= ", r"\less="]},
        {"q": "Greater-than-or-equal.", "a": r"\ge", "options": [r"\ge", r"\gte", r"\>=", r"\great="]},
    ],
    "Equations": [
        {"q": "Open equation env.", "a": r"\begin{equation}", "options": [r"\begin{eq}", r"\begin{equation}", r"\eq{", r"\equation{"]},
        {"q": "Close equation env.", "a": r"\end{equation}", "options": [r"\end{eq}", r"\equation}", r"\end{equation}", r"}"]},
        {"q": "Open align env.", "a": r"\begin{align}", "options": [r"\begin{aligned}", r"\align{", r"\begin{align}", r"\begin{aln}"]},
        {"q": "Close align env.", "a": r"\end{align}", "options": [r"\end{aligned}", r"\align}", r"\end{align}", r"}"]},
        {"q": "Aligned a+b=c in align.", "a": r"\begin{align} a+b&=c \end{align}", "options": [r"\begin{align} a+b=c \end{align}", r"\begin{align} a+b&=c \end{align}", r"\align{a+b=c}", r"a+b=c"]},
    ],
    "Figures & Tables": [
        {"q": "Open figure env.", "a": r"\begin{figure}", "options": [r"\figure{", r"\begin{figure}", r"\fig{", r"\begin{image}"]},
        {"q": "Close figure env.", "a": r"\end{figure}", "options": [r"\end{image}", r"\end{fig}", r"\end{figure}", r"}"]},
        {"q": "Open tabular env.", "a": r"\begin{tabular}", "options": [r"\begin{table}", r"\begin{tab}", r"\begin{tabular}", r"\table{"]},
        {"q": "Close tabular env.", "a": r"\end{tabular}", "options": [r"\end{table}", r"\end{tab}", r"\end{tabular}", r"}"]},
        {"q": "Caption command (blank).", "a": r"\caption{}", "options": [r"\cap{}", r"\caption{}", r"\title{}", r"\figcaption{}"]},
    ],
    "Fractions & Roots": [
        {"q": "a/b as a fraction.", "a": r"\frac{a}{b}", "options": [r"\divide{a}{b}", r"\frac{a}{b}", r"\frac{a,b}", r"a/b"]},
        {"q": "Square root of x.", "a": r"\sqrt{x}", "options": [r"\root{x}", r"\sqrt{x}", r"\sq{x}", r"\sqr{x}"]},
        {"q": "nth root of x.", "a": r"\sqrt[n]{x}", "options": [r"\root[n]{x}", r"\sqrt[n]{x}", r"\nthroot{x}{n}", r"\powerroot{n}{x}"]},
        {"q": "(a+b)/c as fraction.", "a": r"\frac{a+b}{c}", "options": [r"\frac{a+b}{c}", r"\frac{a+b,c}", r"{a+b}/c", r"\frac{a}{b}/c"]},
        {"q": "sqrt(x^2 + y^2).", "a": r"\sqrt{x^2 + y^2}", "options": [r"\sqrt{x^2 + y^2}", r"\sqrt{x^2 + y^2)}", r"\sqrt{x^2 + y^2}}", r"\sqrt{x^2 + y^2]"]},
    ],
    "Summations & Integrals": [
        {"q": "sum k=1..n of k.", "a": r"\sum_{k=1}^{n} k", "options": [r"\sum_{k=1}^{n} k", r"\sum k", r"sum(k)", r"\add_{k=1}^{n} k"]},
        {"q": "sum of squares 1..n.", "a": r"\sum_{k=1}^{n} k^2", "options": [r"\sum_{k=1}^{n} k^2", r"\sum k^2", r"\sigma k^2", r"\sum_{k=1}^n k^2"]},
        {"q": "∫ x from 0 to 1.", "a": r"\int_0^1 x \, dx", "options": [r"\int_0^1 x dx", r"\int_0^1 x \, dx", r"\int^1_0 x \, dx", r"\int x dx"]},
        {"q": "∫ e^{-x} from 0 to ∞.", "a": r"\int_0^{\infty} e^{-x} \, dx", "options": [r"\int_0^{\infty} e^{-x} \, dx", r"\int_0^\infty e^{-x} dx", r"\int e^{-x}", r"\int_0^\infty e^{-x} \, dx"]},
        {"q": "Thin space command used above.", "a": r"\,", "options": [r"\thin", r"\ ", r"\,", r"\~"]},
    ],
    "Limits": [
        {"q": "lim x→0 sin x/x.", "a": r"\lim_{x \to 0} \frac{\sin x}{x}", "options": [r"\lim_{x \to 0} \frac{\sin x}{x}", r"\lim_{x=0} \sin x/x", r"limit(sin x/x)", r"\lim \sin x/x"]},
        {"q": "lim x→∞ (1+1/x)^x.", "a": r"\lim_{x \to \infty} \left(1+\tfrac{1}{x}\right)^x", "options": [r"\lim_{x \to \infty} (1+1/x)^x", r"\lim_{x \to \infty} \left(1+\tfrac{1}{x}\right)^x", r"(1+1/x)^x", r"\lim \tfrac{1}{x}"]},
        {"q": "lim x→0 (1−cos x)/x^2.", "a": r"\lim_{x \to 0} \frac{1-\cos x}{x^2}", "options": [r"\lim_{x \to 0} \frac{1-\cos x}{x^2}", r"(1-\cos x)/x^2", r"\frac{1-\cos x}{x^2}", r"\lim_{x=0} \frac{1-\cos x}{x^2}"]},
        {"q": "Arrow for → in limits.", "a": r"\to", "options": [r"->", r"\rightarrow", r"\to", r"\Rightarrow"]},
        {"q": "Spacing command (just type it).", "a": r"\,", "options": [r"\;", r"\,", r"\:", r"\!"]},
    ],
    "Matrices": [
        {"q": "2x2 bmatrix [[1,2],[3,4]].", "a": r"\begin{bmatrix}1 & 2 \\ 3 & 4\end{bmatrix}", "options": [r"\begin{bmatrix}1,2;3,4\end{bmatrix}", r"\begin{bmatrix}1 & 2 \\ 3 & 4\end{bmatrix}", r"[1 2;3 4]", r"\matrix{1 2; 3 4}"]},
        {"q": "Identity 3x3 bmatrix.", "a": r"\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}", "options": [r"\begin{bmatrix}1 0 0; 0 1 0; 0 0 1\end{bmatrix}", r"\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}", r"\Id_{3}", r"\begin{matrix}...\end{matrix}"]},
        {"q": "Open pmatrix.", "a": r"\begin{pmatrix}", "options": [r"\pmatrix{", r"\begin{pmatrix}", r"\pmatrix()", r"\begin{matrix}"]},
        {"q": "Close pmatrix.", "a": r"\end{pmatrix}", "options": [r"\pmatrix}", r"\end{pmatrix}", r"\end{matrix}", r"}"]},
        {"q": "Row separator command.", "a": r"\\\\", "options": [r"&", r"\\", r"\\\\", r"\;"]},
    ],
    "Cases": [
        {"q": "Open a cases env.", "a": r"\begin{cases}", "options": [r"\begin{case}", r"\cases{", r"\begin{cases}", r"\case{"]},
        {"q": "Close a cases env.", "a": r"\end{cases}", "options": [r"\case}", r"\end{case}", r"\end{cases}", r"}"]},
        {"q": "f(x)=x if x≥0 else -x (cases only).", "a": r"\begin{cases}x & x\ge 0 \\ -x & x<0 \end{cases}", "options": [r"x if x>=0 else -x", r"\begin{cases}x & x\ge 0 \\ -x & x<0 \end{cases}", r"\cases{x,-x}", r"\{x,-x\}"]},
        {"q": "Symbol for ≥.", "a": r"\ge", "options": [r">=", r"\geq", r"\ge", r"\gtr="]},
        {"q": "Symbol for <.", "a": r"<", "options": [r"\lt", r"<", r"\less", r"\lss"]},
    ],
    "Vectors": [
        {"q": "Vector v with arrow.", "a": r"\vec{v}", "options": [r"\vector{v}", r"\vec{v}", r"\overrightarrow{v}", r"\v{v}"]},
        {"q": "Bold vector u.", "a": r"\mathbf{u}", "options": [r"\bold{u}", r"\vec{u}", r"\mathbf{u}", r"\textbf{u}"]},
        {"q": "Angle-bracket vector <1,2,3>.", "a": r"\langle 1,2,3\rangle", "options": [r"<1,2,3>", r"\langle 1,2,3\rangle", r"\<1,2,3\>", r"\left<1,2,3\right>"]},
        {"q": "Dot product u·v.", "a": r"\mathbf{u}\cdot\mathbf{v}", "options": [r"u*v", r"\mathbf{u}\cdot\mathbf{v}", r"\vec{u}\cdot\vec{v}", r"u.v"]},
        {"q": "Norm ||v||.", "a": r"\|v\|", "options": [r"|v|", r"\|v\|", r"\norm{v}", r"\abs{v}"]},
    ],
    "Alignment": [
        {"q": "Open aligned env.", "a": r"\begin{aligned}", "options": [r"\begin{align}", r"\begin{aligned}", r"\aligned{", r"\align{"]},
        {"q": "Close aligned env.", "a": r"\end{aligned}", "options": [r"\end{align}", r"\aligned}", r"\end{aligned}", r"}"]},
        {"q": "Align a+b=c and d-e=f.", "a": r"\begin{aligned} a+b&=c \\ d-e&=f \end{aligned}", "options": [r"a+b=c; d-e=f", r"\begin{aligned} a+b&=c \\ d-e&=f \end{aligned}", r"\begin{aligned} a+b=c \\ d-e=f \end{aligned}", r"\align{a+b=c}"]},
        {"q": "Alignment marker symbol.", "a": r"&", "options": [r"@", r"&", r"#", r"|"]},
        {"q": "Line break in align/aligned.", "a": r"\\\\", "options": [r"\n", r"\\", r"\\\\", r"&"]},
    ],
}

# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.title("📝 LaTeX Learning App")
section = st.sidebar.radio("Choose Section", ["Home", "Mini Compiler", "Teacher", "Quiz"])

# -----------------------------
# Home
# -----------------------------
if section == "Home":
    st.title("🎓 Welcome to the LaTeX Learning App")
    colA, colB = st.columns([1.2, 1])
    with colA:
        st.markdown("""
**Learn, practice, and test** your LaTeX skills — all in one place.

**What you can do:**
- 🖋 **Mini Compiler**: Type LaTeX and see output instantly.
- 📖 **Teacher**: Explore topics with notes and try examples side-by-side.
- 🎯 **Quiz**: Practice questions per topic with instant feedback and a running score.
- ➕ **Generate New Questions**: Get fresh questions automatically via AI.
        """)
    with colB:
        st.info("Quick Start")
        st.markdown("- Go to **Mini Compiler** and paste any LaTeX.\n- Visit **Teacher** to learn a topic, then **Quiz** it!")

# -----------------------------
# Mini Compiler
# -----------------------------
elif section == "Mini Compiler":
    st.title("🖋 Mini LaTeX Compiler")

    if "compiler_code" not in st.session_state:
        st.session_state.compiler_code = r"E=mc^2"

    tab_editor, tab_ai = st.tabs(["✍️ Editor & Preview", "🤖 AI Helper"])

    # -----------------------------
    # Tab 1: Editor + Preview
    # -----------------------------
    with tab_editor:
        col_editor, col_preview = st.columns([1, 1])

        # Editor
        with col_editor:
            st.subheader("Editor")
            btn_frac, btn_sum, btn_matrix = st.columns(3)
            if btn_frac.button("➗ Fraction"):
                st.session_state.compiler_code += "\n\\frac{a}{b}"
            if btn_sum.button("∑ Summation"):
                st.session_state.compiler_code += "\n\\sum_{i=1}^n"
            if btn_matrix.button("📐 Matrix"):
                st.session_state.compiler_code += "\n\\begin{bmatrix} a & b \\\\ c & d \\end{bmatrix}"

            st.session_state.compiler_code = st.text_area(
                "Write your LaTeX here",
                value=st.session_state.compiler_code,
                height=150
            )

            # Show syntax-highlighted code
            st.code(st.session_state.compiler_code, language="latex")

            btn_clear, btn_download = st.columns(2)
            with btn_clear:
                if st.button("🧹 Clear"):
                    st.session_state.compiler_code = ""
            with btn_download:
                st.download_button("💾 Download .tex", st.session_state.compiler_code, file_name="document.tex")

        # Preview
        with col_preview:
            st.subheader("👀 Live Preview")
            render_latex(st.session_state.compiler_code)

    # -----------------------------
    # Tab 2: AI Helper
    # -----------------------------
    with tab_ai:
        st.subheader("🤖 AI Helper (Explain / Debug / Suggest)")
        prompt = st.text_area("Describe your question or paste LaTeX to debug:", height=250, key="compiler_ai_input_tab")
        if st.button("Ask AI about my LaTeX", key="ai_compiler_btn"):
            full_prompt = f"""You are a helpful LaTeX assistant. The user wrote:

{prompt or st.session_state.compiler_code}

Tasks:
1) If there are syntax issues, pinpoint them and show a fixed snippet.
2) Explain briefly why.
3) Provide 1-2 improved suggestions or best practices.
Respond in markdown, include LaTeX fenced blocks when relevant.
"""
            resp_text = ask_llm_ollama(full_prompt)
            st.markdown(resp_text, unsafe_allow_html=True)

# -----------------------------
# Teacher
# -----------------------------
elif section == "Teacher":
    st.title("📖 LaTeX Teacher")
    topic = st.selectbox("📚 Choose a topic", list(TOPICS.keys()))
    note, example = TOPICS[topic]

    tab_notes, tab_ai = st.tabs(["📌 Notes & Practice", "🤖 AI Tutor"])

    # -----------------------------
    # Tab 1: Notes + Practice
    # -----------------------------
    with tab_notes:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.info(note)
            code = st.text_area("Try it here", value=example, height=250, key=f"teacher_{topic}_practice")
        with col2:
            st.subheader("Live Preview")
            render_latex(code)

    
    # -----------------------------
    # Tab 2: AI Tutor
    # -----------------------------
    with tab_ai:
        st.subheader("🤖 AI Tutor")
        st.caption("Ask me to explain, simplify, or extend the topic!")

        if "tutor_history" not in st.session_state:
            st.session_state.tutor_history = []

        user_question = st.text_area(
            "Type your question about this topic (e.g. 'Explain matrices in simple words')",
            key=f"teacher_ai_input_{topic}"
        )

        if st.button("Ask AI Tutor", key=f"teacher_ai_btn_{topic}"):
            full_prompt = f"""
You are a LaTeX tutor. The student is learning the topic: **{topic}**.

Here are the official notes:
{note}

Here is an example code:
{example}

Now the student asked:
{user_question}

Your tasks:
1. Explain the concept in simple, student-friendly words.
2. Provide a corrected or improved LaTeX snippet if useful.
3. Add 1 short tip or best practice.
Respond in **markdown**.
"""
            ai_response = ask_llm_ollama(full_prompt)

            st.session_state.tutor_history.append(("Student", user_question))
            st.session_state.tutor_history.append(("Tutor", ai_response))

        # Display conversation
        for role, msg in st.session_state.tutor_history:
            if role == "Student":
                st.markdown(f"**🧑 You:** {msg}")
            else:
                st.success(msg)

# -----------------------------
# Quiz
# -----------------------------
elif section == "Quiz":
    import re  # <- ensure this import exists somewhere in your file

    st.title("🎯 LaTeX Quiz")
    st.caption("Choose a topic, answer questions, get feedback, track progress, and generate new questions!")

    topic = st.selectbox("📚 Quiz Topic", list(QUIZ.keys()))

    # ------------------ Session state setup ------------------
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "attempted" not in st.session_state:
        st.session_state.attempted = set()
    if "review" not in st.session_state:
        st.session_state.review = []
    # Persist a working, editable copy of the question bank across reruns
    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = {t: list(QUIZ[t]) for t in QUIZ}

    st.metric("Score", st.session_state.score)

    # ------------------ Helpers ------------------
    def clean_label(s: str) -> str:
        """
        Remove a leading label like 'A) ', 'B.', 'c -', etc.
        """
        return re.sub(r'^\s*[A-Da-d]\s*[\)\.\:\-]\s*', '', str(s)).strip()

    def letter_to_index(a: str):
        """
        Turn 'A', 'A)', 'A.' etc. into 0, 'B'->1 ...
        Returns None if not a simple letter answer.
        """
        if not isinstance(a, str):
            return None
        m = re.match(r'^\s*([A-Da-d])\s*[\)\.\:\-]?\s*$', a)
        return (ord(m.group(1).upper()) - ord('A')) if m else None

    def norm(s: str) -> str:
        """
        Normalize for comparison (trim + collapse whitespace).
        Don't lowercase because LaTeX commands are case-sensitive, but we do
        collapse spaces to be forgiving about spacing.
        """
        return re.sub(r'\s+', ' ', str(s).strip())

    # ------------------ Generate New Question ------------------
    if st.button("➕ Generate New Question"):
        prompt = f"""
        Generate a new LaTeX quiz question on topic '{topic}'.
        Include 4 options, mark the correct one.
        Respond ONLY in JSON in this exact format:
        {{
          "q": "Question text",
          "a": "Correct option (letter like A/B/C/D OR full option text)",
          "options": ["A) ...", "B) ...", "C) ...", "D) ..."]
        }}
        """
        new_q_json = ask_llm_ollama(prompt)

        # Try to parse strict JSON; then fallback to extracting the JSON substring
        def try_parse_json(raw: str):
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                start, end = raw.find("{"), raw.rfind("}") + 1
                if start != -1 and end != -1:
                    try:
                        return json.loads(raw[start:end])
                    except:
                        return None
                return None

        new_q = try_parse_json(new_q_json)

        # Validate & normalize the new question
        if new_q and isinstance(new_q.get("options"), list) and new_q.get("q") and new_q.get("a"):
            # Convert letter answer to the *text* of the corresponding option
            idx = letter_to_index(new_q["a"])
            if idx is not None and 0 <= idx < len(new_q["options"]):
                # If options carry labels like "A) ...", strip them from the final answer
                new_q["a"] = clean_label(new_q["options"][idx])
            else:
                # If 'a' is text, make sure it's cleaned (remove accidental labels)
                new_q["a"] = clean_label(new_q["a"])

            # Store the raw options as given; we will clean them for display on the fly
            st.session_state.quiz_data[topic].append(new_q)
            st.success("✅ New question added! Scroll down to answer it.")
        else:
            st.error(f"⚠️ Failed to generate question. Raw output:\n\n{new_q_json}")

    # ------------------ Display All Questions ------------------
    q_list = st.session_state.quiz_data[topic]

    for q_idx, q in enumerate(q_list):
        # Initialize radio state
        radio_key = f"selected_{topic}_{q_idx}"
        if radio_key not in st.session_state:
            st.session_state[radio_key] = None

        # Safely extract only the option text (remove "A) ", "B) " if present)
        options_text = [clean_label(opt) for opt in q["options"]]

        with st.expander(f"Question {q_idx+1} of {len(q_list)}", expanded=True):
            st.warning(q["q"])
            ans = st.radio("Options", options_text, key=radio_key)

            if st.button("✅ Check Answer", key=f"check_{topic}_{q_idx}"):
                if ans is None:
                    st.info("ℹ️ Please select an option first.")
                else:
                    # Determine the correct answer text robustly
                    # If q["a"] is letter-like, map to option text; else clean it.
                    idx = letter_to_index(q["a"])
                    if idx is not None and 0 <= idx < len(options_text):
                        correct_text = options_text[idx]
                    else:
                        correct_text = clean_label(q["a"])

                    if norm(ans) == norm(correct_text):
                        st.success("🎉 Correct!")
                        if f"{topic}_{q_idx}" not in st.session_state.attempted:
                            st.session_state.score += 1
                            st.session_state.attempted.add(f"{topic}_{q_idx}")
                    else:
                        st.error(f"❌ Not quite. Correct answer: {correct_text}")

                    st.session_state.review.append((q["q"], correct_text, ans))

    # ------------------ Review Section ------------------
    if st.session_state.review:
        with st.expander("📋 Review Attempted Questions", expanded=False):
            for qq, correct, given in st.session_state.review:
                if norm(given) == norm(correct):  # ✅ Correct
                    st.success(f"**Q:** {qq}\n\n✅ Correct: `{correct}`  |  📝 Your Answer: `{given}`")
                else:  # ❌ Wrong
                    st.error(f"**Q:** {qq}\n\n❌ Correct: `{correct}`  |  📝 Your Answer: `{given}`")

