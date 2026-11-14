import random
import tkinter as tk
from tkinter import messagebox


class BenchmarkFractionsApp:

    def __init__(self, root):
        self.root = root
        self.root.title("5th Grade Math: Benchmark Fractions Explorer")
        self.root.geometry("760x580")
        self.root.configure(bg="#F0F4F8")

        # Variables
        self.num = tk.IntVar(value=3)
        self.den = tk.IntVar(value=8)
        self.quiz_mode = False
        self.quiz_num = 1
        self.quiz_den = 4
        self.score = 0
        self.total_questions = 0

        self.setup_ui()
        self.update_visuals()

    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#1E3A8A", pady=15)
        header_frame.pack(fill="x")

        title = tk.Label(
            header_frame,
            text="Benchmark Fractions Explorer (0, ½, 1)",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#1E3A8A",
        )
        title.pack()

        subtitle = tk.Label(
            header_frame,
            text=(
                "Use the sliders to explore how fractions compare to 0, ½, and"
                " 1!"
            ),
            font=("Arial", 11),
            fg="#DBEAFE",
            bg="#1E3A8A",
        )
        subtitle.pack()

        # Mode Toggle Bar
        mode_frame = tk.Frame(self.root, bg="#F0F4F8", pady=10)
        mode_frame.pack()

        self.mode_btn = tk.Button(
            mode_frame,
            text="Switch to Practice Quiz Mode",
            font=("Arial", 11, "bold"),
            bg="#0D9488",
            fg="white",
            padx=15,
            pady=5,
            relief="flat",
            cursor="hand2",
            command=self.toggle_mode,
        )
        self.mode_btn.pack()

        # Canvas for Visual Fraction Bars
        self.canvas = tk.Canvas(
            self.root,
            width=680,
            height=220,
            bg="white",
            highlightthickness=2,
            highlightbackground="#CBD5E1",
        )
        self.canvas.pack(pady=10)

        # Explanation / Status Banner
        self.status_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 13, "bold"),
            fg="#1E293B",
            bg="#E2E8F0",
            pady=10,
            padx=20,
            width=62,
        )
        self.status_label.pack(pady=5)

        # Container for Explore Controls vs Quiz Controls
        self.controls_container = tk.Frame(self.root, bg="#F0F4F8")
        self.controls_container.pack(pady=10, fill="x")

        # --- EXPLORE FRAME ---
        self.explore_frame = tk.Frame(self.controls_container, bg="#F0F4F8")

        # Numerator Slider
        num_frame = tk.Frame(self.explore_frame, bg="#F0F4F8")
        num_frame.pack(pady=5)
        tk.Label(
            num_frame,
            text="Numerator (Top Number):",
            font=("Arial", 12, "bold"),
            bg="#F0F4F8",
            width=24,
            anchor="e",
        ).pack(side="left", padx=10)
        self.num_slider = tk.Scale(
            num_frame,
            from_=0,
            to=12,
            orient="horizontal",
            variable=self.num,
            length=300,
            font=("Arial", 10),
            bg="#F0F4F8",
            command=self.on_slider_change,
        )
        self.num_slider.pack(side="left")

        # Denominator Slider
        den_frame = tk.Frame(self.explore_frame, bg="#F0F4F8")
        den_frame.pack(pady=5)
        tk.Label(
            den_frame,
            text="Denominator (Bottom Number):",
            font=("Arial", 12, "bold"),
            bg="#F0F4F8",
            width=24,
            anchor="e",
        ).pack(side="left", padx=10)
        self.den_slider = tk.Scale(
            den_frame,
            from_=1,
            to=12,
            orient="horizontal",
            variable=self.den,
            length=300,
            font=("Arial", 10),
            bg="#F0F4F8",
            command=self.on_slider_change,
        )
        self.den_slider.pack(side="left")

        # --- QUIZ FRAME ---
        self.quiz_frame = tk.Frame(self.controls_container, bg="#F0F4F8")

        self.quiz_prompt = tk.Label(
            self.quiz_frame,
            text="",
            font=("Arial", 14, "bold"),
            bg="#F0F4F8",
            fg="#0F172A",
        )
        self.quiz_prompt.pack(pady=5)

        btn_row = tk.Frame(self.quiz_frame, bg="#F0F4F8")
        btn_row.pack(pady=10)

        for label, val in [
            ("Closest to 0", 0.0),
            ("Closest to ½", 0.5),
            ("Closest to 1", 1.0),
        ]:
            tk.Button(
                btn_row,
                text=label,
                font=("Arial", 12, "bold"),
                bg="#2563EB",
                fg="white",
                width=14,
                pady=8,
                relief="flat",
                cursor="hand2",
                command=lambda v=val: self.check_quiz_answer(v),
            ).pack(side="left", padx=12)

        self.score_label = tk.Label(
            self.quiz_frame,
            text="Score: 0 / 0",
            font=("Arial", 11, "bold"),
            bg="#F0F4F8",
            fg="#475569",
        )
        self.score_label.pack(pady=5)

        # Pack Explore Frame initially
        self.explore_frame.pack()

    def on_slider_change(self, _=None):
        # Prevent improper fractions (> 1) to keep focus on 0, 1/2, 1 benchmarks
        if self.num.get() > self.den.get():
            self.num.set(self.den.get())
        self.update_visuals()

    def get_closest_benchmark(self, n, d):
        val = n / d
        dist_0 = abs(val - 0.0)
        dist_half = abs(val - 0.5)
        dist_1 = abs(val - 1.0)

        min_dist = min(dist_0, dist_half, dist_1)
        # Tie-breaking rounds up to the higher benchmark (standard estimation rule)
        if min_dist == dist_1:
            return 1.0, "1"
        elif min_dist == dist_half:
            return 0.5, "½"
        else:
            return 0.0, "0"

    def update_visuals(self):
        self.canvas.delete("all")

        n = self.quiz_num if self.quiz_mode else self.num.get()
        d = self.quiz_den if self.quiz_mode else self.den.get()

        bar_x = 90
        bar_width = 500
        bar_height = 45

        closest_val, closest_str = self.get_closest_benchmark(n, d)

        # 1. Draw Student's Fraction Bar (Top)
        y1 = 35
        self.canvas.create_text(
            bar_x - 45,
            y1 + bar_height / 2,
            text=f"{n}/{d}",
            font=("Arial", 16, "bold"),
            fill="#1E3A8A",
        )

        # In Quiz mode, hide the shaded fill until they guess so they use mental math!
        part_width = bar_width / d
        for i in range(d):
            x_start = bar_x + (i * part_width)
            x_end = x_start + part_width
            fill_color = (
                "#3B82F6" if (i < n and not self.quiz_mode) else "#F8FAFC"
            )
            self.canvas.create_rectangle(
                x_start,
                y1,
                x_end,
                y1 +
