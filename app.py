import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(page_title="kAIros - HIV/정신건강 통합케어 플랫폼", layout="wide", page_icon="🧬")

@st.cache_data
def load_mock_data():
    patients = pd.DataFrame({
        'Patient_ID': ['PT-1001', 'PT-1002', 'PT-1003', 'PT-1004'],
        'Age': [34, 45, 29, 52],
        'Gender': ['M', 'M', 'F', 'M'],
        'Last_Visit': ['2026-05-10', '2026-04-22', '2026-05-20', '2026-03-15'],
        'Risk_Score': [85, 42, 15, 92], # 0-100 척도
        'Psych_Visit_6m': [0, 2, 0, 0],
        'Sleep_Disorder': [1, 0, 0, 1],
        'ART_Adherence': [65, 95, 100, 50]
    })
    return patients

def main():
    st.sidebar.title("🧬 kAIros Platform")
    st.sidebar.markdown("HIV 감염인 치료 지속성 향상 CDSS")
    
    patients = load_mock_data()
    
    tab1, tab2, tab3 = st.tabs(["📊 이탈 위험 스코어카드", "🗺️ 지역별 서비스 공백 지도", "📑 정책·효과 실증 리포트"])
    
    # TAB 1: 이탈 위험 스코어카드
    with tab1:
        st.header("ART 복약 이탈 위험 예측 및 스크리닝")
        st.markdown("Random Forest & SHAP 기반 변수 중요도 분석 결과를 제공합니다.")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            selected_pt = st.selectbox("환자 선택 (Patient ID)", patients['Patient_ID'])
            pt_data = patients[patients['Patient_ID'] == selected_pt].iloc[0]
            st.metric(label="환자 연령/성별", value=f"{pt_data['Age']}세 / {pt_data['Gender']}")
            st.metric(label="최근 내원일", value=pt_data['Last_Visit'])
            
            if pt_data['Risk_Score'] >= 80:
                st.error("🚨 고위험 환자입니다. 정신건강의학과 협진 의뢰를 적극 권고합니다.")
            elif pt_data['Risk_Score'] >= 50:
                st.warning("⚠️ 중등도 위험 환자입니다.")
            else:
                st.success("✅ 치료 지속성이 양호합니다.")
                
        with col2:
            st.subheader(f"환자 {selected_pt} 이탈 위험도: {pt_data['Risk_Score']} / 100")
            shap_labels = ['정신과 미방문', '수면장애(F51)', '항우울제 미처방', '최근 내원 간격', '기타']
            shap_values = [38, 24, 15, 13, 10] if pt_data['Risk_Score'] >= 80 else [10, 5, 5, 20, 2]
            fig = px.bar(x=shap_values, y=shap_labels, orientation='h', title="이탈 위험 주요 원인 분석 (SHAP Values)", color=shap_values, color_continuous_scale='Reds')
            st.plotly_chart(fig, use_container_width=True)

    # TAB 2: 지역별 서비스 공백 지도
    with tab2:
        st.header("시군구별 정신건강 서비스 공백 지도")
        map_data = pd.DataFrame({
            'City': ['서울 용산구', '대전 서구', '부산 진구', '대구 중구', '광주 동구'],
            'Lat': [37.5326, 36.3554, 35.1631, 35.8661, 35.1460],
            'Lon': [126.9900, 127.3838, 129.0528, 128.6015, 126.9232],
            'Gap_Index': [85, 42, 68, 72, 35],
            'HIV_Prevalence': [300, 150, 220, 180, 90]
        })
        fig2 = px.scatter_mapbox(map_data, lat="Lat", lon="Lon", color="Gap_Index", size="HIV_Prevalence", color_continuous_scale='IceFire', size_max=20, zoom=5, hover_name="City", mapbox_style="carto-positron")
        st.plotly_chart(fig2, use_container_width=True)

    # TAB 3: 정책·효과 실증 리포트
    with tab3:
        st.header("정신건강 개입 효과 실증 (PSM 기반)")
        col_a, col_b = st.columns(2)
        col_a.metric(label="분석 대상 코호트 (B20-B24 상병)", value="15,420 명")
        col_b.metric(label="연간 재입원 비용 절감 추정액", value="약 45억 원")
        
        time = np.arange(0, 36, 1)
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=time, y=np.exp(-0.01 * time), mode='lines', name='정신건강 협진 연계군'))
        fig3.add_trace(go.Scatter(x=time, y=np.exp(-0.025 * time), mode='lines', name='일반 진료군'))
        st.plotly_chart(fig3, use_container_width=True)

if __name__ == "__main__":
    main()
