#include <rokuecp.h>
#include <wx/wx.h>
#include <version.h>

class Controku final : public wxApp {
public:
    bool OnInit() override;
};

wxIMPLEMENT_APP(Controku);

class Frame : public wxFrame {
public:
    Frame();
private:
    void onExit(wxCommandEvent&) {
        Close(true);
    }
    void onAbout(wxCommandEvent&) {
        wxMessageBox("Controku " VERSION, "About Controku", wxOK | wxICON_INFORMATION);
    }
};

bool Controku::OnInit() {
    auto frame = new Frame();
    frame->Show(true);
    return true;
}

Frame::Frame() : wxFrame(nullptr, wxID_ANY, "Controku") {
    auto menuBar = new wxMenuBar;
    auto menuFile = new wxMenu;
    auto menuHelp = new wxMenu;
    menuFile->Append(wxID_EXIT);
    menuHelp->Append(wxID_ABOUT);
    menuBar->Append(menuFile, "&File");
    menuBar->Append(menuHelp, "&Help");
    wxFrame::SetMenuBar(menuBar);

    wxFrame::CreateStatusBar();
    wxFrame::SetStatusText("Hello, world!");

    Bind(wxEVT_MENU, &Frame::onAbout, this, wxID_ABOUT);
    Bind(wxEVT_MENU, &Frame::onExit, this, wxID_EXIT);
}
