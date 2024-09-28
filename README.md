# scraping-sendemail

## 概要

- [kakakuscraping-fastapi](https://github.com/gkjg8787/kakakuscraping-fastapi) のアイテム一覧をチェックし、前回からの差分をメールで通知する WEB アプリケーション。
- 1 日 1 回チェックでの差分通知を想定。
- アイテム一覧のデータは kakakuscraping-fastapi の DB とは別で持っているため実際の想定差分とは異なる結果になる可能性あり。

## 使い方

1. 設定の変更が必要なら変更する。また環境変数をDockerfileに記述や起動後等で設定する。
1. スクリプト（*.sh)に権限を与えておく。
1. docker として起動（説明は省略）。
1. 動作ログと通知設定はコンテナ起動後に`http://127.0.0.1:8020`で確認できる。<br>設定を変更する場合は手動で変更＆再起動が必要。

## 設定

- settings ファイルでは対象の URL、通知設定の ON/OFF、環境変数ではメールアドレスの送信元/先の設定を行う。

### settings ファイル

| 変数名        | 説明                                |
| ------------- | ----------------------------------- |
| DATABASES     | DB の設定。aiosqlite のみ対応       |
| LOGGER_CONFIG | Logger の設定                       |
| KAKAKU_NOTICE | kakakuscraping-fastapi 用の通知設定 |
| NOTICELOG     | 通知ログの設定                      |

##### KAKAKU_NOTICE

- kakakuscraping-fastapi 用の通知設定

| 設定名                         | 説明                                                                                     |
| ------------------------------ | ---------------------------------------------------------------------------------------- |
| kakaku_url                     | kakakuscraping-fastapi のアイテム一覧への URL。`http://～/users/`の形で記述。 |
| kakaku_notice_option           | 通知設定。                                                                        |
| new_item                       | 追加された（一覧から見えるようになった）アイテムの通知 ON/OFF                            |
| remove_item                    | 削除（一覧から見えなくなった）アイテムの通知 ON/OFF                                      |
| change_to_in_stock             | 在庫なし(-1)から在庫ありになったアイテムの通知 ON/OFF                                    |
| change_to_out_of_stock         | 在庫ありから在庫なし(-1)になったアイテムの通知 ON/OFF                                    |
| lowest_price                   | 最安値を更新した通知 ON/OFF                                                              |
| lowest_price_without_no_change | 値段の変更なしで最安値である通知 ON/OFF                                                  |
| price_decline                  | 値段が下がった通知 ON/OFF                                                                |
| price_rise                     | 値段が上がった通知の ON/OFF                                                              |

#### NOTICELOG

- 通知ログの設定

| 設定名 | 説明 |
| ---- | ---- |
| storagecount | 保持するログの最大数。整数で設定。30を設定しているなら30個よりログが多い場合、古いログが削除される。0以下で無効。 |
| storagedays | 保持するログの日数。整数（日数）で設定。30を設定しているなら30日よりも前のログが削除される。0以下で無効。 |

### 環境変数

- 通知の送信元、先のメールアドレスとパスワードは環境変数で設定する
- Gmail のみ動作確認。パスワードはアプリパスワードが必要。

| 環境変数名            | 説明                                     |
| --------------------- | ---------------------------------------- |
| SOURCE_EMAIL_ADDRESS  | 送信元のメールアドレス                   |
| SOURCE_EMAIL_PASSWORD | 送信元のメールアドレスのアプリパスワード |
| DEST_EMAIL_ADDRESS    | 送信（通知）先のメールアドレス           |

### 通知タイマー設定(cron)

- cron による定期実行で差分を確認し、通知を行っている。
- Dockerfile の以下の部分を書き換えることで実行時間の設定を変更可能。<br>
  `RUN echo "30 16 * * * bash /app/cron.sh" | crontab -`
