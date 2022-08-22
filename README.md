# sunmoon-data-crawler

Sunmoonからバス情報を収集するクローラー

## DB設計
[DB設計](https://github.com/dumbled0re/sunmoon-data-crawler/blob/feature/spider_module/spider/models.py#L18)

## 収集サイト名/リンク
[Sunmoon](https://lily.sunmoon.ac.kr/MainDefault3.aspx)

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
│    │   ├── pipelines.py               : DBに保存する処理
│    │   └── settings.py                : スパイダー全体の設定
│    ├── shell
│    │   └── update.sh
│    └── tests
│        ├── data
│        │   └── table_operations.py
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

## Git rules
- コミットメッセージは下記のprefixを使用する。[参考URL](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#type)
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
envファイルコピー 記入
```
cp .env.sample .env
```

## 動作確認(Dockerを使う場合)
```
# ビルド
make db_local_build

# テーブル作成
make data_create_table

# テーブル削除
make data_drop_table

# 終了
make db_local_down
```

デフォルトでport = 5432 に postgresql DB が起動する
### 接続情報
```
POSTGRES_HOST=127.0.0.1
POSTGRES_DB=app
POSTGRES_PASSWORD=pass
POSTGRES_USER=postgres
POSTGRES_DOCKER_PORT=5432
```

## 実行
```
# 新規追加
make crawl

# 更新
make crawl_update
```

## 保存先テーブル
```
sunmoon_bus
```
