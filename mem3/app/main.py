import tkinter as tk
from tkinter import filedialog, messagebox
import os
from datetime import datetime

from app.sender import Sender
from app.receiver import Receiver
from app.package_manager import received_package_exists
from ml.anomaly_detector import analyze_file


class SecureFileTransferApp:

    def __init__(self, root):

        self.root = root

        # ====================================================
        # WINDOW
        # ====================================================

        self.root.title("Secure File Transfer")
        self.root.geometry("760x720")
        self.root.resizable(False, True)

        # ====================================================
        # APPLICATION STATE
        # ====================================================

        self.sender = Sender()
        self.receiver = Receiver()

        self.file_selected = False
        self.package_ready = False
        self.package_sent = False
        self.package_received = False
        self.integrity_verified = False

        # ML state
        self.ml_analyzed = False
        self.ml_status = None

        # ====================================================
        # COLORS
        # ====================================================

        self.bg_color = "#F5F6F8"
        self.header_color = "#DCEFE1"
        self.card_color = "#FFFFFF"

        self.text_color = "#1F2937"
        self.secondary_text = "#6B7280"

        self.button_color = "#5F8068"
        self.button_hover = "#4F7058"

        self.success_color = "#2E7D32"
        self.error_color = "#C62828"
        self.warning_color = "#B26A00"

        self.border_color = "#D9DDE3"

        # ====================================================
        # FONTS
        # ====================================================

        self.font_title = (
            "Segoe UI",
            20,
            "bold"
        )

        self.font_subtitle = (
            "Segoe UI",
            10
        )

        self.font_section = (
            "Segoe UI",
            11,
            "bold"
        )

        self.font_normal = (
            "Segoe UI",
            10
        )

        self.font_small = (
            "Segoe UI",
            9
        )

        self.font_button = (
            "Segoe UI",
            10,
            "bold"
        )

        self.font_status = (
            "Consolas",
            9
        )

        # ====================================================
        # WINDOW BACKGROUND
        # ====================================================

        self.root.configure(
            bg=self.bg_color
        )

        # ====================================================
        # BUILD GUI
        # ====================================================

        self.create_gui()

        # Initial status
        self.add_status(
            "Application ready.",
            "normal"
        )

        # ====================================================
        # RESTORE EXISTING RECEIVER PACKAGE
        # ====================================================

        if received_package_exists():

            try:

                self.receiver.receive_package()
                self.receiver.load_metadata()

                self.package_received = True

                self.add_status(
                    "Existing secure package detected.",
                    "normal"
                )

            except Exception as error:

                self.add_status(
                    f"Existing package could not be loaded: {error}",
                    "error"
                )

        self.update_button_states()

    # ========================================================
    # MAIN GUI
    # ========================================================

    def create_gui(self):

        # ====================================================
        # SCROLLABLE CONTAINER
        # ====================================================

        self.canvas = tk.Canvas(
            self.root,
            bg=self.bg_color,
            highlightthickness=0,
            bd=0
        )

        self.scrollbar = tk.Scrollbar(
            self.root,
            orient="vertical",
            command=self.canvas.yview
        )

        self.scrollable_frame = tk.Frame(
            self.canvas,
            bg=self.bg_color
        )

        self.scrollable_frame.bind(
            "<Configure>",
            lambda event: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )

        # Keep the scrollable frame width equal to the canvas width
        self.canvas.bind(
            "<Configure>",
            self.resize_scrollable_frame
        )

        # Mouse wheel scrolling
        self.canvas.bind_all(
            "<MouseWheel>",
            self.on_mousewheel
        )

        # Linux mouse wheel support
        self.canvas.bind_all(
            "<Button-4>",
            self.on_mousewheel_linux
        )

        self.canvas.bind_all(
            "<Button-5>",
            self.on_mousewheel_linux
        )

        # ====================================================
        # EVERYTHING BELOW IS INSIDE THE SCROLLABLE FRAME
        # ====================================================

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = tk.Frame(
            self.scrollable_frame,
            bg=self.header_color,
            height=115,
            highlightbackground="#C8DDCD",
            highlightthickness=1
        )

        header.pack(
            fill="x",
            padx=0,
            pady=0
        )

        header.pack_propagate(
            False
        )

        # ----------------------------------------------------
        # HEADER TITLE
        # ----------------------------------------------------

        title = tk.Label(
            header,
            text="SECURE FILE TRANSFER",
            font=self.font_title,
            fg=self.text_color,
            bg=self.header_color
        )

        title.pack(
            pady=(25, 2)
        )

        # ----------------------------------------------------
        # HEADER SUBTITLE
        # ----------------------------------------------------

        subtitle = tk.Label(
            header,
            text="AES + RSA • Integrity Protected",
            font=self.font_subtitle,
            fg=self.secondary_text,
            bg=self.header_color
        )

        subtitle.pack()

        # ----------------------------------------------------
        # FILE SELECTION
        # ----------------------------------------------------

        self.create_section(
            "FILE SELECTION"
        )

        file_card = self.create_card()

        self.choose_button = self.create_button(
            file_card,
            "Choose File",
            self.choose_file,
            width=16
        )

        self.choose_button.pack(
            side="left",
            padx=(0, 15)
        )

        self.file_label = tk.Label(
            file_card,
            text="No file selected",
            font=self.font_normal,
            fg=self.secondary_text,
            bg=self.card_color,
            anchor="w"
        )

        self.file_label.pack(
            side="left",
            fill="x",
            expand=True
        )

        # ----------------------------------------------------
        # ML-BASED ANOMALY DETECTION
        # ----------------------------------------------------

        self.create_ml_section()

        # ----------------------------------------------------
        # SENDER
        # ----------------------------------------------------

        self.create_section(
            "SENDER"
        )

        sender_card = self.create_card()

        self.encrypt_button = self.create_button(
            sender_card,
            "Encrypt & Prepare",
            self.encrypt_and_prepare,
            width=18
        )

        self.encrypt_button.pack(
            side="left",
            padx=(0, 12)
        )

        self.send_button = self.create_button(
            sender_card,
            "Send Secure Package",
            self.send_package,
            width=20
        )

        self.send_button.pack(
            side="left"
        )

        # ----------------------------------------------------
        # RECEIVER
        # ----------------------------------------------------

        self.create_section(
            "RECEIVER"
        )

        receiver_card = self.create_card()

        self.receive_button = self.create_button(
            receiver_card,
            "Receive Package",
            self.receive_package,
            width=17
        )

        self.receive_button.pack(
            side="left",
            padx=(0, 12)
        )

        self.verify_button = self.create_button(
            receiver_card,
            "Verify Integrity",
            self.verify_integrity,
            width=17
        )

        self.verify_button.pack(
            side="left",
            padx=(0, 12)
        )

        self.decrypt_button = self.create_button(
            receiver_card,
            "Verify & Decrypt",
            self.decrypt_file,
            width=17
        )

        self.decrypt_button.pack(
            side="left"
        )

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        self.create_section(
            "STATUS"
        )

        status_card = self.create_card()

        status_card.configure(
            height=185
        )

        status_card.pack_propagate(
            False
        )

        text_frame = tk.Frame(
            status_card,
            bg=self.card_color
        )

        text_frame.pack(
            fill="both",
            expand=True
        )

        self.status_text = tk.Text(
            text_frame,
            font=self.font_status,
            bg="#FAFBFC",
            fg=self.text_color,
            relief="flat",
            bd=0,
            wrap="word",
            state="disabled",
            padx=10,
            pady=8
        )

        self.status_text.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = tk.Scrollbar(
            text_frame,
            orient="vertical",
            command=self.status_text.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.status_text.configure(
            yscrollcommand=scrollbar.set
        )

        # ----------------------------------------------------
        # FOOTER
        # ----------------------------------------------------

        footer = tk.Label(
            self.scrollable_frame,
            text="Secure File Transfer Prototype",
            font=(
                "Segoe UI",
                8
            ),
            fg="#9CA3AF",
            bg=self.bg_color
        )

        footer.pack(
            pady=(10, 15)
        )

    # ========================================================
    # SCROLLING
    # ========================================================

    def resize_scrollable_frame(self, event):

        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )

    # --------------------------------------------------------
    # WINDOWS / MACOS MOUSE WHEEL
    # --------------------------------------------------------

    def on_mousewheel(self, event):

        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    # --------------------------------------------------------
    # LINUX MOUSE WHEEL
    # --------------------------------------------------------

    def on_mousewheel_linux(self, event):

        if event.num == 4:

            self.canvas.yview_scroll(
                -1,
                "units"
            )

        elif event.num == 5:

            self.canvas.yview_scroll(
                1,
                "units"
            )

    # ========================================================
    # ML INFORMATION SECTION
    # ========================================================

    def create_ml_section(self):

        self.create_section(
            "ML-BASED FILE TRANSFER ANOMALY DETECTION"
        )

        ml_card = self.create_card()

        # ----------------------------------------------------
        # PURPOSE
        # ----------------------------------------------------

        purpose_title = tk.Label(
            ml_card,
            text="Purpose",
            font=self.font_section,
            fg=self.text_color,
            bg=self.card_color,
            anchor="w"
        )

        purpose_title.pack(
            fill="x",
            pady=(0, 2)
        )

        purpose_text = tk.Label(
            ml_card,
            text=(
                "An additional machine-learning layer monitors "
                "file-transfer characteristics and identifies "
                "unusual transfer behavior."
            ),
            font=self.font_small,
            fg=self.secondary_text,
            bg=self.card_color,
            anchor="w",
            justify="left",
            wraplength=650
        )

        purpose_text.pack(
            fill="x",
            pady=(0, 8)
        )

        # ----------------------------------------------------
        # HOW IT WORKS
        # ----------------------------------------------------

        how_title = tk.Label(
            ml_card,
            text="How It Works",
            font=self.font_section,
            fg=self.text_color,
            bg=self.card_color,
            anchor="w"
        )

        how_title.pack(
            fill="x",
            pady=(0, 2)
        )

        how_text = tk.Label(
            ml_card,
            text=(
                "File / Transfer Characteristics"
                "\n          ↓"
                "\n    Feature Extraction"
                "\n          ↓"
                "\n   ML Anomaly Detector"
                "\n       ↙          ↘"
                "\n   NORMAL      ANOMALOUS"
                "\n      ↓             ↓"
                "\nContinue Flow     Warning"
                "\n                  / Log Event"
            ),
            font=(
                "Consolas",
                8
            ),
            fg=self.secondary_text,
            bg="#FAFBFC",
            anchor="w",
            justify="left",
            padx=10,
            pady=6
        )

        how_text.pack(
            fill="x",
            pady=(0, 8)
        )

        # ----------------------------------------------------
        # ML TECHNIQUE
        # ----------------------------------------------------

        technique_title = tk.Label(
            ml_card,
            text="ML Technique",
            font=self.font_section,
            fg=self.text_color,
            bg=self.card_color,
            anchor="w"
        )

        technique_title.pack(
            fill="x",
            pady=(0, 2)
        )

        technique_text = tk.Label(
            ml_card,
            text=(
                "Isolation Forest\n"
                "• Unsupervised anomaly-detection algorithm\n"
                "• Learns patterns of normal file-transfer activity\n"
                "• Assigns an anomaly score to new transfers\n"
                "• Does not replace cryptographic verification"
            ),
            font=self.font_small,
            fg=self.secondary_text,
            bg=self.card_color,
            anchor="w",
            justify="left"
        )

        technique_text.pack(
            fill="x",
            pady=(0, 8)
        )

        # ----------------------------------------------------
        # SECURITY RELATIONSHIP
        # ----------------------------------------------------

        security_title = tk.Label(
            ml_card,
            text="Security Relationship",
            font=self.font_section,
            fg=self.text_color,
            bg=self.card_color,
            anchor="w"
        )

        security_title.pack(
            fill="x",
            pady=(0, 2)
        )

        security_text = tk.Label(
            ml_card,
            text=(
                "ML → Behavioral monitoring\n"
                "AES-256-GCM → Confidentiality + authenticated encryption\n"
                "RSA-3072/OAEP → AES key protection\n"
                "SHA-256 → Integrity verification"
            ),
            font=self.font_small,
            fg=self.secondary_text,
            bg=self.card_color,
            anchor="w",
            justify="left"
        )

        security_text.pack(
            fill="x"
        )

    # ========================================================
    # SECTION HEADER
    # ========================================================

    def create_section(self, title):

        label = tk.Label(
            self.scrollable_frame,
            text=title,
            font=self.font_section,
            fg=self.text_color,
            bg=self.bg_color,
            anchor="w"
        )

        label.pack(
            fill="x",
            padx=35,
            pady=(8, 6)
        )

    # ========================================================
    # CARD
    # ========================================================

    def create_card(self):

        card = tk.Frame(
            self.scrollable_frame,
            bg=self.card_color,
            highlightbackground=self.border_color,
            highlightthickness=1
        )

        card.pack(
            fill="x",
            padx=35,
            pady=(0, 3),
            ipady=12,
            ipadx=12
        )

        return card

    # ========================================================
    # BUTTON
    # ========================================================

    def create_button(
        self,
        parent,
        text,
        command,
        width
    ):

        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=self.font_button,
            fg="white",
            bg=self.button_color,
            activebackground=self.button_hover,
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=12,
            pady=7,
            width=width,
            cursor="hand2"
        )

        return button

    # ========================================================
    # BUTTON STATE MANAGEMENT
    # ========================================================

    def update_button_states(self):

        # Choose File
        self.choose_button.config(
            state="normal"
        )

        # Encrypt & Prepare
        if self.file_selected:
            self.encrypt_button.config(
                state="normal"
            )
        else:
            self.encrypt_button.config(
                state="disabled"
            )

        # Send Package
        if self.package_ready:
            self.send_button.config(
                state="normal"
            )
        else:
            self.send_button.config(
                state="disabled"
            )

        # Receive Package
        if self.package_sent or self.package_received:
            self.receive_button.config(
                state="normal"
            )
        else:
            self.receive_button.config(
                state="disabled"
            )

        # Verify Integrity
        if self.package_received:
            self.verify_button.config(
                state="normal"
            )
        else:
            self.verify_button.config(
                state="disabled"
            )

        # Verify & Decrypt
        if self.integrity_verified:
            self.decrypt_button.config(
                state="normal"
            )
        else:
            self.decrypt_button.config(
                state="disabled"
            )

    # ========================================================
    # CHOOSE FILE
    # ========================================================

    def choose_file(self):

        file_path = filedialog.askopenfilename(
            title="Select a file"
        )

        if not file_path:

            self.add_status(
                "File selection cancelled.",
                "warning"
            )

            return

        try:

            self.sender.set_file(
                file_path
            )

            self.file_selected = True
            self.package_ready = False
            self.package_sent = False
            self.package_received = False
            self.integrity_verified = False

            self.ml_analyzed = False
            self.ml_status = None

            filename = os.path.basename(
                file_path
            )

            self.file_label.config(
                text=filename,
                fg=self.text_color
            )

            self.add_status(
                f"✓ File selected: {filename}",
                "success"
            )

            # ====================================================
            # ML-BASED ANOMALY ANALYSIS
            # ====================================================

            try:

                ml_result = analyze_file(
                    file_path
                )

                self.ml_analyzed = True
                self.ml_status = ml_result["status"]

                if ml_result["status"] == "NORMAL":

                    self.add_status(
                        "✓ ML security analysis: NORMAL",
                        "success"
                    )

                else:

                    self.add_status(
                        "⚠ ML security analysis: ANOMALOUS",
                        "warning"
                    )

                    self.add_status(
                        "Unusual file-transfer characteristics detected.",
                        "warning"
                    )

            except Exception as error:

                self.ml_analyzed = False
                self.ml_status = None

                self.add_status(
                    f"⚠ ML analysis unavailable: {error}",
                    "warning"
                )

            self.update_button_states()

        except Exception as error:

            messagebox.showerror(
                "File Error",
                str(error)
            )

            self.add_status(
                f"✗ File selection failed: {error}",
                "error"
            )

    # ========================================================
    # ENCRYPT + PREPARE
    # ========================================================

    def encrypt_and_prepare(self):

        try:

            package_path = (
                self.sender.prepare_package()
            )

            self.package_ready = True
            self.package_sent = False
            self.package_received = False
            self.integrity_verified = False

            filename = os.path.basename(
                self.sender.selected_file
            )

            self.add_status(
                f"✓ Secure package prepared: {filename}",
                "success"
            )

            self.add_status(
                "AES-256-GCM + RSA-3072 encryption completed.",
                "success"
            )

            self.add_status(
                f"Location: {package_path}",
                "normal"
            )

            self.update_button_states()

        except Exception as error:

            self.package_ready = False

            messagebox.showerror(
                "Encryption Error",
                str(error)
            )

            self.add_status(
                f"✗ Package preparation failed: {error}",
                "error"
            )

            self.update_button_states()

    # ========================================================
    # SEND PACKAGE
    # ========================================================

    def send_package(self):

        if not self.package_ready:

            self.add_status(
                "⚠ Package is not ready.",
                "warning"
            )

            return

        try:

            receiver_path = (
                self.sender.send_package()
            )

            self.package_sent = True

            self.add_status(
                "✓ Package sent successfully.",
                "success"
            )

            self.add_status(
                "Transfer mode: simulated filesystem transfer.",
                "normal"
            )

            self.add_status(
                f"Receiver location: {receiver_path}",
                "normal"
            )

            self.update_button_states()

        except Exception as error:

            messagebox.showerror(
                "Send Error",
                str(error)
            )

            self.add_status(
                f"✗ Sending failed: {error}",
                "error"
            )

            self.update_button_states()

    # ========================================================
    # RECEIVE PACKAGE
    # ========================================================

    def receive_package(self):

        try:

            package_path = (
                self.receiver.receive_package()
            )

            metadata = (
                self.receiver.load_metadata()
            )

            filename = metadata.get(
                "original_filename",
                "Unknown"
            )

            version = metadata.get(
                "package_version",
                "Unknown"
            )

            self.package_received = True
            self.integrity_verified = False

            self.add_status(
                "✓ Package received.",
                "success"
            )

            self.add_status(
                f"Original file: {filename}",
                "normal"
            )

            self.add_status(
                f"Package version: {version}",
                "normal"
            )

            self.add_status(
                f"Location: {package_path}",
                "normal"
            )

            self.update_button_states()

        except Exception as error:

            self.package_received = False

            messagebox.showerror(
                "Receive Error",
                str(error)
            )

            self.add_status(
                f"✗ Receiving failed: {error}",
                "error"
            )

            self.update_button_states()

    # ========================================================
    # VERIFY INTEGRITY
    # ========================================================

    def verify_integrity(self):

        if not self.package_received:

            self.add_status(
                "⚠ Package has not been received.",
                "warning"
            )

            return

        try:

            result = (
                self.receiver.verify_integrity()
            )

            if result:

                self.integrity_verified = True

                self.add_status(
                    "✓ Integrity verification: VALID",
                    "success"
                )

                self.add_status(
                    "SHA-256 verification successful.",
                    "success"
                )

            else:

                self.integrity_verified = False

                self.add_status(
                    "✗ Integrity verification: INVALID",
                    "error"
                )

                self.add_status(
                    "Package modification detected.",
                    "error"
                )

            self.update_button_states()

        except Exception as error:

            self.integrity_verified = False

            messagebox.showerror(
                "Integrity Error",
                str(error)
            )

            self.add_status(
                f"✗ Integrity verification failed: {error}",
                "error"
            )

            self.update_button_states()

    # ========================================================
    # DECRYPT FILE
    # ========================================================

    def decrypt_file(self):

        if not self.package_received:

            self.add_status(
                "⚠ Package has not been received.",
                "warning"
            )

            return

        if not self.integrity_verified:

            self.add_status(
                "⚠ Integrity has not been verified.",
                "warning"
            )

            return

        try:

            output_path = (
                self.receiver.decrypt_file()
            )

            filename = os.path.basename(
                output_path
            )

            self.add_status(
                "✓ File decrypted successfully.",
                "success"
            )

            self.add_status(
                f"Recovered file: {filename}",
                "success"
            )

            self.add_status(
                f"Output location: {output_path}",
                "normal"
            )

            messagebox.showinfo(
                "Transfer Complete",
                "File decrypted successfully."
            )

            self.update_button_states()

        except Exception as error:

            messagebox.showerror(
                "Decryption Error",
                str(error)
            )

            self.add_status(
                f"✗ Decryption failed: {error}",
                "error"
            )

            self.update_button_states()

    # ========================================================
    # STATUS LOG
    # ========================================================

    def add_status(
        self,
        message,
        status_type="normal"
    ):

        self.status_text.config(
            state="normal"
        )

        timestamp = datetime.now().strftime(
            "%H:%M:%S"
        )

        line = (
            f"[{timestamp}] {message}\n"
        )

        self.status_text.insert(
            "end",
            line
        )

        start_index = (
            self.status_text.index(
                "end-2l"
            )
        )

        if status_type == "success":

            self.status_text.tag_add(
                "success",
                start_index,
                "end-1c"
            )

        elif status_type == "error":

            self.status_text.tag_add(
                "error",
                start_index,
                "end-1c"
            )

        elif status_type == "warning":

            self.status_text.tag_add(
                "warning",
                start_index,
                "end-1c"
            )

        self.status_text.tag_config(
            "success",
            foreground=self.success_color
        )

        self.status_text.tag_config(
            "error",
            foreground=self.error_color
        )

        self.status_text.tag_config(
            "warning",
            foreground=self.warning_color
        )

        self.status_text.config(
            state="disabled"
        )

        self.status_text.see(
            "end"
        )


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = SecureFileTransferApp(
        root
    )

    root.mainloop()