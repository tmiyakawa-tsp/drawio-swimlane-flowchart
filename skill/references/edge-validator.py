"""
draw.io スイムレーンフローチャート エッジ検証スクリプト

使い方:
  python3 edge-validator.py <drawioファイル> [シート名]

機能:
  - 指定シート（省略時は全シート）の全エッジについて、
    線の重なり（CROSS）と不要な迂回（DETOUR）を座標計算で検出する
  - 問題が見つかった場合、エッジID・ラベル・交差先ノードを報告する

検出項目:
  CROSS-H: 水平セグメントがノードを横切る
  CROSS-V: 垂直セグメントがノードを縦切る
  DETOUR-Y: Y座標が下がってから上がる（差分20px超）
  DETOUR-X: X座標が右に行って左に戻る（差分60px超）
"""
import re
import sys
import xml.etree.ElementTree as ET


def validate_sheet(xml_str, sheet_name):
    """1シート分のXMLを検証し、問題リストを返す"""
    try:
        root = ET.fromstring("<mxfile>" + xml_str + "</mxfile>")
    except ET.ParseError as e:
        return [f"XML_ERROR: {e}"]

    graph = root.find(".//root")
    if graph is None:
        return ["XML_ERROR: <root> not found"]

    # レーン・ノード・エッジを収集
    lanes = {}
    nodes = {}
    edges = []

    for cell in graph.findall(".//mxCell"):
        cid = cell.get("id")
        style = cell.get("style", "")
        parent = cell.get("parent", "")
        geo = cell.find("mxGeometry")

        if "swimlane" in style and ("swimlaneLine" in style or "collapsible" in style):
            if geo is not None:
                lanes[cid] = {
                    "x": float(geo.get("x", 0)),
                    "y": float(geo.get("y", 0)),
                    "w": float(geo.get("width", 0)),
                    "h": float(geo.get("height", 0)),
                }

        elif cell.get("edge") == "1":
            source = cell.get("source", "")
            target = cell.get("target", "")
            value = cell.get("value", "")

            exitX = (
                float(re.search(r"exitX=([\d.]+)", style).group(1))
                if "exitX=" in style
                else 0.5
            )
            exitY = (
                float(re.search(r"exitY=([\d.]+)", style).group(1))
                if "exitY=" in style
                else 1.0
            )
            entryX = (
                float(re.search(r"entryX=([\d.]+)", style).group(1))
                if "entryX=" in style
                else 0.5
            )
            entryY = (
                float(re.search(r"entryY=([\d.]+)", style).group(1))
                if "entryY=" in style
                else 0.0
            )

            points = []
            arr = geo.find("Array") if geo is not None else None
            if arr is not None:
                for pt in arr.findall("mxPoint"):
                    points.append((float(pt.get("x", 0)), float(pt.get("y", 0))))

            edges.append(
                {
                    "id": cid,
                    "source": source,
                    "target": target,
                    "exitX": exitX,
                    "exitY": exitY,
                    "entryX": entryX,
                    "entryY": entryY,
                    "points": points,
                    "value": value[:30],
                }
            )

        elif (
            cell.get("vertex") == "1"
            and parent in lanes
            and "swimlane" not in style
        ):
            if geo is not None:
                lane = lanes[parent]
                nodes[cid] = {
                    "gx": lane["x"] + float(geo.get("x", 0)),
                    "gy": lane["y"] + float(geo.get("y", 0)),
                    "w": float(geo.get("width", 0)),
                    "h": float(geo.get("height", 0)),
                }

    # 検証
    problems = []
    MARGIN = 5
    DETOUR_Y_THRESHOLD = 20
    DETOUR_X_THRESHOLD = 60

    for edge in edges:
        src, tgt = edge["source"], edge["target"]
        if src not in nodes or tgt not in nodes:
            continue

        sn, tn = nodes[src], nodes[tgt]
        exit_gx = sn["gx"] + sn["w"] * edge["exitX"]
        exit_gy = sn["gy"] + sn["h"] * edge["exitY"]
        entry_gx = tn["gx"] + tn["w"] * edge["entryX"]
        entry_gy = tn["gy"] + tn["h"] * edge["entryY"]
        path = [(exit_gx, exit_gy)] + edge["points"] + [(entry_gx, entry_gy)]

        eid = edge["id"]
        val = edge["value"]

        # 検出1: 不要な迂回
        for i in range(len(path) - 2):
            p0, p1, p2 = path[i], path[i + 1], path[i + 2]
            if (p1[1] > p0[1] and p2[1] < p1[1]) or (
                p1[1] < p0[1] and p2[1] > p1[1]
            ):
                if abs(p1[1] - p2[1]) > DETOUR_Y_THRESHOLD:
                    problems.append(
                        f"DETOUR-Y {eid} ('{val}'): "
                        f"y={p0[1]:.0f}->{p1[1]:.0f}->{p2[1]:.0f}"
                    )
            if (p1[0] > p0[0] and p2[0] < p1[0]) or (
                p1[0] < p0[0] and p2[0] > p1[0]
            ):
                if abs(p1[0] - p2[0]) > DETOUR_X_THRESHOLD:
                    problems.append(
                        f"DETOUR-X {eid} ('{val}'): "
                        f"x={p0[0]:.0f}->{p1[0]:.0f}->{p2[0]:.0f}"
                    )

        # 検出2: 線の重なり
        for i in range(len(path) - 1):
            s, e = path[i], path[i + 1]
            for nid, nd in nodes.items():
                if nid == src or nid == tgt:
                    continue
                nx1 = nd["gx"] - MARGIN
                ny1 = nd["gy"] - MARGIN
                nx2 = nd["gx"] + nd["w"] + MARGIN
                ny2 = nd["gy"] + nd["h"] + MARGIN

                # 水平セグメント
                if abs(s[1] - e[1]) < 2:
                    sy = s[1]
                    if (
                        ny1 < sy < ny2
                        and min(s[0], e[0]) < nx2
                        and max(s[0], e[0]) > nx1
                    ):
                        problems.append(
                            f"CROSS-H {eid} ('{val}'): "
                            f"y={sy:.0f} thru {nid} "
                            f"(y={nd['gy']:.0f}-{nd['gy']+nd['h']:.0f})"
                        )

                # 垂直セグメント
                elif abs(s[0] - e[0]) < 2:
                    sx = s[0]
                    if (
                        nx1 < sx < nx2
                        and min(s[1], e[1]) < ny2
                        and max(s[1], e[1]) > ny1
                    ):
                        problems.append(
                            f"CROSS-V {eid} ('{val}'): "
                            f"x={sx:.0f} thru {nid} "
                            f"(x={nd['gx']:.0f}-{nd['gx']+nd['w']:.0f})"
                        )

    return problems


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 edge-validator.py <file.drawio> [sheet_name]")
        sys.exit(1)

    filepath = sys.argv[1]
    target_sheet = sys.argv[2] if len(sys.argv) > 2 else None

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 全diagramを抽出
    diagrams = re.findall(
        r'(<diagram[^>]*name="([^"]*)"[^>]*>.*?</diagram>)', content, re.DOTALL
    )
    if not diagrams:
        # name属性がidの後にある場合
        diagrams = re.findall(
            r'(<diagram[^>]*>.*?</diagram>)', content, re.DOTALL
        )
        # nameを再抽出
        diagrams_with_names = []
        for d in diagrams:
            m = re.search(r'name="([^"]*)"', d[0] if isinstance(d, tuple) else d)
            name = m.group(1) if m else "unknown"
            xml = d[0] if isinstance(d, tuple) else d
            diagrams_with_names.append((xml, name))
        diagrams = diagrams_with_names

    total_problems = 0
    for xml_str, name in diagrams:
        if target_sheet and target_sheet not in name:
            continue

        problems = validate_sheet(xml_str, name)
        if problems:
            print(f"\n=== {name}: {len(problems)} problems ===")
            for p in problems:
                print(f"  {p}")
            total_problems += len(problems)
        else:
            print(f"{name}: ALL CLEAR")

    if total_problems > 0:
        print(f"\nTotal: {total_problems} problems found")
        sys.exit(1)
    else:
        print("\nAll sheets passed validation")
        sys.exit(0)


if __name__ == "__main__":
    main()
