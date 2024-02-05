# pandoc
Markdownで書かれた文書をPandocを用いて自動でPDFに変換します。

## 使用法

* このリポジトリをフォークします。
* フォークしたリポジトリで、Actionsの実行を許可します。
* フォークしたリポジトリをクローンします。
* クローンしたディレクトリに新たにディレクトリを作り、その中にMarkdownを作成します。
  * 作成したディレクトリ1つにつき1文書に対応します。
  * Markdownファイルは複数作ったら連結されますが、その順番は設定できないので、ファイル名を調整しておきましょう。
* 変更をpushするとActionsでPDFにしてくれます。

## ローカルでPDFを出力する

* Pythonをインストールしておきます。
* ターミナルを開いてリポジトリをクローンしたディレクトリにカレントディレクトリを移し、`python manage.py`を実行します。
  * ファイルが更新されたら勝手に変換作業が始まります。
  * ファイルを新しく作成したら実行し直しましょう(実行し直すにはターミナル上でCtrlとCを同時押しします)。