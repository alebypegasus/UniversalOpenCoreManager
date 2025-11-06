import QtQuick 6.5
import QtQuick.Controls 6.5
import QtQuick.Layouts 6.5

Rectangle {
    id: root
    color: "#2A2A2A"
    border.color: "#FF6B6B"
    border.width: 1
    radius: 8
    visible: validationErrors.length > 0

    property var validationErrors: []

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 8

        RowLayout {
            Layout.fillWidth: true
            Label {
                text: "Erros de Validação"
                color: "#FF6B6B"
                font.bold: true
                font.pixelSize: 14
            }
            Item { Layout.fillWidth: true }
            Label {
                text: validationErrors.length
                color: "#FF6B6B"
                font.bold: true
            }
        }

        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true

            Column {
                width: parent.width
                spacing: 6

                Repeater {
                    model: validationErrors

                    Rectangle {
                        width: parent.width
                        height: errorText.height + 16
                        color: "#3A3A3A"
                        radius: 4

                        Column {
                            anchors.fill: parent
                            anchors.margins: 8
                            spacing: 4

                            Text {
                                id: errorText
                                text: modelData.message || "Erro desconhecido"
                                color: "#FFE0E0"
                                wrapMode: Text.WordWrap
                                width: parent.width
                            }

                            Text {
                                text: modelData.path ? `Caminho: ${modelData.path}` : ""
                                color: "#CCCCCC"
                                font.pixelSize: 11
                                visible: modelData.path
                            }
                        }
                    }
                }
            }
        }
    }
}

