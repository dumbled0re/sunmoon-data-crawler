# sunmoon-data-crawler

Sunmoon からバス情報を収集するクローラー

## DB 設計

[DB 設計](https://github.com/dumbled0re/sunmoon-data-crawler/blob/develop/app/src/models.py#L15)

## 収集サイト名/リンク

[Sunmoon](https://lily.sunmoon.ac.kr/MainDefault3.aspx)

## ディレクトリ構造

```
sunmoon-data-crawler
│   ├── app
│   │   ├── log
│   │   ├── src
│   │   │   ├── data
│   │   │   │    └── table_operations.py   : テーブル操作
│   │   │   ├── spiders
│   │   │   │    └── sunmoon_spider.py     : クローラー実行
│   │   │   ├── test
│   │   │   ├── utils
│   │   │   │    ├── constants.py          : 定数定義
│   │   │   │    ├── db_adapter.py         : DB接続
│   │   │   │    ├── logger.py             : ログ出力
│   │   │   │    ├── slack_notify.py       : slack通知
│   │   │   │    └── spider_utils.py       : スパイダーutilsモジュール
│   │   │   ├── items.py                   : スパイダーが取得するデータ定義
│   │   │   ├── middlewares.py             : スパイダーの設定
│   │   │   ├── models.py                  : DBテーブル定義
│   │   │   ├── pipelines.py               : DBに保存する処理
│   │   │   └── settings.py                : スパイダー全体の設定
│   │   └── scrapy.cfg
│   └── docker
│        └── docker-compose.yml
├── .env.example
├── .flake8
├── .gitignore
├── .pre-commit-config.yaml
├── crontab.txt
├── Dockerfile
├── Makefile　　　　　　　　　　
├── mypy.ini
├── poetry.lock
├── pyproject.toml
├── README.md
├── requirements.txt
├── setup.cfg
└── update.sh
```

## Git rules

- コミットメッセージは下記の prefix を使用する。[参考 URL](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#type)
  - feat: 新しい機能追加
  - fix: バグ修正
  - docs: ドキュメント修正
  - style: コードスタイル修正
  - refactor: リファクタリング
  - perf: パフォーマンスチューニング
  - test: テストの追加/修正
  - chore: 基盤の修正、ライブラリの追加/削除

## プッシュ前にやること

```
make pre-commit-check
```

## 環境構築

poetry インストール後 以下実行

```
make install
```

.envファイル作成

```
make create_env
```

## 動作確認

```
# ビルド & コンテナの立ち上げ
make docker_build

# テーブル作成
make data_create_table

# 実行
make crawl

# 終了
make docker_down
```

### 接続情報

```
POSTGRES_HOST=my_postgresql
POSTGRES_DB=app
POSTGRES_USER=postgres
POSTGRES_PASSWORD=pass
POSTGRES_PORT=5432
```
