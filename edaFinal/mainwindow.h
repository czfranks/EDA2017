#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "news.h"
using namespace std;

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();
private slots:
    void slot_btn_search(bool);

private:
    void loadNews();
    void search(const QString& s);
    string clearAcent(const string& s);

    double costTime(clock_t i, clock_t f){
        return (double)(f-i)/CLOCKS_PER_SEC;
    }

private:
    Ui::MainWindow *ui;
    Trie trie;
    vector<News> vecNews;
    set<Result,Compare> setResult;
    map<string,char> acent;
};

#endif // MAINWINDOW_H
