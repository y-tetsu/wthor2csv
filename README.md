# wthor2csv
WTHORのリバーシ棋譜をCSVファイルに変換する

## 実行方法
```
> python wthor2csv.py
```
### 入力ファイル名を指定する場合
以下の様に、スクリプトを修正してください。

```python
if __name__ == '__main__':
    Wthor(jou='JOUファイル名', trn='TRNファイル名', wtb='WTBファイル名').to_csv()
```

### 出力ファイル名を指定する場合
以下の様に、スクリプトを修正してください。

```python
if __name__ == '__main__':
    Wthor().to_csv('出力CSVファイル名')
```

## 出力結果
実行後、カレントディレクトリにCSVファイル(デフォルトはoutput.csv)が出力されます。

## 参考サイト
- 「オセロの棋譜データベースWTHORの読み込み方」https://qiita.com/tanaka-a/items/e21d32d2931a24cfdc97
- 「付録A Thorデータベースのファイルフォーマット」http://hp.vector.co.jp/authors/VA015468/platina/algo/append_a.html
