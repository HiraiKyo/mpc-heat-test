# mpc-heat-test

Heat testing with calculating matrix.

# テスト方法

- 行列計算を行い、その間の温度データを計測
- 温度上昇に伴う計算スピードの低下を計測

# テスト要件

- 30 分間稼働
- 5000x5000 の逆行列計算

# データ出力フォーマット

| Timestamp[s] | Temperature[℃] |
| 1.00000 | 24.42 |
