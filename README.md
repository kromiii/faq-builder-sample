# faq-builder

サービスのマニュアルからFAQサイトを生成するツールです。

デモサイト：https://faq-builder.streamlit.app/

## 使い方

PDF形式のマニュアルをアップロードして５分ほど待つとFAQ サイトが生成されます

## Development 

### Requirements

```
% python --version
Python 3.10.13
```

### Install dependencies

```
% pip install -r requirements.txt
```

### Run local server

環境変数 `OPENAI_API_KEY` に OpenAI API のキーを設定してください

```
% streamlit run faq-builder.py
```