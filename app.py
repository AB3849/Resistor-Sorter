import tkinter as tk
from tkinter import font

# Define your resistor bins and target resistance ranges
BINS = {
    1: {"label": "100 Ω", "color": "#2196F3"},
    2: {"label": "1 kΩ", "color": "#4CAF50"},
    3: {"label": "10 kΩ", "color": "#FF9800"},
    4: {"label": "100 kΩ", "color": "#9C27B0"},
    5: {"label": "Reject / Unk", "color": "#F44336"}
}

class ResistorSorterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Resistor Sorting Robot")
        
        # Make full-screen for the Raspberry Pi Touch Display 2
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='#1e1e1e')
        
        self.active_bin = None
        self.bin_widgets = {}
        
        self.setup_ui()

    def setup_ui(self):
        # Header title
        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        header = tk.Label(
            self.root, 
            text="RESISTOR SORTING ROBOT", 
            font=title_font, 
            fg="white", 
            bg="#1e1e1e", 
            pady=15
        )
        header.pack()

        # Status display bar
        self.status_label = tk.Label(
            self.root, 
            text="SYSTEM READY - Select a bin or start sorting", 
            font=("Helvetica", 14), 
            fg="#AAAAAA", 
            bg="#2d2d2d", 
            pady=10
        )
        self.status_label.pack(fill=tk.X, padx=20, pady=5)

        # Bin selection grid container
        grid_frame = tk.Frame(self.root, bg="#1e1e1e")
        grid_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
        
        # Create touchable cards for each bin
        for bin_id, data in BINS.items():
            card = tk.Frame(grid_frame, bg="#2d2d2d", highlightthickness=3, highlightbackground="#3d3d3d")
            card.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)
            
            lbl_id = tk.Label(card, text=f"BIN {bin_id}", font=("Helvetica", 16, "bold"), fg="white", bg="#2d2d2d")
            lbl_id.pack(pady=(15, 5))
            
            lbl_val = tk.Label(card, text=data["label"], font=("Helvetica", 14), fg=data["color"], bg="#2d2d2d")
            lbl_val.pack(pady=5)
            
            # Button for manual trigger/testing
            btn = tk.Button(
                card, 
                text="SELECT", 
                font=("Helvetica", 12, "bold"),
                bg="#3d3d3d", 
                fg="white", 
                activebackground=data["color"],
                command=lambda b=bin_id: self.select_bin(b)
            )
            btn.pack(pady=15, padx=10, fill=tk.X)
            
            self.bin_widgets[bin_id] = {"card": card, "button": btn}

        # Exit button (bottom right corner to close full screen)
        exit_btn = tk.Button(
            self.root, 
            text="Exit GUI", 
            font=("Helvetica", 10), 
            command=self.root.destroy, 
            bg="#333333", 
            fg="#888888"
        )
        exit_btn.pack(side=tk.RIGHT, padx=10, pady=10)

    def select_bin(self, bin_id):
        """Updates UI display and triggers physical sorting mechanism."""
        # Reset previous active bin card appearance
        if self.active_bin in self.bin_widgets:
            self.bin_widgets[self.active_bin]["card"].config(highlightbackground="#3d3d3d", bg="#2d2d2d")
            
        # Highlight new active bin in neon green
        self.active_bin = bin_id
        self.bin_widgets[bin_id]["card"].config(highlightbackground="#00FF00", bg="#1a381a")
        
        # Update text status banner
        bin_name = BINS[bin_id]["label"]
        self.status_label.config(
            text=f"ACTIVE: Bin {bin_id} ({bin_name}) Selected", 
            fg="#00FF00"
        )
        
        # Execute hardware trigger command
        self.trigger_hardware_actuator(bin_id)

    def trigger_hardware_actuator(self, bin_id):
        """Place your GPIO servo movements or Serial commands here."""
        print(f"[HARDWARE ACTION] Moving sorting gate/servo to position for Bin {bin_id}")
        # Example GPIO call:
        # gpio.set_servo_angle(bin_id * 30)

if __name__ == "__main__":
    root = tk.Tk()
    app = ResistorSorterGUI(root)
    root.mainloop()