import sys
import json
import time
import requests
import os

# this is to test if we can access the display

print("Starting application...")
print(f"Python version: {sys.version}")
print(f"DISPLAY environment variable: {os.environ.get('DISPLAY', 'Not set')}")

try:
    print("Importing PySide6...")
    from PySide6.QtWidgets import (
        QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
        QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QScrollArea, QFrame
    )
    from PySide6.QtGui import QFont
    from PySide6.QtCore import Qt, QTimer

    print("PySide6 imported successfully!")
except ImportError as e:
    print(f"Failed to import PySide6: {e}")
    sys.exit(1)

 # this the main part of the application
 

class URLMonitorApp(QWidget):
    def __init__(self):
        super().__init__()
        print("Initializing URLMonitorApp...")
        self.setWindowTitle("Multi URL Health Monitor")
        self.setMinimumSize(1000, 600)

        self.check_results = []
        self.url_entries = []

        main_layout = QVBoxLayout(self)

        heading = QLabel("Multi URL HEALTH MONITOR")
        heading.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(heading)

        self.input_container = QVBoxLayout()
        self.add_input_field("")  # Start with one empty field

        scroll_widget = QWidget()
        scroll_widget.setLayout(self.input_container)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)

        btn_layout = QHBoxLayout()

        add_btn = QPushButton("Add Field")
        add_btn.clicked.connect(self.add_input_field)

        del_btn = QPushButton("Delete Field")
        del_btn.clicked.connect(self.delete_input_field)

        self.check_button = QPushButton("Check All")
        self.check_button.clicked.connect(self.check_all_urls)
        self.style_button(self.check_button, color="#4CAF50")

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(del_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.check_button)
        main_layout.addLayout(btn_layout)

        table_label = QLabel("URL Check Results")
        table_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        table_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(table_label)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["No", "URL", "Status", "Response Time"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 400)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 150)
        main_layout.addWidget(self.table)

        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.auto_refresh_recent_urls)
        self.refresh_timer.start(10000)
        print("URLMonitorApp initialized successfully!")

    def add_input_field(self, default_text=""):
        layout = QHBoxLayout()
        label = QLabel("Enter URL:")
        label.setFixedWidth(80)
        entry = QLineEdit()
        entry.setPlaceholderText("https://example.com")
        entry.setText(str(default_text))
        entry.setMinimumHeight(30)
        layout.addWidget(label)
        layout.addWidget(entry)
        container = QFrame()
        container.setLayout(layout)
        self.input_container.addWidget(container)
        self.url_entries.append((container, entry))

    def delete_input_field(self):
        if self.url_entries:
            container, _ = self.url_entries.pop()
            container.setParent(None)

    def check_all_urls(self):
        print("Checking all URLs...")
        self.table.setRowCount(0)
        self.check_results.clear()

        urls_to_check = []
        for container, entry in self.url_entries:
            url = entry.text().strip()
            if url:
                if not url.startswith("http://") and not url.startswith("https://"):
                    url = f"http://{url}"
                urls_to_check.append(url)

        # Clear entries and keep only one input field
        for container, _ in self.url_entries:
            container.setParent(None)
        self.url_entries.clear()
        self.add_input_field("")

        for i, url in enumerate(urls_to_check):
            print(f"Checking URL {i + 1}: {url}")
            try:
                start = time.perf_counter()
                response = requests.get(url, timeout=5)
                elapsed = time.perf_counter() - start
                status = "Healthy" if response.status_code == 200 else f"Status: {response.status_code}"
                response_time = f"{elapsed:.2f}s" if elapsed < 3.0 else "∞"
                print(f"URL {url}: {status} ({response_time})")
            except requests.exceptions.RequestException as e:
                print(f"URL {url}: Request failed - {e}")
                status = "Not Healthy"
                response_time = "∞"

            self.check_results.append((i + 1, url, status, response_time))

        self.populate_table()
        self.update_recent_urls(urls_to_check)

    def auto_refresh_recent_urls(self):
        print("Auto-refreshing recent URLs...")
        self.table.setRowCount(0)
        self.check_results.clear()

        recent_urls = self.get_recent_urls()[-5:]

        for i, url in enumerate(recent_urls):
            try:
                start = time.perf_counter()
                response = requests.get(url, timeout=5)
                elapsed = time.perf_counter() - start
                status = "Healthy" if response.status_code == 200 else f"Status: {response.status_code}"
                response_time = f"{elapsed:.2f}s" if elapsed < 3.0 else "∞"
            except requests.exceptions.RequestException:
                status = "Not reachable"
                response_time = "∞"

            self.check_results.append((i + 1, url, status, response_time))

        self.populate_table()

    def populate_table(self):
        self.table.setRowCount(len(self.check_results))
        for i, (no, url, status, response_time) in enumerate(self.check_results):
            self.table.setItem(i, 0, QTableWidgetItem(str(no)))
            self.table.setItem(i, 1, QTableWidgetItem(url))
            self.table.setItem(i, 2, QTableWidgetItem(status))
            self.table.setItem(i, 3, QTableWidgetItem(response_time))

    def update_recent_urls(self, urls):
        try:
            with open("recent_urls.json", "r") as f:
                existing = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing = []

        updated = list(dict.fromkeys(urls + existing))[:5]

        with open("recent_urls.json", "w") as f:
            json.dump(updated, f)

    def get_recent_urls(self):
        try:
            with open("recent_urls.json", "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def style_button(self, btn, color="#2196F3"):
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #1976D2;
            }}
            QPushButton:pressed {{
                background-color: #0D47A1;
            }}
        """)
        btn.setMinimumHeight(32)


if __name__ == "__main__":
    print("Creating QApplication...")
    app = QApplication(sys.argv)
    print("QApplication created successfully!")

    print("Creating main window...")
    window = URLMonitorApp()
    print("Main window created successfully!")

    print("Showing window...")
    window.show()
    print("Window shown, starting event loop...")

    try:
        sys.exit(app.exec())
    except Exception as e:
        print(f"Application error: {e}")
        import traceback

        traceback.print_exc()