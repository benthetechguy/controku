#pragma once
#include "FrameBase.h"
#include <nlohmann/json.hpp>

class MainFrame final : public FrameBase {
    public:
        MainFrame();
    private:
        wxTextCtrl* deviceBox;
        wxButton* connectButton;
        nlohmann::json deviceList;
        enum {
            DEVICE_SELECTOR_ID,
            DEVICE_IP_BOX_ID,
            CONNECT_BUTTON_ID,
        };
        void printTest(wxCommandEvent&);
};
