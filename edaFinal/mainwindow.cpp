#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    connect(ui->btn_search,SIGNAL(clicked(bool)),this,SLOT(slot_btn_search(bool)));

    acent["á"] = 'a';
    acent["é"] = 'e';
    acent["í"] = 'i';
    acent["ó"] = 'o';
    acent["ú"] = 'u';
    acent["Á"] = 'A';
    acent["É"] = 'E';
    acent["Í"] = 'I';
    acent["Ó"] = 'O';
    acent["Ú"] = 'U';
    acent["ñ"] = 'ni';
    acent["Ñ"] = 'ni';

    loadNews();
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::loadNews(){
    ifstream in("page.txt",ios_base::in);
    int nrt,nt,ntext;//tamanyo de titulo raw, titulo, texto
    string w,rawTitle, text ;//titulo raw, titulo, texto
    int cont=1;
    while(!in.eof()){
        News news;
        news.reClear();
        in>>nrt;
        //cout << nrt << endl;
        for(int i=0;i<nrt;++i){ //scanning normalized title
            in>>w;
            string wrd = clearAcent(w);
            news.addWord(wrd);
        }
        in>>nt;
        //cout << nt << endl;
        rawTitle="";
        for(int i=0;i<nt;++i){//scanning raw title
            in>>w;
            rawTitle+=w;
            rawTitle+=" ";
        }
        news.title=rawTitle;
        cout << rawTitle << endl;
        in>>ntext;
        //cout << ntext << endl;
        text="";
        for(int i=0;i<ntext;++i){//scanning text
            in>>w;
            string wrd = clearAcent(w);
            text+=wrd;
            text+=" ";
            //cout << "add " << w << endl;
            news.addWord(wrd);
            //cout << "added " << w << endl;
        }
        //cout << "texto" << endl;
        news.text=text;
        cout << text << endl;
        in>>w;//scanning date
        //cout << w << endl;
        news.date=Date(w);

        vecNews.push_back(news);
        cout << cont++ << endl;
        //if(--cont==0) break;
    }
    in.close();
}

void MainWindow::search(const QString& s){
    QStringList words =  s.split(" ");
    setResult.clear();
    int occ;
    for(int ind=0;ind<(int)vecNews.size();++ind){
        News& news = vecNews[ind];
        occ=0;
        for(QString qs : words){
            string w = qs.toStdString();
            occ+=news.searchWord(w);
        }
        if(occ>0){
            Comp comp(occ,news.date);
            Result res(comp, ind);
            setResult.insert( res );
        }
    }
}

string MainWindow::clearAcent(const string& s){
    int i=0;
    string str;
    string ans="";
    while(i<(int)s.size()){
        if(s[i]<0 || s[i]>300) {
            str=acent[s.substr(i,2)];
            i+=2;
        }
        else {
            str=s.substr(i,1);
            i+=1;
        }
        ans+=str;
    }
    return ans;
}

void MainWindow::slot_btn_search(bool){

    //vecNews[0].trie.print();

   //return;
    QString w = ui->txt_pattern->text();
    w=(w.toLower());
    string wrd = w.toStdString();
    string clsAcent = clearAcent(wrd);
    QString wquery = QString(clsAcent.c_str());
    search(wquery);
    cout << setResult.size() << endl;
    ui->tableWidget->clear();
    ui->tableWidget->setColumnCount(4);
    ui->tableWidget->setRowCount(setResult.size());
    ui->tableWidget->setItem(0,0,new QTableWidgetItem("joala"));
    int row=0;
    for(Result res : setResult){
        ui->tableWidget->setItem(row,0,new QTableWidgetItem(QString(vecNews[res.indnews].title.c_str())));
        ui->tableWidget->setItem(row,1,new QTableWidgetItem(QString(vecNews[res.indnews].date.getString().c_str())));
        ui->tableWidget->setItem(row,2,new QTableWidgetItem(QString::number(res.comp.first)));
        ui->tableWidget->setItem(row,3,new QTableWidgetItem(QString(vecNews[res.indnews].text.c_str())));
        ++row;
    }
}
