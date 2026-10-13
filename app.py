
import streamlit as st
from minimax import best_warden_move
from html import escape

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Minimax Escape Room",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# CUSTOM DASHBOARD STYLING
# ==========================================

st.markdown("""
<style>
    .stApp {
        background:
            radial-gradient(
                ellipse at top left,
                #172554 0%,
                #0f172a 40%,
                #080f1e 100%
            );
        color: #f8fafc;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3, h4 {
        color: #f8fafc !important;
    }

    p, label {
        color: #e2e8f0;
    }

    /* Main header */
    .game-header {
        padding: 24px;
        border-radius: 18px;
        background: linear-gradient(
            120deg, #1e3a8a, #312e81, #172554
        );
        border: 1px solid #475569;
        margin-bottom: 20px;
    }

    .game-header h1 {
        font-size: clamp(25px, 4vw, 38px);
        font-weight: 850;
        margin: 0;
        color: #ffffff !important;
    }

    .game-header p {
        color: #c7d2fe;
        margin: 8px 0 0;
        font-size: 15px;
    }

    /* Level label */
    .level-badge {
        display: inline-block;
        background: #3730a3;
        color: #ffffff;
        border: 1px solid #818cf8;
        padding: 8px 15px;
        border-radius: 30px;
        font-weight: 700;
        margin-bottom: 12px;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: #1e293b;
        border: 1px solid #475569;
        border-radius: 16px;
        padding: 18px 16px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.18);
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] * {
        color: #cbd5e1 !important;
        font-size: 15px !important;
        font-weight: 650 !important;
    }

    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] * {
        color: #ffffff !important;
        font-size: clamp(22px, 2.6vw, 31px) !important;
        font-weight: 800 !important;
    }

    /* Game board */
    .game-cell {
        width: 100%;
        aspect-ratio: 1 / 1;
        min-height: 38px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #25344e;
        border: 1px solid #435575;
        border-radius: 10px;
        font-size: clamp(17px, 2.4vw, 30px);
        box-sizing: border-box;
        transition: background 0.2s;
    }

    .game-cell.player {
        background: #1d4ed8;
        border: 2px solid #93c5fd;
        box-shadow: inset 0 0 16px #2563eb;
    }

    .game-cell.key {
        background: #785414;
        border: 2px solid #facc15;
    }

    .game-cell.exit {
        background: #166534;
        border: 2px solid #4ade80;
    }

    .game-cell.warden {
        background: #991b1b;
        border: 2px solid #f87171;
    }

    .game-cell.wall {
        background: #101827;
        border: 1px solid #64748b;
    }

    .game-cell.collision {
        background: #7f1d1d;
        border: 2px solid #fca5a5;
    }

    /* Controls */
    div.stButton > button {
        background: #263a5c;
        color: #ffffff !important;
        border: 1px solid #64748b;
        border-radius: 12px;
        min-height: 52px;
        font-weight: 750;
        font-size: 17px;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        background: #2563eb;
        border-color: #93c5fd;
        color: #ffffff !important;
    }

    div.stButton > button:disabled {
        background: #1e293b;
        color: #94a3b8 !important;
        opacity: 0.7;
    }

    /* Messages */
    [data-testid="stAlert"] {
        border-radius: 12px;
        border-width: 1px;
    }

    /* Captions */
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] * {
        color: #cbd5e1 !important;
    }

    /* Progress bar */
    [data-testid="stProgressBar"] > div > div {
        background-color: #6366f1;
    }

    hr {
        border-color: #334155 !important;
    }

    @media (max-width: 640px) {
        .block-container {
            padding-left: 0.75rem;
            padding-right: 0.75rem;
        }

        .game-cell {
            border-radius: 6px;
            min-height: 28px;
        }

        [data-testid="stMetric"] {
            padding: 12px 10px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# LEVEL CONFIGURATION
# ==========================================

LEVELS = {
    1: {
        "size": 5,
        "keys": [(1, 2)],
        "exit": (4, 0),
        "warden": (4, 4),
        "walls": [],
        "name": "The Beginning",
        "difficulty": "Easy",
        "depth": 2
    },

    2: {
        "size": 6,
        "keys": [(2, 3)],
        "exit": (5, 0),
        "warden": (5, 5),
        "walls": [
            (1, 1), (1, 2),
            (3, 2), (4, 4)
        ],
        "name": "The Maze",
        "difficulty": "Medium",
        "depth": 3
    },

    3: {
        "size": 7,
        "keys": [(1, 5), (4, 2)],
        "exit": (6, 0),
        "warden": (6, 6),
        "walls": [
            (1, 1), (1, 2),
            (2, 4), (3, 3),
            (4, 4), (5, 2)
        ],
        "name": "The Trap Chamber",
        "difficulty": "Hard",
        "depth": 4
    },

    4: {
        "size": 8,
        "keys": [(2, 5), (5, 3)],
        "exit": (7, 0),
        "warden": (7, 7),
        "walls": [
            (1, 1), (1, 2),
            (2, 2), (3, 4),
            (4, 4), (5, 5),
            (6, 2), (6, 3)
        ],
        "name": "Final Escape",
        "difficulty": "Expert",
        "depth": 5
    }
}

# ==========================================
# GAME STATE
# ==========================================

def start_level(level):
    st.session_state.level = level
    st.session_state.player = (0, 0)
    st.session_state.warden = LEVELS[level]["warden"]
    st.session_state.collected_keys = []
    st.session_state.moves = 0
    st.session_state.health = 100
    st.session_state.won = False
    st.session_state.game_over = False
    st.session_state.ai_decision = None
    st.session_state.message = (
        "🎯 Collect all keys and reach the exit!"
    )


required_state = [
    "level", "player", "warden", "collected_keys",
    "moves", "health", "won", "game_over", "ai_decision"
]

if any(name not in st.session_state for name in required_state):
    start_level(1)

# ==========================================
# AI WARDEN MOVEMENT
# ==========================================

def move_warden():
    level_data = LEVELS[st.session_state.level]

    old_position = st.session_state.warden

    best_move, best_score, stats = best_warden_move(
        player=st.session_state.player,
        warden=old_position,
        size=level_data["size"],
        walls=level_data["walls"],
keys=[
    key for key in level_data["keys"]
    if key not in st.session_state.collected_keys
],
exit_pos=level_data["exit"],
depth=level_data["depth"]
    )

    st.session_state.warden = best_move

    row_change = best_move[0] - old_position[0]
    col_change = best_move[1] - old_position[1]

    directions = {
        (-1, 0): "⬆️ Up",
        (1, 0): "⬇️ Down",
        (0, -1): "⬅️ Left",
        (0, 1): "➡️ Right",
        (0, 0): "⏸️ Stay"
    }

    st.session_state.ai_decision = {
        "move": directions.get(
            (row_change, col_change), "Unknown"
        ),
        "depth": level_data["depth"],
        "score": best_score,
        "nodes": stats["nodes"],
        "prunes": stats["prunes"]
    }

# ==========================================
# COLLISION DETECTION
# ==========================================

def check_collision():
    if st.session_state.player == st.session_state.warden:

        st.session_state.health = max(
            0, st.session_state.health - 20
        )

        if st.session_state.health == 0:
            st.session_state.game_over = True
            st.session_state.message = (
                "💀 Game Over! The warden caught you."
            )
        else:
            st.session_state.player = (0, 0)
            st.session_state.message = (
                "🤖 The warden caught you! "
                "You lost 20 health and returned to start."
            )

        return True

    return False

# ==========================================
# PLAYER MOVEMENT
# ==========================================

def move_player(dr, dc):

    if st.session_state.won or st.session_state.game_over:
        return

    level_data = LEVELS[st.session_state.level]
    size = level_data["size"]

    row, col = st.session_state.player
    new_row = row + dr
    new_col = col + dc

    # Check boundaries
    if not (0 <= new_row < size and 0 <= new_col < size):
        st.session_state.message = (
            "🚫 You cannot move outside the room!"
        )
        return

    # Check walls
    if (new_row, new_col) in level_data["walls"]:
        st.session_state.message = (
            "🧱 A wall blocks your path!"
        )
        return

    # Update player
    st.session_state.player = (new_row, new_col)
    st.session_state.moves += 1
    st.session_state.message = (
        "🎮 Keep moving! The warden is watching."
    )

    new_position = (new_row, new_col)

    # Collect key
    if new_position in level_data["keys"]:
        if new_position not in st.session_state.collected_keys:
            st.session_state.collected_keys.append(new_position)
            st.session_state.message = (
                "🔑 Key collected! Keep going!"
            )

    # Check collision
    if check_collision():
        return

    # Check exit
    if new_position == level_data["exit"]:
        if (
            len(st.session_state.collected_keys)
            == len(level_data["keys"])
        ):
            st.session_state.won = True
            st.session_state.message = (
                "🎉 Level completed! You escaped!"
            )
            return
        else:
            st.session_state.message = (
                "🔒 Collect all keys to unlock the exit!"
            )

    # AI takes its turn
    move_warden()

    # Check collision after AI movement
    check_collision()

# ==========================================
# HEADER
# ==========================================

level = st.session_state.level
level_data = LEVELS[level]
size = level_data["size"]

st.markdown("""
<div class="game-header">
    <h1>🔐 MINIMAX ESCAPE ROOM</h1>
    <p>
        Outsmart the AI Warden. Collect the keys.
        Find your way out.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    f'<div class="level-badge">'
    f'🎯 LEVEL {level} — {escape(level_data["name"])}'
    f'</div>',
    unsafe_allow_html=True
)

st.write(
    f"Difficulty: **{level_data['difficulty']}** "
    f" | Chamber: **{size}×{size}** "
    f" | AI Depth: **{level_data['depth']}**"
)

st.progress(level / len(LEVELS))
st.caption(f"Level {level} of {len(LEVELS)}")

# ==========================================
# GAME STATISTICS
# ==========================================

st.subheader("📊 Game Statistics")

health_col, key_col, move_col, level_col = st.columns(4)

with health_col:
    st.metric("❤️ Health", st.session_state.health)

with key_col:
    st.metric(
        "🔑 Keys Collected",
        f"{len(st.session_state.collected_keys)}/"
        f"{len(level_data['keys'])}"
    )

with move_col:
    st.metric("👣 Total Moves", st.session_state.moves)

with level_col:
    st.metric("🏆 Current Level", f"{level}/4")

st.divider()

# ==========================================
# MAIN GAME DASHBOARD
# ==========================================

game_panel, controls_panel = st.columns(
    [3, 2], gap="large"
)

with game_panel:

    st.subheader("🏠 Escape Chamber")
    st.caption(
        f"Level {level} • {size}×{size} Grid"
    )

    room = [
        ["" for _ in range(size)]
        for _ in range(size)
    ]

    # Walls
    for r, c in level_data["walls"]:
        room[r][c] = "🧱"

    # Keys
    for r, c in level_data["keys"]:
        if (r, c) not in st.session_state.collected_keys:
            room[r][c] = "🔑"

    # Exit
    er, ec = level_data["exit"]
    room[er][ec] = "🚪"

    # AI Warden
    wr, wc = st.session_state.warden
    room[wr][wc] = "🤖"

    # Player
    pr, pc = st.session_state.player
    room[pr][pc] = "🧍"

    # Draw grid
    for row in room:
        columns = st.columns(size, gap="small")

        for i, symbol in enumerate(row):

            cell_type = ""

            if symbol == "🧍":
                cell_type = "player"
            elif symbol == "🔑":
                cell_type = "key"
            elif symbol == "🚪":
                cell_type = "exit"
            elif symbol == "🤖":
                cell_type = "warden"
            elif symbol == "🧱":
                cell_type = "wall"

            with columns[i]:
                st.markdown(
                    f'<div class="game-cell {cell_type}">'
                    f'{symbol}</div>',
                    unsafe_allow_html=True
                )

    st.caption(
        "🧍 Player  |  🔑 Key  |  🚪 Exit  "
        "|  🤖 Warden  |  🧱 Wall"
    )

# ==========================================
# PLAYER CONTROLS
# ==========================================

with controls_panel:

    st.subheader("🎮 Player Controls")
    st.caption("Use the buttons to navigate the chamber.")

    controls_disabled = (
        st.session_state.won
        or st.session_state.game_over
    )

    # Up
    _, up_col, _ = st.columns(3)

    with up_col:
        st.button(
            "⬆️",
            key="move_up",
            on_click=move_player,
            args=(-1, 0),
            use_container_width=True,
            disabled=controls_disabled
        )

    # Left, Down, Right
    left_col, down_col, right_col = st.columns(3)

    with left_col:
        st.button(
            "⬅️",
            key="move_left",
            on_click=move_player,
            args=(0, -1),
            use_container_width=True,
            disabled=controls_disabled
        )

    with down_col:
        st.button(
            "⬇️",
            key="move_down",
            on_click=move_player,
            args=(1, 0),
            use_container_width=True,
            disabled=controls_disabled
        )

    with right_col:
        st.button(
            "➡️",
            key="move_right",
            on_click=move_player,
            args=(0, 1),
            use_container_width=True,
            disabled=controls_disabled
        )

    st.divider()

    st.markdown("#### 📡 Game Status")

    if st.session_state.game_over:
        st.error(st.session_state.message)
    elif st.session_state.won:
        st.success(st.session_state.message)
    else:
        st.info(st.session_state.message)

    # Next level
    if st.session_state.won:

        if level < len(LEVELS):
            st.button(
                "🚀 Next Level",
                key="next_level",
                on_click=start_level,
                args=(level + 1,),
                use_container_width=True,
                type="primary"
            )
        else:
            st.success(
                "🏆 You completed all four levels!"
            )

    # Restart level
    st.button(
        "🔄 Restart Level",
        key="restart_level",
        on_click=start_level,
        args=(level,),
        use_container_width=True
    )

    st.divider()

    st.markdown("#### 🎯 Mission")
    st.write(
        "Collect every key, avoid the AI Warden, "
        "and reach the exit before your health runs out."
    )

# ==========================================
# AI DECISION PANEL
# ==========================================

st.divider()

st.subheader(" AI Decision Panel")
st.caption(
    "Real-time Minimax search and Alpha-Beta pruning statistics"
)

decision = st.session_state.get("ai_decision")

if decision is None:

    st.info(
        "🤖 Make your first move to see "
        "how the AI Warden makes decisions."
    )

else:

    ai1, ai2, ai3 = st.columns(3)

    with ai1:
        st.metric(
            "🤖 AI Move",
            decision["move"]
        )

    with ai2:
        st.metric(
            "🔍 Search Depth",
            decision["depth"]
        )

    with ai3:
        st.metric(
            "📈 Evaluation Score",
            decision["score"]
        )

    ai4, ai5 = st.columns(2)

    with ai4:
        st.metric(
            " Nodes Examined",
            decision["nodes"]
        )

    with ai5:
        st.metric(
            "Pruning Events",
            decision["prunes"]
        )

    st.caption(
        "The AI uses Minimax to predict possible moves. "
        "Alpha-Beta pruning skips branches that cannot "
        "improve the selected decision. "
        "Pruning Events counts cutoffs, not individual "
        "nodes skipped."
    )

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "🔐 Minimax-Based Escape Room"
)
