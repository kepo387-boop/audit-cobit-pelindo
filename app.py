import io
import datetime
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Audit SI Terminal Peti Kemas", page_icon="✅", layout="centered")

DOM = {"EDM": "Evaluate, Direct and Monitor", "APO": "Align, Plan and Organize",
       "BAI": "Build, Acquire and Implement", "DSS": "Deliver, Service and Support",
       "MEA": "Monitor, Evaluate and Assess"}

SOAL = {
    "EDM": [("EDM01", "Apakah arah digitalisasi layanan terminal selaras dengan sasaran bisnis perusahaan?"),
            ("EDM01", "Apakah peran dan wewenang pengambil keputusan, pemilik proses, dan pengelola sistem terminal sudah ditetapkan dengan jelas?"),
            ("EDM02", "Apakah manajemen puncak menerima laporan berkala tentang ketersediaan sistem dan kinerja layanan terminal?"),
            ("EDM03", "Apakah manfaat sistem digital terhadap produktivitas bongkar muat dievaluasi?"),
            ("EDM03", "Apakah risiko sistem terhenti, kesalahan data peti kemas, dan serangan siber sudah masuk register risiko?"),
            ("EDM05", "Apakah ada mekanisme eskalasi kepada manajemen ketika gangguan sistem melampaui batas toleransi?")],
    "APO": [("APO02", "Apakah rencana pengembangan sistem terminal disusun berdasarkan kebutuhan operasi dan prioritas bisnis?"),
            ("APO03", "Apakah tersedia gambaran arsitektur yang memetakan TOS, sistem penagihan, perangkat gate, dan integrasi eksternal?"),
            ("APO07", "Apakah kompetensi operator dan administrator sistem sesuai dengan beban tugasnya?"),
            ("APO01", "Apakah kebijakan keamanan informasi, pengelolaan data, dan penggunaan sistem sudah terdokumentasi dan disosialisasikan?"),
            ("APO13", "Apakah klasifikasi informasi dan pengendalian akses mampu mencegah pihak tidak berwenang membuka data pengguna jasa?"),
            ("APO10", "Apakah perjanjian dengan vendor memuat SLA, perlindungan data, dan pembagian tanggung jawab?")],
    "BAI": [("BAI02", "Apakah kebutuhan pengguna jasa dan unit operasi didokumentasikan sebelum sistem diubah atau dikembangkan?"),
            ("BAI03", "Apakah integrasi dengan Inaportnet, INSW, dan sistem mitra diuji agar pertukaran data akurat?"),
            ("BAI07", "Apakah setiap perubahan diuji di lingkungan terpisah dari produksi sebelum diterapkan?"),
            ("BAI06", "Apakah setiap perubahan memiliki tiket, penilaian dampak, persetujuan, dan rencana pemulihan (rollback)?"),
            ("BAI09", "Apakah aset TI (server, perangkat gate, pemindai, jaringan) tercatat lengkap dengan pemilik dan statusnya?"),
            ("BAI08", "Apakah pengguna terdampak mendapat panduan atau pemberitahuan saat fitur baru dirilis?")],
    "DSS": [("DSS01", "Apakah ketersediaan dan kinerja TOS, jaringan, dan perangkat gate dipantau?"),
            ("DSS02", "Apakah insiden dicatat, diprioritaskan, dan ditangani sesuai target waktu penyelesaian?"),
            ("DSS03", "Apakah insiden yang berulang dianalisis untuk menemukan penyebab utamanya?"),
            ("DSS04", "Apakah data dicadangkan sesuai jadwal dan prosedur pemulihan (RTO/RPO) diuji?"),
            ("DSS05", "Apakah hak akses dibatasi sesuai peran, ditinjau berkala, dan akun yang tidak bertugas segera dinonaktifkan?"),
            ("DSS02", "Apakah tersedia prosedur manual sementara agar terminal tetap berjalan saat sistem utama berhenti?")],
    "MEA": [("MEA01", "Apakah kinerja layanan digital dan terminal diukur dengan indikator jelas dan dilaporkan berkala?"),
            ("MEA01", "Apakah selisih antara target dan realisasi kinerja dianalisis penyebabnya?"),
            ("MEA02", "Apakah kontrol akses, persetujuan perubahan, dan pencatatan transaksi (termasuk tagihan) dievaluasi berkala?"),
            ("MEA02", "Apakah kelemahan kontrol dicatat beserta rencana perbaikan dan penanggung jawabnya?"),
            ("MEA03", "Apakah kewajiban regulasi (kepelabuhanan, Inaportnet, perlindungan data pribadi) telah diidentifikasi dan dipantau?"),
            ("MEA03", "Apakah ketidaksesuaian terhadap ketentuan ditindaklanjuti sampai tuntas?")],
}
DAFTAR = []
for d, items in SOAL.items():
    for kode, teks in items:
        DAFTAR.append((len(DAFTAR) + 1, d, kode, teks))

st.markdown("""<style>
.kartu{background:#f1f7f6;border-radius:14px;padding:16px;text-align:center}
.kartu b{display:block;font-size:28px;color:#0f766e}.kartu span{font-size:13px;color:#4b5563}
</style>""", unsafe_allow_html=True)


def status(p):
    # Ambang batas adalah asumsi; sesuaikan dengan ketentuan dosen.
    if pd.isna(p):
        return "Belum dapat disimpulkan"
    return "Memadai" if p >= 80 else "Memadai dengan perbaikan" if p >= 60 else "Perlu perbaikan prioritas"


st.title("✅ Audit Sistem Informasi COBIT 5")
st.subheader("Layanan Digital Terminal Peti Kemas · PT Pelabuhan Indonesia (Persero)")
st.write("Aplikasi ini membantu mengevaluasi tata kelola sistem informasi terminal peti kemas memakai "
         "30 pertanyaan di lima domain COBIT 5 (EDM, APO, BAI, DSS, MEA). Isi identitas, jawab seluruh "
         "pertanyaan dengan **Ya**, **Tidak**, atau **N/A**, lalu lihat hasilnya dan unduh laporan Excel.")
st.caption("Aplikasi akademik. Jawaban yang diisi tidak mewakili hasil audit aktual perusahaan.")

with st.form("audit"):
    st.header("1. Identitas Pengisi")
    nama = st.text_input("Nama lengkap *")
    jabatan = st.text_input("Jabatan/Posisi")
    divisi = st.text_input("Bagian/Divisi")
    tanggal = st.date_input("Tanggal pengisian", datetime.date.today())

    st.header("2. Pertanyaan Audit")
    st.caption("Pilih satu jawaban untuk setiap pertanyaan. Seluruh pertanyaan wajib dijawab.")
    jawab, terakhir = {}, None
    for no, d, kode, teks in DAFTAR:
        if d != terakhir:
            st.subheader(f"Domain {d} · {DOM[d]}")
            terakhir = d
        jawab[no] = st.radio(f"{no}. [{kode}] {teks}", ["Ya", "Tidak", "N/A"], index=None,
                             horizontal=True, key=f"q{no}")
    kirim = st.form_submit_button("Kirim dan lihat hasil", type="primary")

if kirim:
    kosong = [n for n, v in jawab.items() if v is None]
    if not nama.strip():
        st.error("Nama lengkap wajib diisi.")
    elif kosong:
        st.error("Pertanyaan yang belum dijawab: " + ", ".join(map(str, kosong)))
    else:
        df = pd.DataFrame([{"No": n, "Domain": d, "Kode": k, "Pertanyaan": t, "Jawaban": jawab[n]}
                           for n, d, k, t in DAFTAR])
        st.session_state.hasil = (df, {"Nama": nama, "Jabatan": jabatan, "Divisi": divisi, "Tanggal": str(tanggal)})

if "hasil" in st.session_state:
    df, ident = st.session_state.hasil
    st.divider()
    st.header("3. Hasil Audit")
    rk = df.pivot_table(index="Domain", columns="Jawaban", values="No", aggfunc="count", fill_value=0)
    rk = rk.reindex(index=list(DOM), columns=["Ya", "Tidak", "N/A"], fill_value=0)
    rk["Pemenuhan (%)"] = (rk["Ya"] / (rk["Ya"] + rk["Tidak"]).replace(0, float("nan")) * 100).round(1)
    rk["Status"] = rk["Pemenuhan (%)"].apply(status)
    ya, tidak = (df["Jawaban"] == "Ya").sum(), (df["Jawaban"] == "Tidak").sum()
    total = ya / (ya + tidak) * 100 if (ya + tidak) else float("nan")

    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="kartu"><b>{ya}</b><span>jawaban Ya</span></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="kartu"><b>{tidak}</b><span>jawaban Tidak</span></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="kartu"><b>{total:.0f}%</b><span>pemenuhan keseluruhan</span></div>', unsafe_allow_html=True)
    st.write("")
    st.success(f"Kesimpulan: **{status(total)}**")
    st.subheader("Rekapitulasi per domain")
    st.dataframe(rk, width="stretch")
    st.bar_chart(rk["Pemenuhan (%)"])
    st.subheader("Butir yang dijawab Tidak (calon temuan)")
    temuan = df[df["Jawaban"] == "Tidak"]
    st.dataframe(temuan, hide_index=True, width="stretch") if len(temuan) else st.info("Tidak ada.")

    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as xw:
        pd.DataFrame(list(ident.items()), columns=["Data", "Isi"]).to_excel(xw, sheet_name="Identitas", index=False)
        df.to_excel(xw, sheet_name="Jawaban", index=False)
        rk.to_excel(xw, sheet_name="Rekapitulasi")
        temuan.to_excel(xw, sheet_name="Temuan", index=False)
    a, b = st.columns(2)
    a.download_button("⬇️ Unduh laporan Excel", buf.getvalue(), "laporan_audit.xlsx")
    b.download_button("⬇️ Unduh CSV (untuk Colab)", df.to_csv(index=False).encode("utf-8-sig"), "hasil_audit.csv", "text/csv")
