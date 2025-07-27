#include <rokuecp.h>
#include "MainFrame.h"

class Controku final : public wxApp {
public:
    bool OnInit() override;
};

wxIMPLEMENT_APP(Controku);

bool Controku::OnInit() {
    auto frame = new MainFrame();
    frame->Show(true);
    return true;
}
