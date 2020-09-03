# cross_aic_tool
分割表のaic算出  
参考url https://www.dynacom.co.jp/product_service/packages/snpalyze/sa_t2_aic-cont.html

# 使い方
jupyter notebook にプログラムを貼り付け実行する。  
説明変数で構成されるpandasデータフレームをx1、目的変数のpandasシリーズをy1と言う名前で作成した時、以下のように記述する。

#aicクラスを作成  
aic = Aic(x=x1,y=y1,method='Class')  
とする。

現行バージョンではmethod='Class'を固定で使って下さい。  
上で作成したaicクラスに対してfitメソッドを用いることで集計を始める。

#fitして分割表を作成  
aic.fit()

# 注意(20200903時点)

 目的変数はカテゴリタイプに対応しています。その際方はオブジェクト型、整数型いずれでも大丈夫です。  
 連続変数はpd.cutなどでカテゴリタイプに直して下さい。
