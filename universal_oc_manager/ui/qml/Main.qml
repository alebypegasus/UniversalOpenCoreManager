import QtQuick 6.5
import QtQuick.Controls 6.5
import QtQuick.Layouts 6.5
import QtGraphicalEffects 1.15

ApplicationWindow {
    id: win
    width: 1200
    height: 800
    visible: true
    title: "Universal OpenCore Manager"

    property var validationErrors: []

    // Conectar sinal do backend
    Connections {
        target: backend
        function onValidationErrorsChanged(errors) {
            validationErrors = errors
        }
        function onHardwareDetected(profile) {
            statusText.text = `Hardware detectado: ${profile.cpu || "N/A"}`
        }
        function onEfiGenerated(path) {
            statusText.text = `EFI gerada em: ${path}`
        }
    }

    // Tema tipo Liquid Glass básico (placeholder)
    background: Rectangle {
        anchors.fill: parent
        color: "#1A1A1ACC" // translúcido
    }

    header: ToolBar {
        RowLayout {
            anchors.fill: parent
            Label { text: "Mestre EFI"; font.pixelSize: 16; color: "#FFFFFF" }
            Item { Layout.fillWidth: true }
            Label {
                id: statusText
                text: "Pronto"
                color: "#CCCCCC"
                font.pixelSize: 12
            }
            Button { text: qsTr("Preferências") }
        }
    }

    SplitView {
        anchors.fill: parent

        // Sidebar
        Frame {
            implicitWidth: 260
            ColumnLayout {
                anchors.fill: parent
                spacing: 8
                Label { text: qsTr("Dashboard"); color: "#FFFFFF" }
                Button { text: qsTr("Nova EFI"); onClicked: backend.generateEFI() }
                Button { text: qsTr("Abrir Existente") }
                Button { text: qsTr("Detectar Hardware"); onClicked: backend.detectHardware() }
                Button { text: qsTr("Gerar EFI"); onClicked: backend.generateEFI() }
                Button { 
                    text: qsTr("Editor config.plist")
                    onClicked: {
                        // Abrir diálogo de arquivo (placeholder)
                        // Por enquanto, simular validação
                        var testPath = "/tmp/test_config.plist"
                        backend.validateConfigFile(testPath)
                    }
                }
                Button { text: qsTr("Kexts / Drivers / SSDTs") }
                Button { text: qsTr("Debug & Validação") }
                Button { text: qsTr("Comparador & Versionamento") }
                Button { text: qsTr("Exportar") }
            }
        }

        // Conteúdo principal
        ColumnLayout {
            Layout.fillWidth: true
            spacing: 12

            // Painel de validação (visível quando há erros)
            ValidationPanel {
                Layout.fillWidth: true
                Layout.preferredHeight: validationErrors.length > 0 ? 200 : 0
                validationErrors: win.validationErrors
            }

            // Área principal
            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true

                Column {
                    width: parent.width
                    spacing: 12
                    padding: 20

                    Label {
                        text: qsTr("Universal OpenCore Manager")
                        font.pixelSize: 22
                        color: "#FFFFFF"
                    }

                    Text {
                        text: qsTr("Validação em tempo real do config.plist está ativa. Use o editor para carregar e validar arquivos.")
                        color: "#DDDDDD"
                        wrapMode: Text.WordWrap
                    }

                    RowLayout {
                        spacing: 8
                        Button {
                            text: "Validar Config Atual"
                            onClicked: {
                                var errors = backend.validateCurrentConfig()
                                console.log("Erros encontrados:", errors.length)
                            }
                        }
                        Button {
                            text: "Carregar Exemplo"
                            onClicked: {
                                // Exemplo: validar um config padrão
                                var example = JSON.stringify({
                                    "ACPI": {},
                                    "Booter": {},
                                    "Kernel": {},
                                    "Misc": {},
                                    "NVRAM": {},
                                    "PlatformInfo": {},
                                    "UEFI": {}
                                })
                                backend.validateConfigJSON(example)
                            }
                        }
                    }
                }
            }
        }
    }
}
