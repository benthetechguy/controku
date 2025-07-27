#include "MainFrame.h"
#include <fstream>
extern "C" {
#include <rokuecp.h>
}

MainFrame::MainFrame() {
    auto panel = new wxPanel(this);

    std::ifstream devicesFile = std::ifstream("devices.json");
    if (devicesFile.fail()) {
        this->deviceBox = new wxTextCtrl(panel, DEVICE_IP_BOX_ID);
    } else {
        this->deviceList = nlohmann::json::parse(devicesFile);
        devicesFile.close();
    }
    this->connectButton = new wxButton(panel, CONNECT_BUTTON_ID, "Test", wxPoint(100, 0));
    Connect(CONNECT_BUTTON_ID, wxEVT_COMMAND_BUTTON_CLICKED, wxCommandEventHandler(MainFrame::printTest));
}

void MainFrame::printTest(wxCommandEvent&) {
    RokuDevice test;
    getRokuDevice("http://" + this->deviceBox->GetLineText(0) + ":8060", &test);
    std::cout << test.name;
}