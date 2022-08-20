# sunmoon-data-crawler

Sunmoonからバス情報を収集するクローラー

## DB設計
[DB設計](https://github.com/dumbled0re/sunmoon-data-crawler/blob/feature/spider_module/spider/models.py#L18)

## 収集サイト名/リンク
[Sunmoon](https://lily.sunmoon.ac.kr/MainDefault3.aspx)

## 環境構築
poetry インストール後 以下実行
```
make install
```
envファイルコピー 記入
```
cp .env.sample .env
```

## ディレクトリ構造

```
sunmoon-data-crawler
│    ├── logs
│    ├── spider
│    │   ├── spiders
│    │   │  └── sunmoon_spider.py       : クローラー実行
│    │   ├── utils
│    │   │  ├── constants.py            : 定数定義
│    │   │  ├── db_adapter.py           : DB接続
│    │   │  ├── logger.py               : ログ出力
│    │   │  ├── slack_notify.py         : slack通知
│    │   │  └── spider_utils.py         : スパイダーutilsモジュール
│    │   ├── items.py                   : スパイダーが取得するデータ定義
│    │   ├── middlewares.py             : スパイダーの設定
│    │   ├── models.py                  : DBテーブル定義
│    │   ├── pipelines,py               : DBに保存する処理
│    │   └── settings.py                : スパイダー全体の設定
│    ├── shell
│    │   └── update.sh
│    └── tests
│        ├── data
│        ├── docker
│        │   ├── docker-compose.yaml
│        │   └── Dockerfile
│        └── unittest
├── .env.sample
├── .flake8
├── .gitignore
├── .pre-commit-config.yaml
├── crontab.txt
├── Makefile　　　　　　　　　　
├── mypy.ini
├── poetry.lock
├── pyproject.toml
├── README.md
├── scrapy.cfg
└── setup.cfg
```

## 実行方法
### ローカル
```
新規追加
make crawl
```

```
更新
make crawl_update
```

## 保存先テーブル
```
sunmoon_bus
```
