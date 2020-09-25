from django.db import models
from datetime import date

class MatchRecord(models.Model):
    class Meta:
        db_table = 'match_record' # DB内で使用するテーブル名
        verbose_name_plural = 'match_record' # Admionサイトで表示するテーブル名
    
    #勝敗
    WIN_LOSE_CHOICES = (
        (0, '勝利'),
        (1, '敗北'),
    )
    #先攻後攻
    FRIRST_STRIKE_CHOICES = (
        (0, '先攻'),
        (1, '後攻'),
    )
    #フリーor公式
    BATTLE_DIVISION_CHOICES = (
        (0, 'フリー'),
        (1, '公式'),
    )

    user_id = models.IntegerField('user_id', null=True, blank=False) # 数値を格納
    game_date = models.DateField ('game_date', default=date.today, null=True, blank=False) # 文字列を格納
    game_name = models.CharField('game_name', max_length=30, null=True, blank=False) # 文字列を格納
    battle_division = models.IntegerField('battle_division', choices = BATTLE_DIVISION_CHOICES, null=True, blank=False) # 数値
    my_title = models.CharField('my_title', max_length=50, null=True, blank=False) # 文字列を格納
    opp_title = models.CharField('opp_title', max_length=50, null=True, blank=False) # 文字列を格納
    frirst_strike = models.IntegerField('frirst_strike', choices = FRIRST_STRIKE_CHOICES, null=True, blank=False) # 数値
    win_lose = models.IntegerField('win_lose', choices = WIN_LOSE_CHOICES, null=True, blank=False) # 数値
    game_score = models.IntegerField('game_score', null=True, blank=True) # 数値
    comment = models.TextField('comment', max_length=255, null=True, blank=True) # 文字列を格納
    create_date = models.DateTimeField ('create_date', auto_now_add = True, null=True, blank=True) # 文字列を格納
    update_date = models.DateTimeField ('update_date', auto_now = True, null=True, blank=True) # 文字列を格納
    