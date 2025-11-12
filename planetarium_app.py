import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

# ===============================
# 🌏 データ読み込み
# ===============================
# planetarium_data_manual.csv を同じフォルダに置いてね！
try:
    df = pd.read_csv("planetarium_data_manual.csv")
    st.success("✅ データを読み込みました！")
except FileNotFoundError:
    st.error("❌ planetarium_data_manual.csv が見つかりません。アプリと同じフォルダに置いてください。")
    st.stop()

# ======== 列名が日本語のときに対応 ==========
df = df.rename(columns={
    "緯度": "lat",
    "経度": "lon",
    "名前": "name",
    "施設名": "name"
})

# ======== lat / lon が無ければ終了 ==========
if not all(col in df.columns for col in ["name", "lat", "lon"]):
    st.error("❌ CSVの列名が正しくありません。「name」「lat」「lon」または「名前」「緯度」「経度」を含めてください。")
    st.stop()

# visited列（行った／行ってない）が無ければ作成
if "visited" not in df.columns:
    df["visited"] = False

# ===============================
# 🌟 タイトル
# ===============================
st.title("🌌 プラネタリウム訪問マップ")

# ===============================
# 🗺️ 地図の作成
# ===============================
# 日本の中心あたりを表示
m = folium.Map(location=[36.5, 137.0], zoom_start=6)

# ピンを追加
for i, row in df.iterrows():
    color = "red" if row["visited"] else "blue"
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=row["name"],
        icon=folium.Icon(color=color, icon="star")
    ).add_to(m)

# Streamlit上で地図を表示
st_data = st_folium(m, width=700, height=500)

# ===============================
# ✅ チェックボックスで管理
# ===============================
st.subheader("行ったプラネタリウムをチェック")

for i in range(len(df)):
    visited = st.checkbox(df.loc[i, "name"], value=df.loc[i, "visited"])
    df.loc[i, "visited"] = visited

# ===============================
# 💾 CSVに保存
# ===============================
if st.button("💾 変更を保存"):
    df.to_csv("planetarium_data_manual.csv", index=False)
    st.success("変更を保存しました！")

# ===============================
# 📋 現在のデータ
# ===============================
st.subheader("📋 現在のデータ一覧")
st.dataframe(df)
