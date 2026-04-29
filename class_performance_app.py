import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import io
import hashlib

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Class Performance Dashboard",
    page_icon="🎓",
    layout="wide",
)

# ══════════════════════════════════════════════════════════════════════════════
#  AUTH — USER CREDENTIALS  (username : {password_hash, role, display_name})
#  Role can be "admin" or "staff"
#  To add a new user, add an entry below.
#  Password is stored as SHA-256 hash for basic security.
# ══════════════════════════════════════════════════════════════════════════════
def _hash(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

USERS = {
    "admin": {
        "password": _hash("admin123"),
        "role": "admin",
        "display": "Administrator",
    },
    "staff1": {
        "password": _hash("staff123"),
        "role": "staff",
        "display": "Prof. Ramesh Kumar",
    },
    "staff2": {
        "password": _hash("staff456"),
        "role": "staff",
        "display": "Prof. Anitha Nair",
    },
    "staff3": {
        "password": _hash("staff789"),
        "role": "staff",
        "display": "Prof. Suresh Babu",
    },
}

# ── Session-state defaults ─────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in  = False
    st.session_state.username   = ""
    st.session_state.role       = ""
    st.session_state.display    = ""
    st.session_state.login_err  = ""

# ══════════════════════════════════════════════════════════════════════════════
#  LOGIN PAGE  — shown when not authenticated
# ══════════════════════════════════════════════════════════════════════════════
def show_login():
    # login page styling — override the global blue theme with white text for dark bg
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp {
        background: linear-gradient(135deg, #0d2137 0%, #1a3a5c 50%, #0d2137 100%) !important;
    }
    [data-testid="stSidebar"] { display: none; }

    /* Force all text on login page to white */
    .stApp label,
    .stApp .stMarkdown p,
    .stApp .stMarkdown h1,
    .stApp .stMarkdown h2,
    .stApp .stMarkdown h3,
    .stApp .stMarkdown h4,
    .stApp p, .stApp span, .stApp div,
    .stApp .stTextInput label,
    .stApp .stTextInput p,
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] label {
        color: #ffffff !important;
    }

    /* Input box — dark text on white background, clearly readable */
    .stApp .stTextInput input {
        color: #0e3551 !important;
        background-color: #ffffff !important;
        border: 1.5px solid #4a7ab5 !important;
        border-radius: 6px !important;
        font-size: 1rem !important;
        padding: 10px 14px !important;
    }
    .stApp .stTextInput input::placeholder {
        color: #7a9bbf !important;
        opacity: 1 !important;
    }
    /* Input label — bold and clearly white */
    .stApp .stTextInput > label,
    .stApp .stTextInput > div > label,
    [data-testid="stTextInput"] label,
    [data-testid="stTextInput"] p {
        color: #e8f4ff !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        margin-bottom: 4px !important;
    }

    /* Login button — solid blue with bright white text */
    .stApp .stButton > button {
        background-color: #1a6abf !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 0.03em !important;
        padding: 10px 0 !important;
        border-radius: 6px !important;
        transition: background-color 0.2s ease !important;
    }
    .stApp .stButton > button:hover {
        background-color: #1558a3 !important;
        color: #ffffff !important;
    }

    /* Caption text slightly dimmed white */
    .stApp .stCaption, .stApp small {
        color: #b0cce8 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # centred card
    _, col, _ = st.columns([1, 1.4, 1])
    with col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(
                "<h2 style='text-align:center; color:#dbeeff;'>🎓 ClassPerf</h2>"
                "<p style='text-align:center; color:#7aafd4; margin-top:-10px;'>"
                "Class Performance Dashboard</p><hr style='border-color:#2a4a6a;'>",
                unsafe_allow_html=True,
            )
            st.markdown("<p style='color:#ffffff; font-size:1.1rem; font-weight:600;'>🔐 Staff / Admin Login</p>", unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")

            if st.session_state.login_err:
                st.error(st.session_state.login_err)

            if st.button("Login", use_container_width=True):
                user = USERS.get(username.strip().lower())
                if user and user["password"] == _hash(password):
                    st.session_state.logged_in = True
                    st.session_state.username  = username.strip().lower()
                    st.session_state.role      = user["role"]
                    st.session_state.display   = user["display"]
                    st.session_state.login_err = ""
                    st.rerun()
                else:
                    st.session_state.login_err = "❌ Invalid username or password."
                    st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
            st.caption("🔒 Authorised personnel only. Contact admin for access.")

            st.markdown("""
            <div style='background:#0d2137; border-radius:6px; padding:10px; margin-top:8px;
                        font-size:0.78rem; color:#7aafd4;'>
            <b>Demo credentials</b><br>
            Admin &nbsp;→ <code>admin</code> / <code>admin123</code><br>
            Staff &nbsp;&nbsp;→ <code>staff1</code> / <code>staff123</code>
            </div>
            """, unsafe_allow_html=True)

# ── Route: show login or dashboard ────────────────────────────────────────────
if not st.session_state.logged_in:
    show_login()
    st.stop()

# ── Minimal inline styling (blue theme + color tweaks) ───────────────────────
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #87ceeb, #b0e0e6) !important;
    }
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url("https://www.eurokidsindia.com/blog/wp-content/uploads/2023/10/improve-academic-performance-870x570.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        opacity: 0.15;
        z-index: 0;
        pointer-events: none;
    }
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        color: #0e3551 !important;
    }
    [data-testid="stToolbar"],
    [data-testid="stHeader"] {
        background-color: #ffffff !important;
    }
    label {
        color: #1a1a2e !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ── Subject metadata ───────────────────────────────────────────────────────────
SUBJECTS = ["PPDS", "EP", "EM2", "DS", "UHV"]
SUBJECT_NAMES = {
    "PPDS": "Python Programming for Data Science",
    "EP":   "Engineering Physics",
    "EM2":  "Engineering Mathematics 2",
    "DS":   "Data Structures",
    "UHV":  "Universal Human Languages",
}
CREDITS = {"PPDS": 3, "EP": 3, "EM2": 4, "DS": 4, "UHV": 3}
PASS_MARK = 50

# ── Built-in dataset (40 students, realistic spread, a few absents & failures) ──
SAMPLE_DATA = {
    "NAME": [
        "Aarav Shah",       "Ananya Iyer",      "Rithvik Menon",    "Divya Krishnan",
        "Karthik Raju",     "Sneha Pillai",      "Arjun Nair",       "Priya Suresh",
        "Vivek Chandran",   "Meera Raj",         "Nikhil Bose",      "Sana Qureshi",
        "Tarun Gupta",      "Lakshmi Venkat",    "Rohit Patel",      "Ishita Das",
        "Arun Kumar",       "Nithya Mohan",      "Siddharth Jain",   "Pooja Reddy",
        "Harish Balaji",    "Keerthana Nair",    "Pranav Sharma",    "Deepika Rao",
        "Vishnu Prasad",    "Amrita Menon",      "Surya Prakash",    "Kavitha Subramanian",
        "Lokesh Pandey",    "Revathi Krishnan",  "Abhijit Desai",    "Chitra Venkatesh",
        "Manoj Pillai",     "Saranya Rajan",     "Dinesh Kumar",     "Varsha Nambiar",
        "Suresh Babu",      "Pavithra Shankar",  "Ganesh Murthy",    "Bhavana Reddy",
    ],
    "Roll No": list(range(101, 141)),
    "PPDS": [
        88, 72, 45, 91, 63, 78, 55, 82, 40, 95,
        67, 74, 88, 51, 60, 79, "Ab", 84, 73, 66,
        92, 58, 77, 83, 47, 89, 61, 70, 38, 96,
        54, 80, 65, 43, 71, 86, 59, 75, "Ab", 68,
    ],
    "EP": [
        76, 68, 52, 85, 48, 70, 61, 77, 55, 90,
        58, 80, 71, 44, 65, 83, 72, 69, 55, 78,
        88, 63, 74, 91, 50, 82, 46, 67, 53, 94,
        60, 77, 70, 39, 85, 73, 56, 81, 64, 79,
    ],
    "EM2": [
        82, 75, 38, 88, 71, 65, 50, 79, 47, 92,
        63, 70, 84, 55, 58, 76, 68, 91, 60, 72,
        95, 57, 80, 87, 44, 78, 53, 66, 41, 98,
        62, 83, 69, 48, 76, 90, 55, 73, 61, 84,
    ],
    "DS": [
        79, 80, 60, 94, 55, 73, 48, 85, 52, 97,
        70, 66, 76, 49, 62, 88, 75, 80, 67, 74,
        91, 54, 83, 89, 43, 86, 57, 72, 46, 99,
        65, 78, 71, 37, 82, 88, 60, 76, "Ab", 81,
    ],
    "UHV": [
        90, 85, 70, 78, 80, 88, 75, 92, 65, 88,
        72, 83, 95, 68, 77, 91, 80, 86, 74, 82,
        89, 76, 84, 93, 71, 87, 68, 79, 62, 96,
        73, 90, 78, 55, 85, 92, 69, 83, 77, 88,
    ],
}

# ── Helper: load & compute ─────────────────────────────────────────────────────
@st.cache_data
def load_data(df_raw: pd.DataFrame) -> pd.DataFrame:
    df = df_raw.copy()
    if "NAME" in df.columns:
        df.set_index("NAME", inplace=True)
        df.index.name = "NAME"
    df.replace(["ab", "Ab", "AB", "ab ", "AB "], np.nan, inplace=True)
    for col in SUBJECTS + ["Roll No"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["Total"]   = df[SUBJECTS].sum(axis=1)
    df["Average"] = (df["Total"] / len(SUBJECTS)).round(2)
    return df


def compute_stats(df: pd.DataFrame):
    stats = {}
    # pass / fail
    stats["fail_count"]    = (df[SUBJECTS] < PASS_MARK).sum()
    stats["pass_percent"]  = ((df[SUBJECTS] >= PASS_MARK).sum() / len(df) * 100).round(1)
    stats["subject_avg"]   = df[SUBJECTS].mean().round(1)

    # rank list — passed ALL subjects with no missing marks
    passed = df[df[SUBJECTS].notnull().all(axis=1) & (df[SUBJECTS] >= PASS_MARK).all(axis=1)].copy()
    passed["Rank"] = passed["Total"].rank(ascending=False, method="min").astype(int)
    stats["ranklist"] = passed.sort_values("Rank")

    # subject-wise toppers
    toppers = {}
    for s in SUBJECTS:
        col = df[s].dropna()
        if not col.empty:
            idx = col.idxmax()
            toppers[s] = (idx, int(col[idx]))
    stats["toppers"] = toppers
    return stats

# ── Matplotlib theme helper ────────────────────────────────────────────────────
PALETTE = ["#00ADB5", "#FF6F61", "#6A67CE", "#2ECC71", "#F39C12"]

def fig_to_img(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=130, facecolor=fig.get_facecolor())
    buf.seek(0)
    return buf

# ═══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.title("🎓 ClassPerf")
    st.caption("Class Performance Analyser")
    st.divider()

    # ── User info & logout ─────────────────────────────────────────────────────
    role_badge = "🛡️ Admin" if st.session_state.role == "admin" else "👤 Staff"
    st.markdown(f"**{st.session_state.display}**")
    st.caption(role_badge)
    if st.button("🚪 Logout", use_container_width=True):
        for key in ["logged_in", "username", "role", "display", "login_err"]:
            st.session_state[key] = "" if key != "logged_in" else False
        st.rerun()
    st.divider()

    raw_df = pd.DataFrame(SAMPLE_DATA)
    st.success(f"✅ {len(raw_df)} students loaded")

    st.divider()
    st.markdown("**Subjects & Credits**")
    for s, name in SUBJECT_NAMES.items():
        st.markdown(f"- **{s}** ({CREDITS[s]} cr) — {name}")

# ── Process ────────────────────────────────────────────────────────────────────
df   = load_data(raw_df)
stats = compute_stats(df)

# ═══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ═══════════════════════════════════════════════════════════════════════════════
st.title("📊 Class Performance Dashboard")
st.caption("Comprehensive analysis of student marks across all subjects")
st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
#  KPI ROW
# ═══════════════════════════════════════════════════════════════════════════════
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Students",  len(df))
k2.metric("Class Average",   f"{df['Average'].mean():.1f}")
k3.metric("Highest Total",   int(df['Total'].max()))
k4.metric("Lowest Total",    int(df['Total'].min()))
k5.metric("Rank List Size",  len(stats["ranklist"]))

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
#  TABS
# ═══════════════════════════════════════════════════════════════════════════════
IS_ADMIN = st.session_state.role == "admin"

if IS_ADMIN:
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📋 Dataset",
        "🏆 Rankings & Toppers",
        "📈 Student-wise Analysis",
        "📚 Subject-wise Analysis",
        "🥧 Overall Summary",
        "🛡️ Admin Panel",
    ])
else:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Dataset",
        "🏆 Rankings & Toppers",
        "📈 Student-wise Analysis",
        "📚 Subject-wise Analysis",
        "🥧 Overall Summary",
    ])

# ─── TAB 1 : Dataset ──────────────────────────────────────────────────────────
with tab1:
    st.subheader("Class Performance Data")

    display_df = df.copy()
    display_df.index.name = "NAME"

    # colour cells: <50 red, >=50 green, NaN grey
    def colour_marks(val):
        if pd.isna(val):
            return "background-color: #f0f0f0; color: #999"
        try:
            v = float(val)
            if v < PASS_MARK:
                return "background-color: #ffe0e0; color: #c0392b; font-weight:600"
            return "background-color: #e0f7e9; color: #1e8449; font-weight:600"
        except:
            return ""

    styled = display_df[["Roll No"] + SUBJECTS + ["Total", "Average"]].style\
        .apply(lambda col: col.map(colour_marks), subset=SUBJECTS)\
        .format(precision=1, na_rep="Absent")\
        .set_properties(**{"text-align": "center"})

    st.dataframe(styled, width='stretch', height=520)

    col_dl, _ = st.columns([1, 4])
    csv_bytes = df.to_csv().encode()
    col_dl.download_button("⬇️ Download CSV", csv_bytes, "class_performance_processed.csv", "text/csv")

    st.divider()
    st.subheader("Absence Summary")
    absent = df[SUBJECTS].isnull().sum()
    a1, a2 = st.columns(2)
    a1.dataframe(absent.rename("Absent Count").to_frame(), width='stretch')
    ab_students = df[df[SUBJECTS].isnull().any(axis=1)][SUBJECTS]
    a2.dataframe(ab_students.fillna("Absent"), width='stretch')

# ─── TAB 2 : Rankings & Toppers ───────────────────────────────────────────────
with tab2:
    left, right = st.columns([1.2, 1])

    with left:
        st.subheader("🏅 Full Rank List")
        rl = stats["ranklist"][["Roll No"] + SUBJECTS + ["Total", "Average", "Rank"]].copy()
        rl.index.name = "NAME"

        def highlight_top3(row):
            rank = row["Rank"]
            if rank == 1:   return ["background-color:#FFD700; font-weight:700"] * len(row)
            if rank == 2:   return ["background-color:#C0C0C0; font-weight:700"] * len(row)
            if rank == 3:   return ["background-color:#CD7F32; font-weight:700"] * len(row)
            return [""] * len(row)

        st.dataframe(
            rl.style.apply(highlight_top3, axis=1).format(precision=1),
            width='stretch',
            height=420,
        )

    with right:
        st.subheader("🥇 Top 3 Rank Holders")
        top3 = stats["ranklist"].nsmallest(3, "Rank")
        medals = ["🥇", "🥈", "🥉"]
        for i, (name, row) in enumerate(top3.iterrows()):
            with st.container(border=True):
                st.markdown(f"### {medals[i]} {name}")
                c1, c2, c3 = st.columns(3)
                c1.metric("Rank",    int(row["Rank"]))
                c2.metric("Total",   int(row["Total"]))
                c3.metric("Average", f"{row['Average']:.1f}")

        st.divider()
        st.subheader("⭐ Subject-wise Toppers")
        for s, (name, marks) in stats["toppers"].items():
            with st.container(border=True):
                tc1, tc2 = st.columns([2, 1])
                tc1.markdown(f"**{s}** — {SUBJECT_NAMES[s][:30]}…")
                tc1.caption(f"👤 {name}")
                tc2.metric("Score", marks)

# ─── TAB 3 : Student-wise Analysis ────────────────────────────────────────────
with tab3:
    st.subheader("Student-wise Performance")

    mode = st.radio("View mode", ["All Students (Average Bar Chart)", "Individual Student"], horizontal=True)

    if mode == "All Students (Average Bar Chart)":
        plot_df = df[["Average"]].dropna()
        fig, ax = plt.subplots(figsize=(18, 7))
        fig.patch.set_facecolor("#0e1117")
        ax.set_facecolor("#0e1117")

        x = np.arange(len(plot_df))
        ax.bar(x, plot_df["Average"], width=0.6, color=PALETTE[0], alpha=0.85,
               edgecolor="white", linewidth=0.3)

        ax.set_xticks(x)
        ax.set_xticklabels(plot_df.index, rotation=60, ha="right", color="white", fontsize=8)
        ax.set_yticks(range(0, 101, 10))
        ax.set_yticklabels(range(0, 101, 10), color="white")
        ax.set_ylabel("Average Score", color="white")
        ax.set_xlabel("Students", color="white")
        ax.set_title("Student-wise Average Performance", color="white",
                     fontsize=16, fontweight="bold", pad=14)
        ax.tick_params(colors="white")
        ax.spines[:].set_color("#f1e6d6")
        ax.grid(axis="y", linestyle="--", alpha=0.3, color="white")
        ax.axhline(PASS_MARK, color="#FF6F61", linewidth=1.2, linestyle="--", label="Pass Mark (50)")
        ax.legend(framealpha=0.15, labelcolor="white", edgecolor="#555")
        st.pyplot(fig, width='stretch')
        plt.close(fig)

    else:
        student = st.selectbox("Select a student", df.index.tolist())
        row = df.loc[student]

        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        fig.patch.set_facecolor("#0e1117")
        fig.suptitle(f"Performance of {student}", color="white", fontsize=14, fontweight="bold")

        # bar
        ax = axes[0]
        ax.set_facecolor("#0e1117")
        marks = [row[s] if pd.notna(row[s]) else 0 for s in SUBJECTS]
        bars = ax.bar(SUBJECTS, marks, color=PALETTE, edgecolor="white", linewidth=0.5)
        ax.axhline(PASS_MARK, color="#FF6F61", linewidth=1.2, linestyle="--")
        for bar, m in zip(bars, marks):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    str(int(m)) if m >= 0 else "0", ha="center", color="white", fontsize=10, fontweight="bold")
        ax.set_ylim(0, 110)
        ax.set_yticks(range(0, 101, 10))
        ax.set_yticklabels(range(0, 101, 10), color="white")
        ax.set_xticklabels(SUBJECTS, color="white")
        ax.tick_params(colors="white")
        ax.spines[:].set_color("#f1e6d6")
        ax.set_facecolor("#0e1117")
        ax.grid(axis="y", linestyle="--", alpha=0.3, color="white")
        ax.set_title("Marks per Subject", color="white")

        # radar
        ax2 = axes[1]
        ax2.remove()
        ax2 = fig.add_subplot(1, 2, 2, polar=True)
        ax2.set_facecolor("#0e1117")
        N = len(SUBJECTS)
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
        angles += angles[:1]
        vals = marks + marks[:1]
        ax2.plot(angles, vals, color=PALETTE[0], linewidth=2)
        ax2.fill(angles, vals, color=PALETTE[0], alpha=0.25)
        ax2.set_xticks(angles[:-1])
        ax2.set_xticklabels(SUBJECTS, color="white", fontsize=9)
        ax2.set_yticklabels([], color="white")
        ax2.set_ylim(0, 100)
        ax2.set_title("Radar Chart", color="white", pad=14)
        ax2.spines["polar"].set_color("#f1e6d6")
        ax2.grid(color="#f1e6d6")

        st.pyplot(fig, width='stretch')
        plt.close(fig)

        mc1, mc2, mc3, mc4 = st.columns(4)
        mc1.metric("Total",   f"{int(row['Total'])} / {len(SUBJECTS)*100}")
        mc2.metric("Average", f"{row['Average']:.1f}")
        mc3.metric("Passed", sum(1 for s in SUBJECTS if pd.notna(row[s]) and row[s] >= PASS_MARK))
        mc4.metric("Failed",  sum(1 for s in SUBJECTS if pd.notna(row[s]) and row[s] < PASS_MARK))

# ─── TAB 4 : Subject-wise Analysis ────────────────────────────────────────────
with tab4:
    st.subheader("Subject-wise Analysis")

    view = st.selectbox("Choose subject", SUBJECTS,
                        format_func=lambda s: f"{s} — {SUBJECT_NAMES[s]}")
    col_data = df[view].dropna()

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.patch.set_facecolor("#0e1117")
    color = PALETTE[SUBJECTS.index(view)]

    # distribution
    ax = axes[0]
    ax.set_facecolor("#0e1117")
    ax.hist(col_data, bins=10, color=color, edgecolor="white", linewidth=0.5, alpha=0.85)
    ax.axvline(PASS_MARK, color="#FF6F61", linewidth=1.5, linestyle="--", label="Pass Mark")
    ax.axvline(col_data.mean(), color="#FFD700", linewidth=1.5, linestyle="-.", label=f"Mean={col_data.mean():.1f}")
    ax.set_title(f"{view} — Distribution", color="white")
    ax.set_facecolor("#0e1117")
    ax.tick_params(colors="white"); ax.spines[:].set_color("#f1e6d6")
    ax.set_xlabel("Marks", color="white"); ax.set_ylabel("Count", color="white")
    legend = ax.legend(framealpha=0.15, labelcolor="white", edgecolor="#555")
    ax.grid(axis="y", linestyle="--", alpha=0.3, color="white")

    # line trend (student index)
    ax2 = axes[1]
    ax2.set_facecolor("#0e1117")
    ax2.plot(range(len(col_data)), col_data.values, marker="o", color=color,
             linewidth=2, markersize=4, markeredgecolor="white", markeredgewidth=0.5)
    ax2.axhline(PASS_MARK, color="#FF6F61", linewidth=1.2, linestyle="--")
    ax2.set_title(f"{view} — Trend Across Students", color="white")
    ax2.tick_params(colors="white"); ax2.spines[:].set_color("#f1e6d6")
    ax2.set_xlabel("Student Index", color="white"); ax2.set_ylabel("Marks", color="white")
    ax2.grid(linestyle="--", alpha=0.3, color="white")
    ax2.set_ylim(0, 110)

    # pass/fail pie
    ax3 = axes[2]
    ax3.set_facecolor("#0e1117")
    passed = (col_data >= PASS_MARK).sum()
    failed = (col_data < PASS_MARK).sum()
    wedges, texts, autotexts = ax3.pie(
        [passed, failed],
        labels=["Pass", "Fail"],
        autopct="%1.1f%%",
        colors=["#2ECC71", "#FF6F61"],
        startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 1.2},
    )
    for t in texts + autotexts:
        t.set_color("white"); t.set_fontweight("bold")
    ax3.set_title(f"{view} — Pass / Fail", color="white")

    plt.tight_layout()
    st.pyplot(fig, width='stretch')
    plt.close(fig)

    # stats row
    s1, s2, s3, s4, s5 = st.columns(5)
    s1.metric("Mean",   f"{col_data.mean():.1f}")
    s2.metric("Median", f"{col_data.median():.1f}")
    s3.metric("Std Dev",f"{col_data.std():.1f}")
    s4.metric("Highest",int(col_data.max()))
    s5.metric("Lowest", int(col_data.min()))

    st.divider()
    st.subheader("All 5 Subjects — Side-by-Side Line Plots")
    fig2, axes2 = plt.subplots(2, 3, figsize=(18, 9))
    fig2.patch.set_facecolor("#0e1117")
    axes2_flat = axes2.flatten()
    for i, (subj, color_) in enumerate(zip(SUBJECTS, PALETTE)):
        ax_ = axes2_flat[i]
        ax_.set_facecolor("#0e1117")
        data_ = df[subj].dropna()
        ax_.plot(range(len(data_)), data_.values, marker="o", color=color_,
                 linewidth=2, markersize=4, markeredgecolor="white", markeredgewidth=0.5)
        ax_.axhline(PASS_MARK, color="#FF6F61", linewidth=1, linestyle="--")
        ax_.set_title(subj, color="white", fontweight="bold")
        ax_.tick_params(colors="white"); ax_.spines[:].set_color("#f1e6d6")
        ax_.set_xlabel("Student Index", color="white", fontsize=8)
        ax_.set_ylabel("Marks", color="white", fontsize=8)
        ax_.grid(linestyle="--", alpha=0.25, color="white")
        ax_.set_ylim(0, 110)
    axes2_flat[-1].set_visible(False)
    fig2.suptitle("Subject-wise Analysis for All Students", color="white",
                  fontsize=16, fontweight="bold")
    plt.tight_layout()
    st.pyplot(fig2, width='stretch')
    plt.close(fig2)

# ─── TAB 5 : Overall Summary ──────────────────────────────────────────────────
with tab5:
    st.subheader("Overall Class Summary")

    left, right = st.columns(2)

    with left:
        # pie of subject averages
        subject_avg = stats["subject_avg"]
        fig, ax = plt.subplots(figsize=(6, 6))
        fig.patch.set_facecolor("#0e1117")
        ax.set_facecolor("#0e1117")
        colors_p = sns.color_palette("Set2", len(SUBJECTS))
        wedges, texts, autotexts = ax.pie(
            subject_avg.values,
            labels=SUBJECTS,
            autopct="%1.1f%%",
            colors=colors_p,
            startangle=90,
            explode=[0.04] * len(SUBJECTS),
            shadow=True,
            wedgeprops={"edgecolor": "black", "linewidth": 1},
        )
        for t in texts + autotexts:
            t.set_color("white"); t.set_fontweight("bold")
        ax.set_title("Subject Average Contribution", color="white",
                     fontsize=13, fontweight="bold")
        st.pyplot(fig, width='stretch')
        plt.close(fig)

    with right:
        # heatmap
        fig, ax = plt.subplots(figsize=(7, 6))
        fig.patch.set_facecolor("#0e1117")
        heat_data = df[SUBJECTS].apply(pd.to_numeric, errors="coerce")
        sns.heatmap(
            heat_data,
            ax=ax,
            cmap="RdYlGn",
            linewidths=0.3,
            linecolor="#222",
            annot=True,
            fmt=".0f",
            annot_kws={"size": 7},
            vmin=0, vmax=100,
            cbar_kws={"shrink": 0.8},
        )
        ax.set_title("Marks Heatmap (All Students × Subjects)",
                     color="white", fontsize=11, fontweight="bold")
        ax.tick_params(axis="x", colors="white", labelsize=8)
        ax.tick_params(axis="y", colors="white", labelsize=7, rotation=0)
        plt.tight_layout()
        st.pyplot(fig, width='stretch')
        plt.close(fig)

    st.divider()
    st.subheader("Pass % and Failures per Subject")
    summary_df = pd.DataFrame({
        "Subject":        [SUBJECT_NAMES[s] for s in SUBJECTS],
        "Average Mark":   stats["subject_avg"].values,
        "Pass %":         stats["pass_percent"].values,
        "Failures":       stats["fail_count"].values.astype(int),
        "Topper":         [f"{stats['toppers'][s][0]} ({stats['toppers'][s][1]})" for s in SUBJECTS],
    })
    st.dataframe(summary_df.set_index("Subject"), width='stretch')

    st.divider()
    # Boxplot
    st.subheader("Score Distribution (Box Plot)")
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#0e1117")
    ax.set_facecolor("#0e1117")
    box_data = [df[s].dropna().values for s in SUBJECTS]
    bp = ax.boxplot(box_data, patch_artist=True, notch=False,
                    medianprops={"color": "white", "linewidth": 2})
    for patch, color in zip(bp["boxes"], PALETTE):
        patch.set_facecolor(color); patch.set_alpha(0.75)
    for element in ["whiskers", "fliers", "caps"]:
        for item in bp[element]:
            item.set_color("#aaa")
    ax.set_xticks(range(1, len(SUBJECTS)+1))
    ax.set_xticklabels(SUBJECTS, color="white")
    ax.set_yticklabels(ax.get_yticks(), color="white")
    ax.set_ylabel("Marks", color="white")
    ax.axhline(PASS_MARK, color="#FF6F61", linewidth=1.2, linestyle="--", label="Pass Mark (50)")
    ax.legend(framealpha=0.2, labelcolor="white", edgecolor="#555")
    ax.grid(axis="y", linestyle="--", alpha=0.3, color="white")
    ax.spines[:].set_color("#333")
    ax.tick_params(colors="white")
    st.pyplot(fig, width='stretch')
    plt.close(fig)

# ─── TAB 6 : Admin Panel (admin only) ─────────────────────────────────────────
if IS_ADMIN:
    with tab6:
        st.subheader("🛡️ Admin Panel")
        st.caption("Only visible to administrators.")
        st.divider()

        # ── Section 1: User accounts ───────────────────────────────────────────
        st.markdown("### 👥 Registered Users")

        user_rows = []
        for uname, udata in USERS.items():
            user_rows.append({
                "Username":     uname,
                "Display Name": udata["display"],
                "Role":         udata["role"].capitalize(),
                "Status":       "🟢 Active",
            })
        user_df = pd.DataFrame(user_rows)

        def style_role(val):
            if val == "Admin":
                return "background-color:#1f4f8d; color:white; font-weight:700; border-radius:4px;"
            return "background-color:#2d6a4f; color:white; border-radius:4px;"

        st.dataframe(
            user_df.style.map(style_role, subset=["Role"]),
            use_container_width=True,
            hide_index=True,
        )

        st.divider()

        # ── Section 2: Add new staff (demo — shows generated hash) ────────────
        st.markdown("### ➕ Add New Staff Account")
        st.info(
            "In production, copy the generated password hash into the USERS dictionary in the source code.",
            icon="ℹ️",
        )

        with st.container(border=True):
            c1, c2, c3 = st.columns(3)
            new_user    = c1.text_input("Username",     placeholder="e.g. staff4")
            new_display = c2.text_input("Display Name", placeholder="e.g. Prof. Kavya Menon")
            new_role    = c3.selectbox("Role", ["staff", "admin"])
            new_pw      = st.text_input("Temporary Password", type="password", placeholder="Set a password")

            if st.button("Generate Account Entry", use_container_width=True):
                if new_user and new_pw and new_display:
                    h = _hash(new_pw)
                    st.success("✅ Copy the entry below into the USERS dict in your source code:")
                    st.code(
                        f'"{new_user}": {{\n'
                        f'    "password": "{h}",\n'
                        f'    "role": "{new_role}",\n'
                        f'    "display": "{new_display}",\n'
                        f'}},',
                        language="python",
                    )
                else:
                    st.warning("Please fill in all fields.")

        st.divider()

        # ── Section 3: Access log (session activity) ───────────────────────────
        st.markdown("### 📋 Current Session Info")
        with st.container(border=True):
            i1, i2 = st.columns(2)
            i1.metric("Logged-in User", st.session_state.display)
            i2.metric("Role",           st.session_state.role.capitalize())

        st.divider()

        # ── Section 4: Quick class stats for admin ─────────────────────────────
        st.markdown("### 📊 Quick Class Statistics")
        qa1, qa2, qa3, qa4 = st.columns(4)
        qa1.metric("Total Students",  len(df))
        qa2.metric("Class Average",   f"{df['Average'].mean():.1f}")
        qa3.metric("Students on Rank List", len(stats["ranklist"]))
        total_absent = int(df[SUBJECTS].isnull().sum().sum())
        qa4.metric("Total Absent Entries", total_absent)

        st.markdown("**Subject-wise Pass % at a glance**")
        pass_df = pd.DataFrame({
            "Subject":      [SUBJECT_NAMES[s] for s in SUBJECTS],
            "Pass %":       stats["pass_percent"].values,
            "Failures":     stats["fail_count"].values.astype(int),
            "Avg Mark":     stats["subject_avg"].values,
        })
        st.dataframe(pass_df.set_index("Subject"), use_container_width=True)
