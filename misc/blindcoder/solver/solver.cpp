#include<iostream>
using namespace std;

unsigned long query_counter{0};
void debug_readline(){
    string t;
    getline(cin, t);
    cerr << t << endl;
}

#include<vector>
unsigned long query(const vector<pair<unsigned long, unsigned long>>& intervals){
    string s("("), t;
    for(const auto& [l, r] : intervals){
        if(s.size() != 1)s += " || ";
        s += "("s + to_string(l) + " <= N && N < "s + to_string(r) + ")"s;
    }
    s += ") ? N % 10 : 1000000"s;
    cout << 1 << endl;
    cout << s << endl;
    getline(cin, t);
    getline(cin, t);
    unsigned long ret{0};
    cin >> t;
    cin >> t;
    cin >> t;
    cin >> ret;
    cerr << (++query_counter) << endl;
    getline(cin, t);
    getline(cin, t);
    getline(cin, t);
    getline(cin, t);
    getline(cin, t);
    getline(cin, t);
    return ret;
}

#include<queue>
#include<set>
int main(){
    string t;
    for(unsigned long i{0}; i < 9; ++i)getline(cin, t);
    using interval_type = pair<unsigned long, unsigned long>;
    priority_queue<pair<unsigned long, interval_type>> pq;
    pq.emplace(50, interval_type{0, 1UL << 32});

    priority_queue<interval_type, vector<interval_type>, greater<>> singles;
    while(!pq.empty()){
        const auto [size, p] = pq.top();
        const auto [l, r] = p;
        pq.pop();
        const auto m = (l + r) / 2;
        unsigned long size_left = query({interval_type{l, m}});
        unsigned long size_right = size - size_left;
        if(size_left == 1)singles.emplace(m - l, l);
        else if(size_left) pq.emplace(size_left, interval_type{l, m});
        if(size_right == 1)singles.emplace(r - m, m);
        else if(size_right)pq.emplace(size_right, interval_type{m, r});
    }

    set<unsigned long> ans;
    const auto& insert = [&ans, &singles](const interval_type& lr){
        if(lr.first == 1)ans.insert(lr.second);
        else singles.emplace(lr);
    };
    [rec_impl = [&singles, &insert](auto f, const interval_type& lr) -> bool {
        if(singles.empty()){
            bool tmp = static_cast<bool>(query({interval_type{lr.second, lr.second + lr.first / 2}}));
            if(tmp)insert({lr.first / 2, lr.second});
            else insert({lr.first - lr.first / 2, lr.second + lr.first / 2});
            return tmp;
        }
        bool ret{false};
        const auto [width, l] = singles.top();
        singles.pop();
        if(singles.empty()){
            auto tmp = query({interval_type{lr.second, lr.second + lr.first / 2}, interval_type{l, l + width / 2}});
            if(tmp == 2){
                ret = true;
                insert({lr.first / 2, lr.second});
                insert({width / 2, l});
            }else if(tmp == 1){
                ret = !f(f, {width, l});
                if(ret)insert({lr.first / 2, lr.second});
                else insert({lr.first - lr.first / 2, lr.second + lr.first / 2});
            }else{
                ret = false;
                insert({lr.first - lr.first / 2, lr.second + lr.first / 2});
                insert({width - width / 2, l + width / 2});
            }
            return ret;
        }
        const auto [W, L] = singles.top();
        singles.pop();
        auto tmp = query({interval_type{lr.second, lr.second + lr.first / 2}, interval_type{l, l + width / 2}, interval_type{L, L + W / 2}});
        if(tmp == 3){
            ret = true;
            insert({lr.first / 2, lr.second});
            insert({width / 2, l});
            insert({W / 2, L});
        }else if(tmp == 2){
            tmp = f(f, {width, l});
            if(tmp){
                ret = !f(f, {W, L});
                if(ret)insert({lr.first / 2, lr.second});
                else insert({lr.first - lr.first / 2, lr.second + lr.first / 2});
            }else{
                ret = true;
                insert({lr.first / 2, lr.second});
                insert({W / 2, L});
            }
        }else if(tmp == 1){
            tmp = f(f, {width, l});
            if(tmp){
                ret = false;
                insert({lr.first - lr.first / 2, lr.second + lr.first / 2});
                insert({W - W / 2, L + W / 2});
            }else{
                ret = !f(f, {W, L});
                if(ret)insert({lr.first / 2, lr.second});
                else insert({lr.first - lr.first / 2, lr.second + lr.first / 2});
            }
        }else{
            ret = false;
            insert({lr.first - lr.first / 2, lr.second + lr.first / 2});
            insert({width - width / 2, l + width / 2});
            insert({W - W / 2, L + W / 2});
        }
        return ret;
    }, &singles]{
        while(!singles.empty()){
            const auto tmp = singles.top();
            singles.pop();
            rec_impl(rec_impl, tmp);
        }
    }();

    cout << 2 << endl;
    cerr << 2 << endl;
    for(const auto& i : ans)cout << i << " ";
    cout << endl;
    for(unsigned long i{0}; i < 2; ++i)debug_readline();
    return 0;
}
