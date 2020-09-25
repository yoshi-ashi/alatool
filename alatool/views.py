from django.shortcuts import render,redirect,get_object_or_404
from django.views import View  
from .models import MatchRecord
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SampleForm
from django.views.decorators.http import require_POST

#リスト用
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q #追加


class AlaTop(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        #ユーザIDを取得
        user = self.request.user.id
        #初期表示用
        trg_date = date.today()
        trg_year = trg_date.strftime("%Y")
        trg_month = trg_date.strftime("%#m")
        result = MatchRecord.objects.filter(user_id = user,
                                         game_date__year__gte = trg_year,
                                         game_date__month__range = (trg_month,trg_month)
                                         ).order_by("opp_title")

        ###初期表示円グラフ用###
        #相手別対戦回数集計
        #タイトル別の勝ち数と負け数を辞書で作る
        win_dict,lose_dict,total_dict = {},{},{}
        win_cnt,lose_cnt = 0,0
        cur_title = ''

        for obj in result:
            #タイトルが変わったらリセットする
            if cur_title != obj.opp_title:
                cur_title = obj.opp_title
                win_cnt,lose_cnt = 0,0
                #一方が0の可能性を考慮して{"タイトル":0}を設定
                win_dict[cur_title] = win_cnt
                lose_dict[cur_title] = lose_cnt
            if obj.win_lose == 0:
                win_cnt += 1
                win_dict[cur_title] = win_cnt
            elif obj.win_lose == 1:
                lose_cnt += 1
                lose_dict[cur_title] = lose_cnt
            total_dict[cur_title] = win_cnt + lose_cnt
            
            #更新があったか判定

        '''
        if obj.create_date == obj.update_date:
            print("更新なし",obj.create_date,obj.update_date)
        else:
            print("更新あり",obj.create_date,obj.update_date)
        '''

        #グラフ用情報集計
        #トータルカウントを降順に修正(対戦数の多い順)
        new_total_dict = sorted(total_dict.items(),key = lambda x:x[1],reverse=True)
        
        pie_labels,pie_data,bar_data = [],[],[]
        win_cnt,lose_cnt = 0,0
        for k,v in new_total_dict:
            #タイトル作成
            pie_labels.append(k)
            #タイトル別対戦数
            pie_data.append(win_dict[k] + lose_dict[k])
            #タイトル別勝率
            bar_data.append(WinRate(total = v,win = win_dict[k],option = 0))
            #当月勝数
            win_cnt += win_dict[k]

        total_cnt = sum(pie_data)
        lose_cnt = total_cnt - win_cnt
        win_rate = WinRate(total = total_cnt,win = win_cnt,option = 1)
        
        ###初期表示折れ線グラフ用###
        context = {'trg_month':(trg_year + '年' + trg_month + '月'),
                    'total_cnt':total_cnt,
                    'win_cnt':win_cnt,
                    'lose_cnt':lose_cnt,
                    'win_rate':win_rate,
                    'pie_labels':pie_labels,
                    'pie_data':pie_data,
                    'bar_data':bar_data
                    }
        return render(request, 'alatool/top.html', context=context,)

top = AlaTop.as_view()

class AlaInfo(LoginRequiredMixin,View):  
    def get(self, request, *args, **kwargs):
        return render(request, 'alatool/info.html')

info = AlaInfo.as_view()

'''
class AlaRegister(LoginRequiredMixin,View):  
    def get(self, request, *args, **kwargs):
        return render(request, 'alatool/register.html')

    def post(self, request, *args, **kwargs):
        #登録処理
        input_userid = self.request.user.id
        input_game_date = request.POST['input_game_date']
        input_game_name = request.POST['input_game_name']
        input_my_title = request.POST['input_my_title']
        input_opp_title = request.POST['input_opp_title']
        input_win_lose = request.POST['input_win_lose']
        input_comment = request.POST['input_comment']
        input_frirst_strike = request.POST['input_frirst_strike']
        input_battle_division = request.POST['input_battle_division']
        data = MatchRecord( user_id = input_userid,
                         game_date = input_game_date,
                         game_name = input_game_name,
                         my_title = input_my_title,
                         opp_title = input_opp_title,
                         win_lose = input_win_lose,
                         comment = input_comment,
                         frirst_strike = input_frirst_strike,
                         battle_division = input_battle_division)
        data.save()
        return render(request, 'alatool/register.html')

register = AlaRegister.as_view()
'''

#履歴表示
class AlaHistory(LoginRequiredMixin,View):  
    def get(self, request, *args, **kwargs):

        input_userid = self.request.user.id
        querySet = {}
        querySet["user_id"] = input_userid

        result = MatchRecord.objects.filter(**querySet).order_by("game_date").reverse()
        #0 or 1のcolumnは出力前に変換する
        for i,v in enumerate(result):
            if result[i].win_lose == 0:result[i].win_lose = '勝利'
            elif result[i].win_lose == 1:result[i].win_lose = '敗北'
            if result[i].frirst_strike == 0:result[i].frirst_strike = '先攻'
            elif result[i].frirst_strike == 1:result[i].frirst_strike = '後攻'
            elif result[i].frirst_strike is None:result[i].frirst_strike = ''
            if result[i].battle_division == 0:result[i].battle_division = 'フリー'
            elif result[i].battle_division == 1:result[i].battle_division = '公式'
            if result[i].comment is None:result[i].comment = ''

        page_obj = paginate_query(request, result, 10)   # ページネーション
        context={"result_obj":page_obj}

        return render(request, 'alatool/history.html', context=context)

history = AlaHistory.as_view()

def WinRate(total,win,option):
    '''勝率を計算する(勝利数/対戦数)
       optionによって”%”付きか数値か分ける[0:%無し,1:%有り]
       total:int
       win:int
       return:0 == float, 1 == str
    '''
    if total == 0 or win == 0:
        if option == 0:
            win_rate = round((0)*100,1)
        elif option == 1:
            win_rate = '{:.1%}'.format(0)
    else:
        if option == 0:
            win_rate = round((win/total)*100,1)
        elif option == 1:
            win_rate = '{:.1%}'.format(win / total)
    return win_rate



# ページネーション用に、Pageオブジェクトを返す。
def paginate_query(request, queryset, count):
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    

    return page_obj

#詳細表示用
def detail(request, sample_id):
    #DBからキーユーザIDと合致するレコードを取得する
    result = MatchRecord.objects.get(id=sample_id)
    #DBからキーユーザIDと合致するレコードを取得する
    if result.win_lose == 0:result.win_lose = '勝利'
    elif result.win_lose == 1:result.win_lose = '敗北'
    if result.frirst_strike == 0:result.frirst_strike = '先攻'
    elif result.frirst_strike == 1:result.frirst_strike = '後攻'
    elif result.frirst_strike is None:result.frirst_strike = ''
    if result.battle_division == 0:result.battle_division = 'フリー'
    elif result.battle_division == 1:result.battle_division = '公式'
    if result.comment is None:result.comment = ''

    context = {'result':result,}
    return render(request, 'alatool/detail.html', context=context)

#編集用
def edit(request, sample_id):
    sampleDB = get_object_or_404(MatchRecord, id=sample_id)
    #POSTで受け取った場合、値を引き継いで表示
    if request.method == "POST":
        form = SampleForm(request.POST, instance=sampleDB)
        if form.is_valid():
            form.save()
            return redirect('alatool:history')
    else:
        form = SampleForm(instance=sampleDB)
    return render(request, 'alatool/edit.html', {'form': form, 'result':sampleDB })

#削除用POSTの時だけ発火
@require_POST
def delete(request, sample_id):
    sampleDB = get_object_or_404(MatchRecord, id=sample_id)
    sampleDB.delete()
    return redirect('alatool:history')

def register(request):
    if request.method == "POST":
        form = SampleForm(request.POST)
        if form.is_valid():
            tempDB = form.save(commit = False)
            tempDB.user_id = request.user.id
            tempDB.save()
            return redirect('alatool:register')
    else:
        #登録画面初期表示
        defautt_data = {
            'game_date':date.today(),
            'game_name':'WS',
            'battle_division':0,
            'frirst_strike':0,
            'win_lose':0,
            }
        form = SampleForm(defautt_data)
    return render(request, 'alatool/register.html', {'form': form})
