## 何これ
ファイルの変更を検出して、指定したmoduleをreloadし、指定した関数(mod_doc(doc)形式のやつ)でbokehserverのappを更新して、seleniumで開く

## install

pip install git+https://github.com/tanakaht/bokeh_dev_tools

update

pip install -U git+https://github.com/tanakaht/bokeh_dev_tools


## demo

![](https://gyazo.com/f81ecc0bc2bafbcb0718e52486a5df40.gif)

## 使い方

test/test.pyを参照

## requirement

多分

- watchdog
- selenium
- bokeh

(pip化したい)
