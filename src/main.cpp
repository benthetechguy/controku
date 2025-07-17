#include <QApplication>
#include <QMainWindow>
#include <QIcon>

int main(int argc, char *argv[]) {
	QApplication app(argc, argv);
	QMainWindow window;
	window.setWindowTitle("Hello World");
	window.setWindowIcon(QIcon(":/res/controku.png"));
	window.show();

	return QApplication::exec();
}
