import tkinter as tk
from tkinter import messagebox
import numpy as np

# --- Matrix Definitions for (7,4) Linear Block Code ---
# Generator Matrix G (4x7): G = [I4 | P]
G = np.array([
    [1, 0, 0, 0, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 1],
    [0, 0, 1, 0, 1, 1, 1],
    [0, 0, 0, 1, 1, 0, 1]
], dtype=int)

# Parity-Check Matrix H (3x7): H = [P^T | I3]
H = np.array([
    [1, 0, 1, 1, 1, 0, 0],
    [1, 1, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 0, 0, 1]
], dtype=int)

class LinearBlockCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("(7,4) Linear Block Code Simulator")
        self.root.geometry("620x670")
        self.root.config(bg="#f4f6f9")

        # Application Header
        title_label = tk.Label(
            root, 
            text="(7,4) Linear Block Code Error Corrector", 
            font=("Helvetica", 15, "bold"), 
            bg="#f4f6f9", 
            fg="#2c3e50"
        )
        title_label.pack(pady=15)

        # 1. Message Input Section
        input_frame = tk.LabelFrame(
            root, 
            text=" 1. Input 4-Bit Data Message (D) ", 
            font=("Helvetica", 11, "bold"), 
            bg="#ffffff", 
            fg="#34495e", 
            padx=10, 
            pady=10
        )
        input_frame.pack(fill="x", padx=20, pady=10)

        self.data_entries = []
        for i in range(4):
            lbl = tk.Label(input_frame, text=f"d{i+1}:", font=("Helvetica", 10), bg="#ffffff")
            lbl.grid(row=0, column=i*2, padx=5, pady=5)
            entry = tk.Entry(input_frame, width=5, font=("Helvetica", 12), justify="center")
            entry.insert(0, "1" if i % 2 == 0 else "0")
            entry.grid(row=0, column=i*2+1, padx=5, pady=5)
            self.data_entries.append(entry)

        encode_btn = tk.Button(
            input_frame, 
            text="Encode Message", 
            font=("Helvetica", 10, "bold"), 
            bg="#27ae60", 
            fg="white", 
            command=self.encode_data
        )
        encode_btn.grid(row=0, column=8, padx=15, pady=5)

        # 2. Transmitted Codeword Output Section
        encoded_frame = tk.LabelFrame(
            root, 
            text=" 2. Transmitted Codeword (C = D · G mod 2) ", 
            font=("Helvetica", 11, "bold"), 
            bg="#ffffff", 
            fg="#34495e", 
            padx=10, 
            pady=10
        )
        encoded_frame.pack(fill="x", padx=20, pady=10)

        self.cw_label = tk.Label(
            encoded_frame, 
            text="Click 'Encode Message' to generate codeword.", 
            font=("Helvetica", 11, "italic"), 
            bg="#ffffff", 
            fg="#7f8c8d"
        )
        self.cw_label.pack(pady=5)

        # 3. Channel Noise Injection Section
        noise_frame = tk.LabelFrame(
            root, 
            text=" 3. Simulate Channel Noise (Inject 1-Bit Error) ", 
            font=("Helvetica", 11, "bold"), 
            bg="#ffffff", 
            fg="#34495e", 
            padx=10, 
            pady=10
        )
        noise_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(
            noise_frame, 
            text="Select bit position to corrupt in transit:", 
            font=("Helvetica", 10), 
            bg="#ffffff"
        ).pack(anchor="w")
        
        self.error_pos = tk.IntVar(value=3)
        radio_frame = tk.Frame(noise_frame, bg="#ffffff")
        radio_frame.pack(pady=5)
        
        tk.Radiobutton(radio_frame, text="No Error", variable=self.error_pos, value=0, bg="#ffffff").pack(side="left", padx=5)
        for i in range(1, 8):
            tk.Radiobutton(radio_frame, text=f"Bit {i}", variable=self.error_pos, value=i, bg="#ffffff").pack(side="left", padx=3)

        decode_btn = tk.Button(
            noise_frame, 
            text="Transmit & Auto-Correct", 
            font=("Helvetica", 10, "bold"), 
            bg="#2980b9", 
            fg="white", 
            command=self.decode_data
        )
        decode_btn.pack(pady=10)

        # 4. Results & Auto-Correction Section
        results_frame = tk.LabelFrame(
            root, 
            text=" 4. Decoding & Automatic Error Correction ", 
            font=("Helvetica", 11, "bold"), 
            bg="#ffffff", 
            fg="#34495e", 
            padx=10, 
            pady=10
        )
        results_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.rx_label = tk.Label(results_frame, text="Received Vector (R): -", font=("Helvetica", 11), bg="#ffffff", anchor="w")
        self.rx_label.pack(fill="x", pady=2)

        self.syn_label = tk.Label(results_frame, text="Calculated Syndrome (S = R · H^T mod 2): -", font=("Helvetica", 11), bg="#ffffff", anchor="w")
        self.syn_label.pack(fill="x", pady=2)

        self.status_label = tk.Label(results_frame, text="Status: -", font=("Helvetica", 11, "bold"), bg="#ffffff", anchor="w")
        self.status_label.pack(fill="x", pady=2)

        self.rec_label = tk.Label(results_frame, text="Recovered Data Message (D): -", font=("Helvetica", 12, "bold"), bg="#ffffff", fg="#27ae60", anchor="w")
        self.rec_label.pack(fill="x", pady=5)

        self.codeword = None

    def get_input_bits(self):
        bits = []
        for i, entry in enumerate(self.data_entries):
            val = entry.get().strip()
            if val not in ["0", "1"]:
                messagebox.showerror("Invalid Input", f"Bit d{i+1} must be either 0 or 1.")
                return None
            bits.append(int(val))
        return np.array(bits)

    def encode_data(self):
        D = self.get_input_bits()
        if D is None:
            return

        # Matrix Encoding: C = D * G (mod 2)
        self.codeword = np.mod(np.dot(D, G), 2)
        cw_str = " ".join(map(str, self.codeword))
        self.cw_label.config(text=f"Codeword (C): [ {cw_str} ]", font=("Helvetica", 11, "bold"), fg="#2c3e50")

    def decode_data(self):
        if self.codeword is None:
            self.encode_data()
            if self.codeword is None:
                return

        # Step 1: Inject Channel Noise
        err_idx = self.error_pos.get()
        E = np.zeros(7, dtype=int)
        if err_idx > 0:
            E[err_idx - 1] = 1  # 1-bit error vector

        # Received Signal R = C XOR E
        R = np.mod(self.codeword + E, 2)

        # Step 2: Compute Syndrome Vector S = R * H^T (mod 2)
        S = np.mod(np.dot(R, H.T), 2)

        # Step 3: Match Syndrome to Column of H to find error index
        error_detected_at = 0
        if np.any(S != 0):
            for col_idx in range(7):
                if np.array_equal(S, H[:, col_idx]):
                    error_detected_at = col_idx + 1
                    break

        # Step 4: Correct Error by flipping the corrupted bit back
        R_corrected = R.copy()
        if error_detected_at > 0:
            R_corrected[error_detected_at - 1] ^= 1  # XOR flip

        # Extract original 4 data bits
        recovered_D = R_corrected[:4]

        # Update GUI Labels
        self.rx_label.config(text=f"Received Vector (R):  [ {' '.join(map(str, R))} ]")
        self.syn_label.config(text=f"Calculated Syndrome (S):  [ {' '.join(map(str, S))} ]")

        if err_idx == 0:
            self.status_label.config(text="Status: Clean transmission (No error introduced).", fg="#27ae60")
        elif error_detected_at > 0:
            self.status_label.config(text=f"Status: Corrupted Bit {error_detected_at} identified & automatically corrected!", fg="#e67e22")
        else:
            self.status_label.config(text="Status: Uncorrectable error pattern.", fg="#c0392b")

        self.rec_label.config(text=f"Recovered Data Message (D):  [ {' '.join(map(str, recovered_D))} ]")


if __name__ == "__main__":
    root = tk.Tk()
    app = LinearBlockCodeApp(root)
    root.mainloop()
