#include <algorithm>
#include <cstdint>
#include <cstring>
#include <random>
#include <vector>
struct Chain {int n,k;std::vector<int32_t> rows;std::mt19937_64 rng;uint64_t proposals=0,changed=0,moved=0;Chain(const int32_t* a,int nn,int kk,uint64_t seed):n(nn),k(kk),rows(a,a+nn*kk),rng(seed){for(int i=0;i<n;i++)std::sort(rows.begin()+i*k,rows.begin()+(i+1)*k);}};
extern "C" {
void* create_chain(const int32_t*a,int n,int k,uint64_t seed){return new Chain(a,n,k,seed);}
void free_chain(void*h){delete static_cast<Chain*>(h);}
void copy_rows(void*h,int32_t*out){auto*c=static_cast<Chain*>(h);std::memcpy(out,c->rows.data(),c->rows.size()*sizeof(int32_t));}
void counters(void*h,uint64_t*out){auto*c=static_cast<Chain*>(h);out[0]=c->proposals;out[1]=c->changed;out[2]=c->moved;}
void advance_chain(void*h,int sweeps){auto*c=static_cast<Chain*>(h);if(c->n<2)return;std::uniform_int_distribution<int> di(0,c->n-1),dj(0,c->n-2);std::vector<int32_t> common,ex,oldA;common.reserve(c->k);ex.reserve(2*c->k);oldA.reserve(c->k);
for(int step=0;step<sweeps*((c->n+1)/2);step++){c->proposals++;int i=di(c->rng),j=dj(c->rng);if(j>=i)j++;auto*a=&c->rows[i*c->k];auto*b=&c->rows[j*c->k];common.clear();ex.clear();oldA.assign(a,a+c->k);int x=0,y=0;while(x<c->k || y<c->k){if(x==c->k){ex.push_back(b[y++]);}else if(y==c->k){ex.push_back(a[x++]);}else if(a[x]==b[y]){common.push_back(a[x]);x++;y++;}else if(a[x]<b[y])ex.push_back(a[x++]);else ex.push_back(b[y++]);}int u=c->k-int(common.size());if(u==0)continue;std::shuffle(ex.begin(),ex.end(),c->rng);std::copy(common.begin(),common.end(),a);std::copy(common.begin(),common.end(),b);std::copy(ex.begin(),ex.begin()+u,a+common.size());std::copy(ex.begin()+u,ex.end(),b+common.size());std::sort(a,a+c->k);std::sort(b,b+c->k);int keep=0;for(int v=0;v<c->k;v++)keep+=std::binary_search(oldA.begin(),oldA.end(),a[v]);int moved=c->k-keep;if(moved){c->changed++;c->moved+=2*moved;}}
}
}
