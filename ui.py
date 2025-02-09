import tkinter as tk
from tkinter import ttk, messagebox
from game import DynamicDarts  # Assuming your game code is in dynamic_darts.py

class DartsGameUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Dynamic Darts Game")
        self.root.geometry("800x600")  # Larger initial window
        self.root.configure(bg="#2C3E50")  # Dark blue-gray background
        self.game = None
        
        # Configure styles
        self.setup_styles()
        self.setup_start_screen()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")  # Using a modern theme

        # Configure colors
        primary_bg = "#34495E"
        secondary_bg = "#2C3E50"
        text_color = "#ECF0F1"
        button_bg = "#E74C3C"
        button_fg = "#FFFFFF"

        style.configure("Big.TLabel", font=("Helvetica", 24), background=secondary_bg, foreground=text_color)
        style.configure("Title.TLabel", font=("Helvetica", 48, "bold"), background=secondary_bg, foreground="#F39C12")
        style.configure("Header.TLabel", font=("Helvetica", 40, "bold"), background=secondary_bg, foreground=text_color)
        style.configure("Big.TButton", font=("Helvetica", 32), background=button_bg, foreground=button_fg, padding=10)
        style.map("Big.TButton", background=[("active", "#C0392B")])
        style.configure("Big.TLabelframe", font=("Helvetica", 24), background=primary_bg, foreground=text_color, relief="ridge")
        style.configure("Big.TLabelframe.Label", font=("Helvetica", 32), background=primary_bg, foreground="#F39C12")

    def setup_start_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root, padding="40", style="Big.TLabelframe")
        frame.pack(fill=tk.BOTH, expand=True)

        title = ttk.Label(frame, text="Dynamic Darts", style='Title.TLabel')
        title.pack(pady=20)

        players_frame = ttk.Frame(frame)
        players_frame.pack(pady=20)
        ttk.Label(players_frame, text="Nombre de joueurs:", style='Big.TLabel').pack(side=tk.LEFT, padx=10)
        self.player_count = ttk.Spinbox(players_frame, from_=1, to=10, width=5, font=('Helvetica', 32))
        self.player_count.set(3)
        self.player_count.pack(side=tk.LEFT, padx=10)

        prob_frame = ttk.Frame(frame)
        prob_frame.pack(pady=20)
        ttk.Label(prob_frame, text="Probabilité de challenge (0-1):", style='Big.TLabel').pack(side=tk.LEFT, padx=10)
        self.probability = ttk.Entry(prob_frame, width=5, font=('Helvetica', 32))
        self.probability.insert(0, "1.0")
        self.probability.pack(side=tk.LEFT, padx=10)

        start_button = ttk.Button(frame, text="Commencer", command=self.start_game, style='Big.TButton')
        start_button.pack(pady=30)

    def start_game(self):
        try:
            nb_players = int(self.player_count.get())
            prob = float(self.probability.get())
            if nb_players < 1:
                raise ValueError("Le nombre de joueurs doit être supérieur à 0")
            if not 0 <= prob <= 1:
                raise ValueError("La probabilité doit être entre 0 et 1")
            self.game = DynamicDarts(nb_players, prob)
            self.game.next_turn(False)
            self.setup_game_screen()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def setup_game_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.game_frame = ttk.Frame(self.root, padding="20", style="Big.TLabelframe")
        self.game_frame.pack(fill=tk.BOTH, expand=True)

        self.player_label = ttk.Label(self.game_frame, text="", style='Header.TLabel')
        self.player_label.pack(pady=20)

        self.challenge_frame = ttk.LabelFrame(self.game_frame, text="Challenge", padding="20", style='Big.TLabelframe')
        self.challenge_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.challenge_label = ttk.Label(self.challenge_frame, text="", style='Big.TLabel', wraplength=2000)
        self.challenge_label.pack(pady=10)

        self.modifier_label = ttk.Label(self.challenge_frame, text="", style='Big.TLabel', wraplength=2000)
        self.modifier_label.pack(pady=10)

        self.modifiers_frame = ttk.LabelFrame(self.game_frame, text="Modificateurs actifs", padding="20", style='Big.TLabelframe')
        self.modifiers_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.active_modifiers_label = ttk.Label(self.modifiers_frame, text="", style='Big.TLabel', wraplength=2000)
        self.active_modifiers_label.pack(pady=10)

        button_frame = ttk.Frame(self.game_frame)
        button_frame.pack(pady=30)

        ttk.Button(button_frame, text="Challenge réussi", command=lambda: self.handle_turn(True), style='Big.TButton').pack(side=tk.LEFT, padx=0)
        ttk.Button(button_frame, text="Challenge raté", command=lambda: self.handle_turn(False), style='Big.TButton').pack(side=tk.LEFT, padx=0)

        self.update_display()

    def update_display(self):
        current_player = self.game.get_current_player()
        self.player_label.config(text=f"Tour de {current_player.name}")

        if self.game.current_challenge:
            challenge_text = f"Challenge : {self.game.current_challenge}"
            modifier_text = f"Modificateur au tour suivant : {self.game.current_modifier}"
            modifier_type = "BONUS" if self.game.current_modifier_is_bonus else "MALUS"
            self.challenge_label.config(text=f"{challenge_text}")
            self.modifier_label.config(text=f"{modifier_text}\n({modifier_type})")
        else:
            self.challenge_label.config(text="Pas de challenge ce tour")
            self.modifier_label.config(text="")

        if current_player.modifiers:
            modifiers_text = "\n".join(f"• {mod}" for mod in current_player.modifiers)
        else:
            modifiers_text = "Aucun modificateur actif"
        self.active_modifiers_label.config(text=modifiers_text)

    def handle_turn(self, success):
        self.game.next_turn(success)
        self.update_display()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = DartsGameUI()
    app.run()