#ifndef TRIE_H
#define TRIE_H

#include <bits/stdc++.h>

using namespace std;

class Node{
    public:
        Node(){ acept=false; parent=0; }
        Node(int chr):chr(chr){ acept=false; parent=0; }
        ~Node(){}

        Node* parent;
        int chr;
        map<int,Node*> sons;
        bool acept;
    };

const int ALPHA = 300;
class Trie{
public:
    Trie(){ resetTrie(); }
    ~Trie(){}

public:

    //Node* trie[ALPHA]; ???
    vector<Node*> trie;

    void resetTrie(){ //clean and assign memory
        trie.resize(ALPHA);
        for(int i=0;i<ALPHA;++i){
            if(trie[i]!=0){
                trie[i]->sons.clear();
                delete trie[i];
                trie[i] = 0;
            }
        }
        for(int i=0;i<ALPHA;++i) trie[i] = new Node(i);
    }

    void insert(const string& s){ //insert word in trie
        int n = s.size();
        if(n==0) return;
        Node *p = trie[s[0]];
        for(int i=1;i<n;++i){
            Node *&q = p->sons[s[i]];
            if(q==0) {
                q = new Node(s[i]);
                q->parent=p;
            }
            p = q;
        }
        p->acept=true;
    }

    Node* searchWord(const string& s){
        Node* fail = NULL;
        int n = s.size();
        if(n==0) return fail;
        Node *p = trie[s[0]];
        //cout << s[0];
        for(int i=1;i<n;++i){
            if(p->sons.count(s[i])){
                p=p->sons[s[i]];
        //		cout << s[i];
            }
            else break;
        }
        //cout <<"[" <<p->acept << "]\n";
        if(p->acept==true) return p;
        return fail;
    }

    // Imprimir el arbol en forma "inorder" o "dfs"
    void dfs(Node *p, string s){
        if(p==0) return;
        if(p->acept) cout << s << endl;
        for(map<int,Node*>::iterator i=p->sons.begin(); i!=p->sons.end(); ++i){
            dfs(i->second, s+string(1,i->first));
        }
    }
    void print(){
        for(int i=0;i<ALPHA;++i) dfs(trie[i],string(1,i));
    }
};


#endif // TRIE_H
