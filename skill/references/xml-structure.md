# draw.io スイムレーンフローチャート XML構造仕様

## 目次

1. [全体構造](#1-全体構造)
2. [レーン定義](#2-レーン定義)
3. [ノード定義](#3-ノード定義)
4. [エッジ定義](#4-エッジ定義)
5. [座標計算ガイド](#5-座標計算ガイド)
6. [完全なテンプレート](#6-完全なテンプレート)

---

## 1. 全体構造

```xml
<mxfile host="65bd71144e">
    <diagram name="ページ1" id="[一意のID]">
        <mxGraphModel dx="2009" dy="1416" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="0" pageScale="1" pageWidth="1800" pageHeight="2339" math="0" shadow="0">
            <root>
                <mxCell id="0"/>
                <mxCell id="1" parent="0"/>

                <!-- ★ レーン定義 (左から順に) -->
                <!-- ★ レーン内ノード定義 -->
                <!-- ★ エッジ定義 (parent="1") -->

            </root>
        </mxGraphModel>
    </diagram>
</mxfile>
```

### 固定パラメータ

| パラメータ | 値 | 説明 |
|-----------|-----|------|
| `host` | `"65bd71144e"` | 固定値 |
| `dx` | `2009` | キャンバス横オフセット |
| `dy` | `1416` | キャンバス縦オフセット |
| `grid` | `0` | グリッド非表示 |
| `page` | `0` | ページ境界非表示 |
| `pageWidth` | `1800` | ページ幅 |
| `pageHeight` | `2339` | ページ高さ |

### diagram の id 生成

ランダムな英数字（例: `ccuKM5feCdU5HsTSmqlq`）を使用する。
JavaScript の `Math.random().toString(36).substring(2, 22)` 相当。

---

## 2. レーン定義

### 基本構文

```xml
<mxCell id="lane_[名前]" value="[レーン表示名]"
    style="swimlane;startSize=40;html=1;collapsible=1;whiteSpace=wrap;fillColor=[色];strokeColor=[色];[追加スタイル]"
    parent="1" vertex="1">
    <mxGeometry x="[X位置]" y="40" width="[幅]" height="[全体高さ]" as="geometry">
        <!-- alternateBoundsは折りたたみ時のサイズ（省略可） -->
        <mxRectangle x="[X位置]" y="40" width="[折りたたみ幅]" height="40" as="alternateBounds"/>
    </mxGeometry>
</mxCell>
```

### レーンスタイルの共通プロパティ

```
swimlane;startSize=40;html=1;collapsible=1;whiteSpace=wrap;
```

- `startSize=40` : レーンヘッダの高さ（40px固定）
- `collapsible=1` : 折りたたみ可能

### レーン配置の計算方法

```
レーン1: x = 40
レーン2: x = 40 + レーン1の幅
レーン3: x = 40 + レーン1の幅 + レーン2の幅
...以降同様
```

すべてのレーンは `y=40` で開始し、`height` は統一値（デフォルト1600）。

### レーン配色テーブル（デフォルト）

```xml
<!-- パターン1: グレー系（顧客・外部向き） -->
fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;

<!-- パターン2: 緑系（営業・窓口） -->
fillColor=#d5e8d4;strokeColor=#82b366;

<!-- パターン3: 青系（製造・技術） -->
fillColor=#dae8fc;strokeColor=#6c8ebf;

<!-- パターン4: 黄系（資材・管理）※太字 -->
fillColor=#fff2cc;strokeColor=#d6b656;fontStyle=1

<!-- パターン5: 紫系（営業業務・事務） -->
fillColor=#e1d5e7;strokeColor=#9673a6;

<!-- パターン6: 赤系（仕入先・外部） -->
fillColor=#f8cecc;strokeColor=#b85450;
```

### alternateBounds（折りたたみサイズ）

レーン名が長い場合、折りたたみ時の幅を設定する。

```xml
<mxRectangle x="[レーンX]" y="40" width="[文字幅に応じた値]" height="40" as="alternateBounds"/>
```

- 短い名前（2-4文字）: width=71 程度
- 中程度（5-8文字）: width=100 程度
- 長い名前（9文字以上）: width=130 程度

省略可。省略した場合は draw.io がデフォルト動作する。

---

## 3. ノード定義

### 3.1 開始ノード（楕円・緑）

```xml
<mxCell id="start" value="[開始イベント名]"
    style="ellipse;whiteSpace=wrap;html=1;fillColor=#60a917;fontColor=#ffffff;strokeColor=#2D7600;fontSize=12;"
    parent="[レーンID]" vertex="1">
    <mxGeometry x="60" y="60" width="240" height="60" as="geometry"/>
</mxCell>
```

- **用途**: フローの開始点
- **配置**: 通常、最初のレーン（顧客レーン等）の上部
- **スタイル固定値**: `fillColor=#60a917;fontColor=#ffffff;strokeColor=#2D7600;`

### 3.2 終了ノード（楕円・緑・小）

```xml
<mxCell id="end" value="完了"
    style="ellipse;whiteSpace=wrap;html=1;fillColor=#60a917;fontColor=#ffffff;strokeColor=#2D7600;"
    parent="[レーンID]" vertex="1">
    <mxGeometry x="90" y="[Y位置]" width="80" height="40" as="geometry"/>
</mxCell>
```

- **用途**: フローの終了点
- **配置**: フロー最下部。複数の終了ノードがあっても良い
- **サイズ**: 開始より小さめ（80×40）

### 3.3 プロセスノード（角丸矩形）

```xml
<mxCell id="proc_[識別名]" value="[処理名]&#xa;[サブテキスト]"
    style="rounded=1;whiteSpace=wrap;html=1;[追加スタイル]"
    parent="[レーンID]" vertex="1">
    <mxGeometry x="[X]" y="[Y]" width="160" height="60" as="geometry"/>
</mxCell>
```

- **用途**: 通常の処理ステップ
- **ID命名**: `proc_` プレフィックス + 識別名
- **改行**: `&#xa;` を使用
- **追加スタイル（オプション）**:
  - `arcSize=10` : 角丸の大きさ指定
  - `fontStyle=0` : フォントスタイルリセット
  - `dashed=1` : 破線ボーダー（外部処理など）

### 3.4 判断ノード（ひし形）

```xml
<mxCell id="dec_[識別名]" value="[判断内容]"
    style="rhombus;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;"
    parent="[レーンID]" vertex="1">
    <mxGeometry x="[X]" y="[Y]" width="[120-240]" height="80" as="geometry"/>
</mxCell>
```

- **用途**: 分岐判断
- **ID命名**: `dec_` プレフィックス + 識別名
- **デフォルト配色**: オレンジ系 `fillColor=#ffe6cc;strokeColor=#d79b00;`
- **幅**: テキスト量に応じて120〜240px

#### 判断ノードのバリエーション

```xml
<!-- 標準（オレンジ背景） -->
style="rhombus;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;"

<!-- 白背景（サブ判断用） -->
style="rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=default;fontStyle=0;fontSize=14;"
```

### 3.5 システム処理ノード（二重線矩形）

```xml
<mxCell id="proc_system_[識別名]" value="[処理名]&#xa;[サブテキスト]"
    style="shape=process;whiteSpace=wrap;html=1;backgroundOutline=1;fillColor=[色];strokeColor=[色];"
    parent="[レーンID]" vertex="1">
    <mxGeometry x="[X]" y="[Y]" width="160" height="60" as="geometry"/>
</mxCell>
```

- **用途**: システム自動処理、バッチ処理
- **backgroundOutline=1** : 二重線表現に必要
- **配色**: 所属レーンの色に合わせることが多い

### 3.6 付箋メモノード

```xml
<mxCell id="[連番ID]" value="[メモ内容]"
    style="shape=note;whiteSpace=wrap;html=1;backgroundOutline=1;darkOpacity=0.05;fillColor=#fff2cc;strokeColor=#d6b656;align=left;size=14;"
    parent="[レーンID]" vertex="1">
    <mxGeometry x="[X]" y="[Y]" width="[141-165]" height="[68-100]" as="geometry"/>
</mxCell>
```

- **用途**: 補足説明、業務ルール、注意事項
- **配色固定**: 黄色系 `fillColor=#fff2cc;strokeColor=#d6b656;`
- **テキスト配置**: `align=left` （左揃え）
- **折り返し部分の高さ**: `size=14` （ノートアイコンの折り返し部分）
- **配置**: 説明対象のノード近くに配置（レーン外にはみ出してもOK）

---

## 4. エッジ定義

### 4.1 基本エッジ（ラベルなし）

```xml
<mxCell id="edge_[連番]"
    style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"
    parent="1" source="[ソースID]" target="[ターゲットID]" edge="1">
    <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### 4.2 ラベル付きエッジ

```xml
<mxCell id="edge_[連番]" value="[ラベルテキスト]"
    style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=[値];exitY=[値];entryX=[値];entryY=[値];fontSize=12;"
    parent="1" source="[ソースID]" target="[ターゲットID]" edge="1">
    <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

- ラベル内のHTMLタグ対応: `<div>`, `<br>` 等使用可
- `fontSize=12` : ラベルフォントサイズ

### 4.3 経由点を持つエッジ

レーンを跨ぐ場合やルートを指定する場合：

```xml
<mxCell id="edge_[連番]" value="[ラベル]"
    style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=[値];exitY=[値];entryX=[値];entryY=[値];fontSize=12;"
    parent="1" source="[ソースID]" target="[ターゲットID]" edge="1">
    <mxGeometry relative="1" as="geometry">
        <Array as="points">
            <mxPoint x="[グローバルX1]" y="[グローバルY1]"/>
            <mxPoint x="[グローバルX2]" y="[グローバルY2]"/>
        </Array>
    </mxGeometry>
</mxCell>
```

**重要**: points内の座標は**グローバル座標**（レーンのx + ノードのx）。

### 4.4 破線エッジ（差戻し・ループ）

```xml
<mxCell id="edge_[連番]" value="[ラベル]"
    style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=[値];exitY=[値];dashed=1;fontSize=12;"
    parent="1" source="[ソースID]" edge="1">
    <mxGeometry relative="1" as="geometry">
        <Array as="points">
            <mxPoint x="[X]" y="[Y]"/>
        </Array>
        <mxPoint x="[X]" y="[Y]" as="targetPoint"/>
    </mxGeometry>
</mxCell>
```

- `dashed=1` で破線表示
- targetが明示ノードでない場合は `targetPoint` で座標指定

### 4.5 エッジラベル（独立オブジェクト）

エッジのラベルを別セルとして定義する場合：

```xml
<mxCell id="[ラベルID]" value="[ラベルテキスト]"
    style="edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];"
    vertex="1" connectable="0" parent="[エッジID]">
    <mxGeometry x="[相対位置]" y="[オフセット]" relative="1" as="geometry">
        <mxPoint as="offset"/>
    </mxGeometry>
</mxCell>
```

- `parent` にエッジIDを指定
- `relative="1"` でエッジに対する相対位置
- `x` の値: `-1`=始点側、`0`=中央、`1`=終点側

### 4.6 接続方向（exitX/exitY/entryX/entryY）

ノードの接続ポイントを制御する値：

```
exitX/entryX:  0=左端, 0.5=中央, 1=右端
exitY/entryY:  0=上端, 0.5=中央, 1=下端
```

よく使うパターン：

| 接続方向 | exit | entry |
|---------|------|-------|
| 上→下（同レーン） | `exitX=0.5;exitY=1` | `entryX=0.5;entryY=0` |
| 左→右（レーン間） | `exitX=1;exitY=0.5` | `entryX=0;entryY=0.5` |
| 右→左（戻り） | `exitX=0;exitY=0.5` | `entryX=1;entryY=0.5` |
| 下→右（L字） | `exitX=0.5;exitY=1` | `entryX=0;entryY=0.5` |

特殊パターン：
- `entryY=0.25` / `entryY=0.75` : ノード上部/下部寄りの接続
- `exitY=0.75` : ノード下部寄りからの出発

---

## 5. 座標計算ガイド

### グローバル座標の計算

ノードのグローバル座標 = レーンのx + ノードのローカルx

例：
- レーン `lane_mfg` の x=640
- ノード `proc_mfg_repair` のローカル x=120, width=160
- → ノード中央のグローバルX = 640 + 120 + 160/2 = 840

### 推奨レイアウト寸法

```
レーン間隔: 0px（隣接配置）
レーン幅:
  - 狭い（ノード1列）: 240px
  - 標準: 260〜360px
  - 広い（ノード2列 or メモ付き）: 400px

ノード配置:
  - レーン内左マージン: 40〜60px
  - ノード間縦間隔（通常）: 20〜60px
  - セクション間縦間隔: 80〜120px
  - ノード標準幅: 160px
  - ノード標準高さ: 50〜60px
```

### フローの縦位置合わせ

同じ処理段階にあるノードは、レーンが異なっても **Y座標を近い値に揃える** ことで
フローの進行段階が視覚的にわかりやすくなる。

---

## 6. 完全なテンプレート

最小構成のテンプレート（2レーン、開始→プロセス→判断→終了）：

```xml
<mxfile host="65bd71144e">
    <diagram name="ページ1" id="template001">
        <mxGraphModel dx="2009" dy="1416" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="0" pageScale="1" pageWidth="1800" pageHeight="2339" math="0" shadow="0">
            <root>
                <mxCell id="0"/>
                <mxCell id="1" parent="0"/>

                <!-- レーン1 -->
                <mxCell id="lane_a" value="部門A"
                    style="swimlane;startSize=40;html=1;collapsible=1;whiteSpace=wrap;fillColor=#d5e8d4;strokeColor=#82b366;"
                    parent="1" vertex="1">
                    <mxGeometry x="40" y="40" width="300" height="600" as="geometry"/>
                </mxCell>
                <mxCell id="start" value="開始イベント"
                    style="ellipse;whiteSpace=wrap;html=1;fillColor=#60a917;fontColor=#ffffff;strokeColor=#2D7600;fontSize=12;"
                    parent="lane_a" vertex="1">
                    <mxGeometry x="50" y="60" width="200" height="60" as="geometry"/>
                </mxCell>
                <mxCell id="proc_a1" value="処理ステップ1&#xa;詳細説明"
                    style="rounded=1;whiteSpace=wrap;html=1;"
                    parent="lane_a" vertex="1">
                    <mxGeometry x="70" y="160" width="160" height="60" as="geometry"/>
                </mxCell>

                <!-- レーン2 -->
                <mxCell id="lane_b" value="部門B"
                    style="swimlane;startSize=40;html=1;collapsible=1;whiteSpace=wrap;fillColor=#dae8fc;strokeColor=#6c8ebf;"
                    parent="1" vertex="1">
                    <mxGeometry x="340" y="40" width="300" height="600" as="geometry"/>
                </mxCell>
                <mxCell id="dec_b1" value="判断"
                    style="rhombus;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;"
                    parent="lane_b" vertex="1">
                    <mxGeometry x="90" y="250" width="120" height="80" as="geometry"/>
                </mxCell>
                <mxCell id="proc_b1" value="処理ステップ2"
                    style="rounded=1;whiteSpace=wrap;html=1;"
                    parent="lane_b" vertex="1">
                    <mxGeometry x="70" y="380" width="160" height="60" as="geometry"/>
                </mxCell>
                <mxCell id="end" value="完了"
                    style="ellipse;whiteSpace=wrap;html=1;fillColor=#60a917;fontColor=#ffffff;strokeColor=#2D7600;"
                    parent="lane_b" vertex="1">
                    <mxGeometry x="110" y="500" width="80" height="40" as="geometry"/>
                </mxCell>

                <!-- エッジ -->
                <mxCell id="edge_1"
                    style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"
                    parent="1" source="start" target="proc_a1" edge="1">
                    <mxGeometry relative="1" as="geometry"/>
                </mxCell>
                <mxCell id="edge_2"
                    style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;entryX=0.5;entryY=0;"
                    parent="1" source="proc_a1" target="dec_b1" edge="1">
                    <mxGeometry relative="1" as="geometry"/>
                </mxCell>
                <mxCell id="edge_3" value="YES"
                    style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;fontSize=12;"
                    parent="1" source="dec_b1" target="proc_b1" edge="1">
                    <mxGeometry relative="1" as="geometry"/>
                </mxCell>
                <mxCell id="edge_4"
                    style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"
                    parent="1" source="proc_b1" target="end" edge="1">
                    <mxGeometry relative="1" as="geometry"/>
                </mxCell>
            </root>
        </mxGraphModel>
    </diagram>
</mxfile>
```

---

## 補足: ID命名規則

| プレフィックス | 用途 | 例 |
|--------------|------|-----|
| `lane_` | スイムレーン | `lane_cust`, `lane_mfg`, `lane_admin` |
| `start` | 開始ノード | `start`, `start_sub` |
| `end` | 終了ノード | `end`, `end_return` |
| `proc_` | プロセスノード | `proc_sales_input`, `proc_mfg_repair` |
| `dec_` | 判断ノード | `dec_mfg_action`, `dec_cust_reply` |
| `proc_system_` | システム処理 | `proc_system_sales` |
| `proc_ext_` | 外部処理 | `proc_ext_ship` |
| `edge_` | エッジ | `edge_1`, `edge_pq1` |
| 数字のみ | 付箋メモ | `7`, `11`, `12`, `13` |

## 補足: スタイル一覧早見表

```
■ レーン共通
swimlane;startSize=40;html=1;collapsible=1;whiteSpace=wrap;

■ 開始/終了（緑楕円）
ellipse;whiteSpace=wrap;html=1;fillColor=#60a917;fontColor=#ffffff;strokeColor=#2D7600;

■ プロセス（角丸矩形）
rounded=1;whiteSpace=wrap;html=1;

■ 判断（ひし形・オレンジ）
rhombus;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;

■ システム処理（二重線矩形）
shape=process;whiteSpace=wrap;html=1;backgroundOutline=1;

■ 付箋メモ（黄色ノート）
shape=note;whiteSpace=wrap;html=1;backgroundOutline=1;darkOpacity=0.05;fillColor=#fff2cc;strokeColor=#d6b656;align=left;size=14;

■ エッジ共通
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;

■ エッジラベル
edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];
```
