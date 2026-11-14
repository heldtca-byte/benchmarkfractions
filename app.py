import random
import streamlit as st

st.set_page_config(
    page_title="Benchmark Fractions Explorer",
    page_icon="➗",
    layout="centered",
)

# Initialize session state for Quiz Mode
if "quiz_num" not in st.session_state:
    st.session_state.quiz_den = random.choice([3, 4, 5, 6, 8, 10, 12])
    st.session_state.quiz_num = random.randint(0, st.session_state.quiz_den)
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.feedback = None
    st.session_state.answered = False


def get_closest_benchmark(n, d):
    val = n / d
    dist_0 = abs(val - 0.0)
    dist_half = abs(val - 0.5)
    dist_1 = abs(val - 1.0)

    min_dist = min(dist_0, dist_half, dist_1)
    if min_dist == dist_1:
        return 1.0, "1"
    elif min_dist == dist_half:
        return 0.5, "½"
    else:
        return 0.0, "0"


def draw_fraction_visual(
    n, d, show_shaded=True, highlight_benchmark=None
):
    """Renders an HTML visual comparison of the fraction bar against 0, 1/2, and 1."""
    part_width = 100 / d
    boxes_html = "".join(
        f'<div style="width:{part_width}%; height:44px; '
        f'background-color:{"#3B82F6" if (i < n and show_shaded) else "#F8FAFC"}; '
        f'border-right:2px solid #1E293B; box-sizing:border-box;"></div>'
        for i in range(d)
    )

    c0 = "#16A34A" if highlight_benchmark == 0.0 else "#64748B"
    ch = "#16A34A" if highlight_benchmark == 0.5 else "#64748B"
    c1 = "#16A34A" if highlight_benchmark == 1.0 else "#64748B"

    html = (
        '<div style="font-family:sans-serif; background:white; padding:24px 30px; '
        'border-radius:12px; border:1px solid #CBD5E1; margin: 12px 0;">'
        f'<div style="font-weight:bold; font-size:20px; color:#1E3A8A; margin-bottom:8px;">Fraction: {n}/{d}</div>'
        f'<div style="display:flex; width:100%; border:2px solid #1E293B; border-right:none; border-radius:4px; overflow:hidden;">{boxes_html}</div>'
        '<div style="margin-top:28px; position:relative; height:36px; background:#F1F5F9; border:2px solid #64748B; border-radius:4px;">'
        '<div style="position:absolute; left:50%; top:-8px; bottom:-8px; width:3px; background:#DC2626;"></div>'
        '</div>'
        '<div style="display:flex; justify-content:space-between; margin-top:10px; font-weight:bold; font-size:18px;">'
        f'<span style="color:{c0};">● 0</span>'
        f'<span style="color:{ch};">● ½</span>'
        f'<span style="color:{c1};">● 1</span>'
        '</div>'
        '</div>'
    )
    st.html(html)


def next_question():
    st.session_state.quiz_den = random.choice([3, 4, 5, 6, 8, 10, 12])
    st.session_state.quiz_num = random.randint(0, st.session_state.quiz_den)
    st.session_state.feedback = None
    st.session_state.answered = False


# --- UI Layout ---
st.title("➗ Benchmark Fractions Explorer (0, ½, 1)")
st.write(
    "Explore how fractions compare to the three main benchmarks: **0**, **½**, and **1**."
)

mode = st.radio(
    "Choose Mode:",
    ["Sandbox Explorer", "Practice Quiz"],
    horizontal=True,
)

if mode == "Sandbox Explorer":
    col1, col2 = st.columns(2)
    with col1:
        den = st.slider("Denominator (Bottom Number)", min_value=1, max_value=12, value=8)
    with col2:
        num = st.slider("Numerator (Top Number)", min_value=0, max_value=den, value=min(3, den))

    closest_val, closest_str = get_closest_benchmark(num, den)
    draw_fraction_visual(
        num, den, show_shaded=True, highlight_benchmark=closest_val
    )

    half_of_den = den / 2
    if num == 0:
        reason = "0 pieces shaded means the fraction equals **0**."
    elif num == den:
        reason = f"All {den} pieces are shaded, which equals **1 whole**!"
    elif num == half_of_den:
        reason = f"{num} is exactly half of {den}, so it equals **½**!"
    else:
        reason = (
            f"Half of {den} is **{half_of_den:g}**. Since {num} is closest to "
            f"**{closest_str}**, the closest benchmark is **{closest_str}**."
        )

    st.success(f"**{num}/{den} is closest to {closest_str}** — {reason}")

else:
    qn = st.session_state.quiz_num
    qd = st.session_state.quiz_den
    correct_val, correct_str = get_closest_benchmark(qn, qd)

    st.subheader(f"Which benchmark is **{qn}/{qd}** closest to?")
    st.caption("Hint: Compare the numerator to half of the denominator!")

    draw_fraction_visual(
        qn,
        qd,
        show_shaded=st.session_state.answered,
        highlight_benchmark=correct_val if st.session_state.answered else None,
    )

    if not st.session_state.answered:
        b1, b2, b3 = st.columns(3)
        for col, label, choice in [
            (b1, "Closest to 0", 0.0),
            (b2, "Closest to ½", 0.5),
            (b3, "Closest to 1", 1.0),
        ]:
            if col.button(label, use_container_width=True):
                st.session_state.total += 1
                st.session_state.answered = True
                if choice == correct_val:
                    st.session_state.score += 1
                    st.session_state.feedback = (
                        "success",
                        f"Correct! **{qn}/{qd}** is closest to **{correct_str}**.",
                    )
                else:
                    st.session_state.feedback = (
                        "error",
                        f"Not quite! **{qn}/{qd}** is closest to **{correct_str}** "
                        f"(half of {qd} is {qd/2:g}).",
                    )
                st.rerun()

    if st.session_state.feedback:
        msg_type, msg_text = st.session_state.feedback
        if msg_type == "success":
            st.success(msg_text)
        else:
            st.error(msg_text)

        if st.button("Next Question ➡️", type="primary"):
            next_question()
            st.rerun()

    st.divider()
    st.markdown(f"**Score:** {st.session_state.score} / {st.session_state.total}")
