import sys, os
from pathlib import Path
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QMainWindow,
    QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QStackedWidget, QLineEdit, QRadioButton,
    QCheckBox, QButtonGroup, QScrollArea
)


class StepIndicator(QWidget):
    """Custom progress step bar matching circles and connecting lines."""
    def __init__(self):
        super().__init__()
        self.setObjectName("step_container")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 10, 50, 10)

        top_layout = QHBoxLayout()
        top_layout.setSpacing(0)

        self.circle1 = QLabel("1", alignment=Qt.AlignmentFlag.AlignCenter)
        self.circle2 = QLabel("2", alignment=Qt.AlignmentFlag.AlignCenter)
        self.circle3 = QLabel("3", alignment=Qt.AlignmentFlag.AlignCenter)

        line1 = QFrame()
        line1.setObjectName("step_line")
        line1.setFrameShape(QFrame.Shape.HLine)

        line2 = QFrame()
        line2.setObjectName("step_line")
        line2.setFrameShape(QFrame.Shape.HLine)

        top_layout.addWidget(self.circle1)
        top_layout.addWidget(line1, stretch=1)
        top_layout.addWidget(self.circle2)
        top_layout.addWidget(line2, stretch=1)
        top_layout.addWidget(self.circle3)

        bottom_layout = QHBoxLayout()
        self.label1 = QLabel("Booking Details", alignment=Qt.AlignmentFlag.AlignCenter)
        self.label2 = QLabel("Confirmation", alignment=Qt.AlignmentFlag.AlignCenter)
        self.label3 = QLabel("Success", alignment=Qt.AlignmentFlag.AlignCenter)

        bottom_layout.addWidget(self.label1)
        bottom_layout.addWidget(self.label2)
        bottom_layout.addWidget(self.label3)

        layout.addLayout(top_layout)
        layout.addLayout(bottom_layout)

        self.set_step(0)

    def set_step(self, step_index: int):
        circles = [self.circle1, self.circle2, self.circle3]
        labels = [self.label1, self.label2, self.label3]

        for i in range(3):
            if i == step_index:
                circles[i].setProperty("class", "step-circle-active")
                labels[i].setProperty("class", "step-label-active")
            else:
                circles[i].setProperty("class", "step-circle-inactive")
                labels[i].setProperty("class", "step-label-inactive")

            circles[i].style().unpolish(circles[i])
            circles[i].style().polish(circles[i])
            labels[i].style().unpolish(labels[i])
            labels[i].style().polish(labels[i])


class addAppointment(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Book Appointment")
        self.setFixedSize(720, 560)

        main_container = QWidget()
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 15)
        main_layout.setSpacing(0)
        self.setCentralWidget(main_container)

        # ======= Top Header =======
        header_container = QWidget()
        header_container.setObjectName("header_container")
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(10, 8, 10, 8)

        self.close_btn = QPushButton("✕")
        self.close_btn.setObjectName("close_btn")
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.clicked.connect(self.close)

        self.header_title = QLabel("Book Appointment")
        self.header_title.setObjectName("header_title")

        self.confirm_btn = QPushButton("Confirm")
        self.confirm_btn.setObjectName("header_confirm_btn")
        self.confirm_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.confirm_btn.setFixedSize(110, 34)
        self.confirm_btn.clicked.connect(self.handle_next_confirm)

        header_layout.addWidget(self.close_btn)
        header_layout.addWidget(self.header_title)
        header_layout.addStretch()
        header_layout.addWidget(self.confirm_btn)

        # ======= Step Indicator =======
        self.step_indicator = StepIndicator()

        # ======= Stacked Content Pages =======
        self.stacked_widget = QStackedWidget()
        self.page1 = self.create_booking_details_page()
        self.page2 = self.create_confirmation_page()
        self.page3 = self.create_success_page()

        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)
        self.stacked_widget.addWidget(self.page3)

        main_layout.addWidget(header_container)
        main_layout.addWidget(self.step_indicator)
        main_layout.addWidget(self.stacked_widget)

        self.update_step_ui()

    # ---------------- PAGE 1: Booking Details ----------------
    def create_booking_details_page(self) -> QWidget:
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(35, 5, 35, 10)
        layout.setSpacing(10)

        lbl_pd = QLabel("Personal Details")
        lbl_pd.setProperty("class", "section-title")
        layout.addWidget(lbl_pd)

        pd_grid = QGridLayout()
        pd_grid.setHorizontalSpacing(15)
        pd_grid.setVerticalSpacing(6)

        self.first_name_in = QLineEdit()
        self.last_name_in = QLineEdit()
        self.phone_in = QLineEdit()
        self.email_in = QLineEdit()
        self.address_in = QLineEdit()

        pd_grid.addWidget(QLabel("First Name*"), 0, 0)
        pd_grid.addWidget(self.first_name_in, 1, 0)
        pd_grid.addWidget(QLabel("Last Name*"), 0, 1)
        pd_grid.addWidget(self.last_name_in, 1, 1)
        pd_grid.addWidget(QLabel("Phone No.*"), 0, 2)
        pd_grid.addWidget(self.phone_in, 1, 2)

        pd_grid.addWidget(QLabel("Email Address*"), 2, 0)
        pd_grid.addWidget(self.email_in, 3, 0, 1, 2)
        pd_grid.addWidget(QLabel("Home Address*"), 2, 2)
        pd_grid.addWidget(self.address_in, 3, 2)

        layout.addLayout(pd_grid)

        lbl_srv = QLabel("Services*")
        lbl_srv.setProperty("class", "section-title")
        layout.addWidget(lbl_srv)

        srv_layout = QHBoxLayout()
        self.srv_group = QButtonGroup(self)
        self.radio_fold = QRadioButton("Wash-and-Fold")
        self.radio_iron = QRadioButton("Pressing & Ironing")
        self.radio_dry = QRadioButton("Dry-Cleaning")

        self.radio_fold.setChecked(True)
        self.srv_group.addButton(self.radio_fold)
        self.srv_group.addButton(self.radio_iron)
        self.srv_group.addButton(self.radio_dry)

        srv_layout.addWidget(self.radio_fold)
        srv_layout.addWidget(self.radio_iron)
        srv_layout.addWidget(self.radio_dry)
        srv_layout.addStretch()
        layout.addLayout(srv_layout)

        lbl_spec = QLabel("Laundry Specifications")
        lbl_spec.setProperty("class", "section-title")
        layout.addWidget(lbl_spec)

        spec_grid = QGridLayout()
        spec_grid.setHorizontalSpacing(15)

        self.weight_in = QLineEdit()
        self.weight_in.setPlaceholderText("kg")
        self.count_in = QLineEdit()
        self.count_in.setPlaceholderText("#")

        spec_grid.addWidget(QLabel("Weight of Laundry (kg)*"), 0, 0)
        spec_grid.addWidget(self.weight_in, 1, 0)

        spec_grid.addWidget(QLabel("Count of Garments*"), 0, 1)
        spec_grid.addWidget(self.count_in, 1, 1)

        addons_box = QVBoxLayout()
        addons_box.addWidget(QLabel("Add-ons"))
        addons_row = QHBoxLayout()
        self.cb_softener = QCheckBox("Fabric Softener")
        self.cb_bleach = QCheckBox("Bleach")
        self.cb_soda = QCheckBox("Baking Soda")
        self.cb_spin = QCheckBox("Extra Spin")

        addons_row.addWidget(self.cb_softener)
        addons_row.addWidget(self.cb_bleach)
        addons_row.addWidget(self.cb_soda)
        addons_row.addWidget(self.cb_spin)
        addons_box.addLayout(addons_row)

        spec_grid.addLayout(addons_box, 0, 2, 2, 1)
        layout.addLayout(spec_grid)

        layout.addWidget(QLabel("Note/Additional Requests"))
        self.note_in = QLineEdit()
        layout.addWidget(self.note_in)

        lbl_sched = QLabel("Schedule Pick-Up/Delivery*")
        lbl_sched.setProperty("class", "section-title")
        layout.addWidget(lbl_sched)

        delivery_layout = QHBoxLayout()
        delivery_layout.setSpacing(15)

        self.pill_priority = QPushButton("Priority\n15~60 mins")
        self.pill_sameday = QPushButton("Same-Day\n~24 hours")
        self.pill_standard = QPushButton("Standard\n24~ hours")

        self.delivery_pills = [self.pill_priority, self.pill_sameday, self.pill_standard]
        self.selected_delivery = "Priority (15~60 mins)"

        for btn in self.delivery_pills:
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setCheckable(True)

        self.pill_priority.setChecked(True)
        self.update_delivery_pills()

        self.pill_priority.clicked.connect(lambda: self.select_delivery(0, "Priority (15~60 mins)"))
        self.pill_sameday.clicked.connect(lambda: self.select_delivery(1, "Same-Day (~24 hours)"))
        self.pill_standard.clicked.connect(lambda: self.select_delivery(2, "Standard (24~ hours)"))

        delivery_layout.addWidget(self.pill_priority)
        delivery_layout.addWidget(self.pill_sameday)
        delivery_layout.addWidget(self.pill_standard)
        delivery_layout.addStretch()

        layout.addLayout(delivery_layout)

        scroll_area.setWidget(page)
        return scroll_area

    def select_delivery(self, index: int, value: str):
        self.selected_delivery = value
        for idx, btn in enumerate(self.delivery_pills):
            btn.setChecked(idx == index)
        self.update_delivery_pills()

    def update_delivery_pills(self):
        for btn in self.delivery_pills:
            if btn.isChecked():
                btn.setProperty("class", "delivery-pill-selected")
            else:
                btn.setProperty("class", "delivery-pill")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    # ---------------- PAGE 2: Confirmation ----------------
    def create_confirmation_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(60, 10, 60, 20)

        card = QFrame()
        card.setObjectName("payment_card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 15, 25, 20)

        title = QLabel("Payment Details", alignment=Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("payment_title")

        divider = QFrame()
        divider.setObjectName("card_divider")
        divider.setFrameShape(QFrame.Shape.HLine)

        self.summary_lbl = QLabel()
        self.summary_lbl.setObjectName("summary_text")
        self.summary_lbl.setTextFormat(Qt.TextFormat.RichText)

        card_layout.addWidget(title)
        card_layout.addWidget(divider)
        card_layout.addWidget(self.summary_lbl)
        card_layout.addStretch()

        layout.addWidget(card)
        return page

    # ---------------- PAGE 3: Success Screen ----------------
    def create_success_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        msg = QLabel("Appointment has been successfully booked.")
        msg.setObjectName("success_msg")
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)

        outer_circle = QLabel()
        outer_circle.setObjectName("success_check_outer")
        outer_layout = QVBoxLayout(outer_circle)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        inner_circle = QLabel("✓", alignment=Qt.AlignmentFlag.AlignCenter)
        inner_circle.setObjectName("success_check_inner")

        outer_layout.addWidget(inner_circle)

        proceed_btn = QPushButton("Proceed to Dashboard")
        proceed_btn.setObjectName("proceed_btn")
        proceed_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        proceed_btn.clicked.connect(self.close)

        thank_you = QLabel("Thank you for trusting us!")
        thank_you.setObjectName("thank_you_lbl")

        layout.addWidget(msg)
        layout.addWidget(outer_circle, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(proceed_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(thank_you, alignment=Qt.AlignmentFlag.AlignCenter)

        return page

    # ---------------- Navigation Logic ----------------
    def handle_next_confirm(self):
        curr = self.stacked_widget.currentIndex()

        if curr == 0:
            self.populate_summary()
            self.stacked_widget.setCurrentIndex(1)
            self.update_step_ui()
        elif curr == 1:
            self.stacked_widget.setCurrentIndex(2)
            self.update_step_ui()

    def update_step_ui(self):
        curr = self.stacked_widget.currentIndex()
        self.step_indicator.set_step(curr)

        if curr == 2:
            self.confirm_btn.hide()
        else:
            self.confirm_btn.show()

    def populate_summary(self):
        fname = self.first_name_in.text().strip() or "Guest"
        lname = self.last_name_in.text().strip()
        full_name = f"{fname} {lname}".strip()

        weight = self.weight_in.text().strip() or "N/A"
        garments = self.count_in.text().strip() or "N/A"

        addons = []
        if self.cb_softener.isChecked(): addons.append("Fabric Softener")
        if self.cb_bleach.isChecked(): addons.append("Bleach")
        if self.cb_soda.isChecked(): addons.append("Baking Soda")
        if self.cb_spin.isChecked(): addons.append("Extra Spin")
        addons_str = ", ".join(addons) if addons else "None"

        selected_service = "Wash-and-Fold"
        if self.radio_iron.isChecked(): selected_service = "Pressing & Ironing"
        if self.radio_dry.isChecked(): selected_service = "Dry-Cleaning"

        try:
            cost = float(weight) * 5.0 + 10.0
            cost_str = f"${cost:.2f}"
        except ValueError:
            cost_str = "$45.00"

        html_summary = f"""
        <table width='100%' style='margin-top:15px; line-height: 2.2;'>
            <tr>
                <td style='font-size: 15px; font-weight: bold;'>Total Cost:</td>
                <td align='right' style='font-size: 18px; font-weight: bold;'>{cost_str}</td>
            </tr>
            <tr>
                <td style='font-size: 14px; font-weight: bold;'>Name:</td>
                <td align='right' style='font-size: 14px;'>{full_name}</td>
            </tr>
            <tr>
                <td style='font-size: 14px; font-weight: bold;'>Option of Delivery:</td>
                <td align='right' style='font-size: 14px;'>{self.selected_delivery}</td>
            </tr>
        </table>
        <br>
        <p style='font-size: 14px; font-weight: bold; margin-bottom: 5px;'>Laundry Specifications:</p>
        <ul style='margin-left: 15px; line-height: 1.8; color: #3C5670;'>
            <li>Service: <b>{selected_service}</b></li>
            <li>Weight: <b>{weight} kg</b> ({garments} Garments)</li>
            <li>Add-ons: <b>{addons_str}</b></li>
        </ul>
        """
        self.summary_lbl.setText(html_summary)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qss_file = Path(__file__).with_name("addAppointment.qss")
    if qss_file.exists():
        app.setStyleSheet(qss_file.read_text())
    win = addAppointment()
    win.show()
    sys.exit(app.exec())