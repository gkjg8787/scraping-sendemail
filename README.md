# scraping-sendemail

## 概要

- kakakuscraping-fastapi のアイテム一覧をチェックし、前日の差分をメールで通知する WEB アプリケーション

## 設定

### settings ファイル

| 変数名        | 説明                                |
| ------------- | ----------------------------------- |
| DATABASES     | DB の設定。aiosqlite のみ対応       |
| LOGGER_CONFIG | Logger の設定                       |
| KAKAKU_NOTICE | kakakuscraping-fastapi 用の通知設定 |

#### KAKAKU_NOTICE

- kakakuscraping-fastapi 用の通知設定

| 設定名                         | 説明                                                                                   |
| ------------------------------ | -------------------------------------------------------------------------------------- |
| kakaku_url                     | kakakuscraping-fastapi のアイテム一覧への URL。http://～で記述。リダイレクトには未対応 |
| kakaku_notice_option           | 通知設定。dict 型                                                                      |
| new_item                       | 追加された（一覧から見えるようになった）アイテムの通知 ON/OFF                          |
| remove_item                    | 削除（一覧から見えなくなった）アイテムの通知 ON/OFF                                    |
| change_to_in_stock             | 在庫なし(-1)から在庫ありになったアイテムの通知 ON/OFF                                  |
| change_to_out_of_stock         | 在庫ありから在庫なし(-1)になったアイテムの通知 ON/OFF                                  |
| lowest_price                   | 最安値を更新した通知 ON/OFF                                                            |
| lowest_price_without_no_change | 値段の変更なしで最安値である通知 ON/OFF                                                |
| price_decline                  | 値段が下がった通知 ON/OFF                                                              |
| price_rise                     | 値段が上がった通知の ON/OFF                                                            |

### 環境変数

- 通知の送信元、先のメールアドレスとパスワードは環境変数で設定する
- Gmail のみ確認。パスワードはアプリパスワードが必要。

| 環境変数名            | 説明                                     |
| --------------------- | ---------------------------------------- |
| SOURCE_EMAIL_ADDRESS  | 送信元のメールアドレス                   |
| SOURCE_EMAIL_PASSWORD | 送信元のメールアドレスのアプリパスワード |
| DEST_EMAIL_ADDRESS    | 送信（通知）先のメールアドレス           |
