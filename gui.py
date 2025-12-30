#!/usr/bin/env python3
"""Voyager PyQt6 configuration GUI.

This tool provides a graphical interface to configure Voyager's LLM settings.

It offers two mutually-exclusive option sets based on the selected models:
- Settings (new): reasoning_effort / verbosity / store
- Old settings (legacy): temperature / max_tokens / top_p / store

The "Old settings" tab is only available when *all* selected agent models are
within the legacy range: gpt-3.5-turbo .. gpt-4.1.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Dict, List, Tuple

from PyQt6.QtCore import QSignalBlocker, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


PREMIUM_QSS = """
QWidget {
    background: #0b1020;
    color: #e5e7eb;
    font-family: "Segoe UI", "Inter", "Arial";
    font-size: 13px;
}

QLabel#TitleLabel {
    font-size: 18px;
    font-weight: 700;
    color: #f8fafc;
}

QLabel#SubtitleLabel {
    color: #94a3b8;
}

QTabWidget::pane {
    border: 1px solid #24314f;
    border-radius: 10px;
    padding: 8px;
}

QTabBar::tab {
    background: #101b33;
    border: 1px solid #24314f;
    border-bottom: none;
    padding: 8px 14px;
    margin-right: 4px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}

QTabBar::tab:selected {
    background: #162443;
    color: #e0f2fe;
}

QGroupBox {
    border: 1px solid #24314f;
    border-radius: 10px;
    margin-top: 12px;
    padding: 14px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    color: #93c5fd;
    font-weight: 600;
}

QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
    background: #0a1328;
    border: 1px solid #24314f;
    border-radius: 8px;
    padding: 6px 10px;
}

QComboBox::drop-down {
    border: none;
}

QComboBox QAbstractItemView {
    background: #0a1328;
    border: 1px solid #24314f;
    selection-background-color: #1d4ed8;
}

QCheckBox {
    spacing: 10px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
}

QPushButton {
    background: #1d4ed8;
    border: 1px solid #1e40af;
    border-radius: 10px;
    padding: 8px 14px;
    font-weight: 600;
}

QPushButton:hover {
    background: #2563eb;
}

QPushButton:disabled {
    background: #101b33;
    color: #64748b;
    border: 1px solid #24314f;
}
"""


LEGACY_MODELS = {
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-turbo",
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4.1",
}

LEGACY_MODEL_MAX_TOKENS = {
    "gpt-3.5-turbo": 16385,
    "gpt-4": 8192,
    "gpt-4-turbo": 128000,
    "gpt-4o": 128000,
    "gpt-4o-mini": 128000,
    "gpt-4.1": 128000,
}


@dataclass(frozen=True)
class SettingsSupport:
    reasoning_effort: bool
    verbosity: bool
    store: bool
    xhigh_reasoning: bool


def _boolish(value) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes", "y", "on"}
    return False


def model_support(model: str) -> SettingsSupport:
    if model in LEGACY_MODELS:
        return SettingsSupport(
            reasoning_effort=False,
            verbosity=False,
            store=True,
            xhigh_reasoning=False,
        )

    if model == "gpt-5.2-pro":
        return SettingsSupport(
            reasoning_effort=False,
            verbosity=False,
            store=True,
            xhigh_reasoning=False,
        )

    if model in {"o1", "o3", "o4-mini"}:
        return SettingsSupport(
            reasoning_effort=True,
            verbosity=False,
            store=True,
            xhigh_reasoning=False,
        )

    if model == "gpt-5.2":
        return SettingsSupport(
            reasoning_effort=True,
            verbosity=True,
            store=True,
            xhigh_reasoning=True,
        )

    return SettingsSupport(
        reasoning_effort=True,
        verbosity=True,
        store=True,
        xhigh_reasoning=False,
    )


class VoyagerConfigWindow(QMainWindow):
    MODELS = [
        "gpt-5.2-pro",
        "gpt-5.2",
        "gpt-5.1",
        "gpt-5-mini",
        "gpt-4.1",
        "gpt-4.1-mini",
        "o4-mini",
        "o3",
        "o1",
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo",
        "gpt-4",
        "gpt-3.5-turbo",
    ]

    VERBOSITY = ["low", "medium", "high"]

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Voyager • Model & Settings")
        self.setMinimumSize(900, 620)

        font = QFont()
        font.setPointSize(10)
        self.setFont(font)

        root = QWidget()
        self.setCentralWidget(root)

        outer = QVBoxLayout(root)
        outer.setContentsMargins(18, 16, 18, 16)
        outer.setSpacing(12)

        title = QLabel("Voyager Configuration")
        title.setObjectName("TitleLabel")
        subtitle = QLabel(
            "Choose agent models, then configure either Settings (new) or Old settings (legacy)."
        )
        subtitle.setObjectName("SubtitleLabel")
        outer.addWidget(title)
        outer.addWidget(subtitle)

        self.tabs = QTabWidget()
        outer.addWidget(self.tabs, 1)

        self.models_tab = QWidget()
        self.settings_tab = QWidget()
        self.old_settings_tab = QWidget()

        self.tabs.addTab(self.models_tab, "Models")
        self.settings_tab_index = self.tabs.addTab(self.settings_tab, "Settings")
        self.old_settings_tab_index = self.tabs.addTab(self.old_settings_tab, "Old settings")

        self._build_models_tab()
        self._build_settings_tab()
        self._build_old_settings_tab()

        outer.addLayout(self._build_buttons())

        self._reset_to_defaults(show_message=False)

        QApplication.instance().setStyleSheet(PREMIUM_QSS)

        self._on_models_changed()

    def _build_models_tab(self) -> None:
        layout = QVBoxLayout(self.models_tab)
        layout.setContentsMargins(8, 8, 8, 8)

        group = QGroupBox("Agent models")
        layout.addWidget(group)

        form = QFormLayout(group)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        form.setHorizontalSpacing(14)
        form.setVerticalSpacing(10)

        self.action_agent_model = QComboBox()
        self.action_agent_model.addItems(self.MODELS)

        self.curriculum_agent_model = QComboBox()
        self.curriculum_agent_model.addItems(self.MODELS)

        self.curriculum_qa_model = QComboBox()
        self.curriculum_qa_model.addItems(self.MODELS)

        self.critic_agent_model = QComboBox()
        self.critic_agent_model.addItems(self.MODELS)

        self.skill_manager_model = QComboBox()
        self.skill_manager_model.addItems(self.MODELS)

        form.addRow("Action agent", self.action_agent_model)
        form.addRow("Curriculum agent", self.curriculum_agent_model)
        form.addRow("Curriculum QA", self.curriculum_qa_model)
        form.addRow("Critic agent", self.critic_agent_model)
        form.addRow("Skill manager", self.skill_manager_model)

        note = QLabel(
            "Old settings are only available when all selected models are between gpt-3.5-turbo and gpt-4.1."
        )
        note.setObjectName("SubtitleLabel")
        layout.addWidget(note)

        for combo in (
            self.action_agent_model,
            self.curriculum_agent_model,
            self.curriculum_qa_model,
            self.critic_agent_model,
            self.skill_manager_model,
        ):
            combo.currentTextChanged.connect(self._on_models_changed)

    def _build_settings_tab(self) -> None:
        layout = QVBoxLayout(self.settings_tab)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(12)

        self.settings_unavailable = QLabel("")
        self.settings_unavailable.setObjectName("SubtitleLabel")
        self.settings_unavailable.setWordWrap(True)
        layout.addWidget(self.settings_unavailable)

        self.settings_group = QGroupBox("Settings")
        layout.addWidget(self.settings_group)

        form = QFormLayout(self.settings_group)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form.setHorizontalSpacing(14)
        form.setVerticalSpacing(12)

        self.reasoning_effort = QComboBox()
        self.verbosity = QComboBox()

        self.store_settings = QCheckBox("Enable store")
        self.store_settings.setToolTip("Whether to store conversation history (store).")

        form.addRow("Reasoning effort", self.reasoning_effort)
        form.addRow("Verbosity", self.verbosity)
        form.addRow("Store", self.store_settings)

        self.store_settings.stateChanged.connect(lambda _: self._sync_store(from_settings=True))

        layout.addStretch(1)

    def _build_old_settings_tab(self) -> None:
        layout = QVBoxLayout(self.old_settings_tab)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(12)

        self.old_unavailable = QLabel("")
        self.old_unavailable.setObjectName("SubtitleLabel")
        self.old_unavailable.setWordWrap(True)
        layout.addWidget(self.old_unavailable)

        self.old_group = QGroupBox("Old settings")
        layout.addWidget(self.old_group)

        form = QFormLayout(self.old_group)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form.setHorizontalSpacing(14)
        form.setVerticalSpacing(12)

        self.temperature = QDoubleSpinBox()
        self.temperature.setRange(0.0, 2.0)
        self.temperature.setDecimals(2)
        self.temperature.setSingleStep(0.05)

        self.top_p = QDoubleSpinBox()
        self.top_p.setRange(0.0, 2.0)
        self.top_p.setDecimals(2)
        self.top_p.setSingleStep(0.05)
        self.top_p.setValue(1.0)

        self.max_tokens = QSpinBox()
        self.max_tokens.setRange(0, 128000)
        self.max_tokens.setSingleStep(256)

        self.max_tokens_hint = QLabel("")
        self.max_tokens_hint.setObjectName("SubtitleLabel")

        self.store_old = QCheckBox("Enable store")
        self.store_old.setToolTip("Whether to store conversation history (store).")
        self.store_old.stateChanged.connect(lambda _: self._sync_store(from_settings=False))

        form.addRow("Temperature", self.temperature)
        form.addRow("Top-p", self.top_p)
        form.addRow("Max tokens", self.max_tokens)
        form.addRow("", self.max_tokens_hint)
        form.addRow("Store", self.store_old)

        layout.addStretch(1)

    def _build_buttons(self) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(10)

        self.save_btn = QPushButton("Save config")
        self.save_btn.clicked.connect(self._save_config)

        self.load_btn = QPushButton("Load config")
        self.load_btn.clicked.connect(self._load_config)

        self.generate_btn = QPushButton("Generate code")
        self.generate_btn.clicked.connect(self._generate_code)

        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(lambda: self._reset_to_defaults(show_message=True))

        self.exit_btn = QPushButton("Exit")
        self.exit_btn.clicked.connect(self.close)

        row.addWidget(self.save_btn)
        row.addWidget(self.load_btn)
        row.addWidget(self.generate_btn)
        row.addWidget(self.reset_btn)
        row.addStretch(1)
        row.addWidget(self.exit_btn)
        return row

    def _selected_models(self) -> List[str]:
        return [
            self.action_agent_model.currentText(),
            self.curriculum_agent_model.currentText(),
            self.curriculum_qa_model.currentText(),
            self.critic_agent_model.currentText(),
            self.skill_manager_model.currentText(),
        ]

    def _compute_mode(self) -> Tuple[bool, bool]:
        selected = self._selected_models()
        all_legacy = all(m in LEGACY_MODELS for m in selected)
        any_legacy = any(m in LEGACY_MODELS for m in selected)
        return all_legacy, any_legacy

    def _on_models_changed(self) -> None:
        all_legacy, any_legacy = self._compute_mode()

        # Fix: Enable new settings if ANY model is non-legacy (new)
        # Enable old settings only if ALL models are legacy
        old_enabled = all_legacy
        settings_enabled = not all_legacy  # Enable new settings if not all legacy (including mixed)

        self.tabs.setTabEnabled(self.settings_tab_index, settings_enabled)
        self.tabs.setTabEnabled(self.old_settings_tab_index, old_enabled)

        if not settings_enabled:
            # This should never happen now since settings_enabled = not all_legacy
            self.settings_unavailable.setText(
                "Settings are disabled because all selected models are legacy. Use Old settings instead."
            )
        else:
            self.settings_unavailable.setText("")

        if not old_enabled:
            if any_legacy:
                self.old_unavailable.setText(
                    "Old settings are only available when all selected models are legacy (gpt-3.5-turbo..gpt-4.1). "
                    "You have selected newer models, so use Settings instead."
                )
            else:
                self.old_unavailable.setText(
                    "Old settings are only available for legacy models (gpt-3.5-turbo..gpt-4.1)."
                )
        else:
            self.old_unavailable.setText("")

        self.settings_group.setEnabled(settings_enabled)
        self.old_group.setEnabled(old_enabled)

        if settings_enabled:
            self._refresh_settings_controls()

        if old_enabled:
            self._refresh_old_settings_controls()

        current = self.tabs.currentIndex()
        if not self.tabs.isTabEnabled(current):
            self.tabs.setCurrentIndex(0)

    def _refresh_settings_controls(self) -> None:
        selected = self._selected_models()
        supports = [model_support(m) for m in selected]

        # Fix: Enable settings if ANY model supports them (for mixed scenarios)
        reasoning_ok = any(s.reasoning_effort for s in supports)
        verbosity_ok = any(s.verbosity for s in supports)
        store_ok = any(s.store for s in supports)
        xhigh_ok = any(s.xhigh_reasoning for s in supports)

        reasoning_values = ["none", "low", "medium", "high"]
        if xhigh_ok:
            reasoning_values.append("xhigh")

        current_reasoning = self.reasoning_effort.currentText() or "none"
        with QSignalBlocker(self.reasoning_effort):
            self.reasoning_effort.clear()
            self.reasoning_effort.addItems(reasoning_values)
            if current_reasoning in reasoning_values:
                self.reasoning_effort.setCurrentText(current_reasoning)
            else:
                self.reasoning_effort.setCurrentText("high" if "high" in reasoning_values else "none")

        current_verbosity = self.verbosity.currentText() or "medium"
        with QSignalBlocker(self.verbosity):
            self.verbosity.clear()
            self.verbosity.addItems(self.VERBOSITY)
            if current_verbosity in self.VERBOSITY:
                self.verbosity.setCurrentText(current_verbosity)
            else:
                self.verbosity.setCurrentText("medium")

        self.reasoning_effort.setEnabled(reasoning_ok)
        self.verbosity.setEnabled(verbosity_ok)
        self.store_settings.setEnabled(store_ok)

        if not reasoning_ok:
            with QSignalBlocker(self.reasoning_effort):
                if self.reasoning_effort.currentText() != "none":
                    self.reasoning_effort.setCurrentText("none")

        if not verbosity_ok:
            with QSignalBlocker(self.verbosity):
                if self.verbosity.currentText() != "medium":
                    self.verbosity.setCurrentText("medium")

    def _refresh_old_settings_controls(self) -> None:
        selected = self._selected_models()
        maxes = [LEGACY_MODEL_MAX_TOKENS.get(m, 8192) for m in selected]
        limit = min(maxes) if maxes else 8192

        with QSignalBlocker(self.max_tokens):
            self.max_tokens.setMaximum(limit)

        self.max_tokens_hint.setText(f"Max tokens range: 0 .. {limit} (based on selected model(s))")

    def _sync_store(self, *, from_settings: bool) -> None:
        if from_settings:
            value = self.store_settings.isChecked()
            with QSignalBlocker(self.store_old):
                self.store_old.setChecked(value)
        else:
            value = self.store_old.isChecked()
            with QSignalBlocker(self.store_settings):
                self.store_settings.setChecked(value)

    def _default_config(self) -> Dict:
        return {
            "action_agent": {"model": "gpt-4", "temperature": 0.0},
            "curriculum_agent": {
                "model": "gpt-4",
                "temperature": 0.0,
                "qa_model": "gpt-3.5-turbo",
                "qa_temperature": 0.0,
            },
            "critic_agent": {"model": "gpt-4", "temperature": 0.0},
            "skill_manager": {"model": "gpt-3.5-turbo", "temperature": 0.0},
            "settings": {
                "reasoning_effort": "none",
                "verbosity": "medium",
                "store": False,
            },
            "old_settings": {
                "temperature": 0.0,
                "top_p": 1.0,
                "max_tokens": 0,
                "store": False,
            },
        }

    def _reset_to_defaults(self, *, show_message: bool) -> None:
        cfg = self._default_config()

        self.action_agent_model.setCurrentText(cfg["action_agent"]["model"])
        self.curriculum_agent_model.setCurrentText(cfg["curriculum_agent"]["model"])
        self.curriculum_qa_model.setCurrentText(cfg["curriculum_agent"]["qa_model"])
        self.critic_agent_model.setCurrentText(cfg["critic_agent"]["model"])
        self.skill_manager_model.setCurrentText(cfg["skill_manager"]["model"])

        self.temperature.setValue(float(cfg["old_settings"]["temperature"]))
        self.top_p.setValue(float(cfg["old_settings"]["top_p"]))
        self.max_tokens.setValue(int(cfg["old_settings"]["max_tokens"]))

        self.reasoning_effort.setCurrentText(cfg["settings"]["reasoning_effort"])
        self.verbosity.setCurrentText(cfg["settings"]["verbosity"])

        self.store_settings.setChecked(bool(cfg["settings"]["store"]))
        self.store_old.setChecked(bool(cfg["old_settings"]["store"]))
        self._sync_store(from_settings=True)

        self._on_models_changed()

        if show_message:
            QMessageBox.information(self, "Reset", "Configuration reset to defaults.")

    def _config_from_ui(self) -> Dict:
        cfg = self._default_config()

        cfg["action_agent"]["model"] = self.action_agent_model.currentText()
        cfg["curriculum_agent"]["model"] = self.curriculum_agent_model.currentText()
        cfg["curriculum_agent"]["qa_model"] = self.curriculum_qa_model.currentText()
        cfg["critic_agent"]["model"] = self.critic_agent_model.currentText()
        cfg["skill_manager"]["model"] = self.skill_manager_model.currentText()

        all_legacy, any_legacy = self._compute_mode()

        if all_legacy:
            temp = float(self.temperature.value())
            cfg["action_agent"]["temperature"] = temp
            cfg["curriculum_agent"]["temperature"] = temp
            cfg["curriculum_agent"]["qa_temperature"] = temp
            cfg["critic_agent"]["temperature"] = temp
            cfg["skill_manager"]["temperature"] = temp

            cfg["old_settings"]["temperature"] = temp
            cfg["old_settings"]["top_p"] = float(self.top_p.value())
            cfg["old_settings"]["max_tokens"] = int(self.max_tokens.value())
        else:
            cfg["old_settings"]["temperature"] = None
            cfg["old_settings"]["top_p"] = None
            cfg["old_settings"]["max_tokens"] = None

        # Fix: Save settings if settings tab is enabled (i.e., not all models are legacy)
        if not all_legacy:
            cfg["settings"]["reasoning_effort"] = (
                self.reasoning_effort.currentText() if self.reasoning_effort.isEnabled() else None
            )
            cfg["settings"]["verbosity"] = (
                self.verbosity.currentText() if self.verbosity.isEnabled() else None
            )
        else:
            cfg["settings"]["reasoning_effort"] = None
            cfg["settings"]["verbosity"] = None

        store_value = self.store_settings.isChecked() or self.store_old.isChecked()
        cfg["settings"]["store"] = store_value
        cfg["old_settings"]["store"] = store_value

        return cfg

    def _apply_loaded_config(self, cfg: Dict) -> None:
        def _get_settings(source: Dict) -> Dict:
            if isinstance(source.get("settings"), dict):
                return source["settings"]
            return {
                "reasoning_effort": source.get("reasoning_effort"),
                "verbosity": source.get("verbosity"),
                "store": source.get("store"),
            }

        def _get_old_settings(source: Dict) -> Dict:
            if isinstance(source.get("old_settings"), dict):
                return source["old_settings"]
            return {
                "temperature": source.get("temperature"),
                "top_p": source.get("top_p"),
                "max_tokens": source.get("max_tokens"),
                "store": source.get("store"),
            }

        settings = _get_settings(cfg)
        old = _get_old_settings(cfg)

        self.action_agent_model.setCurrentText(cfg.get("action_agent", {}).get("model", "gpt-4"))
        self.curriculum_agent_model.setCurrentText(
            cfg.get("curriculum_agent", {}).get("model", "gpt-4")
        )
        self.curriculum_qa_model.setCurrentText(
            cfg.get("curriculum_agent", {}).get("qa_model", "gpt-3.5-turbo")
        )
        self.critic_agent_model.setCurrentText(cfg.get("critic_agent", {}).get("model", "gpt-4"))
        self.skill_manager_model.setCurrentText(
            cfg.get("skill_manager", {}).get("model", "gpt-3.5-turbo")
        )

        self._on_models_changed()

        if self.old_group.isEnabled():
            temp = old.get("temperature")
            if temp is None:
                temp = cfg.get("action_agent", {}).get("temperature", 0.0)
            if temp is not None:
                self.temperature.setValue(float(temp))

            if old.get("top_p") is not None:
                self.top_p.setValue(float(old["top_p"]))
            if old.get("max_tokens") is not None:
                self.max_tokens.setValue(int(old["max_tokens"]))

        if self.settings_group.isEnabled():
            if settings.get("reasoning_effort"):
                self.reasoning_effort.setCurrentText(str(settings["reasoning_effort"]))
            if settings.get("verbosity"):
                self.verbosity.setCurrentText(str(settings["verbosity"]))

        store = _boolish(settings.get("store") if settings.get("store") is not None else old.get("store"))
        self.store_settings.setChecked(store)
        self.store_old.setChecked(store)
        self._sync_store(from_settings=True)

        self._on_models_changed()

    def _save_config(self) -> None:
        cfg = self._config_from_ui()

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Voyager configuration",
            "voyager_config.json",
            "JSON files (*.json);;All files (*.*)",
        )
        if not filename:
            return

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(cfg, f, indent=4)
            QMessageBox.information(self, "Saved", f"Configuration saved to:\n{filename}")
        except Exception as e:  # pragma: no cover
            QMessageBox.critical(self, "Error", f"Failed to save configuration:\n{e}")

    def _load_config(self) -> None:
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Load Voyager configuration",
            "",
            "JSON files (*.json);;All files (*.*)",
        )
        if not filename:
            return

        try:
            with open(filename, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            if not isinstance(cfg, dict):
                raise ValueError("Config must be a JSON object")
            self._apply_loaded_config(cfg)
            QMessageBox.information(self, "Loaded", f"Configuration loaded from:\n{filename}")
        except Exception as e:  # pragma: no cover
            QMessageBox.critical(self, "Error", f"Failed to load configuration:\n{e}")

    def _generate_code(self) -> None:
        cfg = self._config_from_ui()

        models = {
            "action": cfg["action_agent"]["model"],
            "curriculum": cfg["curriculum_agent"]["model"],
            "qa": cfg["curriculum_agent"]["qa_model"],
            "critic": cfg["critic_agent"]["model"],
            "skill": cfg["skill_manager"]["model"],
        }
        temps = {
            "action": cfg["action_agent"]["temperature"],
            "curriculum": cfg["curriculum_agent"]["temperature"],
            "qa": cfg["curriculum_agent"]["qa_temperature"],
            "critic": cfg["critic_agent"]["temperature"],
            "skill": cfg["skill_manager"]["temperature"],
        }

        all_legacy, any_legacy = self._compute_mode()

        chat_opts: Dict[str, object] = {"store": bool(cfg["settings"]["store"])}

        # Fix: Use settings if not all models are legacy (including mixed scenarios)
        if not all_legacy:
            if cfg["settings"]["reasoning_effort"] is not None:
                chat_opts["reasoning_effort"] = cfg["settings"]["reasoning_effort"]
            if cfg["settings"]["verbosity"] is not None:
                chat_opts["verbosity"] = cfg["settings"]["verbosity"]

        if all_legacy:
            if cfg["old_settings"]["max_tokens"] is not None:
                chat_opts["max_tokens"] = int(cfg["old_settings"]["max_tokens"])
            if cfg["old_settings"]["top_p"] is not None:
                chat_opts["top_p"] = float(cfg["old_settings"]["top_p"])

        code = f'''"""Voyager configuration generated by the PyQt6 GUI.

You can also save a JSON config and load it from example_usage.py.
"""

from voyager import Voyager

openai_api_key = "YOUR_OPENAI_API_KEY"

azure_login = {{
    "client_id": "YOUR_CLIENT_ID",
    "redirect_url": "https://127.0.0.1/auth-response",
    "secret_value": "[OPTIONAL] YOUR_SECRET_VALUE",
    "version": "fabric-loader-0.14.18-1.19",
}}

voyager = Voyager(
    azure_login=azure_login,
    openai_api_key=openai_api_key,
    action_agent_model_name={models["action"]!r},
    action_agent_temperature={temps["action"]!r},
    curriculum_agent_model_name={models["curriculum"]!r},
    curriculum_agent_temperature={temps["curriculum"]!r},
    curriculum_agent_qa_model_name={models["qa"]!r},
    curriculum_agent_qa_temperature={temps["qa"]!r},
    critic_agent_model_name={models["critic"]!r},
    critic_agent_temperature={temps["critic"]!r},
    skill_manager_model_name={models["skill"]!r},
    skill_manager_temperature={temps["skill"]!r},
)

# Additional Chat Completions API options (LangChain ChatOpenAI kwargs)
chat_completions_options = {json.dumps(chat_opts, indent=4)}

# voyager.learn()
'''

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save generated Python code",
            "voyager_config.py",
            "Python files (*.py);;All files (*.*)",
        )
        if not filename:
            return

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(code)
            QMessageBox.information(self, "Generated", f"Code generated and saved to:\n{filename}")
        except Exception as e:  # pragma: no cover
            QMessageBox.critical(self, "Error", f"Failed to save code:\n{e}")


def main() -> None:
    app = QApplication([])
    win = VoyagerConfigWindow()
    win.show()
    app.exec()


if __name__ == "__main__":
    main()
