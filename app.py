from flask import Flask, request, render_template
import pandas as pd
import joblib

app = Flask(__name__)

# Load model dan mapping
model = joblib.load("model_rfr.pkl")
mappings = joblib.load("mappings.pkl")
ikan_mapping = mappings['ikan']       # key: nama ikan (str), value: kode (int)
kabupaten_mapping = mappings['kabupaten']  # key: kode (int), value: nama kabupaten (atau sebaliknya, pastikan konsisten)

@app.route('/')
def home():
    # Untuk dropdown, kita ingin [(kode, nama kabupaten)] dan [(nama ikan)] dalam urutan terurut
    # Asumsi kabupaten_mapping: dict int->str, ikan_mapping: dict str->int
    
    # Balik mapping kabupaten ke format [(kode, nama)] utk dropdown
    kabupaten_items = sorted(kabupaten_mapping.items())  # [(kode, nama)]

    # Ikan dari mapping key (nama ikan), urutkan alphabet
    ikan_items = sorted(ikan_mapping.keys())

    return render_template('index.html', kabupaten_items=kabupaten_items, ikan_items=ikan_items)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        tahun = int(request.form['tahun'])
        kabupaten_kota_str = request.form['kabupaten_kota'].strip()
        jenis_ikan_str = request.form['jenis_ikan'].strip().upper()
        volume = float(request.form['volume'])
        nilai = float(request.form['nilai'])

        # Convert kabupaten input ke int key
        try:
            kabupaten_kota_key = int(kabupaten_kota_str)
        except ValueError:
            return render_template('index.html', prediction_text='❌ Error: Kabupaten tidak valid.')

        kabupaten_nama = kabupaten_mapping.get(kabupaten_kota_key)
        jenis_ikan_kode = ikan_mapping.get(jenis_ikan_str)

        if kabupaten_nama is None or jenis_ikan_kode is None:
            return render_template('index.html', prediction_text='❌ Error: Nama ikan atau kabupaten tidak dikenali.')

        # Buat DataFrame input untuk model sesuai kolom yang dipakai model
        input_data = pd.DataFrame([[tahun, kabupaten_kota_key, jenis_ikan_kode, volume, nilai]], 
                                  columns=['Tahun', 'Kabupaten Kota', 'Jenis Ikan (kode)', 'Volume (ton)', 'Nilai (Rp. Juta)'])

        prediction = model.predict(input_data)[0]

        return render_template('index.html', prediction_text=f'✅ Harga Rata-Rata Tertimbang: {prediction:.2f} Rp/kg',
                               kabupaten_items=sorted(kabupaten_mapping.items()),
                               ikan_items=sorted(ikan_mapping.keys()))

    except Exception as e:
        return render_template('index.html', prediction_text=f'⚠️ Error: {str(e)}',
                               kabupaten_items=sorted(kabupaten_mapping.items()),
                               ikan_items=sorted(ikan_mapping.keys()))

if __name__ == "__main__":
    app.run(debug=True, port=5000)