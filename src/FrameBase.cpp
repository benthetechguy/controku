#include "FrameBase.h"
#include <version.h>

void FrameBase::onExit(wxCommandEvent&) {
    Close(true);
}
void FrameBase::onAbout(wxCommandEvent&) {
    wxMessageBox("Controku " VERSION, "About Controku", wxOK | wxICON_INFORMATION);
}

FrameBase::FrameBase() : wxFrame(nullptr, wxID_ANY, "Controku") {
    SetIcon(wxIcon(wxString("../res/controku.xpm")));

    auto menuBar = new wxMenuBar;
    auto menuFile = new wxMenu;
    auto menuHelp = new wxMenu;
    menuFile->Append(wxID_EXIT);
    menuHelp->Append(wxID_ABOUT);
    menuBar->Append(menuFile, "&File");
    menuBar->Append(menuHelp, "&Help");
    wxFrame::SetMenuBar(menuBar);

    Bind(wxEVT_MENU, &FrameBase::onAbout, this, wxID_ABOUT);
    Bind(wxEVT_MENU, &FrameBase::onExit, this, wxID_EXIT);
}
