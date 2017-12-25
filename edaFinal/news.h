#ifndef NOTICIA_H
#define NOTICIA_H
#include "trie.h"



class Date{
public:
    Date(){}
    Date(const string &s){
        set(s);
    }
    ~Date(){}
    void set(const string& s){
        //"2017-02-18T07:55:57-05:00"
        year=atoi(s.substr(0,4).c_str());
        month = atoi(s.substr(5,2).c_str());
        day = atoi(s.substr(8,2).c_str());
        hour = atoi(s.substr(11,2).c_str());
        minute = atoi(s.substr(14,2).c_str());
        seconds = atoi(s.substr(17,2).c_str());
    }
    string getString(){
        return to_string(year)+"/"+to_string(month)+"/"+to_string(day)+" - "+to_string(hour)+":"+to_string(minute)+":"+to_string(seconds);
    }

public:
    int day,month,year;
    int hour, minute, seconds;
};

class News{
public:
    News(){reClear();}
    ~News(){}

    void reClear(){
        trie.resetTrie();
    }
    void addWord(const string &w){
        trie.insert(w);
    }
    bool searchWord(const string &w){
        Node *p = trie.searchWord(w);
        return (p != NULL);
    }


public:
    Trie trie;
    Date date;
    string title, text;


};

typedef pair<int,Date> Comp;
class Result{
public:
    Result(){}
    //Result(Comp& comp, int& indnews):comp(comp),indnews(indnews){}
    Result(Comp comp, int indnews):comp(comp),indnews(indnews){}

    Comp comp;
    int indnews;
};

class Compare{
public:
    Compare(){}
    ~Compare(){}
    bool operator() (const Result resa, const Result resb){
        Comp ca = resa.comp;
        Comp cb = resb.comp;
        if(ca.first == cb.first){
            Date& a = ca.second;
            Date& b = cb.second;
            if(a.year == b.year){
                if(a.month == b.month){
                    if(a.day == b.day){
                        if(a.hour == b.hour){
                            if(a.minute == b.minute){
                                return a.seconds > b.seconds;
                            }
                            return a.minute > b.minute;
                        }
                        return a.hour > b.hour;
                    }
                    return a.day > b.day;
                }
                return a.month > b.month;
            }
            return a.year > b.year;
        }
        return ca.first > cb.first;
    }
};



#endif // NOTICIA_H
