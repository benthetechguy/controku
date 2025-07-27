#pragma once
#include <wx/wx.h>

class FrameBase : public wxFrame {
public:
    FrameBase();
private:
    void onExit(wxCommandEvent&);
    void onAbout(wxCommandEvent&);
};
