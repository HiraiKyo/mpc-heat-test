# mpc-heat-test

Heat testing with calculating matrix.

# テスト方法

- 行列計算を行い、その間の内部温度データを計測
- 温度上昇に伴う計算スピードの低下を計測

# テスト要件

- 5000x5000 の逆行列計算
- 100 回反復
- インターバル 8 秒設定

# データ出力フォーマット

| Time Lapsed[s] | Calculation Time[s] | Temperature[℃] |
| 1.00000 | 1.00000 | 24.42 |
| 2.10000 | 1.00000 | 24.54 |
| 3.30000 | 1.00000 | 24.64 |
