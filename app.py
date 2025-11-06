from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from pathlib import Path
import sys
from universal_oc_manager.ui.backend import AppController


def main() -> int:
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    
    # Project base path
    base_path = Path(__file__).parent
    qml_path = base_path / "universal_oc_manager" / "ui" / "qml"
    engine.addImportPath(str(qml_path))
    
    backend = AppController()
    engine.rootContext().setContextProperty("backend", backend)
    
    main_qml = qml_path / "Main.qml"
    if not main_qml.exists():
        print(f"ERROR: {main_qml} not found!", file=sys.stderr)
        return 1
    
    engine.load(QUrl.fromLocalFile(str(main_qml)))
    if not engine.rootObjects():
        return 1
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
