# faq-builder

サービスのマニュアルからFAQサイトを生成するツールです。

## 使い方

PDF形式のマニュアルをアップロードして、しばらく待ちます

FAQ サイトが生成されます

## Development 

### Requirements

```
% python --version
Python 3.10.13
```

必要なライブラリを適宜インストールしてください

### Run local server

環境変数 `OPENAI_API_KEY` に OpenAI API のキーを設定してください

```
% streamlit run faq-builder.py
```